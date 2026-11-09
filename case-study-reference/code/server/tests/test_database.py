"""Checks database/schema.sql, seed.sql, and queries.sql against a real PostgreSQL.

Needs a database to connect to, given as DATABASE_URL, for example with Docker:
    docker compose up -d database
    DATABASE_URL=postgresql://postgres@localhost:5432/postgres python3 -m pytest tests/test_database.py
Without DATABASE_URL these tests are skipped. Each test makes its own database and drops it after.
"""

import json
import os
import re
import secrets

import pytest

from conftest import API_FOLDER

psycopg = pytest.importorskip("psycopg")
DATABASE_URL = os.environ.get("DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="set DATABASE_URL to run the database tests")
DATABASE_FOLDER = API_FOLDER / "database"


def sql_statements(file_name):
    """Splits a .sql file into statements, without the comment lines."""
    lines = [line for line in (DATABASE_FOLDER / file_name).read_text().split("\n") if not line.strip().startswith("--")]
    return [statement.strip() for statement in re.split(r";\s*\n", "\n".join(lines) + "\n") if statement.strip()]


@pytest.fixture
def database():
    """A fresh database with the schema and seed data loaded."""
    database_name = "renovation_test_" + secrets.token_hex(4)
    with psycopg.connect(DATABASE_URL, autocommit=True) as admin_connection:
        admin_connection.execute("CREATE DATABASE " + database_name + " ENCODING 'UTF8' TEMPLATE template0")
    test_url = re.sub(r"/[^/?]*(\?|$)", "/" + database_name + r"\1", DATABASE_URL, count=1) \
        if re.search(r"//[^/]+/", DATABASE_URL) else DATABASE_URL + "/" + database_name
    try:
        with psycopg.connect(test_url, autocommit=True) as connection:
            for file_name in ("schema.sql", "seed.sql"):
                for statement in sql_statements(file_name):
                    connection.execute(statement)
            yield connection
    finally:
        with psycopg.connect(DATABASE_URL, autocommit=True) as admin_connection:
            admin_connection.execute("DROP DATABASE IF EXISTS " + database_name + " WITH (FORCE)")


def queries():
    statements = sql_statements("queries.sql")
    return {"directory": statements[0], "profile": statements[1], "explain": statements[3]}


def test_directory_query_finds_the_kitchen_remodeler(database):
    rows = database.execute(queries()["directory"]).fetchall()
    assert [(row[0], row[1], row[2]) for row in rows] == [("c_51d2e0", "Bright Kitchen & Bath", ["Kitchen Remodel", "Bathroom Remodel"])]


def test_profile_query_matches_the_api_response(database):
    """The same profile, services in order, and review as the REST example shows."""
    contractor_id, company_name, services, service_area, availability, insurance_date, reviews = \
        database.execute(queries()["profile"]).fetchone()
    assert (contractor_id, company_name, services, service_area, availability, str(insurance_date)) == \
        ("c_8f3a2b", "Acme Renovations", ["Painting", "Flooring"], "Los Angeles, CA", "OPEN", "2027-03-31")
    rest_text = (API_FOLDER / "rest.http").read_text()
    review_block = rest_text.split("### Create Review\n", 1)[1].split("\n### ", 1)[0]
    review_lines = [line[2:] for line in review_block.split("# Content-Type: application/json\n#\n", 1)[1].split("\n") if line.startswith("# ")]
    assert reviews == [json.loads("\n".join(review_lines))]


def test_the_directory_search_uses_its_indexes(database):
    database.execute("SET enable_seqscan = off")
    plan = "\n".join(row[0] for row in database.execute(queries()["explain"]).fetchall())
    assert "contractor_services_by_service" in plan
    assert "contractor_profiles_by_area_and_availability" in plan


@pytest.mark.parametrize("statement, error_class", [
    # Each user can have one contractor profile (409 in the API)
    ("INSERT INTO contractor_profiles (contractor_id, owner_user_id, company_name, service_area, availability) "
     "VALUES ('c_000001', 'u_contractor', 'Acme West', 'Pasadena, CA', 'OPEN')", "UniqueViolation"),
    # Ratings are 1 to 5
    ("INSERT INTO reviews (contractor_id, author_user_id, rating) VALUES ('c_8f3a2b', 'u_homeowner', 6)", "CheckViolation"),
    # Availability is one of three values
    ("INSERT INTO contractor_profiles (contractor_id, owner_user_id, company_name, service_area, availability) "
     "VALUES ('c_000002', 'u_homeowner', 'Hana Builds', 'Pasadena, CA', 'opne')", "InvalidTextRepresentation"),
    # Company names can't be blank
    ("INSERT INTO contractor_profiles (contractor_id, owner_user_id, company_name, service_area, availability) "
     "VALUES ('c_000003', 'u_homeowner', '   ', 'Pasadena, CA', 'OPEN')", "CheckViolation"),
])
def test_the_database_enforces_the_api_rules(database, statement, error_class):
    with pytest.raises(getattr(psycopg.errors, error_class)):
        database.execute(statement)


def test_deleting_a_profile_removes_its_services_and_reviews(database):
    database.execute("DELETE FROM contractor_profiles WHERE contractor_id = 'c_8f3a2b'")
    assert database.execute("SELECT count(*) FROM contractor_services WHERE contractor_id = 'c_8f3a2b'").fetchone()[0] == 0
    assert database.execute("SELECT count(*) FROM reviews WHERE contractor_id = 'c_8f3a2b'").fetchone()[0] == 0
