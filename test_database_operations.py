import pytest
import sqlite3
from fastapi.testclient import TestClient
from db import DB
from table_methods import TableMethods
from routes import app

# Use TestClient to test FastAPI routes
client = TestClient(app)

@pytest.fixture
def test_db():
    """
    Pytest fixture to set up and tear down a test database.
    """
    db = DB(sqlite3, ":memory:")  # Use an in-memory SQLite database for testing
    table_methods = TableMethods(db)

    # Create a test table
    columns = {
        "eventtimestamputc": "TEXT NOT NULL",
        "userid": "TEXT NOT NULL",
        "eventname": "TEXT NOT NULL"
    }
    table_methods.create_table("events", columns)
    yield table_methods
    db.close()


def test_create_table(test_db):
    """
    Test if the table is created successfully.
    """
    db = test_db.db
    cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events';")
    assert cursor.fetchone() is not None, "Table 'events' exist."


def test_insert_to_table(test_db):
    """
    Test inserting valid data into the table.
    """
    data_to_insert = {
        "eventtimestamputc": "2025-01-01 00:00:00",
        "userid": "user123",
        "eventname": "test_event"
    }
    test_db.insert_to_table("events", data_to_insert)

    # Verify insertion
    cursor = test_db.db.execute("SELECT * FROM events WHERE userid = ?", ("user123",))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "user123"


def test_insert_empty_data(test_db):
    """
    Test inserting empty data into the table (edge case).
    """
    with pytest.raises(Exception, match="Error inserting data"):
        test_db.insert_to_table("events", {})



def test_process_event_endpoint():
    """
    Test the /process_event endpoint of the FastAPI application with valid data.
    """
    event_data = {
        "userid": "user456",
        "eventname": "click_button"
    }

    response = client.post("/process_event", json=event_data)

    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["userid"] == "user456"
    assert response_data["eventname"] == "click_button"
    assert "eventtimestamputc" in response_data


def test_process_event_missing_fields():
    """
    Test sending incomplete data to the /process_event endpoint.
    """
    incomplete_event_data = {
        "userid": "user789"
    }

    response = client.post("/process_event", json=incomplete_event_data)
    assert response.status_code == 422


def test_process_event_empty_fields():
    """
    Test sending incomplete data to the /process_event endpoint.
    """
    incomplete_event_data = {
        "userid": "user789",
        "eventname": ""
    }

    response = client.post("/process_event", json=incomplete_event_data)
    assert response.status_code == 400


def test_process_event_large_payload():
    """
    Test sending a large payload to the /process_event endpoint.
    """
    large_event_data = {
        "userid": "x" * 1000,  # Excessively long string
        "eventname": "y" * 1000,  # Excessively long string
    }

    response = client.post("/process_event", json=large_event_data)
    assert response.status_code == 200


def test_insert_to_table_duplicate_entry(test_db):
    """
    Test inserting duplicate entries into the table.
    """
    data_to_insert = {
        "eventtimestamputc": "2025-01-01 00:00:00",
        "userid": "user_duplicate",
        "eventname": "test_event",
    }
    test_db.insert_to_table("events", data_to_insert)

    # Insert duplicate
    test_db.insert_to_table("events", data_to_insert)

    cursor = test_db.db.execute("SELECT COUNT(*) FROM events WHERE userid = ?", ("user_duplicate",))
    result = cursor.fetchone()
    assert result[0] == 2


def test_invalid_table_name_creating(test_db):
    """
    Test operations with an invalid table name while creating a table.
    """
    with pytest.raises(Exception, match="Error creating table"):
        test_db.create_table("", {"col1": "TEXT"})  # Invalid table name


def test_invalid_table_name_inserting(test_db):
    """
    Test operations with an invalid table name while creating a table.
    """
    data_to_insert = {
        "eventtimestamputc": "2025-01-01 00:00:00",
        "userid": "user123",
        "eventname": "test_event"
    }
    with pytest.raises(Exception, match="Error inserting data"):
        test_db.insert_to_table("", data_to_insert)  # Invalid table name
