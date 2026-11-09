"""Photo analysis through a queue and an event bus, with progress streamed to the homeowner.

  1. The homeowner uploads photos, and POST /api/rooms/{roomId}/photo-batches answers 202 right away.
  2. The room service puts an AnalyzePhotos command on the queue. Commands go on queues.
  3. The image analysis service takes it off the queue and publishes progress, then its findings, on the
     event bus. Results go on the event bus.
  4. The room service subscribes to the bus, saves the findings, and passes each update to the homeowner's
     open server-sent events stream at .../events.

The queue and event bus here are in memory, standing in for SQS and SNS. The message shapes are the
ones in messaging/asyncapi.yaml.
"""

import asyncio
import copy
import datetime
import json
import secrets

from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route

from auth import user_from_authorization_header
from directory import NotFound, NotSignedIn, ValidationFailed
from rest_api import problem_response

ANALYZE_PHOTOS = "com.renovationrevolution.imageanalysis.analyze-photos.v1"
PHOTO_ANALYSIS_PROGRESSED = "com.renovationrevolution.imageanalysis.photo-analysis-progressed.v1"
PHOTOS_ANALYZED = "com.renovationrevolution.imageanalysis.photos-analyzed.v1"
PHOTOS_PER_PROGRESS_UPDATE = 10


def cloud_event(event_type, source, data):
    """Wraps data in the CloudEvents envelope every service reads the same way."""
    return {
        "specversion": "1.0",
        "id": "evt_" + secrets.token_hex(4),
        "source": source,
        "type": event_type,
        "time": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data": data,
    }


class MessageQueue:
    """Each message is handled once, by one consumer."""

    def __init__(self):
        self.waiting_messages = asyncio.Queue()
        self.sent_messages = []  # kept so tests can check every message against asyncapi.yaml

    async def send(self, message):
        self.sent_messages.append(copy.deepcopy(message))
        await self.waiting_messages.put(copy.deepcopy(message))

    async def receive(self):
        return await self.waiting_messages.get()


class EventBus:
    """Every subscriber gets its own copy of each event."""

    def __init__(self):
        self.subscribers = []
        self.published_events = []

    def subscribe(self, handler):
        self.subscribers.append(handler)

    async def publish(self, event):
        self.published_events.append(copy.deepcopy(event))
        for handler in self.subscribers:
            await handler(copy.deepcopy(event))


class RoomService:
    """Owns everything about a room, including what its photos showed."""

    def __init__(self, queue, event_bus):
        self.queue = queue
        self.batches = {}
        self.listeners = {}  # batch ID -> asyncio queues of updates, one per open events stream
        event_bus.subscribe(self.on_image_analysis_event)

    async def start_batch(self, room_id, photo_location, photo_count):
        batch_id = "b_" + secrets.token_hex(3)
        self.batches[batch_id] = {"room_id": room_id, "analyzed": 0, "total": photo_count, "findings": None}
        command = cloud_event(ANALYZE_PHOTOS, "/services/rooms", {
            "roomId": room_id, "batchId": batch_id, "photoLocation": photo_location, "photoCount": photo_count,
        })
        await self.queue.send(command)
        return batch_id

    async def on_image_analysis_event(self, event):
        batch_id = event["data"]["batchId"]
        if batch_id not in self.batches:
            return
        batch = self.batches[batch_id]
        if event["type"] == PHOTO_ANALYSIS_PROGRESSED:
            batch["analyzed"] = event["data"]["analyzed"]
            update = ("progress", {"batchId": batch_id, "analyzed": batch["analyzed"], "total": batch["total"]})
        elif event["type"] == PHOTOS_ANALYZED:
            batch["analyzed"] = batch["total"]
            batch["findings"] = event["data"]["findings"]
            update = ("completed", {"batchId": batch_id, "findings": batch["findings"]})
        else:
            return
        for listener in self.listeners.get(batch_id, []):
            await listener.put(update)


