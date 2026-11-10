"""A webhook: the payment processor calls this when a contractor's subscription payment clears.

Treat every webhook as untrusted until its signature checks out. This uses the Standard Webhooks
scheme (standardwebhooks.com), which many providers follow: three headers, and a signature that is
the HMAC-SHA256 of "id.timestamp.body" with a secret you share with the sender.

Expect the same call more than once, too. The handler remembers each webhook-id and acknowledges a
repeat without processing it again, so a second delivery changes nothing.

To try it against the running server, print a signed curl command:
    python3 payment_webhooks.py c_8f3a2b
"""

import base64
import hashlib
import hmac
import json
import sys
import time

from starlette.responses import JSONResponse, Response
from starlette.routing import Route

# The shared secret. In production it comes from your secrets manager, never from code.
DEMO_WEBHOOK_SECRET = "whsec_" + base64.b64encode(b"renovation-revolution-demo-secret").decode()
OLDEST_ALLOWED_SECONDS = 5 * 60


def secret_key(secret):
    return base64.b64decode(secret[len("whsec_"):])


def sign(secret, webhook_id, timestamp, body_bytes):
    signed_content = webhook_id.encode() + b"." + str(timestamp).encode() + b"." + body_bytes
    digest = hmac.new(secret_key(secret), signed_content, hashlib.sha256).digest()
    return "v1," + base64.b64encode(digest).decode()


def signature_is_valid(secret, headers, body_bytes, now=None):
    webhook_id = headers.get("webhook-id")
    timestamp_text = headers.get("webhook-timestamp")
    signature_header = headers.get("webhook-signature")
    if not webhook_id or not timestamp_text or not signature_header or not timestamp_text.isdigit():
        return False
    current_time = int(now if now is not None else time.time())
    # An old timestamp means a replayed call, even if the signature is right.
    if abs(current_time - int(timestamp_text)) > OLDEST_ALLOWED_SECONDS:
        return False
    expected_signature = sign(secret, webhook_id, timestamp_text, body_bytes)
    # The header can list several signatures (during a secret rotation); any one matching is enough.
    # compare_digest takes the same time whether or not they match, so timing gives nothing away.
    return any(hmac.compare_digest(expected_signature, candidate) for candidate in signature_header.split(" "))


async def receive_payment_webhook(request):
    body_bytes = await request.body()  # the exact bytes that were signed, before any parsing
    if not signature_is_valid(request.app.state.webhook_secret, request.headers, body_bytes):
        return JSONResponse({"error": "Missing, wrong, or stale signature."}, status_code=401)

    webhook_id = request.headers["webhook-id"]
    handled_ids = request.app.state.handled_webhook_ids
    if webhook_id in handled_ids:
        return Response(status_code=204)

    try:
        payload = json.loads(body_bytes)
        data = payload["data"]
        if payload["type"] != "subscription.payment_succeeded":
            raise ValueError(payload["type"])
        subscription = {
            "contractorId": str(data["contractorId"]),
            "subscriptionId": str(data["subscriptionId"]),
            "amountCents": int(data["amountCents"]),
            "currency": str(data["currency"]),
            "status": "ACTIVE",
        }
    except (ValueError, KeyError, TypeError):
        return JSONResponse({"error": "Signed correctly, but not a payload this endpoint understands."}, status_code=400)

    request.app.state.subscriptions[subscription["contractorId"]] = subscription
    handled_ids.add(webhook_id)
    return Response(status_code=204)


routes = [Route("/webhooks/payments", receive_payment_webhook, methods=["POST"])]


if __name__ == "__main__":
    contractor_id = sys.argv[1] if len(sys.argv) > 1 else "c_8f3a2b"
    body = json.dumps({"type": "subscription.payment_succeeded", "data": {
        "contractorId": contractor_id, "subscriptionId": "sub_4471", "amountCents": 4900, "currency": "USD"}})
    webhook_id = "msg_" + str(int(time.time()))
    timestamp = str(int(time.time()))
    signature = sign(DEMO_WEBHOOK_SECRET, webhook_id, timestamp, body.encode())
    print("curl -i -X POST http://localhost:8000/webhooks/payments \\")
    print("  -H 'content-type: application/json' \\")
    print("  -H 'webhook-id: " + webhook_id + "' \\")
    print("  -H 'webhook-timestamp: " + timestamp + "' \\")
    print("  -H 'webhook-signature: " + signature + "' \\")
    print("  -d '" + body + "'")
