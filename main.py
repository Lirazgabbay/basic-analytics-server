import sqlite3
from db import DB
from table_methods import TableMethods
import uvicorn
from routes import app

def main():
    """
    Main function to initialize the database and start the FastAPI server.
    """
    # Initialize database and create table
    db = DB(sqlite3, 'analytics_events.db')
    table_methods = TableMethods(db)

    columns = {
        "eventtimestamputc": "TEXT NOT NULL",
        "userid": "TEXT NOT NULL",
        "eventname": "TEXT NOT NULL",
    }
    table_methods.create_table("events", columns)

    db.close()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