class ImageAnalysisService:
    """Takes commands off the queue. Delivery is at least once, so it skips commands it has seen."""

    def __init__(self, queue, event_bus, seconds_per_update):
        self.queue = queue
        self.event_bus = event_bus
        self.seconds_per_update = seconds_per_update
        self.handled_command_ids = set()

    async def run_forever(self):
        while True:
            command = await self.queue.receive()
            if command["id"] in self.handled_command_ids:
                continue
            self.handled_command_ids.add(command["id"])
            await self.analyze(command["data"])

    async def analyze(self, batch):
        analyzed = 0
        while analyzed < batch["photoCount"]:
            await asyncio.sleep(self.seconds_per_update)
            analyzed = min(analyzed + PHOTOS_PER_PROGRESS_UPDATE, batch["photoCount"])
            if analyzed < batch["photoCount"]:
                await self.event_bus.publish(cloud_event(PHOTO_ANALYSIS_PROGRESSED, "/services/image-analysis", {
                    "roomId": batch["roomId"], "batchId": batch["batchId"],
                    "analyzed": analyzed, "total": batch["photoCount"],
                }))
        # A real service would run a vision model on the photos at photoLocation. This one always finds the same kitchen.
        await self.event_bus.publish(cloud_event(PHOTOS_ANALYZED, "/services/image-analysis", {
            "roomId": batch["roomId"], "batchId": batch["batchId"],
            "findings": [
                {"component": "cabinets", "material": "oak", "condition": "worn"},
                {"component": "countertop", "material": "laminate", "condition": "chipped"},
            ],
        }))


def server_sent_event(event_name, data, event_number):
    """One event in the text/event-stream format: id, event name, JSON data, then a blank line."""
    return "id: " + str(event_number) + "\nevent: " + event_name + "\ndata: " + json.dumps(data) + "\n\n"


async def analyze_photo_batch(request):
    try:
        user = user_from_authorization_header(request.headers.get("authorization"))
        if user is None:
            raise NotSignedIn("Sign in first. Send your token as Authorization: Bearer <token>.")
        try:
            body = await request.json()
        except ValueError:
            body = None
        field_errors = []
        if not isinstance(body, dict):
            raise ValidationFailed([("body", "Send a JSON object.")])
        if not isinstance(body.get("photoLocation"), str) or not body["photoLocation"].strip():
            field_errors.append(("photoLocation", "Say where the photos are stored."))
        photo_count = body.get("photoCount")
        if not isinstance(photo_count, int) or isinstance(photo_count, bool) or photo_count < 1 or photo_count > 200:
            field_errors.append(("photoCount", "Send from 1 to 200 photos at a time."))
        if field_errors:
            raise ValidationFailed(field_errors)
    except (NotSignedIn, ValidationFailed) as error:
        return problem_response(error)

    room_id = request.path_params["roomId"]
    batch_id = await request.app.state.room_service.start_batch(room_id, body["photoLocation"], photo_count)
    events_url = "/api/rooms/" + room_id + "/photo-batches/" + batch_id + "/events"
    return JSONResponse({"batchId": batch_id, "status": "QUEUED", "eventsUrl": events_url}, status_code=202)


async def stream_photo_batch_events(request):
    # EventSource in the browser can't send headers, so this also accepts ?token=. Use a short-lived
    # token for that in production, since URLs end up in logs.
    user = user_from_authorization_header(request.headers.get("authorization"))
    if user is None and request.query_params.get("token"):
        user = user_from_authorization_header("Bearer " + request.query_params["token"])
    if user is None:
        return problem_response(NotSignedIn("Sign in first."))
    room_service = request.app.state.room_service
    batch_id = request.path_params["batchId"]
    batch = room_service.batches.get(batch_id)
    if batch is None or batch["room_id"] != request.path_params["roomId"]:
        return problem_response(NotFound("There's no photo batch with the ID " + batch_id + "."))

    updates = asyncio.Queue()
    room_service.listeners.setdefault(batch_id, []).append(updates)

    async def event_stream():
        event_number = 1
        try:
            # Start with where things stand, so a browser that reconnects catches up right away.
            yield "retry: 3000\n\n"
            if batch["findings"] is not None:
                yield server_sent_event("completed", {"batchId": batch_id, "findings": batch["findings"]}, event_number)
                return
            yield server_sent_event("progress", {"batchId": batch_id, "analyzed": batch["analyzed"], "total": batch["total"]}, event_number)
            while True:
                event_name, data = await updates.get()
                event_number = event_number + 1
                yield server_sent_event(event_name, data, event_number)
                if event_name == "completed":
                    return
        finally:
            room_service.listeners[batch_id].remove(updates)

    return StreamingResponse(event_stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


routes = [
    Route("/api/rooms/{roomId}/photo-batches", analyze_photo_batch, methods=["POST"]),
    Route("/api/rooms/{roomId}/photo-batches/{batchId}/events", stream_photo_batch_events, methods=["GET"]),
]
