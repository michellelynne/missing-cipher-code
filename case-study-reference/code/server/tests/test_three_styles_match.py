"""Keeps REST, gRPC, and GraphQL in step: the same operations, the same availability values, and the
same fields. These are the inconsistencies that crept into the first version of the examples."""

import re

from graphql import build_schema

from conftest import API_FOLDER, OPENAPI, bearer, contractor_pb2, create_acme, grpc_metadata

GRAPHQL_SCHEMA = build_schema((API_FOLDER / "schema.graphql").read_text())


def lowercase_first(name):
    return name[0].lower() + name[1:]


def test_same_operations_in_all_three():
    rest_operations = set()
    for path_item in OPENAPI["paths"].values():
        for operation in path_item.values():
            if isinstance(operation, dict) and "Contractors" in operation.get("tags", []):
                rest_operations.add(operation["operationId"])
    grpc_operations = {lowercase_first(name) for name in
                       contractor_pb2.DESCRIPTOR.services_by_name["ContractorProfileService"].methods_by_name}
    graphql_operations = set()
    renamed = {"contractorProfile": "getContractorProfile", "contractorProfiles": "listContractorProfiles"}
    for field_name in list(GRAPHQL_SCHEMA.query_type.fields) + list(GRAPHQL_SCHEMA.mutation_type.fields):
        graphql_operations.add(renamed.get(field_name, field_name))
    assert rest_operations == grpc_operations == graphql_operations
    assert len(rest_operations) == 6


def test_same_availability_values():
    rest_values = OPENAPI["components"]["schemas"]["Availability"]["enum"]
    grpc_values = [name for name in contractor_pb2.Availability.keys() if name != "AVAILABILITY_UNSPECIFIED"]
    graphql_values = list(GRAPHQL_SCHEMA.type_map["Availability"].values)
    assert rest_values == grpc_values == graphql_values == ["OPEN", "LIMITED", "BOOKED"]


def snake_to_camel(name):
    return re.sub(r"_([a-z])", lambda match: match.group(1).upper(), name)


def test_same_profile_and_review_fields():
    rest_profile = set(OPENAPI["components"]["schemas"]["ContractorProfile"]["properties"])
    grpc_profile = {snake_to_camel(field.name) for field in contractor_pb2.ContractorProfile.DESCRIPTOR.fields}
    graphql_profile = set(GRAPHQL_SCHEMA.type_map["ContractorProfile"].fields)
    assert rest_profile == grpc_profile == graphql_profile

    rest_review = set(OPENAPI["components"]["schemas"]["Review"]["properties"])
    grpc_review = {snake_to_camel(field.name) for field in contractor_pb2.Review.DESCRIPTOR.fields}
    graphql_review = set(GRAPHQL_SCHEMA.type_map["Review"].fields)
    assert rest_review == grpc_review == graphql_review


def test_optional_fields_are_optional_everywhere():
    """A missing insurance date or review body is null in REST and GraphQL, and left out in gRPC."""
    profile_fields = contractor_pb2.ContractorProfile.DESCRIPTOR.fields_by_name
    review_fields = contractor_pb2.Review.DESCRIPTOR.fields_by_name
    assert profile_fields["insurance_expires_on"].has_presence
    assert review_fields["body"].has_presence
    assert "insuranceExpiresOn" not in OPENAPI["components"]["schemas"]["ContractorProfile"]["required"]
    assert "body" not in OPENAPI["components"]["schemas"]["Review"]["required"]
    assert str(GRAPHQL_SCHEMA.type_map["ContractorProfile"].fields["insuranceExpiresOn"].type) == "String"
    assert str(GRAPHQL_SCHEMA.type_map["Review"].fields["body"].type) == "String"


def test_one_directory_behind_three_doors(client, grpc_stub):
    """A profile created in REST reads the same through gRPC and GraphQL."""
    contractor_id = create_acme(client)
    rest_profile = client.get("/api/contractors/" + contractor_id, headers=bearer("homeowner")).json()
    grpc_profile = grpc_stub.GetContractorProfile(
        contractor_pb2.GetContractorProfileRequest(contractor_id=contractor_id), metadata=grpc_metadata("homeowner"))
    graphql_profile = client.post("/graphql", headers=bearer("homeowner"), json={
        "query": "query($id: ID!) { contractorProfile(contractorId: $id) { contractorId companyName services serviceArea availability insuranceExpiresOn reviews { authorName body rating } } }",
        "variables": {"id": contractor_id}}).json()["data"]["contractorProfile"]
    assert graphql_profile == rest_profile
    assert grpc_profile.company_name == rest_profile["companyName"]
    assert contractor_pb2.Availability.Name(grpc_profile.availability) == rest_profile["availability"]
    assert grpc_profile.insurance_expires_on == rest_profile["insuranceExpiresOn"]
