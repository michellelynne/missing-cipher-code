"""Polling, the queue and event bus, server-sent events, WebSockets, and webhooks."""

import asyncio
import json
import time

import pytest
from starlette.websockets import WebSocketDisconnect

import delivery_polling
import image_analysis
from conftest import bearer, check_against_asyncapi, check_against_openapi
from payment_webhooks import DEMO_WEBHOOK_SECRET, sign

PHOTOS = {"photoLocation": "s3://renovation-uploads/rooms/r_42/batch-7/", "photoCount": 25}


# ---------- Polling ----------

def test_polling_sees_a_change_after_304s(client):
    first = client.get("/api/orders/o_1001/delivery", headers=bearer("homeowner"))
    unchanged = client.get("/api/orders/o_1001/delivery", headers=bearer("homeowner") | {"If-None-Match": first.headers["etag"]})
    assert unchanged.status_code == 304
    assert unchanged.content == b""
    delivery_polling.advance_delivery(client.app.state.orders, "o_1001")
    changed = client.get("/api/orders/o_1001/delivery", headers=bearer("homeowner") | {"If-None-Match": first.headers["etag"]})
    assert changed.status_code == 200
    assert changed.json()["status"] == "OUT_FOR_DELIVERY"
    assert changed.headers["etag"] != first.headers["etag"]
    check_against_openapi(changed)


def test_polling_needs_sign_in_and_a_real_order(client):
    assert client.get("/api/orders/o_1001/delivery").status_code == 401
    missing = client.get("/api/orders/o_9999/delivery", headers=bearer("homeowner"))
    assert missing.status_code == 404
    check_against_openapi(missing)


# ---------- Queue, event bus, and server-sent events ----------

def read_events(client, events_url, headers):
    with client.stream("GET", events_url, headers=headers) as stream:
        assert stream.status_code == 200
        assert stream.headers["content-type"].startswith("text/event-stream")
        text = stream.read().decode()
    events = []
    for block in text.strip().split("\n\n"):
        fields = dict(line.split(": ", 1) for line in block.split("\n") if ": " in line)
        if "event" in fields:
            events.append((fields["event"], json.loads(fields["data"])))
    return events


def test_upload_answers_202_then_streams_progress_and_findings(client):
    accepted = client.post("/api/rooms/r_42/photo-batches", json=PHOTOS, headers=bearer("homeowner"))
    assert accepted.status_code == 202
    check_against_openapi(accepted)
    events = read_events(client, accepted.json()["eventsUrl"], bearer("homeowner"))
    assert events[-1][0] == "completed"
    assert [component["component"] for component in events[-1][1]["findings"]] == ["cabinets", "countertop"]
    progress = [data["analyzed"] for name, data in events if name == "progress"]
    assert progress == sorted(progress)


def test_every_message_matches_asyncapi(client):
    accepted = client.post("/api/rooms/r_42/photo-batches", json=PHOTOS, headers=bearer("homeowner"))
    read_events(client, accepted.json()["eventsUrl"], bearer("homeowner"))
    commands = client.app.state.queue.sent_messages
    events = client.app.state.event_bus.published_events
    assert len(commands) == 1
    check_against_asyncapi("AnalyzePhotosCommand", commands[0])
    for event in events:
        schema = {image_analysis.PHOTO_ANALYSIS_PROGRESSED: "PhotoAnalysisProgressedEvent",
                  image_analysis.PHOTOS_ANALYZED: "PhotosAnalyzedEvent"}[event["type"]]
        check_against_asyncapi(schema, event)
    assert [event["data"]["analyzed"] for event in events[:-1]] == [10, 20]


def test_a_command_delivered_twice_is_handled_once():
    """Queues deliver at least once, so the consumer skips IDs it has seen."""
    async def scenario():
        queue = image_analysis.MessageQueue()
        bus = image_analysis.EventBus()
        received = []

        async def record(event):
            received.append(event)
        bus.subscribe(record)
        worker = image_analysis.ImageAnalysisService(queue, bus, seconds_per_update=0)
        command = image_analysis.cloud_event(image_analysis.ANALYZE_PHOTOS, "/services/rooms",
                                             {"roomId": "r_1", "batchId": "b_1", "photoLocation": "s3://x/", "photoCount": 5})
        await queue.send(command)
        await queue.send(command)
        task = asyncio.create_task(worker.run_forever())
        await asyncio.sleep(0.05)
        task.cancel()
        return received
    received = asyncio.run(scenario())
    assert [event["type"] for event in received] == [image_analysis.PHOTOS_ANALYZED]


def test_every_subscriber_gets_its_own_copy():
    async def scenario():
        bus = image_analysis.EventBus()
        copies = []

        async def change_it(event):
            event["data"]["changed"] = True
            copies.append(event)

        async def read_it(event):
            copies.append(event)
        bus.subscribe(change_it)
        bus.subscribe(read_it)
        await bus.publish({"type": "test", "data": {}})
        return copies
    first_copy, second_copy = asyncio.run(scenario())
    assert first_copy["data"] == {"changed": True}
    assert second_copy["data"] == {}


