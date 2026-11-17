import time


def to_seconds(date_string):
    # Convert YYYY-MM-DDTHH:MM:SS to seconds
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    hour = int(date_string[11:13])
    minute = int(date_string[14:16])
    second = int(date_string[17:19])

    return time.mktime((year, month, day, hour, minute, second, 0, 0))


def to_readible_time(minutes_left):
    if minutes_left >= 60:
        hours = minutes_left // 60
        remaining_minutes = minutes_left % 60

        minutes = str(hours) + " h " + str(remaining_minutes) + " m"
    else:
        minutes = str(minutes_left) + " m"

    return minutes


def format_departures(data):
    result = []

    # Timestamp returned by API
    current_time = data.get("timestamp")

    # Handle each departure seperetly in this loop
    for departure in data.get("departures", []):
        route = departure.get("route") or {}

        # Transport type
        mode = route.get("transport_mode", "")

        types = {
            "BUS": "Bus",
            "TRAIN": "Train",
            "BOAT": "Ferry",
            "TRAM": "Tram",
            "METRO": "Metro",
        }

        kind = types.get(mode, mode)

        # Extract the name of the destination
        destination = route.get("direction") or "Unknown"
        destination = destination.replace("Ø", "Ö")
        destination = destination.replace("é", "e")

        # The departure time
        departure_time = departure.get("realtime") or departure.get("scheduled")

        if not departure_time:
            continue

        scheduled = departure.get("scheduled")
        clock_time = scheduled[11:16] if scheduled else "--:--"

        # Minutes until departure
        minutes = "--"
        minutes_left = None

        if current_time:
            seconds_left = to_seconds(departure_time) - to_seconds(current_time)

            minutes_left = max(0, (int(seconds_left) + 59) // 60)

            minutes = to_readible_time(minutes_left)

        if departure.get("canceled"):
            minutes = "-"
        elif minutes_left == 0:
            minutes = "Now"

        # Tuple matching DeparturePage
        result.append((kind, clock_time, destination, minutes))

    return result
