-- The same people and profiles as the API examples, so the queries have something to find.

INSERT INTO users (user_id, display_name, email, phone) VALUES
  ('u_homeowner',         'Hana Okafor',          'hana@example.com',    '+1-213-555-0142'),
  ('u_contractor',        'Acme Renovations',     'office@acme.example', '+1-213-555-0187'),
  ('u_second_contractor', 'Bright Kitchen & Bath', 'hello@bright.example', NULL);

INSERT INTO contractor_profiles (contractor_id, owner_user_id, company_name, service_area, availability, insurance_expires_on, created_at) VALUES
  ('c_8f3a2b', 'u_contractor',        'Acme Renovations',      'Los Angeles, CA', 'OPEN', '2027-03-31', '2026-11-08 09:00:00+00'),
  ('c_51d2e0', 'u_second_contractor', 'Bright Kitchen & Bath', 'Los Angeles, CA', 'OPEN', NULL,         '2026-11-08 09:05:00+00');

INSERT INTO contractor_services (contractor_id, position, service) VALUES
  ('c_8f3a2b', 1, 'Painting'),
  ('c_8f3a2b', 2, 'Flooring'),
  ('c_51d2e0', 1, 'Kitchen Remodel'),
  ('c_51d2e0', 2, 'Bathroom Remodel');

INSERT INTO reviews (contractor_id, author_user_id, rating, body) VALUES
  ('c_8f3a2b', 'u_homeowner', 5, 'They found the leak behind the tile and fixed it the same day.');
