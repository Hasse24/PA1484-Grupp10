import lvgl as lv
import json


SAMPLE_DEPARTURES = [('Bus', '12:05', 'Centrum', '5 m'), ('Train', '12:15', 'Malmö C', '15 m'), ('Ferry', '12:25', 'Aspö', '25 m'), ('Bus', '12:05', 'Centrum', '5 m'), ('Train', '12:15', 'Malmö C', '15 m'), ('Ferry', '12:25', 'Aspö', '25 m'), ('Bus', '12:05', 'Centrum', '5 m'), ('Train', '12:15', 'Malmö C', '15 m'), ('Ferry', '12:25', 'Aspö', '25 m')]


class DeparturePage:
    def __init__(self, parent, swedish_font=None, swedish_font_20=None):

        self.parent = parent

        # Colors and fonts
        self.BG = 0x0B1423
        self.ROW_BG = 0x192A43
        self.WHITE = 0xFFFFFF
        self.MUTED = 0xA8B7D0
        self.font_small = getattr(lv, "font_montserrat_16", None)
        self.font_medium = swedish_font_20 if swedish_font_20 is not None else getattr(lv, "font_montserrat_20", None)
        self.font_large = swedish_font if swedish_font is not None else getattr(lv, "font_montserrat_28", None)
        # data
        self.departures = []

        parent.set_style_bg_color(lv.color_hex(self.BG), 0)
        parent.set_style_bg_opa(lv.OPA.COVER, 0)

        # Info about stop
        self.create_text(parent, "Selected stop", 30, 27, self.MUTED, self.font_small)
        self.stop_label = self.create_text(parent, "Loading data...", 30, 53, self.WHITE, self.font_large)
        self.stop_label.set_width(350)
        self.stop_label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)

        self.reload_button = lv.button(parent)
        self.reload_button.set_size(110, 42)
        self.reload_button.set_pos(440, 40)
        
        self.reload_label = lv.label(self.reload_button)
        self.reload_label.set_text("Reload")
        self.reload_label.center()
        
        self.reload_button.add_event_cb(
            self.reload_departures,
            lv.EVENT.CLICKED,
            None
        )

        # Headers
        self.create_text(parent, "TYPE", 30, 115, self.MUTED, self.font_small, 100)
        self.create_text(parent, "IN", 100, 115, self.MUTED, self.font_small, 100)
        self.create_text(parent, "TIME", 180, 115, self.MUTED, self.font_small, 100)
        self.create_text(parent, "DESTINATION", 280, 115, self.MUTED, self.font_small, 280)

        # Departure rows
        self.rows = []

        for i in range(5):

            y = 155 + i * 48

            # row background
            type_label = self.create_text(parent, "", 20, y, self.WHITE, self.font_medium)
            type_label.set_size(560, 42)
            type_label.set_style_bg_color(lv.color_hex(self.ROW_BG), 0)
            type_label.set_style_bg_opa(lv.OPA.COVER, 0)
            type_label.set_style_radius(8, 0)
            type_label.set_style_pad_left(10, 0)
            type_label.set_style_pad_top(10, 0)

            # Dictionary
            row = {
                "type": type_label,
                "minutes": self.create_text(parent, "", 100, y + 10, self.WHITE, self.font_medium, 100),
                "time": self.create_text(parent, "", 180, y + 10, self.WHITE, self.font_medium, 100),
                "destination": self.create_text(parent, "", 280, y + 10, self.WHITE, self.font_medium, 280),
            }

            self.rows.append(row)

        self.update_departures()

    def set_departures(self, departures, stop_name=None):

        self.departures = departures

        if stop_name is not None:
            self.stop_label.set_text(stop_name)

        self.update_departures()


    # Create a textdiv
    def create_text(self, parent, text, x, y, color, font=None, width=150):

        label = lv.label(parent)
        label.set_text(text)
        label.set_pos(x, y)
        label.set_style_text_color(lv.color_hex(color), 0)
        label.set_style_text_font(font, 0)
        label.set_width(width)
        label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)

        return label

    # Update departures
    def update_departures(self, event=None):

        with open("selected_filter.json", "r") as file:
            saved = json.load(file)

        filter_nr = saved["filter"]
        filters = ["All", "Bus", "Train", "Ferry"]
        chosen_filter = filters[filter_nr]

        filtered = []

        for departure in self.departures:

            kind = departure[0]

            if chosen_filter == "All" or kind == chosen_filter:
                filtered.append(departure)

        for i, row in enumerate(self.rows):

            if i < len(filtered):

                kind, dep_time, destination, minutes = filtered[i]

                row["type"].set_text(kind)
                row["minutes"].set_text(minutes)
                row["time"].set_text(dep_time)
                row["destination"].set_text(destination)

            else:
                row["type"].set_text("")
                row["minutes"].set_text("")
                row["time"].set_text("")
                row["destination"].set_text("")

    
    def load_sample_departures(self, stop_name):
        self.set_departures(SAMPLE_DEPARTURES, stop_name)

    def reload_departures(self, event=None):
        try:
            with open("selected_station.json", "r") as file:
                station = json.load(file)
            stop_name = station["name"]
        except (OSError, ValueError, KeyError):
            stop_name = "Karlskrona C"

        self.load_sample_departures(stop_name)
