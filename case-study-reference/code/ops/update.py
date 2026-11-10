"""Updates the running server to the newest signed image, and rolls back if the new one isn't healthy.

Run it from case-study-reference/code (it needs Docker Compose and cosign, nothing else):

    python3 ops/update.py                         update to the newest signed image
    python3 ops/update.py --digest sha256:...     go to one exact image, newer or older (pin or roll back by hand)
    python3 ops/update.py --verify-only           find and verify the newest signed image, change nothing

What it does, in order:
  1. Lists the image's tags in the registry and picks the newest dated one (CI tags every push to
     main with the date and time, like 2026-11-10.153012), or takes the digest you give it.
  2. Checks the image's Cosign signature. It refuses an image that isn't signed by this repository's
     CI workflow. When the newest image isn't signed, it says so and tries the next newest.
  3. Notes the digest that's running now, so it has something to go back to.
  4. Starts the new digest with compose.published.yaml and waits for Docker's health check.
  5. If the health check fails, starts the previous digest again and waits for it to be healthy.

Every change is added to ops/deploy-history.log. The image is public, so no registry password is
needed: the registry hands out an anonymous token for reading a public image.

Signed by a key instead of by CI (for example on a network with no internet access, where you run
your own registry and sign with your own key): pass --key cosign.pub, and --ignore-tlog if you have
no transparency log to check against.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CODE_FOLDER = Path(__file__).resolve().parent.parent
COMPOSE_FILE = CODE_FOLDER / "compose.published.yaml"
HISTORY_FILE = Path(__file__).resolve().parent / "deploy-history.log"
SERVICE_NAME = "api"

DEFAULT_IMAGE = "ghcr.io/michellelynne/renovation-revolution"
# Who is allowed to have signed the image: the container workflow in this repository, on main.
# Anyone can get a Sigstore certificate, so checking the signature alone isn't enough; this is the part
# that says "and it was signed by our CI, from our main branch".
DEFAULT_IDENTITY = ("https://github.com/michellelynne/missing-cipher-code/.github/workflows/container.yml"
                    "@refs/heads/main")
DEFAULT_ISSUER = "https://token.actions.githubusercontent.com"

# CI's dated tags, like 2026-11-10.153012. They sort by time as plain text.
DATED_TAG = re.compile(r"^\d{4}-\d{2}-\d{2}\.\d{6}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
MANIFEST_TYPES = ", ".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])


class UpdateFailed(Exception):
    pass


def say(message):
    print(message, flush=True)


def record(action, image_reference):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with HISTORY_FILE.open("a") as history:
        history.write(timestamp + " " + action + " " + image_reference + "\n")


# ---------- Reading the registry, anonymously ----------

class Registry:
    """Just enough of the OCI distribution API to list tags and look up digests of a public image."""

    def __init__(self, image_name):
        self.host, _, self.repository = image_name.partition("/")
        self.token = None

    def request(self, path, method="GET", accept=None):
        url = "https://" + self.host + "/v2/" + self.repository + path
        headers = {"Accept": accept} if accept else {}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=headers, method=method), timeout=30)
        except urllib.error.HTTPError as error:
            if error.code != 401 or self.token:
                raise
            # The registry says how to get a token. For a public image, asking without a password works.
            self.token = self.anonymous_token(error.headers.get("WWW-Authenticate", ""))
            return self.request(path, method, accept)

    def anonymous_token(self, challenge):
        settings = dict(re.findall(r'(\w+)="([^"]*)"', challenge))
        if "realm" not in settings:
            raise UpdateFailed("The registry asked for a sign-in this script can't do: " + challenge)
        query = {"service": settings.get("service", ""),
                 "scope": settings.get("scope", "repository:" + self.repository + ":pull")}
        with urllib.request.urlopen(settings["realm"] + "?" + urllib.parse.urlencode(query), timeout=30) as response:
            answer = json.load(response)
        return answer.get("token") or answer.get("access_token")

    def tags(self):
        all_tags = []
        path = "/tags/list?n=1000"
        while path:
            with self.request(path) as response:
                all_tags = all_tags + (json.load(response).get("tags") or [])
                next_link = response.headers.get("Link", "")
            # More pages come as a Link header: </v2/<repository>/tags/list?last=...>; rel="next"
            match = re.search(r"<[^>]*/tags/list(\?[^>]*)>", next_link)
            path = "/tags/list" + match.group(1) if match else None
        return all_tags

    def digest_of(self, tag):
        with self.request("/manifests/" + tag, method="HEAD", accept=MANIFEST_TYPES) as response:
            return response.headers["Docker-Content-Digest"]


# ---------- Checking signatures ----------

def verify_signature(image_reference, options):
    """True when cosign confirms the signature. Prints cosign's reason when it doesn't."""
    command = ["cosign", "verify", image_reference, "--output", "json"]
    if options.key:
        command = command + ["--key", options.key]
    else:
        command = command + ["--certificate-identity", options.certificate_identity,
                             "--certificate-oidc-issuer", options.certificate_oidc_issuer]
    if options.ignore_tlog:
        command = command + ["--insecure-ignore-tlog=true"]
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        say("  not verified: " + (completed.stderr.strip().splitlines() or ["no reason given"])[-1])
    return completed.returncode == 0


def choose_image(registry, options):
    """Returns image@digest for the image to run: the pinned one, or the newest that's signed."""
    if options.digest:
        if not DIGEST.match(options.digest):
            raise UpdateFailed("--digest must look like sha256:<64 hex characters>, not " + options.digest)
        image_reference = options.image + "@" + options.digest
        say("Checking the signature of " + image_reference)
        if not verify_signature(image_reference, options):
            raise UpdateFailed("Refusing to run an image that isn't signed: " + image_reference)
        say("  signature verified")
        return image_reference

    dated_tags = sorted([tag for tag in registry.tags() if DATED_TAG.match(tag)], reverse=True)
    if not dated_tags:
        raise UpdateFailed("No dated tags in " + options.image + " yet. Has CI published an image?")
    for tag in dated_tags[:options.how_many_to_try]:
        # Look up the digest first, then verify and run that digest. If someone moves the tag in the
        # meantime, it doesn't matter: the digest is what was checked and what runs.
        image_reference = options.image + "@" + registry.digest_of(tag)
        say("Newest candidate: " + tag + " = " + image_reference)
        if verify_signature(image_reference, options):
            say("  signature verified")
            return image_reference
        say("  skipping it: unsigned images never run")
    raise UpdateFailed("None of the newest " + str(options.how_many_to_try) + " images is signed.")


