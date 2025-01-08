"""
routes.py - FastAPI routes for the analytics_events table.
"""
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from table_methods import TableMethods
from db import DB
from event import Event
from report_request import ReportRequest
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
    

@app.post("/get_reports")
def get_reports(report_request: ReportRequest):
    """
    RESTful endpoint to retrieve reports.
    Takes in 'lastseconds' and 'userid' as parameters and returns all matching events.
    """
    lastseconds = report_request.lastseconds
    userid = report_request.userid
    if lastseconds <= 0 or not userid:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid 'lastseconds' or 'userid' parameter."
        )
    
    try:
        db = DB(sqlite3, 'analytics_events.db')
        table_methods = TableMethods(db)

        start_time = datetime.utcnow() - timedelta(seconds=lastseconds)
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")

        query = """
            SELECT eventtimestamputc, userid, eventname
            FROM events
            WHERE userid = ? AND eventtimestamputc >= ?
        """
        cursor = db.execute(query, (userid, start_time_str))
        events = cursor.fetchall()

        db.close()

        event_list = [
            {"eventtimestamputc": row[0], "userid": row[1], "eventname": row[2]}
            for row in events
        ]

        return {"events": event_list, "status_code": HTTP_200_OK}

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve reports: {str(e)}"
        )
