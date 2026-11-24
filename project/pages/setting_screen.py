import lvgl as lv
import json
import network
from trafiklab_api import get_journey
from trafiklab_data import format_journey


def stop_search_text(value):
    # The supplied touch keyboard can spell Gräsvik as 'grasvik'.
    value = value.replace("Å", "a").replace("Ä", "a").replace("Ö", "o")
    return value.strip().lower().replace("å", "a").replace("ä", "a").replace("ö", "o")


class SettingsPage:
    def __init__(self, parent, on_station_saved=None, swedish_font=None, swedish_font_20=None,
                 on_filter_saved=None, on_reload=None):
        self.WIFI = "Wi-Fi..."
        self.API = "API..."
        self.BG = 0x0B1423
        self.parent = parent
        self.on_station_saved = on_station_saved
        self.on_reload = on_reload
        self.font_medium = swedish_font_20 if swedish_font_20 is not None else lv.font_montserrat_20
        self.font_large = swedish_font if swedish_font is not None else lv.font_montserrat_28

        self.on_filter_saved = on_filter_saved

        parent.set_style_bg_color(lv.color_hex(self.BG), 0)
        parent.set_style_bg_opa(lv.OPA.COVER, 0)

        self.title_wifi = lv.label(parent)
        self.title_wifi.set_text(self.WIFI)
        self.title_wifi.set_style_text_font(self.font_medium, 0)
        self.title_wifi.set_pos(490, 9)

        self.title_API = lv.label(parent)
        self.title_API.set_text(self.API)
        self.title_API.set_style_text_font(self.font_medium, 0)
        self.title_API.set_pos(370, 9)

        # US4.2B: manual refresh of the departure data from the settings screen
        self.reload_button = lv.button(parent)
        self.reload_button.set_size(110, 36)
        self.reload_button.set_pos(20, 4)
        self.reload_button.set_style_bg_color(lv.color_hex(0x192A43), 0)
        reload_label = lv.label(self.reload_button)
        reload_label.set_text("Reload")
        reload_label.set_style_text_font(self.font_medium, 0)
        reload_label.center()
        self.reload_button.add_event_cb(self.reload_departures, lv.EVENT.CLICKED, None)

        self.button = lv.button(parent)
        self.button.set_size(270, 50)
        self.button.align(lv.ALIGN.CENTER, 0, 90)
        self.button.set_style_bg_color(lv.color_hex(0x192A43), 0)
        self.button_label = lv.label(self.button)
        self.button_label.set_text("Set as default")
        self.button.add_event_cb(self.save_default, lv.EVENT.CLICKED, None)
        self.button_label.center()
        self.button_label.set_style_text_font(self.font_medium, 0)

        self.button2 = lv.button(parent)
        self.button2.set_size(270, 50)
        self.button2.align(lv.ALIGN.CENTER, 0, 30)
        self.button2.set_style_bg_color(lv.color_hex(0x192A43), 0)
        self.button2.add_event_cb(self.restore_default, lv.EVENT.CLICKED, None)
        self.button_label2 = lv.label(self.button2)
        self.button_label2.set_text("Restore Default")
        self.button_label2.center()
        self.button_label2.set_style_text_font(self.font_medium, 0)

        self.button3 = lv.button(parent)
        self.button3.set_size(270, 50)
        self.button3.align(lv.ALIGN.CENTER, 0, -30)
        self.button3.set_style_bg_color(lv.color_hex(0x192A43), 0)
        self.button_label3 = lv.label(self.button3)
        self.button_label3.set_text("Choose stop")
        self.button_label3.center()
        self.button_label3.set_style_text_font(self.font_medium, 0)
        self.button3.add_event_cb(self.open_station_page, lv.EVENT.CLICKED, None)

        self.journey_step = None
        self.create_station_page()

        # US5.1: open the journey planner
        journey_button = lv.button(parent)
        journey_button.set_size(270, 50)
        journey_button.align(lv.ALIGN.CENTER, 0, 150)
        journey_button.set_style_bg_color(lv.color_hex(0x192A43), 0)
        label = lv.label(journey_button)
        label.set_text("Plan journey")
        label.set_style_text_font(self.font_medium, 0)
        label.center()
        journey_button.add_event_cb(self.open_journey, lv.EVENT.CLICKED, None)

        # The dropdown
        self.dropdown = lv.dropdown(parent)
        self.dropdown.set_symbol("v")
        self.dropdown.set_options("All\nBus\nTrain\nFerry")
        self.dropdown.set_size(270, 50)
        self.dropdown.align(lv.ALIGN.CENTER, 0, -90)
        with open("selected_filter.json", "r") as file:
            saved = json.load(file)

        savednr = saved["filter"]
        self.dropdown.set_selected(savednr)
        self.dropdown.set_style_bg_color(lv.color_hex(0x192A43), 0)
        self.dropdown.set_style_text_font(self.font_medium, 0)
        self.dropdown.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.dropdown.add_event_cb(self.save_filter, lv.EVENT.VALUE_CHANGED, None)

    def reload_departures(self, event=None):
        # US4.2B: same reload as on the departure screen
        if self.on_reload is not None:
            self.on_reload()

    def save_filter(self, event):
        selected_index = self.dropdown.get_selected()
        with open("selected_filter.json", "w") as file:
            json.dump({"filter": selected_index}, file)

        if self.on_filter_saved is not None:
            self.on_filter_saved()

    def check_wifi(self):
        wlan = network.WLAN(network.STA_IF)

        worked = 1

        if wlan.isconnected():
            self.WIFI = "WIFI OK"
        else:
            self.WIFI = "NO WIFI"
            worked = 0
        self.title_wifi.set_text(self.WIFI)

        return worked

    def update_api_status(self, number):
        if (number == 0):
            self.title_API.set_text("API ERR")
        else:
            self.title_API.set_text("API UP")

    def restore_default(self, event=None):
        # US3.5: reset the current settings to the stored default settings
        try:
            with open("default_station.json", "r") as file:
                station = json.load(file)
        except (OSError, ValueError):
            station = {"name": "Karlskrona C", "id": "740000230"}

        try:
            with open("default_filter.json", "r") as file:
                saved_filter = json.load(file)
        except (OSError, ValueError):
            saved_filter = {"filter": 0}

        with open("selected_station.json", "w") as file:
            json.dump(station, file)

        with open("selected_filter.json", "w") as file:
            json.dump(saved_filter, file)

        self.dropdown.set_selected(saved_filter["filter"])
        self.station_dropdown.set_selected(self.current_station_index())

        if self.on_filter_saved is not None:
            self.on_filter_saved()

        if self.on_station_saved is not None:
            self.on_station_saved()

    def save_default(self, event=None):
        with open("selected_station.json", "r") as file:
            saved = json.load(file)

        with open("default_station.json", "w") as file:
            json.dump(saved, file)

        with open("selected_filter.json", "r") as file:
            saved = json.load(file)

        with open("default_filter.json", "w") as file:
            json.dump(saved, file)

    def create_station_page(self):

        # Load stops from local JSON file
        with open("stations.json", "rb") as file:
            self.stations = json.loads(file.read().decode("utf-8"))
        self.matches = self.stations

        # New view on top of Settings
        self.station_page = lv.obj(self.parent)
        self.station_page.set_size(600, 450)
        self.station_page.set_pos(0, 0)
        self.station_page.set_style_bg_color(
            lv.color_hex(0x0B1423), 0
        )
        self.station_page.set_style_bg_opa(lv.OPA.COVER, 0)

        # Title
        title = lv.label(self.station_page)
        title.set_text("Choose station")
        title.set_pos(30, 30)
        title.set_style_text_font(
            self.font_large, 0
        )

        # Dropdown with stops
        self.station_dropdown = lv.dropdown(self.station_page)
        self.station_dropdown.set_symbol("v")

        names = [station["name"] for station in self.stations]

        self.station_dropdown.set_options("\n".join(names))
        self.station_dropdown.set_size(510, 48)
        self.station_dropdown.set_pos(30, 110)
        self.station_dropdown.set_style_text_font(self.font_medium, 0)
        self.station_dropdown.get_list().set_style_text_font(self.font_medium, 0)

        # Back button
        back_button = lv.button(self.station_page)
        back_button.set_size(150, 50)
        back_button.set_pos(100, 210)

        back_label = lv.label(back_button)
        back_label.set_text("Back")
        back_label.set_style_text_font(self.font_medium, 0)
        back_label.center()

        back_button.add_event_cb(
            self.close_station_page,
            lv.EVENT.CLICKED,
            None
        )

        # Save button
        save_button = lv.button(self.station_page)
        save_button.set_size(150, 50)
        save_button.set_pos(310, 210)

        save_label = lv.label(save_button)
        save_label.set_text("Save")
        save_label.set_style_text_font(self.font_medium, 0)
        save_label.center()

        save_button.add_event_cb(
            self.save_station,
            lv.EVENT.CLICKED,
            None
        )

        # Search field, keyboard and journey result (US3.2C, US5.2B, US5.3B)
        self.station_title = title
        self.back_button = back_button
        self.save_button = save_button
        self.save_label = save_label
        self.query = lv.textarea(self.station_page)
        self.query.set_one_line(True)
        self.query.set_pos(30, 54)
        self.query.set_size(510, 48)
        self.query.set_placeholder_text("Search stop")
        self.query.set_style_text_font(self.font_medium, 0)
        self.query.add_event_cb(self.filter_stations, lv.EVENT.VALUE_CHANGED, None)

        self.keyboard = lv.keyboard(self.station_page)
        self.keyboard.set_size(540, 170)
        self.keyboard.set_pos(20, 228)
        self.keyboard.set_textarea(self.query)

        self.journey_result = lv.label(self.station_page)
        self.journey_result.set_pos(30, 94)
        self.journey_result.set_width(510)
        self.journey_result.set_style_text_font(self.font_medium, 0)
        self.journey_result.set_text("")
        self.query.add_flag(lv.obj.FLAG.HIDDEN)
        self.keyboard.add_flag(lv.obj.FLAG.HIDDEN)
        self.journey_result.add_flag(lv.obj.FLAG.HIDDEN)

        # Restore previous selection
        self.station_dropdown.set_selected(self.current_station_index())

        # Hide until opened
        self.station_page.add_flag(lv.obj.FLAG.HIDDEN)

    def current_station_index(self):
        # Index in self.stations for the stop saved in selected_station.json
        try:
            with open("selected_station.json", "r") as file:
                saved = json.load(file)
            for i, station in enumerate(self.stations):
                if str(station["id"]) == str(saved["id"]):
                    return i
        except (OSError, ValueError, KeyError):
            pass
        return 0

    def open_journey(self, event):
        self.journey_step = "start"
        self.station_title.set_pos(30, 5)
        self.station_title.set_text("1. Choose starting stop")
        self.save_label.set_text("Next")
        self.back_button.set_pos(100, 169)
        self.save_button.set_pos(310, 169)
        self.query.remove_flag(lv.obj.FLAG.HIDDEN)
        self.keyboard.remove_flag(lv.obj.FLAG.HIDDEN)
        self.query.set_text("")
        self.filter_stations(None)
        self.open_station_page(event)

    def open_station_page(self, event):
        if self.journey_step is None:
            # US3.2C: normal "Choose stop" for the departure board, with search
            self.station_title.set_pos(30, 5)
            self.station_title.set_text("Choose station")
            self.save_label.set_text("Save")
            self.back_button.set_pos(100, 169)
            self.save_button.set_pos(310, 169)
            self.query.remove_flag(lv.obj.FLAG.HIDDEN)
            self.keyboard.remove_flag(lv.obj.FLAG.HIDDEN)
            self.query.set_text("")
            self.filter_stations(None)
            # Empty search shows all stops, so mark the saved one
            self.station_dropdown.set_selected(self.current_station_index())
        self.station_page.move_foreground()
        self.station_page.remove_flag(lv.obj.FLAG.HIDDEN)

    def close_station_page(self, event):
        self.journey_step = None
        self.query.add_flag(lv.obj.FLAG.HIDDEN)
        self.keyboard.add_flag(lv.obj.FLAG.HIDDEN)
        self.journey_result.add_flag(lv.obj.FLAG.HIDDEN)
        self.journey_result.set_text("")
        self.station_title.set_pos(30, 30)
        self.station_title.set_text("Choose station")
        self.back_button.set_pos(100, 210)
        self.save_button.set_pos(310, 210)
        self.save_button.remove_flag(lv.obj.FLAG.HIDDEN)
        self.save_label.set_text("Save")
        self.station_dropdown.remove_flag(lv.obj.FLAG.HIDDEN)
        self.station_dropdown.set_options("\n".join(s["name"] for s in self.stations))
        self.matches = self.stations
        self.station_dropdown.set_selected(self.current_station_index())
        self.station_page.scroll_to_y(0, lv.ANIM.OFF)
        self.station_page.add_flag(lv.obj.FLAG.HIDDEN)

    def filter_stations(self, event):
        query = stop_search_text(self.query.get_text())
        self.matches = [s for s in self.stations if query in stop_search_text(s["name"])]
        options = "\n".join(s["name"] for s in self.matches)
        self.station_dropdown.set_options(options or "No matching stops")
        self.station_dropdown.set_selected(0)

    def choose_journey_stop(self):
        if not self.matches:
            return
        station = self.matches[self.station_dropdown.get_selected()]
        if self.journey_step == "start":
            self.start_station = station
            self.journey_step = "destination"
            self.station_title.set_text("2. Choose destination")
            self.save_label.set_text("Search")
            self.query.set_text("")
            self.filter_stations(None)
            return

        if station["id"] == self.start_station["id"]:
            self.station_title.set_text("Choose a different destination")
            return

        if self.check_wifi():
            data, error = get_journey(self.start_station["id"], station["id"])
            result = error or format_journey(data)
        else:
            result = "No Wi-Fi. Connect and try again."

        self.journey_step = "result"
        self.query.add_flag(lv.obj.FLAG.HIDDEN)
        self.keyboard.add_flag(lv.obj.FLAG.HIDDEN)
        self.station_dropdown.add_flag(lv.obj.FLAG.HIDDEN)
        self.save_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.back_button.set_pos(380, 10)
        self.station_title.set_text("Journey result")
        self.journey_result.set_text(result)
        self.journey_result.remove_flag(lv.obj.FLAG.HIDDEN)

    def save_station(self, event):
        if self.journey_step is not None:
            self.choose_journey_stop()
            return

        if not self.matches:
            return
        selected = self.matches[self.station_dropdown.get_selected()]

        with open("selected_station.json", "w") as file:
            json.dump(selected, file)

        self.close_station_page(event)

        if self.on_station_saved is not None:
            self.on_station_saved()
