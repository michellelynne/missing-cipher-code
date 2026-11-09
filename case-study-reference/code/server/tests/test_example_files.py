"""Runs every request in the published example files against a fresh server, and checks that the
response is exactly the one the file shows. If a file and the server ever disagree, this fails."""

import json
import re

import grpc
from google.protobuf import json_format
from google.rpc import error_details_pb2
from grpc_status import rpc_status

from conftest import API_FOLDER, check_against_asyncapi, check_against_openapi, contractor_pb2
from payment_webhooks import DEMO_WEBHOOK_SECRET, signature_is_valid

PLACEHOLDER_IDS = ["c_8f3a2b", "c_51d2e0"]
GRPC_CODES = {
    "OK": grpc.StatusCode.OK,
    "InvalidArgument": grpc.StatusCode.INVALID_ARGUMENT,
    "Unauthenticated": grpc.StatusCode.UNAUTHENTICATED,
    "PermissionDenied": grpc.StatusCode.PERMISSION_DENIED,
    "NotFound": grpc.StatusCode.NOT_FOUND,
    "AlreadyExists": grpc.StatusCode.ALREADY_EXISTS,
    "FailedPrecondition": grpc.StatusCode.FAILED_PRECONDITION,
}


# ---------- Reading the files ----------

def example_blocks(file_name):
    """Splits a file into its ### sections, skipping the header before the first one."""
    text = (API_FOLDER / file_name).read_text()
    return [block for block in re.split(r"^### ", text, flags=re.MULTILINE)[1:]]


def expected_status(block):
    return re.search(r"^# Expect: (\S+)", block, flags=re.MULTILINE).group(1)


def shown_response(block):
    """The response written as comments after "# Response", without the "# " in front of each line."""
    response_part = block.split("\n# Response", 1)[1]
    after_marker = response_part.split("\n", 1)[1] if "\n" in response_part else ""
    lines = []
    for line in after_marker.split("\n"):
        if line.startswith("# "):
            lines.append(line[2:])
        elif line == "#":
            lines.append("")
    return "\n".join(lines)


def shown_json(block):
    """The JSON body shown in the response, or None when there isn't one."""
    response_text = shown_response(block)
    start = response_text.find("{")
    if start == -1:
        return None
    return json.loads(response_text[start:])


def parse_http_request(block):
    """Reads the method, path, headers, and body of one request in a .http file."""
    request_part = block.split("\n# Response", 1)[0]
    lines = [line for line in request_part.split("\n")[1:] if not line.startswith("#")]
    while lines and not lines[0].strip():
        lines.pop(0)
    method, path = lines[0].split(" ", 1)
    path = path.replace("{{baseUrl}}", "")
    headers = {}
    line_number = 1
    while line_number < len(lines) and lines[line_number].strip():
        name, value = lines[line_number].split(":", 1)
        headers[name.strip()] = value.strip()
        line_number = line_number + 1
    body = "\n".join(lines[line_number:]).strip()
    return method, path, headers, body


class IdTracker:
    """Swaps the files' placeholder IDs for the ones the server really makes, and back."""

    def __init__(self):
        self.actual_for_placeholder = {}

    def learn(self, actual_id):
        if actual_id not in self.actual_for_placeholder.values():
            placeholder = PLACEHOLDER_IDS[len(self.actual_for_placeholder)]
            self.actual_for_placeholder[placeholder] = actual_id

    def to_actual(self, text):
        for placeholder, actual in self.actual_for_placeholder.items():
            text = text.replace(placeholder, actual)
        return text

    def to_placeholder(self, value):
        text = json.dumps(value)
        for placeholder, actual in self.actual_for_placeholder.items():
            text = text.replace(actual, placeholder)
        return json.loads(text)


# ---------- REST ----------

def test_rest_file(client):
    ids = IdTracker()
    blocks = example_blocks("rest.http")
    assert len(blocks) >= 14
    for block in blocks:
        title = block.split("\n", 1)[0]
        method, path, headers, body = parse_http_request(block)
        response = client.request(method, ids.to_actual(path), headers=headers,
                                  content=ids.to_actual(body) if body else None)
        assert str(response.status_code) == expected_status(block), title
        check_against_openapi(response)
        if method == "POST" and path == "/api/contractors" and response.status_code == 201:
            ids.learn(response.json()["contractorId"])
        if response.content:
            assert ids.to_placeholder(response.json()) == shown_json(block), title
        else:
            assert shown_json(block) is None, title
        shown_replay = "Idempotent-Replayed: true" in shown_response(block)
        assert (response.headers.get("idempotent-replayed") == "true") == shown_replay, title


# ---------- GraphQL ----------

def test_graphql_file(client):
    ids = IdTracker()
    blocks = example_blocks("graphql.http")
    assert len(blocks) >= 14
    for block in blocks:
        title = block.split("\n", 1)[0]
        method, path, headers, body = parse_http_request(block)
        assert headers.pop("X-Request-Type") == "GraphQL"
        query, variables_text = body.rsplit("\n\n", 1)
        response = client.post("/graphql", headers=headers,
                               json={"query": query, "variables": json.loads(ids.to_actual(variables_text))})
        assert str(response.status_code) == expected_status(block), title
        created = (response.json().get("data") or {}).get("createContractorProfile")
        if created:
            ids.learn(created["contractorId"])
        assert ids.to_placeholder(response.json()) == shown_json(block), title


# ---------- gRPC ----------

