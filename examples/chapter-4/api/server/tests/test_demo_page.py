"""Opens the demo page in a real browser and uses every section. Skipped if Playwright isn't installed:
    pip install playwright
    python3 -m playwright install chromium
"""

import socket
import threading
import time

import pytest
import uvicorn

from app import build_app

sync_api = pytest.importorskip("playwright.sync_api")


def free_port():
    with socket.socket() as probe:
        probe.bind(("localhost", 0))
        return probe.getsockname()[1]


@pytest.fixture(scope="module")
def server_address():
    port = free_port()
    server = uvicorn.Server(uvicorn.Config(build_app(seconds_per_analysis_update=0.05), host="localhost",
                                           port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 10
    while not server.started and time.time() < deadline:
        time.sleep(0.05)
    yield "http://localhost:" + str(port)
    server.should_exit = True
    thread.join(timeout=5)


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as playwright_session:
        try:
            launched_browser = playwright_session.chromium.launch()
        except Exception as launch_error:
            pytest.skip("Chromium isn't installed for Playwright: " + str(launch_error).split("\n")[0])
        yield launched_browser
        launched_browser.close()


def test_every_section_works(server_address, browser):
    page = browser.new_page()
    console_errors = []
    page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
    page.goto(server_address + "/")
    assert page.url.endswith("/demo")

    # REST: create, then the same request again comes back as a replay, not a 409
    page.click("#rest-create")
    sync_api.expect(page.locator("#rest-output")).to_contain_text("201")
    page.click("#rest-retry")
    sync_api.expect(page.locator("#rest-output")).to_contain_text("Idempotent-Replayed: true")

    # GraphQL finds the profile just created
    page.click("#graphql-form button")
    sync_api.expect(page.locator("#graphql-output")).to_contain_text("My Renovation Co., Los Angeles, CA, OPEN")

    # Server-sent events run to the findings
    page.click("#events-start")
    sync_api.expect(page.locator("#events-output")).to_contain_text("worn oak cabinets", timeout=10000)

    # WebSocket: a second window as the homeowner sees the contractor's message arrive
    homeowner_page = browser.new_page()
    homeowner_page.goto(server_address + "/demo")
    homeowner_page.select_option("#token", "homeowner-token")
    homeowner_page.click("#socket-connect")
    sync_api.expect(homeowner_page.locator("#socket-messages")).to_contain_text("Connected.")
    page.click("#socket-connect")
    sync_api.expect(page.locator("#socket-messages")).to_contain_text("Connected.")
    page.click("#socket-send")
    sync_api.expect(homeowner_page.locator("#socket-messages")).to_contain_text("Acme Renovations: Should the cabinets stay?")

    # Polling: the first answer is 200, the next ones 304 with no body
    page.click("#polling-start")
    sync_api.expect(page.locator("#polling-output")).to_contain_text("200  SHIPPED")
    sync_api.expect(page.locator("#polling-output")).to_contain_text("304  Not Modified", timeout=8000)
    page.click("#polling-stop")

    assert console_errors == []
