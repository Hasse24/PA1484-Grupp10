

import time


def to_seconds(date_string):
    # Convert YYYY-MM-DDTHH:MM:SS to seconds
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    hour = int(date_string[11:13])
    minute = int(date_string[14:16])
    second = int(date_string[17:19])

    return time.mktime((
        year, month, day,
        hour, minute, second, 0, 0
    ))

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

        # The API can leave out the delay, so treat a missing value as 0
        delay_sec = departure.get("delay") or 0
        delay_minutes = delay_sec // 60
        cancelled = departure.get("canceled")

        if (cancelled == True):
            delayed = "Canc."
        else:
            delayed = to_readible_time(delay_minutes)

        # Extract the transportation line
        the_line = route.get("designation")or "-"
        line = str(the_line)

        # Transport type
        mode = route.get("transport_mode", "")

        types = {
            "BUS": "Bus",
            "TRAIN": "Train",
            "BOAT": "Ferry",
            "TRAM": "Tram",
            "METRO": "Metro"
        }

        kind = types.get(mode, mode)

        # Extract the name of the destination
        destination = route.get("direction") or "Unknown"
        destination = destination.replace("Ø", "Ö")
        destination = destination.replace("é", "e")

        # The departure time
        departure_time = (
            departure.get("realtime")
            or departure.get("scheduled")
        )

        if not departure_time:
            continue

        clock_time = departure_time[11:16]

        # Minutes until departure
        minutes = "--"
        minutes_left = None

        if current_time:
            seconds_left = (
                to_seconds(departure_time)
                - to_seconds(current_time)
            )

            minutes_left = max(
                0, (int(seconds_left) + 59) // 60
            )

            minutes = to_readible_time(minutes_left)

        if departure.get("canceled"):
            minutes = "-"
        elif minutes_left == 0:
            minutes = "Now"

        # Tuple matching DeparturePage
        result.append((
            kind,
            clock_time,
            destination,
            line,
            minutes, 
            delayed
        ))

    return result


def stop_time(stop):
    # Use real-time date and time when ResRobot provides them
    if stop.get("rtDate") and stop.get("rtTime"):
        return stop["rtDate"], stop["rtTime"]
    return stop["date"], stop["time"]


def format_journey(data):
    # US5.3B: show the journey with the earliest arrival and every change
    if not isinstance(data, dict):
        return "Could not read journey data."
    if data.get("errorCode") == "SVC_NO_RESULT":
        return "No journey found."
    if data.get("errorCode") or not isinstance(data.get("Trip"), list):
        return "Could not read journey data."

    best_arrival = None
    best_lines = []
    for trip in data["Trip"]:
        try:
            legs = trip["LegList"]["Leg"]
            if not legs or any(leg.get("cancelled") for leg in legs):
                continue
            # Include the final leg even when the journey ends with a walk.
            end = legs[-1]["Destination"]
            arrival = stop_time(end)
            if best_arrival is not None and arrival >= best_arrival:
                continue
            lines = []
            for leg in legs:
                if leg["type"] == "JNY":
                    stop = leg["Origin"]
                    _, dep_time = stop_time(stop)
                    action = "Change" if lines else "Depart"
                    lines.append("%s %s  %s  %s" % (
                        action, dep_time[:5], stop["name"], leg.get("name", "")
                    ))
            if not lines:
                lines.append("Walk to destination")
            elif len(lines) == 1:
                lines.append("Direct - no changes")
            lines.append("Arrive %s %s  %s" % (arrival[0], arrival[1][:5], end["name"]))
        except (KeyError, IndexError, TypeError, AttributeError):
            continue
        best_arrival, best_lines = arrival, lines

    if best_lines:
        return "\n".join(best_lines) + "\n\nSource: Trafiklab / ResRobot"
    return "No journey found."
