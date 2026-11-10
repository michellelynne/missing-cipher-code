"""The REST version of the Contractors API, following openapi.yaml."""

import json

from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from auth import user_from_authorization_header
from directory import (AlreadyExists, DirectoryError, IdempotencyKeyReused, NotAllowed, NotFound, NotSignedIn,
                       ValidationFailed)

# REST uses camelCase field names; the directory uses snake_case, like the .proto file.
REST_TO_FIELD = {
    "companyName": "company_name",
    "services": "services",
    "serviceArea": "service_area",
    "availability": "availability",
    "insuranceExpiresOn": "insurance_expires_on",
    "contractorId": "contractor_id",
    "pageSize": "page_size",
    "pageToken": "page_token",
    "rating": "rating",
    "body": "body",
    "Idempotency-Key": "idempotency_key",
}
FIELD_TO_REST = {field_name: rest_name for rest_name, field_name in REST_TO_FIELD.items()}

PROBLEM_TYPES = {
    ValidationFailed: (400, "validation-failed", "Some fields aren't valid"),
    NotSignedIn: (401, "not-signed-in", "Sign in first"),
    NotAllowed: (403, "not-allowed", "You can't do that"),
    NotFound: (404, "not-found", "Not found"),
    AlreadyExists: (409, "already-exists", "It already exists"),
    IdempotencyKeyReused: (422, "idempotency-key-reused", "That idempotency key was already used"),
}


def problem_response(error):
    """Turns a directory error into an RFC 9457 problem response."""
    status, slug, title = PROBLEM_TYPES[type(error)]
    problem = {
        "type": "https://missingcipher.com/problems/" + slug,
        "title": title,
        "status": status,
        "detail": error.message,
    }
    if isinstance(error, ValidationFailed):
        problem["detail"] = "Fix the fields listed in fieldErrors and send it again."
        problem["fieldErrors"] = [
            {"field": FIELD_TO_REST.get(field_name, field_name), "message": message}
            for field_name, message in error.field_errors
        ]
    headers = {"WWW-Authenticate": "Bearer"} if status == 401 else None
    return JSONResponse(problem, status_code=status, media_type="application/problem+json", headers=headers)


def review_to_rest(review):
    return {"authorName": review["author_name"], "body": review["body"], "rating": review["rating"]}


def to_rest(record):
    """Renames a profile's fields to camelCase, including the reviews inside it."""
    renamed = {}
    for field_name, value in record.items():
        if field_name == "reviews":
            value = [review_to_rest(review) for review in value]
        renamed[FIELD_TO_REST.get(field_name, field_name)] = value
    return renamed


def from_rest(body):
    """Renames camelCase fields to the directory's names. Unknown fields pass through so they're reported."""
    return {REST_TO_FIELD.get(rest_name, rest_name): value for rest_name, value in body.items()}


async def read_json_object(request):
    try:
        body = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValidationFailed([("body", "Send a JSON object.")]) from None
    if not isinstance(body, dict):
        raise ValidationFailed([("body", "Send a JSON object.")])
    return body


def endpoint(handler):
    """Wraps a handler so every directory error becomes the matching problem response."""
    async def wrapped(request):
        try:
            user = user_from_authorization_header(request.headers.get("authorization"))
            return await handler(request, user)
        except DirectoryError as error:
            return problem_response(error)
    return wrapped


def created_headers(replayed, extra_headers=None):
    """A retry with the same Idempotency-Key gets the first response again, marked as a replay."""
    headers = dict(extra_headers or {})
    if replayed:
        headers["Idempotent-Replayed"] = "true"
    return headers


@endpoint
async def create_contractor_profile(request, user):
    request.app.state.directory.require_user(user)
    body = await read_json_object(request)
    profile, replayed = request.app.state.directory.create_profile(
        user, from_rest(body), idempotency_key=request.headers.get("idempotency-key"))
    return JSONResponse(to_rest(profile), status_code=201,
                        headers=created_headers(replayed, {"Location": "/api/contractors/" + profile["contractor_id"]}))


@endpoint
async def list_contractor_profiles(request, user):
    query = request.query_params
    page_size_text = query.get("pageSize")
    page_size = None
    if page_size_text is not None:
        # Unlike gRPC, where 0 means "not set", REST has no unset number, so 0 is just too small.
        if not page_size_text.isdigit() or int(page_size_text) < 1:
            raise ValidationFailed([("page_size", "Use a page size from 1 to 50.")])
        page_size = int(page_size_text)
    profiles, next_page_token = request.app.state.directory.list_profiles(
        user,
        service=query.get("service"),
        service_area=query.get("serviceArea"),
        availability=query.get("availability"),
        page_size=page_size,
        page_token=query.get("pageToken"),
    )
    return JSONResponse({"contractorProfiles": [to_rest(profile) for profile in profiles],
                         "nextPageToken": next_page_token})


@endpoint
async def get_contractor_profile(request, user):
    profile = request.app.state.directory.get_profile(user, request.path_params["contractorId"])
    return JSONResponse(to_rest(profile))


@endpoint
async def update_contractor_profile(request, user):
    # Check sign-in and ownership before reading the body, so a stranger learns nothing from validation.
    directory = request.app.state.directory
    directory.require_user(user)
    contractor_id = request.path_params["contractorId"]
    if directory.find_profile(contractor_id)["owner_id"] != user["user_id"]:
        raise NotAllowed("Only the profile's owner can change it.")
    body = await read_json_object(request)
    profile = directory.update_profile(user, contractor_id, from_rest(body))
    return JSONResponse(to_rest(profile))


@endpoint
async def delete_contractor_profile(request, user):
    request.app.state.directory.delete_profile(user, request.path_params["contractorId"])
    return Response(status_code=204)


@endpoint
async def create_review(request, user):
    directory = request.app.state.directory
    directory.require_user(user)
    directory.find_profile(request.path_params["contractorId"])
    body = await read_json_object(request)
    unknown_fields = [name for name in body if name not in ("rating", "body")]
    if unknown_fields:
        raise ValidationFailed([(name, "This isn't a field you can set.") for name in unknown_fields])
    review, replayed = directory.create_review(user, request.path_params["contractorId"], body.get("rating"),
                                               body.get("body"), idempotency_key=request.headers.get("idempotency-key"))
    return JSONResponse(review_to_rest(review), status_code=201, headers=created_headers(replayed))


routes = [
    Route("/api/contractors", create_contractor_profile, methods=["POST"]),
    Route("/api/contractors", list_contractor_profiles, methods=["GET"]),
    Route("/api/contractors/{contractorId}", get_contractor_profile, methods=["GET"]),
    Route("/api/contractors/{contractorId}", update_contractor_profile, methods=["PATCH"]),
    Route("/api/contractors/{contractorId}", delete_contractor_profile, methods=["DELETE"]),
    Route("/api/contractors/{contractorId}/reviews", create_review, methods=["POST"]),
]
