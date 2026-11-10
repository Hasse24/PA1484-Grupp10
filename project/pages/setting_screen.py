import lvgl as lv
import json

class SettingsPage:
    def __init__(self, parent, swedish_font=None, swedish_font_20=None, on_filter_saved=None):
        self.BG = 0x0B1423
        self.parent = parent
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
