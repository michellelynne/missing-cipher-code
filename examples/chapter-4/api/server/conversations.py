"""WebSocket messaging between a homeowner and their contractor.

The app opens one connection and keeps it open, so either side can send at any moment. When the
contractor asks whether the cabinets should stay, the question appears for the homeowner without a
refresh. The frames are the ones in messaging/asyncapi.yaml.
"""

import asyncio
import datetime
import json

from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocketDisconnect

from auth import user_for_token

SECONDS_TO_AUTHENTICATE = 10
LONGEST_MESSAGE = 2000


def starting_conversations():
    """Who may join each conversation. In the real app this comes from the project's records."""
    return {"conv_1": {"participants": {"u_homeowner", "u_contractor"}, "connections": set(), "message_count": 0}}


async def send_error(websocket, code, message):
    await websocket.send_text(json.dumps({"type": "error", "code": code, "message": message}))


async def conversation_socket(websocket):
    await websocket.accept()
    conversations = websocket.app.state.conversations
    conversation = conversations.get(websocket.path_params["conversationId"])

    # Browsers can't add headers to a WebSocket, so the token comes in the first message.
    try:
        first_text = await asyncio.wait_for(websocket.receive_text(), timeout=SECONDS_TO_AUTHENTICATE)
        first_frame = json.loads(first_text)
    except (asyncio.TimeoutError, ValueError, WebSocketDisconnect):
        first_frame = None
    user = None
    if isinstance(first_frame, dict) and first_frame.get("type") == "authenticate":
        user = user_for_token(first_frame.get("token"))
    if user is None:
        await send_error(websocket, "UNAUTHENTICATED", "The first message must be authenticate, with a valid token.")
        await websocket.close(code=4401)
        return
    if conversation is None or user["user_id"] not in conversation["participants"]:
        await send_error(websocket, "FORBIDDEN", "You're not part of this conversation.")
        await websocket.close(code=4403)
        return

    conversation["connections"].add(websocket)
    try:
        while True:
            try:
                frame = json.loads(await websocket.receive_text())
            except ValueError:
                await send_error(websocket, "BAD_MESSAGE", "Send JSON, like {\"type\": \"send\", \"text\": \"Hi\"}.")
                continue
            text = frame.get("text") if isinstance(frame, dict) else None
            if not isinstance(frame, dict) or frame.get("type") != "send" or not isinstance(text, str) \
                    or not text.strip() or len(text) > LONGEST_MESSAGE:
                await send_error(websocket, "BAD_MESSAGE", "Send {\"type\": \"send\", \"text\": ...} with 1 to 2,000 characters.")
                continue
            conversation["message_count"] = conversation["message_count"] + 1
            posted = {
                "type": "message",
                "messageId": "m_" + str(conversation["message_count"]),
                "senderName": user["display_name"],
                "text": text,
                "sentAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            # Everyone connected gets it, including the sender, so every screen shows the same order.
            for connection in list(conversation["connections"]):
                await connection.send_text(json.dumps(posted))
    except WebSocketDisconnect:
        pass
    finally:
        # Once the app closes, this connection is gone. A notification service would send a push or
        # email for anything that arrives after that.
        conversation["connections"].discard(websocket)


routes = [WebSocketRoute("/ws/conversations/{conversationId}", conversation_socket)]
