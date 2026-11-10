"""Generates the Python gRPC code from contractor.proto into server/generated/.

The server calls make_sure_grpc_code_is_current() on startup, so you only need to run this by hand if
you want to look at the generated code: python3 generate_grpc.py

The Docker image runs this file while it builds, so the image has the generated code already and
doesn't need grpcio-tools (or a writable folder) when it runs.
"""

import hashlib
from pathlib import Path

SERVER_FOLDER = Path(__file__).resolve().parent
PROTO_FOLDER = SERVER_FOLDER.parent
PROTO_PATH = PROTO_FOLDER / "contractor.proto"
GENERATED_FOLDER = SERVER_FOLDER / "generated"
# Holds the SHA-256 of the contractor.proto the code was generated from, so a stale copy is noticed
FINGERPRINT_PATH = GENERATED_FOLDER / "contractor.proto.sha256"


def proto_fingerprint():
    return hashlib.sha256(PROTO_PATH.read_bytes()).hexdigest()


def generated_code_is_current():
    if not FINGERPRINT_PATH.exists() or not (GENERATED_FOLDER / "contractor_pb2.py").exists():
        return False
    return FINGERPRINT_PATH.read_text().strip() == proto_fingerprint()


def generate_grpc_code():
    import grpc_tools
    from grpc_tools import protoc

    # The standard .proto files (empty.proto, field_mask.proto) that ship with grpcio-tools
    standard_proto_folder = Path(grpc_tools.__file__).resolve().parent / "_proto"
    GENERATED_FOLDER.mkdir(exist_ok=True)
    exit_code = protoc.main([
        "protoc",
        "-I" + str(PROTO_FOLDER),
        "-I" + str(standard_proto_folder),
        "--python_out=" + str(GENERATED_FOLDER),
        "--grpc_python_out=" + str(GENERATED_FOLDER),
        str(PROTO_PATH),
    ])
    if exit_code != 0:
        raise RuntimeError("protoc couldn't compile contractor.proto")
    FINGERPRINT_PATH.write_text(proto_fingerprint() + "\n")


def make_sure_grpc_code_is_current():
    """Uses the generated code if it matches contractor.proto, and generates it again if not."""
    if generated_code_is_current():
        return
    try:
        generate_grpc_code()
    except ImportError:
        raise RuntimeError("The gRPC code in " + str(GENERATED_FOLDER) + " is missing or older than contractor.proto, "
                           "and grpcio-tools isn't installed to generate it. Run: "
                           "pip install -r requirements-test.txt") from None


if __name__ == "__main__":
    generate_grpc_code()
    print("Generated code in " + str(GENERATED_FOLDER))
