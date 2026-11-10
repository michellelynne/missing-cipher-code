"""GraphQL cases the example file doesn't show."""

from conftest import bearer, create_acme


def run(client, query, variables=None, person="homeowner"):
    headers = bearer(person) if person else {}
    return client.post("/graphql", headers=headers, json={"query": query, "variables": variables or {}}).json()


UPDATE = """mutation($id: ID!, $input: UpdateContractorProfileInput!) {
  updateContractorProfile(contractorId: $id, input: $input) { companyName services insuranceExpiresOn }
}"""


def test_left_out_fields_stay_and_null_clears_the_date(client):
    contractor_id = create_acme(client)
    kept = run(client, UPDATE, {"id": contractor_id, "input": {"services": ["Kitchen Remodel"]}}, "contractor")
    assert kept["data"]["updateContractorProfile"] == {
        "companyName": "Acme Renovations", "services": ["Kitchen Remodel"], "insuranceExpiresOn": "2027-03-31"}
    cleared = run(client, UPDATE, {"id": contractor_id, "input": {"insuranceExpiresOn": None}}, "contractor")
    assert cleared["data"]["updateContractorProfile"]["insuranceExpiresOn"] is None


def test_null_for_a_required_field_is_a_field_error(client):
    contractor_id = create_acme(client)
    result = run(client, UPDATE, {"id": contractor_id, "input": {"companyName": None}}, "contractor")
    assert result["errors"][0]["extensions"] == {
        "code": "BAD_USER_INPUT", "fieldErrors": [{"field": "companyName", "message": "This field can't be cleared."}]}


def test_each_error_code(client):
    contractor_id = create_acme(client)
    review = "mutation($id: ID!) { createReview(contractorId: $id, input: {rating: 5}) { rating } }"
    codes = {
        "UNAUTHENTICATED": run(client, review, {"id": contractor_id}, None),
        "FORBIDDEN": run(client, review, {"id": contractor_id}, "contractor"),
        "NOT_FOUND": run(client, review, {"id": "c_000000"}),
        "BAD_USER_INPUT": run(client, "mutation($id: ID!) { createReview(contractorId: $id, input: {rating: 0}) { rating } }", {"id": contractor_id}),
    }
    for expected_code, result in codes.items():
        assert result["errors"][0]["extensions"]["code"] == expected_code


def test_schema_rejects_unknown_enum_values_before_the_resolver_runs(client):
    result = run(client, "{ contractorProfiles(availability: SOMETIMES) { nextPageToken } }")
    assert "SOMETIMES" in result["errors"][0]["message"]


def test_delete_returns_the_id(client):
    contractor_id = create_acme(client)
    result = run(client, "mutation($id: ID!) { deleteContractorProfile(contractorId: $id) }", {"id": contractor_id}, "contractor")
    assert result == {"data": {"deleteContractorProfile": contractor_id}}
    gone = run(client, "query($id: ID!) { contractorProfile(contractorId: $id) { companyName } }", {"id": contractor_id})
    assert gone["errors"][0]["extensions"]["code"] == "NOT_FOUND"


def test_one_request_can_ask_for_several_things(client):
    """The reason GraphQL exists: fewer round trips."""
    contractor_id = create_acme(client)
    result = run(client, """query($id: ID!) {
      profile: contractorProfile(contractorId: $id) { companyName }
      openNow: contractorProfiles(availability: OPEN) { contractorProfiles { contractorId } }
    }""", {"id": contractor_id})
    assert result["data"]["profile"]["companyName"] == "Acme Renovations"
    assert result["data"]["openNow"]["contractorProfiles"] == [{"contractorId": contractor_id}]
