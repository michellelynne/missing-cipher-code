# The example server with everything it needs, so nothing has to be installed but Docker.
# From this folder:
#   docker compose up          then open http://localhost:8000/demo
#   docker compose run --rm api python -m pytest       runs the tests, database ones included

FROM python:3.13-slim

WORKDIR /examples
COPY server/requirements.txt server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt

COPY . .
WORKDIR /examples/server

# Listen on every interface inside the container, so the published ports reach it
ENV HOST=0.0.0.0
EXPOSE 8000 50051

# Run as a regular user, not root. It owns the folder because the server writes its generated gRPC code there.
RUN useradd --create-home renovation && chown -R renovation /examples
USER renovation

CMD ["python", "app.py"]
