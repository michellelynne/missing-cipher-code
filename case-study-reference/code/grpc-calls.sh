# The Contractors API in gRPC, as grpcurl commands (github.com/fullstorydev/grpcurl). Every call here
# runs against the example server in server/, and every response is what it really sends back;
# server/tests/test_example_files.py checks that.
#
# Start the server first (python3 server/app.py), then run these from this folder so grpcurl can read
# contractor.proto. grpcurl writes messages as JSON, with camelCase names and enum values as words.
# The IDs c_8f3a2b and c_51d2e0 stand for the two profiles the first two calls create; put in the IDs
# your server sends back.

### Create Contractor Profile
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer contractor-token' \
  -d '{
    "companyName": "Acme Renovations",
    "services": ["Painting", "Flooring"],
    "serviceArea": "Los Angeles, CA",
    "availability": "OPEN",
    "insuranceExpiresOn": "2027-03-31"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/CreateContractorProfile

# Response:
# {
#   "contractorId": "c_8f3a2b",
#   "companyName": "Acme Renovations",
#   "services": ["Painting", "Flooring"],
#   "serviceArea": "Los Angeles, CA",
#   "availability": "OPEN",
#   "insuranceExpiresOn": "2027-03-31",
#   "reviews": []
# }

### Create a Second Profile
# Signed in as a different contractor, so the directory has two profiles to list.
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer second-contractor-token' \
  -d '{
    "companyName": "Bright Kitchen & Bath",
    "services": ["Kitchen Remodel", "Bathroom Remodel"],
    "serviceArea": "Los Angeles, CA",
    "availability": "OPEN"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/CreateContractorProfile

# Response:
# {
#   "contractorId": "c_51d2e0",
#   "companyName": "Bright Kitchen & Bath",
#   "services": ["Kitchen Remodel", "Bathroom Remodel"],
#   "serviceArea": "Los Angeles, CA",
#   "availability": "OPEN",
#   "reviews": []
# }

### Get Contractor Profile
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -d '{
    "contractorId": "c_8f3a2b"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/GetContractorProfile

# Response:
# {
#   "contractorId": "c_8f3a2b",
#   "companyName": "Acme Renovations",
#   "services": ["Painting", "Flooring"],
#   "serviceArea": "Los Angeles, CA",
#   "availability": "OPEN",
#   "insuranceExpiresOn": "2027-03-31",
#   "reviews": []
# }

### List Contractors for the Directory
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -d '{
    "service": "Kitchen Remodel",
    "serviceArea": "Los Angeles, CA",
    "availability": "OPEN"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/ListContractorProfiles

# Response:
# {
#   "contractorProfiles": [
#     {
#       "contractorId": "c_51d2e0",
#       "companyName": "Bright Kitchen & Bath",
#       "services": ["Kitchen Remodel", "Bathroom Remodel"],
#       "serviceArea": "Los Angeles, CA",
#       "availability": "OPEN",
#       "reviews": []
#     }
#   ],
#   "nextPageToken": ""
# }

### List One Page at a Time
# nextPageToken comes back until the last page, where it's empty.
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -d '{
    "serviceArea": "Los Angeles, CA",
    "pageSize": 1
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/ListContractorProfiles

# Response:
# {
#   "contractorProfiles": [
#     {
#       "contractorId": "c_8f3a2b",
#       "companyName": "Acme Renovations",
#       "services": ["Painting", "Flooring"],
#       "serviceArea": "Los Angeles, CA",
#       "availability": "OPEN",
#       "insuranceExpiresOn": "2027-03-31",
#       "reviews": []
#     }
#   ],
#   "nextPageToken": "b2Zmc2V0OjE="
# }

### Get the Next Page
# Send the nextPageToken from the previous response as pageToken.
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -d '{
    "serviceArea": "Los Angeles, CA",
    "pageSize": 1,
    "pageToken": "b2Zmc2V0OjE="
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/ListContractorProfiles

# Response:
# {
#   "contractorProfiles": [
#     {
#       "contractorId": "c_51d2e0",
#       "companyName": "Bright Kitchen & Bath",
#       "services": ["Kitchen Remodel", "Bathroom Remodel"],
#       "serviceArea": "Los Angeles, CA",
#       "availability": "OPEN",
#       "reviews": []
#     }
#   ],
#   "nextPageToken": ""
# }

### Update Contractor Profile
# updateMask lists the fields to change; the rest stay as they are. In JSON it's one comma-separated string.
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer contractor-token' \
  -d '{
    "contractorProfile": {
      "contractorId": "c_8f3a2b",
      "availability": "LIMITED"
    },
    "updateMask": "availability"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/UpdateContractorProfile

# Response:
# {
#   "contractorId": "c_8f3a2b",
#   "companyName": "Acme Renovations",
#   "services": ["Painting", "Flooring"],
#   "serviceArea": "Los Angeles, CA",
#   "availability": "LIMITED",
#   "insuranceExpiresOn": "2027-03-31",
#   "reviews": []
# }

### Create Review
# The reviewer comes from sign-in. The idempotency-key metadata makes it safe to retry: any unique
# string works, like a UUID, and a retry with the same key and request gets this same response back.
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -H 'idempotency-key: 5b0f3c1e-8a4d-4f7e-9c2b-1d6e7a8f9b30' \
  -d '{
    "contractorId": "c_8f3a2b",
    "rating": 5,
    "body": "They found the leak behind the tile and fixed it the same day."
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/CreateReview

# Response:
# {
#   "authorName": "Hana Okafor",
#   "body": "They found the leak behind the tile and fixed it the same day.",
#   "rating": 5
# }

### Retry the Same Review
# The connection dropped before the response arrived, so the app calls again. It gets the saved
# response back (grpcurl -v shows the idempotent-replayed: true header), and no second review is added.
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -H 'idempotency-key: 5b0f3c1e-8a4d-4f7e-9c2b-1d6e7a8f9b30' \
  -d '{
    "contractorId": "c_8f3a2b",
    "rating": 5,
    "body": "They found the leak behind the tile and fixed it the same day."
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/CreateReview

# Response:
# {
#   "authorName": "Hana Okafor",
#   "body": "They found the leak behind the tile and fixed it the same day.",
#   "rating": 5
# }

### Error: A Field Is Missing or Malformed
# The field errors come in the standard google.rpc.BadRequest details.
# Expect: InvalidArgument
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -d '{
    "companyName": "",
    "serviceArea": "Los Angeles, CA",
    "availability": "OPEN",
    "insuranceExpiresOn": "next March"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/CreateContractorProfile

# Response:
# ERROR:
#   Code: InvalidArgument
#   Message: Some fields aren't valid: company_name, services, insurance_expires_on
#   Details:
#   1)	{"@type": "type.googleapis.com/google.rpc.BadRequest", "fieldViolations": [{"field": "company_name", "description": "This field is required."}, {"field": "services", "description": "This field is required."}, {"field": "insurance_expires_on", "description": "Use a date like 2027-03-31."}]}

### Error: Not Signed In
# Expect: Unauthenticated
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -d '{
    "contractorId": "c_8f3a2b"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/GetContractorProfile

# Response:
# ERROR:
#   Code: Unauthenticated
#   Message: Sign in first. Send your token as Authorization: Bearer <token>.

### Error: Not Allowed
# Signed in as the other contractor, who doesn't own this profile.
# Expect: PermissionDenied
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer second-contractor-token' \
  -d '{
    "contractorProfile": {
      "contractorId": "c_8f3a2b",
      "availability": "BOOKED"
    },
    "updateMask": "availability"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/UpdateContractorProfile

# Response:
# ERROR:
#   Code: PermissionDenied
#   Message: Only the profile's owner can change it.

### Error: Not Found
# Expect: NotFound
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -d '{
    "contractorId": "c_000000"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/GetContractorProfile

# Response:
# ERROR:
#   Code: NotFound
#   Message: There's no contractor profile with the ID c_000000.

### Error: Already Exists
# Each user can have one contractor profile.
# Expect: AlreadyExists
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer contractor-token' \
  -d '{
    "companyName": "Acme Renovations West",
    "services": ["Painting"],
    "serviceArea": "Pasadena, CA",
    "availability": "OPEN"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/CreateContractorProfile

# Response:
# ERROR:
#   Code: AlreadyExists
#   Message: You already have a contractor profile: c_8f3a2b.

### Error: Idempotency Key Reused
# The same key with a different request. Use a new key for each new request.
# Expect: FailedPrecondition
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer homeowner-token' \
  -H 'idempotency-key: 5b0f3c1e-8a4d-4f7e-9c2b-1d6e7a8f9b30' \
  -d '{
    "contractorId": "c_8f3a2b",
    "rating": 4,
    "body": "They found the leak behind the tile and fixed it the same day."
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/CreateReview

# Response:
# ERROR:
#   Code: FailedPrecondition
#   Message: This idempotency key was already used for a different request. Use a new key for each new request.

### Delete Contractor Profile
# Returns google.protobuf.Empty, which grpcurl prints as {}.
# Expect: OK
grpcurl -plaintext -emit-defaults -import-path . -proto contractor.proto \
  -H 'authorization: Bearer second-contractor-token' \
  -d '{
    "contractorId": "c_51d2e0"
  }' \
  localhost:50051 renovationrevolution.contractors.v1.ContractorProfileService/DeleteContractorProfile

# Response:
# {}
