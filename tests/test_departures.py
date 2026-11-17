"""Desktop checks of the departure pipeline with a fixture API and label doubles."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "project"))
api = Mock()
with patch.dict(sys.modules, {"lvgl": Mock(), "trafiklab_api": api}):
    from pages.departure_screen import DeparturePage
    from trafiklab_data import format_departures


def departure(mode="BUS", destination="Centrum"):
    return {
        "route": {"transport_mode": mode, "direction": destination},
        "scheduled": "2026-11-17T12:05:00",
        "realtime": "2026-11-17T12:09:00",
    }


class DepartureTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(self.folder.name)
        Path("selected_filter.json").write_text('{"filter": 0}')
        self.page = object.__new__(DeparturePage)
        self.page.rows = [
            {key: Mock() for key in ("type", "minutes", "time", "destination")}
            for _ in range(5)
        ]
        self.page.stop_label = Mock()
        self.page.departures = []
        api.get_departures.reset_mock()
        api.get_departures.return_value = {"departures": [departure()]}

    def test_clean_reload_uses_karlskrona_and_displays_returned_destination(self):
        self.page.reload_departures()
        api.get_departures.assert_called_once_with("740000230")
        self.page.rows[0]["destination"].set_text.assert_called_with("Centrum")
        self.page.stop_label.set_text.assert_called_with("Karlskrona C")

    def test_interrupted_station_save_still_allows_boot_reload(self):
        Path("selected_station.json").write_text('{"id":')
        self.page.reload_departures()
        api.get_departures.assert_called_once_with("740000230")

    def test_failed_fetch_followed_by_recovery(self):
        api.get_departures.return_value = None
        self.page.reload_departures()
        self.page.stop_label.set_text.assert_not_called()
        api.get_departures.return_value = {"departures": [departure("TRAIN", "Lund")]}
        self.page.reload_departures()
        self.page.rows[0]["destination"].set_text.assert_called_with("Lund")

    def test_saved_station_and_transport_filter(self):
        Path("selected_station.json").write_text(
            json.dumps({"id": 123, "name": "Test stop"})
        )
        api.get_departures.return_value = {
            "departures": [
                departure("BUS"),
                departure("BOAT", "Aspö"),
                departure("TRAIN", "Lund"),
            ]
        }
        self.page.reload_departures()
        api.get_departures.assert_called_once_with("123")
        self.page.stop_label.set_text.assert_called_with("Test stop")
        for i, expected in enumerate(
            [["Bus", "Ferry", "Train"], ["Bus"], ["Train"], ["Ferry"]]
        ):
            with self.subTest(filter=i):
                Path("selected_filter.json").write_text(json.dumps({"filter": i}))
                self.page.update_departures()
                labels = [
                    row["type"].set_text.call_args.args[0] for row in self.page.rows
                ]
                self.assertEqual(labels, expected + [""] * (5 - len(expected)))

    def test_empty_response_clears_previous_row(self):
        Path("selected_station.json").write_text('{"id": "123", "name": "Test stop"}')
        self.page.reload_departures()
        api.get_departures.return_value = {"departures": []}
        self.page.reload_departures()
        self.page.rows[0]["destination"].set_text.assert_called_with("")

    def test_delayed_departure_shows_planned_clock_and_live_countdown(self):
        from datetime import datetime

        # MicroPython mktime accepts eight fields. Model that interface on CPython.
        clock = SimpleNamespace(
            mktime=lambda parts: (
                datetime(*parts[:6]) - datetime(2000, 1, 1)
            ).total_seconds()
        )
        with patch.dict(format_departures.__globals__, {"time": clock}):
            rows = format_departures(
                {"timestamp": "2026-11-17T12:00:00", "departures": [departure()]}
            )
        self.assertEqual(rows, [("Bus", "12:05", "Centrum", "9 m")])
