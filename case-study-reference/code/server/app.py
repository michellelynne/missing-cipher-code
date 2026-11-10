"""Runs every Renovation Revolution API example at once, sharing one Contractors Directory:

  Demo page            http://localhost:8000/demo        (try every style from the browser)
  REST and messaging   http://localhost:8000/api/...    (openapi.yaml)
  GraphQL              http://localhost:8000/graphql     (schema.graphql; open it in a browser to try queries)
  WebSocket            ws://localhost:8000/ws/conversations/conv_1   (messaging/asyncapi.yaml)
  gRPC                 localhost:50051                   (contractor.proto)
  Health check         http://localhost:8000/health      (for Docker and load balancers, not part of the API)

Start it from this folder:
    pip install -r requirements-test.txt
    python3 app.py

A profile created through one style can be read through the other two, since they're three doors
into the same directory. Everything is in memory and resets when you stop the server.
"""

import asyncio
import contextlib
import os
from pathlib import Path

import uvicorn
from starlette.applications import Starlette
from starlette.responses import FileResponse, JSONResponse, RedirectResponse
from starlette.routing import Route

import conversations
import delivery_polling
import image_analysis
import payment_webhooks
import rest_api
from directory import ContractorDirectory
from graphql_api import build_graphql_app

HTTP_PORT = 8000
GRPC_PORT = 50051
# localhost on your own machine. The Docker image sets HOST=0.0.0.0, so the ports reach outside the container.
HOST = os.environ.get("HOST", "localhost")
DEMO_PAGE = Path(__file__).resolve().parent / "static" / "demo.html"


async def demo_page(request):
    return FileResponse(DEMO_PAGE)


async def go_to_demo(request):
    return RedirectResponse("/demo")


async def health(request):
    """Answers 200 while the web server is up. Docker's health check and the update script call it.
    It needs no sign-in and says nothing about the data, so it's safe to leave open."""
    return JSONResponse({"status": "ok"})


def build_app(directory=None, seconds_per_analysis_update=0.5):
    """Builds the web app. Tests pass their own directory and a zero delay."""
    directory = directory if directory is not None else ContractorDirectory()

    @contextlib.asynccontextmanager
    async def lifespan(app):
        # The image analysis worker runs alongside the web server, taking commands off the queue.
        worker = asyncio.create_task(app.state.image_analysis_service.run_forever())
        try:
            yield
        finally:
            worker.cancel()

    app = Starlette(
        routes=rest_api.routes + delivery_polling.routes + image_analysis.routes + payment_webhooks.routes
        + conversations.routes + [
            Route("/graphql", build_graphql_app(), methods=["GET", "POST"]),
            Route("/demo", demo_page, methods=["GET"]),
            Route("/", go_to_demo, methods=["GET"]),
            Route("/health", health, methods=["GET"]),
        ],
        lifespan=lifespan,
    )
    app.state.directory = directory
    app.state.orders = delivery_polling.starting_orders()
    app.state.conversations = conversations.starting_conversations()
    app.state.webhook_secret = payment_webhooks.DEMO_WEBHOOK_SECRET
    app.state.handled_webhook_ids = set()
    app.state.subscriptions = {}
    app.state.queue = image_analysis.MessageQueue()
    app.state.event_bus = image_analysis.EventBus()
    app.state.room_service = image_analysis.RoomService(app.state.queue, app.state.event_bus)
    app.state.image_analysis_service = image_analysis.ImageAnalysisService(
        app.state.queue, app.state.event_bus, seconds_per_analysis_update)
    return app


def main():
    from grpc_api import build_grpc_server
    directory = ContractorDirectory()
    grpc_server, _ = build_grpc_server(directory, HOST + ":" + str(GRPC_PORT))
    grpc_server.start()
    print("gRPC on localhost:" + str(GRPC_PORT))
    print("REST, GraphQL, and messaging on http://localhost:" + str(HTTP_PORT))
    print("Demo page: http://localhost:" + str(HTTP_PORT) + "/demo")
    print("Demo tokens: homeowner-token, contractor-token, second-contractor-token")
    try:
        uvicorn.run(build_app(directory), host=HOST, port=HTTP_PORT, log_level="warning")
    finally:
        grpc_server.stop(grace=1)


if __name__ == "__main__":
    main()
