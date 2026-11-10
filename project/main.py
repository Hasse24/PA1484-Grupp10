import sys
import time

import lvgl as lv
import network

from board_lvgl import start_board
from debug_log import log
import time

from secrets import WIFI_SSID, WIFI_PASSWORD

from pages.start_screen import HomePage
from pages.setting_screen import SettingsPage
from pages.departure_screen import DeparturePage

class Application:
    def __init__(self):
        self.display, self.touch, self.handler = start_board()

        self.create_ui()
        self.connect_wifi()

        # Load Karlskrona C at startup
        self.startingprocedure()

        log("student application ready")

    def startingprocedure(self):
        self.departure_page.load_sample_departures("Karlskrona C")

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
            swedish_font=self.home_page.swedish_font,
            swedish_font_20=self.home_page.swedish_font_20,
            on_filter_saved=self.departure_page.update_departures,
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
