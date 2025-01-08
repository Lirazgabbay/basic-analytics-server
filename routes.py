"""
routes.py - FastAPI routes for the analytics_events table.
"""
from datetime import datetime
from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from table_methods import TableMethods
from db import DB
from event import Event
import sqlite3

app = FastAPI()

@app.post("/process_event")
def process_event(event: Event):
    """
    RESTful endpoint to process an event.
    Takes in the event data, validates it, and saves it to the database.
    """
    if event.userid == "" or event.userid is None or event.eventname == "" or event.eventname is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Missing required fields: 'userid' or 'eventname'"
        )
    try:
        db = DB(sqlite3, 'analytics_events.db')
        table_methods = TableMethods(db)

        # Capture the current UTC timestamp
        eventtimestamputc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        data_to_insert = {
            "eventtimestamputc": eventtimestamputc,
            "userid": event.userid,
            "eventname": event.eventname
        }

        # Insert the data into the table
        table_methods.insert_to_table("events", data_to_insert)

        # Close the database connection
        db.close()

        return {"data": data_to_insert, "status_code": HTTP_200_OK}

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process event: {str(e)}"
        )
