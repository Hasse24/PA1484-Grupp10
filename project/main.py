import sys
import time
import json

import lvgl as lv
import network

from board_lvgl import start_board
from debug_log import log
import time

from secrets import WIFI_SSID, WIFI_PASSWORD

from pages.start_screen import HomePage
from pages.setting_screen import SettingsPage
from pages.departure_screen import DeparturePage
from fetch_data import retrieve_data

class Application:
    def __init__(self):
        self.display, self.touch, self.handler = start_board()

        self.create_ui()
        self.connect_wifi()

        # Load previously selected station
        self.startingprocedure_selected_station()

        log("student application ready")

        self.refresh_timer = lv.timer_create(
            self.refresh_departures,
            60000,
            None
        )

    def refresh_departures(self, timer):
        wifi_working = self.settings_page.check_wifi()

        if wifi_working != 1:
            self.connect_wifi()
            self.settings_page.check_wifi()

        self.load_selected_station()

    def startingprocedure_selected_station(self):

            #Make the deafult the current selected
            with open("default_filter.json", "r") as file:
                saved = json.load(file)

            self.settings_page.dropdown.set_selected(saved["filter"])

            with open("selected_filter.json", "w") as file:
                json.dump(saved,file)
    
            #Make the default station data appear
            with open("default_station.json", "r") as file:
                station = json.load(file)

            station_id = str(station["id"])
            station_name = station["name"]

            with open("selected_station.json", "w") as file:
                json.dump(station, file)  
    
            departures = retrieve_data(station_id, self.settings_page.update_api_status)
            self.settings_page.check_wifi()

            if departures is not None:
                self.departure_page.set_departures(
                    departures,
                    station_name
                )

    def load_selected_station(self):

        try:
            with open("selected_station.json", "r") as file:
                station = json.load(file)

            station_id = str(station["id"])
            station_name = station["name"]

        except (OSError, ValueError, KeyError):
            # Default station
            station_id = "740000230"
            station_name = "Karlskrona C"

        print("Fetching departures from:", station_name)

        departures = retrieve_data(station_id, self.settings_page.update_api_status)

        if departures is not None:
            self.departure_page.set_departures(
                departures,
                station_name
            )

    def create_ui(self):
        'Function: Creates UI'
        self.tileview = lv.tileview(lv.screen_active())
        self.tileview.set_size(600, 450)
        self.tileview.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        self.tile1 = self.tileview.add_tile(0, 0, lv.DIR.RIGHT)
        self.tile2 = self.tileview.add_tile(1, 0, lv.DIR.LEFT | lv.DIR.RIGHT)
        self.tile3 = self.tileview.add_tile(2, 0, lv.DIR.LEFT)

        # Ladda sidornas komponenter
        self.home_page = HomePage(self.tile1)
        self.departure_page = DeparturePage(
            self.tile2,
            swedish_font=self.home_page.swedish_font,
            swedish_font_20=self.home_page.swedish_font_20,
        )
        self.settings_page = SettingsPage(
            self.tile3,
            on_station_saved=self.departure_page.reload_departures,
            swedish_font=self.home_page.swedish_font,
            swedish_font_20=self.home_page.swedish_font_20,
            on_filter_saved=self.departure_page.update_departures,
        )

        self.departure_page.update_api_status = (
            self.settings_page.update_api_status
        )

    @staticmethod
    def connect_wifi():
        'Function: Connects to WiFi'
        log("connecting to Wi-Fi SSID: " + WIFI_SSID)
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(WIFI_SSID, WIFI_PASSWORD)
        started = time.ticks_ms()
        while (not station.isconnected() and
               time.ticks_diff(time.ticks_ms(), started) < 15_000):
            time.sleep_ms(250)
        log("Wi-Fi connected" if station.isconnected()
            else "Wi-Fi could not connect (timeout)")
try:
    
    app = Application()
except Exception as error:
    log("FATAL: %r" % (error,))
    sys.print_exception(error)
    raise
