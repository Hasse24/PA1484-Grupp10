import lvgl as lv
import json

class SettingsPage:
    def __init__(self, parent, on_station_saved=None, swedish_font=None, swedish_font_20=None, on_filter_saved=None):
        self.BG = 0x0B1423
        self.parent = parent
        self.on_station_saved = on_station_saved
        self.font_medium = swedish_font_20 if swedish_font_20 is not None else lv.font_montserrat_20
        self.font_large = swedish_font if swedish_font is not None else lv.font_montserrat_28

        self.on_filter_saved = on_filter_saved

        parent.set_style_bg_color(lv.color_hex(self.BG), 0)
        parent.set_style_bg_opa(lv.OPA.COVER, 0)

        self.button = lv.button(parent)
        self.button.set_size(270, 50)
        self.button.align(lv.ALIGN.CENTER, 0,90)
        self.button.set_style_bg_color(lv.color_hex(0x192A43), 0)
        self.button_label = lv.label(self.button)
        self.button_label.set_text("Set as deafult")
        self.button_label.center()
        self.button_label.set_style_text_font(self.font_medium, 0)
        
        self.button2 = lv.button(parent)
        self.button2.set_size(270, 50)
        self.button2.align(lv.ALIGN.CENTER, 0, 30)
        self.button2.set_style_bg_color(lv.color_hex(0x192A43), 0)
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
        self.button3.add_event_cb( self.open_station_page, lv.EVENT.CLICKED, None)
        self.create_station_page()

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

    def save_filter(self, event):
        selected_index = self.dropdown.get_selected()
        with open("selected_filter.json", "w") as file:
            json.dump({"filter": selected_index}, file)

        if self.on_filter_saved is not None:
            self.on_filter_saved()

        
    def create_station_page(self):

        # Load stops from local JSON file
        with open("stations.json", "r") as file:
            self.stations = json.load(file)

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

        # Restore previous selection
        try:
            with open("selected_station.json", "r") as file:
                saved = json.load(file)

            for i, station in enumerate(self.stations):
                if str(station["id"]) == str(saved["id"]):
                    self.station_dropdown.set_selected(i)
                    break
        except (OSError, ValueError, KeyError):
            pass

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

        # Hide until opened
        self.station_page.add_flag(lv.obj.FLAG.HIDDEN)
    
    def open_station_page(self, event):
        self.station_page.move_foreground()
        self.station_page.remove_flag(lv.obj.FLAG.HIDDEN)


    def close_station_page(self, event):
        self.station_page.add_flag(lv.obj.FLAG.HIDDEN)


    def save_station(self, event):

        index = self.station_dropdown.get_selected()

        selected = self.stations[index]

        with open("selected_station.json", "w") as file:
            json.dump(selected, file)

        self.close_station_page(event)

        if self.on_station_saved is not None:
            self.on_station_saved()
