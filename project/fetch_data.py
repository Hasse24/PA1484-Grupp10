from trafiklab_api import get_departures
from trafiklab_data import format_departures


def retrieve_data(station):

    raw_data = get_departures(station)

    if raw_data is None:
        return None

    try:
        departures = format_departures(raw_data)

    except Exception:
        return None

    return departures
