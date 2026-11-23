from trafiklab_api import get_departures
from trafiklab_data import format_departures


def retrieve_data(station, update_api_status):

    raw_data = get_departures(station)

    if raw_data is None:
        update_api_status(0)
        return None

    try:
        departures = format_departures(raw_data)

    except Exception:
        update_api_status(0)
        return None

    update_api_status(1)
    return departures
