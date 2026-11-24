
try:
    import requests
except ImportError:
    import urequests as requests

from secrets import API_KEY

def get_departures(stop_id="740000230"):

    special_time = False

    if special_time == True:
        requested_time = "2026-11-10T10:00"

        url = (
            "https://realtime-api.trafiklab.se/v1/departures/"
            + stop_id
            + "/" + requested_time
            + "?key=" + API_KEY
        )
    else:
        url = (
                "https://realtime-api.trafiklab.se/v1/departures/"
                + stop_id
                + "?key=" + API_KEY
            )

    response = None

    try:
        response = requests.get(url)

        print("HTTP status:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            return data

        return None

    except Exception:
        return None

    finally:
        if response is not None:
            response.close()


def get_journey(start_id, end_id):
    """Return (ResRobot response, error message) for the two selected stops."""
    import secrets
    key = getattr(secrets, "RESROBOT_API_KEY", "")
    if not key:
        return None, "Set RESROBOT_API_KEY in secrets.py."

    url = ("https://api.resrobot.se/v2.1/trip?format=json&passlist=0"
           "&originId=%s&destId=%s&accessId=%s" % (start_id, end_id, key))
    response = None
    try:
        response = requests.get(url, timeout=12)
        if response.status_code == 403:
            return None, "Access denied. Check the ResRobot key."
        if response.status_code != 200:
            return None, "Journey service returned HTTP %s." % response.status_code
        return response.json(), None
    except OSError:
        return None, "Journey service unavailable. Check Wi-Fi."
    except MemoryError:
        return None, "Too little memory for the journey response."
    except (ValueError, TypeError):
        return None, "Could not read journey data."
    finally:
        if response is not None:
            response.close()
