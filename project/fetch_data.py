from trafiklab_api import get_departures


def retrieve_data(station):
    # Make the API request, but no precoss yet
    get_departures(station)

    # Dummy data
    return [
        ("Bus", "12:05", "Centrum", "5 m"),
        ("Train", "12:15", "Malmö C", "15 m"),
        ("Ferry", "12:25", "Aspö", "25 m"),
        ("Bus", "12:05", "Centrum", "5 m"),
        ("Train", "12:15", "Malmö C", "15 m"),
        ("Ferry", "12:25", "Aspö", "25 m"),
        ("Bus", "12:05", "Centrum", "5 m"),
        ("Train", "12:15", "Malmö C", "15 m"),
        ("Ferry", "12:25", "Aspö", "25 m"),
    ]
