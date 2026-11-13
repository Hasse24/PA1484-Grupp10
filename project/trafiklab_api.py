
try:
    import requests
except ImportError:
    import urequests as requests

from secrets import API_KEY

def get_departures(stop_id="740000230"):

    
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
