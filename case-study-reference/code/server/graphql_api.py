"""The GraphQL version of the Contractors API. It loads schema.graphql itself, so the server can't
drift from the schema beside it."""

import logging
from pathlib import Path

from ariadne import MutationType, QueryType, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from graphql import GraphQLError

from auth import user_from_authorization_header
from directory import (AlreadyExists, DirectoryError, IdempotencyKeyReused, NotAllowed, NotFound, NotSignedIn,
                       ValidationFailed)
from rest_api import FIELD_TO_REST, REST_TO_FIELD, review_to_rest, to_rest

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema.graphql"

ERROR_CODES = {
    ValidationFailed: "BAD_USER_INPUT",
    NotSignedIn: "UNAUTHENTICATED",
    NotAllowed: "FORBIDDEN",
    NotFound: "NOT_FOUND",
    AlreadyExists: "ALREADY_EXISTS",
    IdempotencyKeyReused: "IDEMPOTENCY_KEY_REUSED",
}

query = QueryType()
mutation = MutationType()


def graphql_error(error):
    """Turns a directory error into a GraphQL error with extensions.code, like the schema describes."""
    extensions = {"code": ERROR_CODES[type(error)]}
    message = error.message
    if isinstance(error, ValidationFailed):
        extensions["fieldErrors"] = [
            {"field": FIELD_TO_REST.get(field_name, field_name), "message": field_message}
            for field_name, field_message in error.field_errors
        ]
        message = "Some fields aren't valid: " + ", ".join(field_error["field"] for field_error in extensions["fieldErrors"])
    return GraphQLError(message, extensions=extensions)


def directory_call(resolver):
    """Runs a resolver with the signed-in user and directory, turning directory errors into GraphQL errors."""
    def wrapped(parent, info, **arguments):
        request = info.context["request"]
        user = user_from_authorization_header(request.headers.get("authorization"))
        if resolver.__name__ in ("resolve_create_contractor_profile", "resolve_create_review"):
            # Like REST, the key travels in the Idempotency-Key header, not in the query.
            arguments["idempotency_key"] = request.headers.get("idempotency-key")
        try:
            return resolver(request.app.state.directory, user, **arguments)
        except DirectoryError as error:
            raise graphql_error(error) from error
    return wrapped


def from_input(input_fields):
    return {REST_TO_FIELD.get(name, name): value for name, value in input_fields.items()}


@query.field("contractorProfile")
@directory_call
def resolve_contractor_profile(directory, user, contractorId):
    return to_rest(directory.get_profile(user, contractorId))


@query.field("contractorProfiles")
@directory_call
def resolve_contractor_profiles(directory, user, service=None, serviceArea=None, availability=None,
                                pageSize=None, pageToken=None):
    profiles, next_page_token = directory.list_profiles(
        user, service=service, service_area=serviceArea, availability=availability,
        page_size=pageSize, page_token=pageToken)
    return {"contractorProfiles": [to_rest(profile) for profile in profiles], "nextPageToken": next_page_token}


@mutation.field("createContractorProfile")
@directory_call
def resolve_create_contractor_profile(directory, user, input, idempotency_key=None):
    profile, replayed = directory.create_profile(user, from_input(input), idempotency_key=idempotency_key)
    return to_rest(profile)


@mutation.field("updateContractorProfile")
@directory_call
def resolve_update_contractor_profile(directory, user, contractorId, input):
    # Fields left out of the input aren't in the dictionary at all; a field sent as null is there as None.
    return to_rest(directory.update_profile(user, contractorId, from_input(input)))


@mutation.field("deleteContractorProfile")
@directory_call
def resolve_delete_contractor_profile(directory, user, contractorId):
    return directory.delete_profile(user, contractorId)


@mutation.field("createReview")
@directory_call
def resolve_create_review(directory, user, contractorId, input, idempotency_key=None):
    review, replayed = directory.create_review(user, contractorId, input["rating"], input.get("body"),
                                               idempotency_key=idempotency_key)
    return review_to_rest(review)


schema = make_executable_schema(load_schema_from_path(str(SCHEMA_PATH)), query, mutation)


class SkipExpectedErrors(logging.Filter):
    """Ariadne logs every error with a traceback. Errors with one of our five codes are answers, not
    bugs, so only log the rest."""

    def filter(self, record):
        if not record.exc_info:
            return True
        error = record.exc_info[1]
        while error is not None:
            if isinstance(error, GraphQLError) and (error.extensions or {}).get("code") in ERROR_CODES.values():
                return False
            error = error.__context__
        return True


GRAPHQL_LOGGER_NAME = "renovation_revolution.graphql"
logging.getLogger(GRAPHQL_LOGGER_NAME).addFilter(SkipExpectedErrors())


def build_graphql_app():
    return GraphQL(schema, context_value=lambda request, data=None: {"request": request}, logger=GRAPHQL_LOGGER_NAME)
