# The example server as a small, locked-down image. From this folder:
#   docker compose up                  then open http://localhost:8000/demo
#   docker compose run --rm tests      runs every test, database ones included, in the test image
#
# Four stages, so the image that runs holds only what the server needs at run time:
#   builder   a full Debian with pip, which installs the server's libraries into /opt/venv
#   codegen   turns contractor.proto into Python, so grpcio-tools never reaches the final image
#   test      the runtime image plus the test libraries and the tests (docker build --target test)
#   runtime   distroless Python: no shell, no package manager, runs as a regular user (the default)
#
# Base images are pinned by digest, so a build next month uses the same bytes as today. To update
# one, look up the new digest and paste it in, then let CI build, scan, and test it:
#   docker buildx imagetools inspect debian:13-slim --format '{{json .Manifest.Digest}}'
#   docker buildx imagetools inspect gcr.io/distroless/python3-debian13:nonroot --format '{{json .Manifest.Digest}}'
# Keep the two on the same Debian release, so the Python that builds /opt/venv is the Python that runs it.

ARG BUILDER_IMAGE=debian:13-slim@sha256:a72b4433de1cf7d6bae0c4cee74d0547f58601a643b3375f070c51600d63b6b2
ARG RUNTIME_IMAGE=gcr.io/distroless/python3-debian13:nonroot@sha256:c3ed2b61f3c4e410685565ceb3c818197b552832521b39d53eca5d2d9d0dc1e1

# ---------- builder: install the libraries into a virtual environment ----------
FROM ${BUILDER_IMAGE} AS builder

# Debian's own Python, the same one the distroless image ships, so the venv works there unchanged
RUN apt-get update \
    && apt-get install --yes --no-install-recommends python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Requirements first and code later, so changing the code doesn't reinstall every library
COPY server/requirements.txt /build/requirements.txt
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --disable-pip-version-check -r /build/requirements.txt \
    # pip is only needed to install; leaving it out of the final image means one less thing to patch
    && /opt/venv/bin/pip uninstall --yes pip \
    # Compile now, because the running container's filesystem is read-only
    && /opt/venv/bin/python -m compileall -q /opt/venv

# ---------- codegen: generate the gRPC code at build time ----------
FROM builder AS codegen

RUN python3 -m venv /opt/codegen \
    && /opt/codegen/bin/pip install --no-cache-dir --disable-pip-version-check grpcio-tools==1.85.1
COPY contractor.proto /examples/contractor.proto
COPY server/generate_grpc.py /examples/server/generate_grpc.py
RUN /opt/codegen/bin/python /examples/server/generate_grpc.py \
    && /opt/venv/bin/python -m compileall -q /examples/server/generated

# ---------- the shared runtime base ----------
FROM ${RUNTIME_IMAGE} AS runtime-base

# The venv's python comes first on the PATH, so "python" means the one with the libraries
ENV PATH=/opt/venv/bin:/usr/local/bin:/usr/bin:/bin \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Listen on every interface inside the container, so the published ports reach it
    HOST=0.0.0.0
COPY --from=builder /opt/venv /opt/venv

WORKDIR /examples/server
EXPOSE 8000 50051
# The distroless image's own user, uid 65532. It owns nothing it could change.
USER nonroot
# distroless starts python by default; clear that so CMD is the whole command
ENTRYPOINT []

# ---------- test: the runtime image plus the tests and their libraries ----------
FROM builder AS test-libraries
COPY server/requirements-test.txt server/requirements.txt /build/
RUN /opt/venv/bin/python -m ensurepip \
    && /opt/venv/bin/python -m pip install --no-cache-dir --disable-pip-version-check -r /build/requirements-test.txt

FROM runtime-base AS test
COPY --from=test-libraries /opt/venv /opt/venv
COPY . /examples
COPY --from=codegen /examples/server/generated /examples/server/generated
# -p no:cacheprovider: pytest's cache would need a writable folder
CMD ["python", "-m", "pytest", "-q", "-p", "no:cacheprovider"]

# ---------- runtime: what ships (the last stage, so a plain docker build makes this one) ----------
FROM runtime-base AS runtime

# Only what the server reads: its code, the demo page, the GraphQL schema, and the .proto
COPY server/*.py /examples/server/
COPY server/static /examples/server/static
COPY schema.graphql contractor.proto /examples/
COPY --from=codegen /examples/server/generated /examples/server/generated

# Docker marks the container unhealthy if /health stops answering. There's no curl or shell
# here, so Python makes the request.
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)"]

CMD ["python", "app.py"]