def parse_grpcurl(block):
    command = block.split("\n# Response", 1)[0]
    method_name = re.search(r"ContractorProfileService/(\w+)", command).group(1)
    metadata = re.findall(r"-H '([^:']+): ([^']+)'", command)
    request_json = re.search(r"-d '(.*?)' \\", command, flags=re.DOTALL).group(1)
    return method_name, metadata, request_json


def test_grpc_file(grpc_stub):
    ids = IdTracker()
    service = contractor_pb2.DESCRIPTOR.services_by_name["ContractorProfileService"]
    blocks = example_blocks("grpc-calls.sh")
    assert len(blocks) >= 14
    for block in blocks:
        title = block.split("\n", 1)[0]
        method_name, metadata, request_json = parse_grpcurl(block)
        request_class = getattr(contractor_pb2, service.methods_by_name[method_name].input_type.name)
        request = json_format.Parse(ids.to_actual(request_json), request_class())
        try:
            response = getattr(grpc_stub, method_name)(request, metadata=metadata)
            code = grpc.StatusCode.OK
        except grpc.RpcError as error:
            code = error.code()
            response = error
        assert code == GRPC_CODES[expected_status(block)], title
        if code == grpc.StatusCode.OK:
            result = json_format.MessageToDict(response, always_print_fields_with_no_presence=True)
            if method_name == "CreateContractorProfile":
                ids.learn(result["contractorId"])
            assert ids.to_placeholder(result) == shown_json(block), title
        else:
            shown = shown_response(block)
            assert "  Message: " + response.details() in ids.to_actual(shown), title
            status = rpc_status.from_call(response)
            if status is not None and status.details:
                bad_request = error_details_pb2.BadRequest()
                status.details[0].Unpack(bad_request)
                for violation in bad_request.field_violations:
                    assert '"field": "' + violation.field + '", "description": "' + violation.description + '"' in shown, title


# ---------- Messaging ----------

def test_polling_file(client):
    blocks = example_blocks("messaging/polling.http")
    previous_etag = None
    for block in blocks:
        method, path, headers, body = parse_http_request(block)
        response = client.request(method, path, headers=headers)
        assert str(response.status_code) == expected_status(block)
        check_against_openapi(response)
        assert "ETag: " + response.headers["etag"] in shown_response(block)
        if response.status_code == 200:
            assert response.json() == shown_json(block)
            previous_etag = response.headers["etag"]
        else:
            assert headers["If-None-Match"] == previous_etag


def test_photo_analysis_file(client):
    upload_block, events_block = example_blocks("messaging/photo-analysis.http")
    method, path, headers, body = parse_http_request(upload_block)
    accepted = client.post(path, headers=headers, content=body)
    assert str(accepted.status_code) == expected_status(upload_block)
    check_against_openapi(accepted)
    batch_id = accepted.json()["batchId"]
    assert json.loads(json.dumps(accepted.json()).replace(batch_id, "b_7")) == shown_json(upload_block)

    method, path, headers, body = parse_http_request(events_block)
    with client.stream("GET", path.replace("b_7", batch_id), headers=headers) as stream:
        assert str(stream.status_code) == expected_status(events_block)
        stream_text = stream.read().decode().replace(batch_id, "b_7")
    # How many progress events arrive depends on timing, so check the shape rather than every line:
    # the same kinds of event, counts that only go up, and the same findings at the end.
    shown_events = re.findall(r"^event: (\w+)\ndata: (.*)$", shown_response(events_block), flags=re.MULTILINE)
    real_events = re.findall(r"^event: (\w+)\ndata: (.*)$", stream_text, flags=re.MULTILINE)
    assert [name for name, _ in real_events][-1] == "completed"
    assert set(name for name, _ in real_events) == set(name for name, _ in shown_events)
    counts = [json.loads(data)["analyzed"] for name, data in real_events if name == "progress"]
    assert counts == sorted(counts)
    assert json.loads(real_events[-1][1]) == json.loads(shown_events[-1][1])


def test_payment_webhook_file():
    block = example_blocks("messaging/payment-webhook.http")[0]
    method, path, headers, body = parse_http_request(block)
    lowercase_headers = {name.lower(): value for name, value in headers.items()}
    signed_at = int(lowercase_headers["webhook-timestamp"])
    # Correctly signed for the moment it was made...
    assert signature_is_valid(DEMO_WEBHOOK_SECRET, lowercase_headers, body.encode(), now=signed_at)
    # ...and rejected as a replay once it's old, which is what the file says will happen.
    assert not signature_is_valid(DEMO_WEBHOOK_SECRET, lowercase_headers, body.encode(), now=signed_at + 301)


def test_conversation_file(client):
    lines = (API_FOLDER / "messaging" / "conversation.txt").read_text().split("\n")
    steps = [re.match(r"^(\w+)\s+(sends|receives)\s+(\{.*\})$", line) for line in lines]
    steps = [step.groups() for step in steps if step]
    connections = {}
    for who, action, frame_text in steps:
        frame = json.loads(frame_text)
        if who not in connections:
            connections[who] = client.websocket_connect("/ws/conversations/conv_1").__enter__()
        connection = connections[who]
        if action == "sends":
            schema = {"authenticate": "AuthenticateFrame", "send": "SendMessageFrame"}[frame["type"]]
            if frame["type"] == "send" and frame["text"]:
                check_against_asyncapi(schema, frame)
            connection.send_text(json.dumps(frame))
        else:
            received = json.loads(connection.receive_text())
            schema = {"message": "MessagePostedFrame", "error": "ErrorFrame"}[received["type"]]
            check_against_asyncapi(schema, received)
            if "sentAt" in received:
                received["sentAt"] = frame["sentAt"]
            assert received == frame
    for connection in connections.values():
        connection.__exit__(None, None, None)
