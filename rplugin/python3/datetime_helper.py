from datetime import datetime


def get_current_timestamp():
    # Get the current date and time
    now = datetime.now()

    # Format the current timestamp as a string
    # You can adjust the format as needed
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    return timestamp
