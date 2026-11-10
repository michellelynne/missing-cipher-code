"""The gRPC version of the Contractors API. The message and service code is generated from
contractor.proto by generate_grpc.py, so the server can't drift from the .proto beside it. It is
generated again whenever contractor.proto changes."""

import sys
from concurrent import futures

import grpc
from google.protobuf import any_pb2, empty_pb2
from google.rpc import code_pb2, error_details_pb2, status_pb2
from grpc_status import rpc_status

from auth import user_from_authorization_header
from directory import (AlreadyExists, DirectoryError, IdempotencyKeyReused, NotAllowed, NotFound, NotSignedIn,
                       PROFILE_FIELDS, ValidationFailed)
from generate_grpc import GENERATED_FOLDER, make_sure_grpc_code_is_current

make_sure_grpc_code_is_current()
sys.path.insert(0, str(GENERATED_FOLDER))
import contractor_pb2  # noqa: E402  (generated, or checked as current, just above)
import contractor_pb2_grpc  # noqa: E402

STATUS_CODES = {
    ValidationFailed: code_pb2.INVALID_ARGUMENT,
    NotSignedIn: code_pb2.UNAUTHENTICATED,
    NotAllowed: code_pb2.PERMISSION_DENIED,
    NotFound: code_pb2.NOT_FOUND,
    AlreadyExists: code_pb2.ALREADY_EXISTS,
    IdempotencyKeyReused: code_pb2.FAILED_PRECONDITION,
}


def abort_with_directory_error(context, error):
    """Ends the call with the matching status code. Field errors go in the standard BadRequest details,
    which is how gRPC clients get the same fieldErrors list that REST and GraphQL send."""
    rich_status = status_pb2.Status(code=STATUS_CODES[type(error)], message=error.message)
    if isinstance(error, ValidationFailed):
        bad_request = error_details_pb2.BadRequest(field_violations=[
            error_details_pb2.BadRequest.FieldViolation(field=field_name, description=message)
            for field_name, message in error.field_errors
        ])
        detail = any_pb2.Any()
        detail.Pack(bad_request)
        rich_status.details.append(detail)
    context.abort_with_status(rpc_status.to_status(rich_status))


def to_message(profile):
    reviews = []
    for review in profile["reviews"]:
        review_message = contractor_pb2.Review(author_name=review["author_name"], rating=review["rating"])
        if review["body"] is not None:
            review_message.body = review["body"]
        reviews.append(review_message)
    profile_message = contractor_pb2.ContractorProfile(
        contractor_id=profile["contractor_id"],
        company_name=profile["company_name"],
        services=profile["services"],
        service_area=profile["service_area"],
        availability=contractor_pb2.Availability.Value(profile["availability"]),
        reviews=reviews,
    )
    # optional in the .proto, so "no date" is left out instead of sent as an empty string
    if profile["insurance_expires_on"] is not None:
        profile_message.insurance_expires_on = profile["insurance_expires_on"]
    return profile_message


def availability_name(availability_number):
    """Turns the enum number into OPEN, LIMITED, or BOOKED. Unset (0) becomes None."""
    if availability_number == contractor_pb2.AVAILABILITY_UNSPECIFIED:
        return None
    return contractor_pb2.Availability.Name(availability_number)


class ContractorProfileService(contractor_pb2_grpc.ContractorProfileServiceServicer):
    def __init__(self, directory):
        self.directory = directory

    def signed_in_user(self, context):
        metadata = dict(context.invocation_metadata())
        return user_from_authorization_header(metadata.get("authorization"))

    def idempotency_key(self, context):
        return dict(context.invocation_metadata()).get("idempotency-key")

    def mark_replay(self, context, replayed):
        """Like REST's Idempotent-Replayed header, a retry's response says it's the first one again."""
        if replayed:
            context.send_initial_metadata([("idempotent-replayed", "true")])

    def run(self, context, action):
        try:
            return action(self.signed_in_user(context))
        except DirectoryError as error:
            abort_with_directory_error(context, error)

    def CreateContractorProfile(self, request, context):
        fields = {
            "company_name": request.company_name,
            "services": list(request.services),
            "service_area": request.service_area,
            "availability": availability_name(request.availability),
            "insurance_expires_on": request.insurance_expires_on if request.HasField("insurance_expires_on") else None,
        }
        def create(user):
            profile, replayed = self.directory.create_profile(user, fields, idempotency_key=self.idempotency_key(context))
            self.mark_replay(context, replayed)
            return to_message(profile)
        return self.run(context, create)

    def GetContractorProfile(self, request, context):
        return self.run(context, lambda user: to_message(self.directory.get_profile(user, request.contractor_id)))

    def ListContractorProfiles(self, request, context):
        def list_page(user):
            profiles, next_page_token = self.directory.list_profiles(
                user,
                service=request.service or None,
                service_area=request.service_area or None,
                availability=availability_name(request.availability),
                page_size=request.page_size,
                page_token=request.page_token or None,
            )
            return contractor_pb2.ListContractorProfilesResponse(
                contractor_profiles=[to_message(profile) for profile in profiles],
                next_page_token=next_page_token or "",
            )
        return self.run(context, list_page)

    def UpdateContractorProfile(self, request, context):
        def update(user):
            new_values = request.contractor_profile
            self.directory.require_user(user)
            profile = self.directory.find_profile(new_values.contractor_id)
            if profile["owner_id"] != user["user_id"]:
                raise NotAllowed("Only the profile's owner can change it.")
            if not request.update_mask.paths:
                raise ValidationFailed([("update_mask", "List the fields to change, like availability.")])
            changes = {}
            for path in request.update_mask.paths:
                if path not in PROFILE_FIELDS:
                    raise ValidationFailed([(path, "This isn't a field you can change.")])
                if path == "services":
                    changes[path] = list(new_values.services)
                elif path == "availability":
                    changes[path] = availability_name(new_values.availability) or "AVAILABILITY_UNSPECIFIED"
                elif path == "insurance_expires_on":
                    # In the mask but not set clears the date, like null does in REST and GraphQL.
                    changes[path] = new_values.insurance_expires_on if new_values.HasField("insurance_expires_on") else None
                else:
                    changes[path] = getattr(new_values, path)
            return to_message(self.directory.update_profile(user, new_values.contractor_id, changes))
        return self.run(context, update)

    def DeleteContractorProfile(self, request, context):
        def delete(user):
            self.directory.delete_profile(user, request.contractor_id)
            return empty_pb2.Empty()
        return self.run(context, delete)

    def CreateReview(self, request, context):
        def create(user):
            body = request.body if request.HasField("body") else None
            review, replayed = self.directory.create_review(user, request.contractor_id, request.rating, body,
                                                            idempotency_key=self.idempotency_key(context))
            self.mark_replay(context, replayed)
            review_message = contractor_pb2.Review(author_name=review["author_name"], rating=review["rating"])
            if review["body"] is not None:
                review_message.body = review["body"]
            return review_message
        return self.run(context, create)


def build_grpc_server(directory, address):
    """Builds (but doesn't start) a gRPC server on address, like "localhost:50051". Returns (server, port)."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    contractor_pb2_grpc.add_ContractorProfileServiceServicer_to_server(ContractorProfileService(directory), server)
    port = server.add_insecure_port(address)
    return server, port