def test_events_stream_rules(client):
    accepted = client.post("/api/rooms/r_42/photo-batches", json=PHOTOS, headers=bearer("homeowner")).json()
    events_url = accepted["eventsUrl"]
    assert client.get(events_url).status_code == 401
    assert client.get(events_url.replace("r_42", "r_43"), headers=bearer("homeowner")).status_code == 404
    # EventSource can't send headers, so the token can come in the URL instead.
    events = read_events(client, events_url + "?token=homeowner-token", {})
    assert events[-1][0] == "completed"


def test_upload_is_checked(client):
    for body in ({"photoLocation": "", "photoCount": 3}, {"photoLocation": "s3://x/", "photoCount": 0}, ["not", "an", "object"]):
        response = client.post("/api/rooms/r_42/photo-batches", json=body, headers=bearer("homeowner"))
        assert response.status_code == 400
        check_against_openapi(response)


# ---------- WebSocket ----------

def test_websocket_needs_a_token_first(client):
    with client.websocket_connect("/ws/conversations/conv_1") as connection:
        connection.send_text(json.dumps({"type": "send", "text": "hi"}))
        error = json.loads(connection.receive_text())
        check_against_asyncapi("ErrorFrame", error)
        assert error["code"] == "UNAUTHENTICATED"
        with pytest.raises(WebSocketDisconnect) as closed:
            connection.receive_text()
        assert closed.value.code == 4401


def test_websocket_rejects_unknown_conversations(client):
    with client.websocket_connect("/ws/conversations/conv_404") as connection:
        connection.send_text(json.dumps({"type": "authenticate", "token": "homeowner-token"}))
        assert json.loads(connection.receive_text())["code"] == "FORBIDDEN"


def test_websocket_survives_bad_json(client):
    with client.websocket_connect("/ws/conversations/conv_1") as connection:
        connection.send_text(json.dumps({"type": "authenticate", "token": "homeowner-token"}))
        connection.send_text("this isn't JSON")
        assert json.loads(connection.receive_text())["code"] == "BAD_MESSAGE"
        connection.send_text(json.dumps({"type": "send", "text": "Still here?"}))
        posted = json.loads(connection.receive_text())
        check_against_asyncapi("MessagePostedFrame", posted)
        assert posted["text"] == "Still here?"


# ---------- Webhooks ----------

def signed_webhook(client, body, webhook_id="msg_1", timestamp=None, secret=DEMO_WEBHOOK_SECRET):
    body_text = json.dumps(body)
    timestamp = str(timestamp if timestamp is not None else int(time.time()))
    headers = {"content-type": "application/json", "webhook-id": webhook_id, "webhook-timestamp": timestamp,
               "webhook-signature": sign(secret, webhook_id, timestamp, body_text.encode())}
    return client.post("/webhooks/payments", content=body_text, headers=headers)


PAYMENT = {"type": "subscription.payment_succeeded",
           "data": {"contractorId": "c_8f3a2b", "subscriptionId": "sub_4471", "amountCents": 4900, "currency": "USD"}}


def test_a_signed_webhook_activates_the_subscription(client):
    response = signed_webhook(client, PAYMENT)
    assert response.status_code == 204
    check_against_openapi(response)
    assert client.app.state.subscriptions["c_8f3a2b"]["status"] == "ACTIVE"


def test_the_same_webhook_twice_changes_nothing(client):
    assert signed_webhook(client, PAYMENT).status_code == 204
    client.app.state.subscriptions["c_8f3a2b"]["status"] = "CANCELLED"
    assert signed_webhook(client, PAYMENT).status_code == 204
    assert client.app.state.subscriptions["c_8f3a2b"]["status"] == "CANCELLED"


def test_bad_signatures_are_rejected(client):
    wrong_secret = "whsec_" + "c29tZWJvZHktZWxzZQ=="
    assert signed_webhook(client, PAYMENT, secret=wrong_secret).status_code == 401
    assert signed_webhook(client, PAYMENT, timestamp=int(time.time()) - 600).status_code == 401
    unsigned = client.post("/webhooks/payments", json=PAYMENT)
    assert unsigned.status_code == 401
    # A tampered body fails even with headers from a real call.
    real = json.dumps(PAYMENT)
    timestamp = str(int(time.time()))
    headers = {"webhook-id": "msg_2", "webhook-timestamp": timestamp,
               "webhook-signature": sign(DEMO_WEBHOOK_SECRET, "msg_2", timestamp, real.encode())}
    tampered = real.replace("4900", "1")
    assert client.post("/webhooks/payments", content=tampered, headers=headers).status_code == 401
    assert client.app.state.subscriptions == {}


def test_any_listed_signature_can_match(client):
    """During a secret rotation the sender lists signatures from the old and new secrets."""
    body_text = json.dumps(PAYMENT)
    timestamp = str(int(time.time()))
    good = sign(DEMO_WEBHOOK_SECRET, "msg_3", timestamp, body_text.encode())
    headers = {"webhook-id": "msg_3", "webhook-timestamp": timestamp, "webhook-signature": "v1,b2xkLXNpZw== " + good}
    assert client.post("/webhooks/payments", content=body_text, headers=headers).status_code == 204


def test_signed_but_unknown_payload_is_400(client):
    assert signed_webhook(client, {"type": "subscription.cancelled", "data": {}}).status_code == 400
    assert signed_webhook(client, {"type": "subscription.payment_succeeded"}, webhook_id="msg_4").status_code == 400
