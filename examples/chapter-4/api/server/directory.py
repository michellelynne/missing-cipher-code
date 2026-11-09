"""The Contractors Directory itself: the rules every API style shares.

REST, gRPC, and GraphQL are three doors into this one room. Each API file only translates its own
request format into these calls, and these errors into its own error format, so the three can't drift
apart on what's allowed.

Data lives in memory, so it resets every time the server starts.
"""

import base64
import datetime
import json
import secrets
import time

AVAILABILITY_VALUES = ("OPEN", "LIMITED", "BOOKED")
DEFAULT_PAGE_SIZE = 20
LARGEST_PAGE_SIZE = 50
PROFILE_FIELDS = ("company_name", "services", "service_area", "availability", "insurance_expires_on")
IDEMPOTENCY_KEY_SECONDS = 24 * 60 * 60  # how long a create can be safely retried with the same key
LONGEST_IDEMPOTENCY_KEY = 255


# ---------- The five kinds of error, named the same way in all three APIs ----------

class DirectoryError(Exception):
    """Base class, so each API can catch every directory error in one place."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationFailed(DirectoryError):
    """A field is missing or malformed. field_errors is a list of (field_name, message) pairs."""

    def __init__(self, field_errors):
        super().__init__("Some fields aren't valid: " + ", ".join(field for field, _ in field_errors))
        self.field_errors = field_errors


class NotSignedIn(DirectoryError):
    pass


class NotAllowed(DirectoryError):
    pass


class NotFound(DirectoryError):
    pass


class AlreadyExists(DirectoryError):
    pass


class IdempotencyKeyReused(DirectoryError):
    """The same idempotency key was sent with a different request."""
    pass


# ---------- Checking input ----------

def check_profile_fields(fields, required):
    """Checks the profile fields that were sent. With required=True, the four required fields must be there."""
    field_errors = []
    if required:
        for field_name in ("company_name", "services", "service_area", "availability"):
            if field_name not in fields or fields[field_name] in (None, "", []):
                field_errors.append((field_name, "This field is required."))
    for field_name, value in fields.items():
        if field_name not in PROFILE_FIELDS:
            field_errors.append((field_name, "This isn't a field you can set."))
            continue
        if value is None and field_name != "insurance_expires_on":
            if not required:
                field_errors.append((field_name, "This field can't be cleared."))
            continue
        if field_name == "company_name" and value is not None:
            if not isinstance(value, str) or not value.strip():
                field_errors.append((field_name, "Enter a company name."))
            elif len(value) > 100:
                field_errors.append((field_name, "Keep the company name under 100 characters."))
        if field_name == "services" and value is not None:
            if not isinstance(value, list) or not value or not all(isinstance(service, str) and service.strip() for service in value):
                field_errors.append((field_name, "List at least one service."))
        if field_name == "service_area" and value is not None:
            if not isinstance(value, str) or not value.strip():
                field_errors.append((field_name, "Enter a service area."))
        if field_name == "availability" and value is not None:
            if value not in AVAILABILITY_VALUES:
                field_errors.append((field_name, "Use OPEN, LIMITED, or BOOKED."))
        if field_name == "insurance_expires_on" and value not in (None, ""):
            try:
                datetime.date.fromisoformat(value)
            except (TypeError, ValueError):
                field_errors.append((field_name, "Use a date like 2027-03-31."))
    # Keep only the first message for each field, so a missing field isn't reported twice.
    first_errors = []
    seen_fields = set()
    for field_name, message in field_errors:
        if field_name not in seen_fields:
            first_errors.append((field_name, message))
            seen_fields.add(field_name)
    if first_errors:
        raise ValidationFailed(first_errors)


def encode_page_token(offset):
    return base64.urlsafe_b64encode(("offset:" + str(offset)).encode()).decode()


def decode_page_token(page_token):
    try:
        decoded = base64.urlsafe_b64decode(page_token.encode()).decode()
        label, offset_text = decoded.split(":")
        offset = int(offset_text)
        if label != "offset" or offset < 0:
            raise ValueError(page_token)
        return offset
    except (ValueError, UnicodeDecodeError):
        raise ValidationFailed([("page_token", "Use the nextPageToken from the previous page.")]) from None


# ---------- The directory ----------

class ContractorDirectory:
    def __init__(self):
        self.profiles = {}
        # (user ID, operation, key) -> (fingerprint of the request, saved result, when it was saved)
        self.idempotent_results = {}

    def run_once(self, user, operation, idempotency_key, request_fields, action):
        """Runs action once per idempotency key. A retry with the same key and the same request gets the
        saved result back instead of creating a second one. Returns (result, replayed)."""
        if idempotency_key is None:
            return action(), False
        if not isinstance(idempotency_key, str) or not idempotency_key.strip() \
                or len(idempotency_key) > LONGEST_IDEMPOTENCY_KEY:
            raise ValidationFailed([("idempotency_key", "Use 1 to 255 characters, like a UUID.")])
        saved_key = (user["user_id"], operation, idempotency_key)
        fingerprint = json.dumps(request_fields, sort_keys=True)
        now = time.time()
        if saved_key in self.idempotent_results:
            saved_fingerprint, saved_result, saved_at = self.idempotent_results[saved_key]
            if now - saved_at < IDEMPOTENCY_KEY_SECONDS:
                if saved_fingerprint != fingerprint:
                    raise IdempotencyKeyReused("This idempotency key was already used for a different request. Use a new key for each new request.")
                return json.loads(json.dumps(saved_result)), True
        result = action()
        # Only successes are saved, so a request that failed can be fixed and retried with the same key.
        self.idempotent_results[saved_key] = (fingerprint, json.loads(json.dumps(result)), now)
        return result, False

    def require_user(self, user):
        if user is None:
            raise NotSignedIn("Sign in first. Send your token as Authorization: Bearer <token>.")

    def find_profile(self, contractor_id):
        if contractor_id not in self.profiles:
            raise NotFound("There's no contractor profile with the ID " + str(contractor_id) + ".")
        return self.profiles[contractor_id]

    def public_view(self, profile):
        """Everything except the owner, which stays private."""
        return {
            "contractor_id": profile["contractor_id"],
            "company_name": profile["company_name"],
            "services": list(profile["services"]),
            "service_area": profile["service_area"],
            "availability": profile["availability"],
            "insurance_expires_on": profile["insurance_expires_on"],
            "reviews": [dict(review) for review in profile["reviews"]],
        }

    def create_profile(self, user, fields, idempotency_key=None):
        """Returns (profile, replayed). replayed is True when this was a retry of an earlier create."""
        self.require_user(user)
        return self.run_once(user, "create_profile", idempotency_key, fields,
                             lambda: self.create_new_profile(user, fields))

    def create_new_profile(self, user, fields):
        check_profile_fields(fields, required=True)
        for profile in self.profiles.values():
            if profile["owner_id"] == user["user_id"]:
                raise AlreadyExists("You already have a contractor profile: " + profile["contractor_id"] + ".")
        contractor_id = "c_" + secrets.token_hex(3)
        self.profiles[contractor_id] = {
            "contractor_id": contractor_id,
            "owner_id": user["user_id"],
            "company_name": fields["company_name"].strip(),
            "services": [service.strip() for service in fields["services"]],
            "service_area": fields["service_area"].strip(),
            "availability": fields["availability"],
            "insurance_expires_on": fields.get("insurance_expires_on") or None,
            "reviews": [],
        }
        return self.public_view(self.profiles[contractor_id])

    def get_profile(self, user, contractor_id):
        self.require_user(user)
        return self.public_view(self.find_profile(contractor_id))

    def list_profiles(self, user, service=None, service_area=None, availability=None, page_size=None, page_token=None):
        """Returns (profiles, next_page_token). next_page_token is None on the last page."""
        self.require_user(user)
        if availability is not None and availability not in AVAILABILITY_VALUES:
            raise ValidationFailed([("availability", "Use OPEN, LIMITED, or BOOKED.")])
        if page_size is None or page_size == 0:
            page_size = DEFAULT_PAGE_SIZE
        if page_size < 1 or page_size > LARGEST_PAGE_SIZE:
            raise ValidationFailed([("page_size", "Use a page size from 1 to " + str(LARGEST_PAGE_SIZE) + ".")])
        offset = decode_page_token(page_token) if page_token else 0

        matching_profiles = []
        for profile in self.profiles.values():
            if service and service.lower() not in [offered.lower() for offered in profile["services"]]:
                continue
            if service_area and service_area.lower() != profile["service_area"].lower():
                continue
            if availability and availability != profile["availability"]:
                continue
            matching_profiles.append(profile)

        page_end = offset + page_size
        page = matching_profiles[offset:page_end]
        next_page_token = encode_page_token(page_end) if page_end < len(matching_profiles) else None
        return [self.public_view(profile) for profile in page], next_page_token

    def update_profile(self, user, contractor_id, changes):
        """changes holds only the fields to change. insurance_expires_on set to None clears it."""
        self.require_user(user)
        profile = self.find_profile(contractor_id)
        if profile["owner_id"] != user["user_id"]:
            raise NotAllowed("Only the profile's owner can change it.")
        if not changes:
            raise ValidationFailed([("update", "Send at least one field to change.")])
        check_profile_fields(changes, required=False)
        for field_name, value in changes.items():
            if field_name == "services":
                profile["services"] = [service.strip() for service in value]
            elif isinstance(value, str):
                profile[field_name] = value.strip() or None
            else:
                profile[field_name] = value
        return self.public_view(profile)

    def delete_profile(self, user, contractor_id):
        self.require_user(user)
        profile = self.find_profile(contractor_id)
        if profile["owner_id"] != user["user_id"]:
            raise NotAllowed("Only the profile's owner can delete it.")
        del self.profiles[contractor_id]
        return contractor_id

    def create_review(self, user, contractor_id, rating, body, idempotency_key=None):
        """Returns (review, replayed). replayed is True when this was a retry of an earlier review."""
        self.require_user(user)
        self.find_profile(contractor_id)
        request_fields = {"contractor_id": contractor_id, "rating": rating, "body": body}
        return self.run_once(user, "create_review", idempotency_key, request_fields,
                             lambda: self.add_review(user, contractor_id, rating, body))

    def add_review(self, user, contractor_id, rating, body):
        profile = self.find_profile(contractor_id)
        if profile["owner_id"] == user["user_id"]:
            raise NotAllowed("Contractors can't review their own profile.")
        field_errors = []
        if not isinstance(rating, int) or isinstance(rating, bool) or rating < 1 or rating > 5:
            field_errors.append(("rating", "Give a rating from 1 to 5."))
        if body is not None and (not isinstance(body, str) or len(body) > 2000):
            field_errors.append(("body", "Keep the review under 2,000 characters."))
        if field_errors:
            raise ValidationFailed(field_errors)
        review = {"author_name": user["display_name"], "body": body or None, "rating": rating}
        profile["reviews"].append(review)
        return dict(review)