# ---------- Running it with Docker Compose ----------

def compose(arguments, image_reference=None, check=True):
    environment = dict(os.environ)
    if image_reference:
        environment["RENOVATION_IMAGE"] = image_reference
    else:
        # Compose needs a value to read the file, even for commands that don't start anything
        environment.setdefault("RENOVATION_IMAGE", DEFAULT_IMAGE + "@sha256:" + "0" * 64)
    return subprocess.run(["docker", "compose", "-f", str(COMPOSE_FILE)] + arguments,
                          env=environment, capture_output=True, text=True, check=check)


def running_container():
    container_ids = compose(["ps", "--quiet", SERVICE_NAME]).stdout.split()
    return container_ids[0] if container_ids else None


def running_image():
    container_id = running_container()
    if not container_id:
        return None
    inspected = subprocess.run(["docker", "inspect", "--format", "{{.Config.Image}}", container_id],
                               capture_output=True, text=True, check=True)
    return inspected.stdout.strip()


def start(image_reference):
    say("Starting " + image_reference)
    completed = compose(["up", "--detach", SERVICE_NAME], image_reference, check=False)
    if completed.returncode != 0:
        say(completed.stderr.strip())
        return False
    return True


def wait_until_healthy(seconds_to_wait):
    """Waits for the image's HEALTHCHECK (GET /health) to pass. False if it fails or takes too long."""
    deadline = time.monotonic() + seconds_to_wait
    status = "unknown"
    while time.monotonic() < deadline:
        container_id = running_container()
        if container_id:
            inspected = subprocess.run(["docker", "inspect", "--format", "{{.State.Status}} {{.State.Health.Status}}",
                                        container_id], capture_output=True, text=True)
            status = inspected.stdout.strip()
            if status == "running healthy":
                say("  healthy")
                return True
            if status.startswith("exited") or status.endswith("unhealthy"):
                break
        time.sleep(2)
    say("  not healthy (" + status + ")")
    return False


def update(options):
    registry = Registry(options.image)
    new_image = choose_image(registry, options)
    if options.verify_only:
        say("Verified, and changed nothing: " + new_image)
        return

    previous_image = running_image()
    say("Running now: " + (previous_image or "nothing"))
    if previous_image == new_image:
        say("Already running that image. Nothing to do.")
        return

    if start(new_image) and wait_until_healthy(options.health_timeout):
        record("updated-to", new_image)
        say("Updated to " + new_image)
        return

    record("failed", new_image)
    if not previous_image:
        compose(["stop", SERVICE_NAME], check=False)
        raise UpdateFailed("The new image isn't healthy and nothing ran before it, so the server is stopped.")
    say("Rolling back to " + previous_image)
    # The previous image was verified when it went in; check again, in case the key or policy changed.
    if not verify_signature(previous_image, options):
        raise UpdateFailed("The previous image no longer verifies, so it wasn't restarted: " + previous_image)
    if start(previous_image) and wait_until_healthy(options.health_timeout):
        record("rolled-back-to", previous_image)
        raise UpdateFailed("The new image wasn't healthy. Rolled back to " + previous_image)
    raise UpdateFailed("The new image wasn't healthy, and the rollback didn't come up healthy either.")


def main():
    parser = argparse.ArgumentParser(description="Update to the newest signed image, rolling back if it isn't healthy.")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="registry/repository, without a tag")
    parser.add_argument("--digest", help="run this exact image (sha256:...) instead of the newest")
    parser.add_argument("--verify-only", action="store_true", help="find and verify the image, then stop")
    parser.add_argument("--health-timeout", type=int, default=90, help="seconds to wait for healthy (default 90)")
    parser.add_argument("--how-many-to-try", type=int, default=5,
                        help="how many of the newest tags to try before giving up (default 5)")
    parser.add_argument("--certificate-identity", default=DEFAULT_IDENTITY,
                        help="the workflow that must have signed the image")
    parser.add_argument("--certificate-oidc-issuer", default=DEFAULT_ISSUER)
    parser.add_argument("--key", help="verify with this public key instead of keyless signing")
    parser.add_argument("--ignore-tlog", action="store_true",
                        help="don't check the transparency log (only with --key, for a network with no log)")
    options = parser.parse_args()
    if options.ignore_tlog and not options.key:
        parser.error("--ignore-tlog only makes sense with --key: keyless signatures rely on the transparency log")
    try:
        update(options)
    except UpdateFailed as failure:
        say("FAILED: " + str(failure))
        sys.exit(1)
    except urllib.error.HTTPError as error:
        say("FAILED: the registry answered " + str(error.code) + " for " + error.url + ". If that's 403 or 404, "
            "the image hasn't been published yet, or its package isn't public.")
        sys.exit(1)


if __name__ == "__main__":
    main()
