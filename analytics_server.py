"""
analytics_server.py - A server that generates n events for testing /process_event endpoint of the FastAPI application.
"""
import random
import string
import requests
import joblib

def random_event():
    """
    Generate a random event with a random user ID and event name.
    """
    user_id_len = random.randint(5, 15)
    random_user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=user_id_len))
    event_name = random.choice([
        "click", "view", "purchase", "login", "logout", "signup",
        "delete", "update", "search", "share", "error", "warning",
        "info", "debug"
    ])
    return {
        "userid": random_user_id,
        "eventname": event_name
    }

def post_n_times_to_server(n=1000):
    """
    Send 'n' random events to the server in parallel using joblib.
    """
    base_url = "https://ourapp-fucph9h2dpbbhacj.israelcentral-01.azurewebsites.net"
    endpoint = "/process_event"
    url = base_url + endpoint

    events = [random_event() for _ in range(n)]

    # Post events in parallel
    results = joblib.Parallel(n_jobs=-1, backend="threading")(
        joblib.delayed(requests.post)(url, json=event) for event in events
    )

    return results

if __name__ == "__main__":
    # Post 1000 events to the server
    responses = post_n_times_to_server(1000)
    for response in responses:
        print(f"Status: {response.status_code}, Response: {response.json()}")
