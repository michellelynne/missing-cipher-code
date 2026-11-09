"""REST cases the example file doesn't show. Every response is also checked against openapi.yaml."""

from conftest import ACME, bearer, check_against_openapi, create_acme


def call(client, method, path, person=None, headers=None, **options):
    all_headers = (bearer(person) if person else {}) | (headers or {})
    response = client.request(method, path, headers=all_headers, **options)
    check_against_openapi(response)
    return response


def test_not_signed_in_says_how_to_sign_in(client):
    response = call(client, "GET", "/api/contractors")
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_wrong_token_is_not_signed_in(client):
    response = client.get("/api/contractors", headers={"Authorization": "Bearer made-up"})
    assert response.status_code == 401


def test_unknown_fields_are_rejected(client):
    response = call(client, "POST", "/api/contractors", "contractor", json=ACME | {"email": "hi@acme.example"})
    assert response.status_code == 400
    assert response.json()["fieldErrors"] == [{"field": "email", "message": "This isn't a field you can set."}]


def test_body_must_be_a_json_object(client):
    response = call(client, "POST", "/api/contractors", "contractor", content=b"[1, 2]",
                    headers={"Content-Type": "application/json"})
    assert response.status_code == 400


def test_merge_patch_changes_only_what_is_sent(client):
    contractor_id = create_acme(client)
    response = call(client, "PATCH", "/api/contractors/" + contractor_id, "contractor", json={"services": ["Kitchen Remodel"]})
    assert response.status_code == 200
    assert response.json()["services"] == ["Kitchen Remodel"]
    assert response.json()["companyName"] == "Acme Renovations"
    assert response.json()["insuranceExpiresOn"] == "2027-03-31"


def test_null_clears_the_insurance_date_but_not_required_fields(client):
    contractor_id = create_acme(client)
    cleared = call(client, "PATCH", "/api/contractors/" + contractor_id, "contractor", json={"insuranceExpiresOn": None})
    assert cleared.status_code == 200
    assert cleared.json()["insuranceExpiresOn"] is None
    refused = call(client, "PATCH", "/api/contractors/" + contractor_id, "contractor", json={"companyName": None})
    assert refused.status_code == 400
    assert refused.json()["fieldErrors"][0]["field"] == "companyName"


def test_empty_patch_is_rejected(client):
    contractor_id = create_acme(client)
    assert call(client, "PATCH", "/api/contractors/" + contractor_id, "contractor", json={}).status_code == 400


def test_stranger_learns_nothing_from_validation(client):
    """A non-owner gets 403 even with a bad body, so they can't probe the rules on someone else's profile."""
    contractor_id = create_acme(client)
    response = call(client, "PATCH", "/api/contractors/" + contractor_id, "homeowner", json={"availability": "NOPE"})
    assert response.status_code == 403


def test_only_the_owner_can_delete_and_then_it_is_gone(client):
    contractor_id = create_acme(client)
    assert call(client, "DELETE", "/api/contractors/" + contractor_id, "homeowner").status_code == 403
    assert call(client, "DELETE", "/api/contractors/" + contractor_id, "contractor").status_code == 204
    assert call(client, "GET", "/api/contractors/" + contractor_id, "homeowner").status_code == 404
    assert call(client, "DELETE", "/api/contractors/" + contractor_id, "contractor").status_code == 404


def test_review_rules(client):
    contractor_id = create_acme(client)
    path = "/api/contractors/" + contractor_id + "/reviews"
    assert call(client, "POST", path, "contractor", json={"rating": 5}).status_code == 403
    assert call(client, "POST", path, "homeowner", json={"rating": 6}).status_code == 400
    assert call(client, "POST", path, "homeowner", json={"rating": True}).status_code == 400
    assert call(client, "POST", path, "homeowner", json={"rating": 4, "stars": 4}).status_code == 400
    assert call(client, "POST", "/api/contractors/c_000000/reviews", "homeowner", json={"rating": 4}).status_code == 404
    without_body = call(client, "POST", path, "homeowner", json={"rating": 4})
    assert without_body.status_code == 201
    assert without_body.json() == {"authorName": "Hana Okafor", "body": None, "rating": 4}
    profile = call(client, "GET", "/api/contractors/" + contractor_id, "homeowner").json()
    assert profile["reviews"] == [without_body.json()]


def test_page_size_and_token_are_checked(client):
    for query in ("pageSize=0", "pageSize=51", "pageSize=ten", "pageToken=not-a-token", "availability=SOMETIMES"):
        response = call(client, "GET", "/api/contractors?" + query, "homeowner")
        assert response.status_code == 400, query


def test_paging_walks_every_profile_once(client):
    for person in ("contractor", "second_contractor", "homeowner"):
        created = call(client, "POST", "/api/contractors", person,
                       json=ACME | {"companyName": person.replace("_", " ").title()})
        assert created.status_code == 201
    seen_names = []
    page_token = None
    while True:
        query = "pageSize=2" + ("&pageToken=" + page_token if page_token else "")
        page = call(client, "GET", "/api/contractors?" + query, "homeowner").json()
        seen_names.extend(profile["companyName"] for profile in page["contractorProfiles"])
        page_token = page["nextPageToken"]
        if page_token is None:
            break
    assert seen_names == ["Contractor", "Second Contractor", "Homeowner"]


def test_filters_ignore_capitals(client):
    create_acme(client)
    response = call(client, "GET", "/api/contractors?service=painting&serviceArea=los%20angeles%2C%20ca", "homeowner")
    assert len(response.json()["contractorProfiles"]) == 1
