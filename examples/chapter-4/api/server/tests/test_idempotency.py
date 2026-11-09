"""Idempotency keys: a create that's retried with the same key happens once, in all three styles."""

import grpc
import pytest

from conftest import bearer, check_against_openapi, contractor_pb2, create_acme, grpc_metadata

KEY = "5b0f3c1e-8a4d-4f7e-9c2b-1d6e7a8f9b30"
REVIEW = {"rating": 5, "body": "Great work."}


def review_count(client, contractor_id):
    return len(client.get("/api/contractors/" + contractor_id, headers=bearer("homeowner")).json()["reviews"])


def test_rest_retry_returns_the_first_response(client):
    contractor_id = create_acme(client)
    headers = bearer("homeowner") | {"Idempotency-Key": KEY}
    first = client.post("/api/contractors/" + contractor_id + "/reviews", json=REVIEW, headers=headers)
    retry = client.post("/api/contractors/" + contractor_id + "/reviews", json=REVIEW, headers=headers)
    check_against_openapi(first)
    check_against_openapi(retry)
    assert first.status_code == retry.status_code == 201
    assert retry.json() == first.json()
    assert "idempotent-replayed" not in first.headers
    assert retry.headers["idempotent-replayed"] == "true"
    assert review_count(client, contractor_id) == 1


def test_rest_create_profile_retry_is_not_a_conflict(client):
    """Without a key, a second create is 409. With the same key, it's the first 201 again."""
    headers = bearer("contractor") | {"Idempotency-Key": KEY}
    profile = {"companyName": "Acme Renovations", "services": ["Painting"], "serviceArea": "Los Angeles, CA", "availability": "OPEN"}
    first = client.post("/api/contractors", json=profile, headers=headers)
    retry = client.post("/api/contractors", json=profile, headers=headers)
    assert retry.status_code == 201
    assert retry.json()["contractorId"] == first.json()["contractorId"]
    assert retry.headers["location"] == first.headers["location"]
    assert client.post("/api/contractors", json=profile, headers=bearer("contractor")).status_code == 409


def test_rest_same_key_different_request_is_422(client):
    contractor_id = create_acme(client)
    headers = bearer("homeowner") | {"Idempotency-Key": KEY}
    client.post("/api/contractors/" + contractor_id + "/reviews", json=REVIEW, headers=headers)
    reused = client.post("/api/contractors/" + contractor_id + "/reviews", json=REVIEW | {"rating": 4}, headers=headers)
    assert reused.status_code == 422
    check_against_openapi(reused)
    assert review_count(client, contractor_id) == 1


def test_keys_belong_to_one_user(client):
    """Someone else's key, even the same string, is a different key."""
    contractor_id = create_acme(client)
    for person in ("homeowner", "second_contractor"):
        response = client.post("/api/contractors/" + contractor_id + "/reviews", json=REVIEW,
                               headers=bearer(person) | {"Idempotency-Key": KEY})
        assert response.status_code == 201
        assert "idempotent-replayed" not in response.headers
    assert review_count(client, contractor_id) == 2


def test_a_failed_request_can_be_fixed_and_retried_with_the_same_key(client):
    contractor_id = create_acme(client)
    headers = bearer("homeowner") | {"Idempotency-Key": KEY}
    failed = client.post("/api/contractors/" + contractor_id + "/reviews", json={"rating": 9}, headers=headers)
    assert failed.status_code == 400
    fixed = client.post("/api/contractors/" + contractor_id + "/reviews", json={"rating": 5}, headers=headers)
    assert fixed.status_code == 201


def test_key_length_is_checked(client):
    contractor_id = create_acme(client)
    response = client.post("/api/contractors/" + contractor_id + "/reviews", json=REVIEW,
                           headers=bearer("homeowner") | {"Idempotency-Key": "x" * 256})
    assert response.status_code == 400
    assert response.json()["fieldErrors"][0]["field"] == "Idempotency-Key"


def test_graphql_retry_and_reuse(client):
    contractor_id = create_acme(client)
    mutation = "mutation($id: ID!, $input: CreateReviewInput!) { createReview(contractorId: $id, input: $input) { rating } }"
    headers = bearer("homeowner") | {"Idempotency-Key": KEY}
    for _ in range(2):
        result = client.post("/graphql", headers=headers, json={"query": mutation, "variables": {"id": contractor_id, "input": REVIEW}}).json()
        assert result == {"data": {"createReview": {"rating": 5}}}
    assert review_count(client, contractor_id) == 1
    reused = client.post("/graphql", headers=headers, json={"query": mutation, "variables": {"id": contractor_id, "input": {"rating": 3}}}).json()
    assert reused["errors"][0]["extensions"]["code"] == "IDEMPOTENCY_KEY_REUSED"


def test_grpc_retry_and_reuse(client, grpc_stub):
    contractor_id = create_acme(client)
    metadata = grpc_metadata("homeowner") + [("idempotency-key", KEY)]
    request = contractor_pb2.CreateReviewRequest(contractor_id=contractor_id, rating=5, body="Great work.")
    first, first_call = grpc_stub.CreateReview.with_call(request, metadata=metadata)
    retry, retry_call = grpc_stub.CreateReview.with_call(request, metadata=metadata)
    assert retry == first
    assert ("idempotent-replayed", "true") not in first_call.initial_metadata()
    assert ("idempotent-replayed", "true") in retry_call.initial_metadata()
    assert review_count(client, contractor_id) == 1
    with pytest.raises(grpc.RpcError) as reused:
        grpc_stub.CreateReview(contractor_pb2.CreateReviewRequest(contractor_id=contractor_id, rating=2), metadata=metadata)
    assert reused.value.code() == grpc.StatusCode.FAILED_PRECONDITION
