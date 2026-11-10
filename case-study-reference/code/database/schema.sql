-- The tables behind the Contractors Directory API (Renovation Revolution), for PostgreSQL 16 or newer.
--
-- The example server keeps its data in memory so it runs with nothing installed. This is how you'd
-- store the same data for real, with the rules the server checks written into the database too,
-- and an index behind each filter the directory offers.
--
-- Try it: docker compose up database (from the api folder), then
--   psql -h localhost -U postgres -d renovation -f database/queries.sql

-- The same three values as the API. A typo like 'opne' can't get in.
CREATE TYPE availability AS ENUM ('OPEN', 'LIMITED', 'BOOKED');

-- Email and phone belong to the person, not the profile, so they live here and come from sign-in.
CREATE TABLE users (
  user_id      text PRIMARY KEY,
  display_name text NOT NULL,
  email        text NOT NULL UNIQUE,
  phone        text
);

CREATE TABLE contractor_profiles (
  contractor_id        text PRIMARY KEY,
  -- UNIQUE is the "each user can have one contractor profile" rule (409 Already Exists in the API)
  owner_user_id        text NOT NULL UNIQUE REFERENCES users (user_id),
  company_name         text NOT NULL CHECK (length(btrim(company_name)) BETWEEN 1 AND 100),
  service_area         text NOT NULL CHECK (btrim(service_area) <> ''),
  availability         availability NOT NULL,
  insurance_expires_on date,
  created_at           timestamptz NOT NULL DEFAULT now()
);

-- One row per service a contractor offers, so "everyone who does Kitchen Remodel" is an index lookup
-- instead of a search through every profile's list.
CREATE TABLE contractor_services (
  contractor_id text NOT NULL REFERENCES contractor_profiles (contractor_id) ON DELETE CASCADE,
  position      smallint NOT NULL,  -- keeps the order the contractor listed them in
  service       text NOT NULL CHECK (btrim(service) <> ''),
  PRIMARY KEY (contractor_id, position),
  UNIQUE (contractor_id, service)
);

CREATE TABLE reviews (
  review_id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  contractor_id  text NOT NULL REFERENCES contractor_profiles (contractor_id) ON DELETE CASCADE,
  author_user_id text NOT NULL REFERENCES users (user_id),
  rating         smallint NOT NULL CHECK (rating BETWEEN 1 AND 5),
  body           text CHECK (length(body) <= 2000),
  created_at     timestamptz NOT NULL DEFAULT now()
);

-- Saved results for Idempotency-Key retries. A retry looks up its key here instead of creating again.
CREATE TABLE idempotency_keys (
  user_id             text NOT NULL REFERENCES users (user_id),
  operation           text NOT NULL,
  idempotency_key     text NOT NULL CHECK (length(idempotency_key) BETWEEN 1 AND 255),
  request_fingerprint text NOT NULL,
  response            jsonb NOT NULL,
  created_at          timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, operation, idempotency_key)
);

-- ---------- One index for each way the directory is searched ----------

-- ?service=Kitchen%20Remodel   Filters ignore capitals, so the index is on lower(service) too.
CREATE INDEX contractor_services_by_service ON contractor_services (lower(service), contractor_id);

-- ?serviceArea=...&availability=OPEN   Ends with the page order, so a page reads straight off the index.
CREATE INDEX contractor_profiles_by_area_and_availability
  ON contractor_profiles (lower(service_area), availability, created_at, contractor_id);

-- A profile's reviews, newest last
CREATE INDEX reviews_by_contractor ON reviews (contractor_id, created_at);

-- Cleaning out idempotency keys older than 24 hours
CREATE INDEX idempotency_keys_by_age ON idempotency_keys (created_at);
