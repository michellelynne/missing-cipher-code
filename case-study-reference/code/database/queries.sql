-- The queries behind the Contractors Directory API. Run schema.sql and seed.sql first.
-- Each one says which API call it answers.

-- ---------- List Contractors for the Directory ----------
-- GET /api/contractors?service=Kitchen%20Remodel&serviceArea=Los%20Angeles%2C%20CA&availability=OPEN&pageSize=20
-- Asks for one more row than the page holds: if it comes back, there's a next page.
SELECT profile.contractor_id,
       profile.company_name,
       ARRAY(SELECT offered.service FROM contractor_services AS offered
             WHERE offered.contractor_id = profile.contractor_id ORDER BY offered.position) AS services,
       profile.service_area,
       profile.availability,
       profile.insurance_expires_on
FROM contractor_profiles AS profile
WHERE lower(profile.service_area) = lower('Los Angeles, CA')
  AND profile.availability = 'OPEN'
  AND EXISTS (SELECT 1 FROM contractor_services AS offered
              WHERE offered.contractor_id = profile.contractor_id
                AND lower(offered.service) = lower('Kitchen Remodel'))
ORDER BY profile.created_at, profile.contractor_id
LIMIT 20 + 1 OFFSET 0;

-- ---------- Get Contractor Profile, with its reviews ----------
-- GET /api/contractors/c_8f3a2b
SELECT profile.contractor_id,
       profile.company_name,
       ARRAY(SELECT offered.service FROM contractor_services AS offered
             WHERE offered.contractor_id = profile.contractor_id ORDER BY offered.position) AS services,
       profile.service_area,
       profile.availability,
       profile.insurance_expires_on,
       COALESCE((SELECT json_agg(json_build_object('authorName', author.display_name,
                                                   'body', review.body,
                                                   'rating', review.rating) ORDER BY review.created_at)
                 FROM reviews AS review JOIN users AS author ON author.user_id = review.author_user_id
                 WHERE review.contractor_id = profile.contractor_id), '[]'::json) AS reviews
FROM contractor_profiles AS profile
WHERE profile.contractor_id = 'c_8f3a2b';

-- ---------- Check that the directory search uses its indexes ----------
-- With only two rows PostgreSQL would rather read the whole table, so turn that off to see the plan
-- it would use at scale. Look for contractor_services_by_service in the output.
SET enable_seqscan = off;
EXPLAIN
SELECT profile.contractor_id
FROM contractor_profiles AS profile
WHERE lower(profile.service_area) = lower('Los Angeles, CA')
  AND profile.availability = 'OPEN'
  AND EXISTS (SELECT 1 FROM contractor_services AS offered
              WHERE offered.contractor_id = profile.contractor_id
                AND lower(offered.service) = lower('Kitchen Remodel'));
RESET enable_seqscan;
