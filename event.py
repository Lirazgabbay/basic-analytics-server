"""
Pydantic model for the request body

using BaseMode class from pydantic for validates incoming request data against the model,
raises errors for missing/incorrect fields and converts JSON into Python object.
"""
from pydantic import BaseModel

class Event(BaseModel):
    userid: str
    eventname: str