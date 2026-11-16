
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
