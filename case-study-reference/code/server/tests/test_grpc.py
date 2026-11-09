"""gRPC cases the example file doesn't show."""

import grpc
import pytest
from google.protobuf import field_mask_pb2
from google.rpc import error_details_pb2
from grpc_status import rpc_status

from conftest import contractor_pb2, grpc_metadata

ACME_REQUEST = contractor_pb2.CreateContractorProfileRequest(
    company_name="Acme Renovations", services=["Painting", "Flooring"], service_area="Los Angeles, CA",
    availability=contractor_pb2.OPEN, insurance_expires_on="2027-03-31")


def create_acme(grpc_stub):
    return grpc_stub.CreateContractorProfile(ACME_REQUEST, metadata=grpc_metadata("contractor")).contractor_id


def update(grpc_stub, profile, paths, person="contractor"):
    request = contractor_pb2.UpdateContractorProfileRequest(
        contractor_profile=profile, update_mask=field_mask_pb2.FieldMask(paths=paths))
    return grpc_stub.UpdateContractorProfile(request, metadata=grpc_metadata(person))


def field_violations(error):
    bad_request = error_details_pb2.BadRequest()
    rpc_status.from_call(error).details[0].Unpack(bad_request)
    return [(violation.field, violation.description) for violation in bad_request.field_violations]


def test_update_mask_is_required_and_checked(grpc_stub):
    contractor_id = create_acme(grpc_stub)
    profile = contractor_pb2.ContractorProfile(contractor_id=contractor_id, availability=contractor_pb2.BOOKED)
    with pytest.raises(grpc.RpcError) as no_mask:
        update(grpc_stub, profile, [])
    assert no_mask.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert field_violations(no_mask.value)[0][0] == "update_mask"
    with pytest.raises(grpc.RpcError) as reviews_in_mask:
        update(grpc_stub, profile, ["reviews"])
    assert field_violations(reviews_in_mask.value)[0][0] == "reviews"


def test_only_masked_fields_change(grpc_stub):
    contractor_id = create_acme(grpc_stub)
    # company_name is set here but not in the mask, so it must not change.
    profile = contractor_pb2.ContractorProfile(contractor_id=contractor_id, company_name="Ignored",
                                               availability=contractor_pb2.BOOKED)
    updated = update(grpc_stub, profile, ["availability"])
    assert updated.availability == contractor_pb2.BOOKED
    assert updated.company_name == "Acme Renovations"


def test_masked_but_unset_insurance_date_clears_it(grpc_stub):
    contractor_id = create_acme(grpc_stub)
    updated = update(grpc_stub, contractor_pb2.ContractorProfile(contractor_id=contractor_id), ["insurance_expires_on"])
    assert not updated.HasField("insurance_expires_on")


def test_masked_but_unset_availability_is_an_error(grpc_stub):
    contractor_id = create_acme(grpc_stub)
    with pytest.raises(grpc.RpcError) as error:
        update(grpc_stub, contractor_pb2.ContractorProfile(contractor_id=contractor_id), ["availability"])
    assert field_violations(error.value) == [("availability", "Use OPEN, LIMITED, or BOOKED.")]


def test_each_status_code(grpc_stub):
    contractor_id = create_acme(grpc_stub)
    review = contractor_pb2.CreateReviewRequest(contractor_id=contractor_id, rating=5)
    cases = [
        (grpc.StatusCode.UNAUTHENTICATED, lambda: grpc_stub.CreateReview(review)),
        (grpc.StatusCode.PERMISSION_DENIED, lambda: grpc_stub.CreateReview(review, metadata=grpc_metadata("contractor"))),
        (grpc.StatusCode.NOT_FOUND, lambda: grpc_stub.CreateReview(
            contractor_pb2.CreateReviewRequest(contractor_id="c_000000", rating=5), metadata=grpc_metadata("homeowner"))),
        (grpc.StatusCode.INVALID_ARGUMENT, lambda: grpc_stub.CreateReview(
            contractor_pb2.CreateReviewRequest(contractor_id=contractor_id, rating=0), metadata=grpc_metadata("homeowner"))),
        (grpc.StatusCode.ALREADY_EXISTS, lambda: create_acme(grpc_stub)),
    ]
    for expected_code, make_call in cases:
        with pytest.raises(grpc.RpcError) as error:
            make_call()
        assert error.value.code() == expected_code


def test_review_without_a_body_leaves_it_unset(grpc_stub):
    contractor_id = create_acme(grpc_stub)
    review = grpc_stub.CreateReview(contractor_pb2.CreateReviewRequest(contractor_id=contractor_id, rating=4),
                                    metadata=grpc_metadata("homeowner"))
    assert not review.HasField("body")


def test_delete_then_not_found(grpc_stub):
    contractor_id = create_acme(grpc_stub)
    request = contractor_pb2.DeleteContractorProfileRequest(contractor_id=contractor_id)
    grpc_stub.DeleteContractorProfile(request, metadata=grpc_metadata("contractor"))
    with pytest.raises(grpc.RpcError) as error:
        grpc_stub.GetContractorProfile(contractor_pb2.GetContractorProfileRequest(contractor_id=contractor_id),
                                       metadata=grpc_metadata("homeowner"))
    assert error.value.code() == grpc.StatusCode.NOT_FOUND
