"""Generates the Python gRPC code from contractor.proto into server/generated/.

The server runs this by itself on startup, so you only need it if you want to look at the generated
code: python3 generate_grpc.py
"""

from pathlib import Path

import grpc_tools
from grpc_tools import protoc

SERVER_FOLDER = Path(__file__).resolve().parent
PROTO_FOLDER = SERVER_FOLDER.parent
GENERATED_FOLDER = SERVER_FOLDER / "generated"
# The standard .proto files (empty.proto, field_mask.proto) that ship with grpcio-tools
STANDARD_PROTO_FOLDER = Path(grpc_tools.__file__).resolve().parent / "_proto"


def generate_grpc_code():
    GENERATED_FOLDER.mkdir(exist_ok=True)
    exit_code = protoc.main([
        "protoc",
        "-I" + str(PROTO_FOLDER),
        "-I" + str(STANDARD_PROTO_FOLDER),
        "--python_out=" + str(GENERATED_FOLDER),
        "--grpc_python_out=" + str(GENERATED_FOLDER),
        str(PROTO_FOLDER / "contractor.proto"),
    ])
    if exit_code != 0:
        raise RuntimeError("protoc couldn't compile contractor.proto")


if __name__ == "__main__":
    generate_grpc_code()
    print("Generated code in " + str(GENERATED_FOLDER))
