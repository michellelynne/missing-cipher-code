"""Shared setup for the tests: a fresh server for each test, and checks against the published specs.

Run the tests from the server folder:
    pip install -r requirements.txt
    python3 -m pytest
"""

import re
import sys
from pathlib import Path

import grpc
import pytest
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from starlette.testclient import TestClient

SERVER_FOLDER = Path(__file__).resolve().parent.parent
API_FOLDER = SERVER_FOLDER.parent
sys.path.insert(0, str(SERVER_FOLDER))

from app import build_app  # noqa: E402
from directory import ContractorDirectory  # noqa: E402
from grpc_api import build_grpc_server, contractor_pb2, contractor_pb2_grpc  # noqa: E402, F401  (tests import contractor_pb2 from here)

OPENAPI = yaml.safe_load((API_FOLDER / "openapi.yaml").read_text())
ASYNCAPI = yaml.safe_load((API_FOLDER / "messaging" / "asyncapi.yaml").read_text())
OPENAPI_URI = "urn:renovation-revolution:openapi"
ASYNCAPI_URI = "urn:renovation-revolution:asyncapi"
SCHEMA_REGISTRY = Registry().with_resources([
    (OPENAPI_URI, Resource.from_contents(OPENAPI, default_specification=DRAFT202012)),
    (ASYNCAPI_URI, Resource.from_contents(ASYNCAPI, default_specification=DRAFT202012)),
])

TOKENS = {
    "homeowner": "homeowner-token",
    "contractor": "contractor-token",
    "second_contractor": "second-contractor-token",
}


def bearer(person):
    return {"Authorization": "Bearer " + TOKENS[person]}


def grpc_metadata(person):
    return [("authorization", "Bearer " + TOKENS[person])]


# ---------- Fresh servers ----------

@pytest.fixture
def directory():
    return ContractorDirectory()


@pytest.fixture
def client(directory):
    """The web app (REST, GraphQL, messaging) with a small delay, so progress events have time to happen."""
    with TestClient(build_app(directory, seconds_per_analysis_update=0.01)) as test_client:
        yield test_client


@pytest.fixture
def grpc_stub(directory):
    """A gRPC server sharing the same directory as client, on a free port."""
    server, port = build_grpc_server(directory, "localhost:0")
    server.start()
    channel = grpc.insecure_channel("localhost:" + str(port))
    yield contractor_pb2_grpc.ContractorProfileServiceStub(channel)
    channel.close()
    server.stop(None)


# ---------- Checking responses against openapi.yaml ----------

def json_pointer_part(text):
    return text.replace("~", "~0").replace("/", "~1")


def openapi_path_template(url_path):
    """Finds the openapi.yaml path that a real URL path matches, like /api/contractors/{contractorId}."""
    for template in OPENAPI["paths"]:
        pattern = "^" + re.sub(r"\{[^/]+\}", "[^/]+", template) + "$"
        if re.match(pattern, url_path):
            return template
    raise AssertionError("openapi.yaml has no path for " + url_path)


def check_against_openapi(response):
    """Fails unless openapi.yaml lists this status for this call, and the body matches its schema."""
    request = response.request
    template = openapi_path_template(request.url.path)
    method = request.method.lower()
    operation = OPENAPI["paths"][template].get(method)
    assert operation is not None, "openapi.yaml has no " + method.upper() + " for " + template
    status = str(response.status_code)
    assert status in operation["responses"], "openapi.yaml doesn't list " + status + " for " + method.upper() + " " + template
    response_spec = operation["responses"][status]
    pointer = "/paths/" + json_pointer_part(template) + "/" + method + "/responses/" + status
    if "$ref" in response_spec:
        pointer = response_spec["$ref"].lstrip("#")
        response_spec = OPENAPI["components"]["responses"][response_spec["$ref"].split("/")[-1]]
    content = response_spec.get("content")
    if not content:
        return
    content_type = response.headers.get("content-type", "").split(";")[0]
    assert content_type in content, "openapi.yaml doesn't list " + content_type + " for " + status
    if content_type.endswith("json"):
        schema_pointer = pointer + "/content/" + json_pointer_part(content_type) + "/schema"
        validator = Draft202012Validator({"$ref": OPENAPI_URI + "#" + schema_pointer},
                                         registry=SCHEMA_REGISTRY, format_checker=FormatChecker())
        validator.validate(response.json())


# ---------- Checking messages against asyncapi.yaml ----------

def check_against_asyncapi(schema_name, message):
    validator = Draft202012Validator({"$ref": ASYNCAPI_URI + "#/components/schemas/" + schema_name},
                                     registry=SCHEMA_REGISTRY, format_checker=FormatChecker())
    validator.validate(message)


# ---------- Shortcuts ----------

ACME = {
    "companyName": "Acme Renovations",
    "services": ["Painting", "Flooring"],
    "serviceArea": "Los Angeles, CA",
    "availability": "OPEN",
    "insuranceExpiresOn": "2027-03-31",
}


def create_acme(client):
    response = client.post("/api/contractors", json=ACME, headers=bearer("contractor"))
    assert response.status_code == 201
    return response.json()["contractorId"]
