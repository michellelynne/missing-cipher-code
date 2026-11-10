"""The health check that Docker and the update script use. It isn't part of the Contractors API, so
openapi.yaml doesn't list it."""


def test_health_check_answers_without_signing_in(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
