"""Polling: the client asks again on a timer.

Order and Delivery Tracking can check for a new status every hour, since a package changes status only a
handful of times a day. The ETag keeps those checks cheap: the client sends back the ETag it got last
time, and if nothing changed the server answers 304 Not Modified with no body.
"""

import datetime
import hashlib
import json

from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from auth import user_from_authorization_header
from directory import NotFound, NotSignedIn
from rest_api import problem_response

DELIVERY_STEPS = ("ORDERED", "SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED")


def starting_orders():
    return {"o_1001": {"orderId": "o_1001", "status": "SHIPPED", "updatedAt": "2026-11-08T09:00:00Z"}}


def entity_tag(delivery_status):
    """A fingerprint of the response body. It changes whenever the status does."""
    fingerprint = hashlib.sha256(json.dumps(delivery_status, sort_keys=True).encode()).hexdigest()
    return '"' + fingerprint[:16] + '"'


def advance_delivery(orders, order_id):
    """Moves an order to its next step, the way the shipping company's update would."""
    order = orders[order_id]
    step_number = DELIVERY_STEPS.index(order["status"])
    if step_number + 1 < len(DELIVERY_STEPS):
        order["status"] = DELIVERY_STEPS[step_number + 1]
        order["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


async def get_delivery_status(request):
    if user_from_authorization_header(request.headers.get("authorization")) is None:
        return problem_response(NotSignedIn("Sign in first. Send your token as Authorization: Bearer <token>."))
    order_id = request.path_params["orderId"]
    order = request.app.state.orders.get(order_id)
    if order is None:
        return problem_response(NotFound("There's no order with the ID " + order_id + "."))
    current_tag = entity_tag(order)
    # no-cache means "check with me every time", which is what makes the 304 answer possible.
    headers = {"ETag": current_tag, "Cache-Control": "no-cache"}
    if request.headers.get("if-none-match") == current_tag:
        return Response(status_code=304, headers=headers)
    return JSONResponse(order, headers=headers)


routes = [Route("/api/orders/{orderId}/delivery", get_delivery_status, methods=["GET"])]
