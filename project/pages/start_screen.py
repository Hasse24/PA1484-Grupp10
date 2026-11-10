
import lvgl as lv

class HomePage:
    def __init__(self, parent):
        self.BG = 0x0B1423
        import fs_driver

        self.font_fs = lv.fs_drv_t()
        fs_driver.fs_register(self.font_fs, "S")

        self.swedish_font_20 = lv.binfont_create("S:montserrat_20_sv.bin")
        if self.swedish_font_20 is None:
            raise RuntimeError("Kunde inte ladda svenska 20-fonten")
        self.swedish_font = lv.binfont_create("S:montserrat_30_sv.bin")

        if any(font is None for font in (
            self.swedish_font,
        )):
            raise RuntimeError("Kunde inte ladda svenska fonterna")

        parent.set_style_bg_color(lv.color_hex(self.BG), 0)
        parent.set_style_bg_opa(lv.OPA.COVER, 0)

        # Rubriken
        self.title = lv.label(parent)
        self.title.set_text("TrafficAPP v2.0\n-\nGroup 10")
        self.title.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.title.set_style_text_font(self.swedish_font, 0)
        self.title.align(lv.ALIGN.CENTER, 0, -60)

        # Membz
        self.members = lv.label(parent)
        self.members.set_text(
            "Hasan Suleiman - Pontus Nordenfors\n"
            "Ali Agha - Wassim Akkkash - Hazem Alesa\n"
        )
        self.members.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.members.set_style_text_font(lv.font_montserrat_16, 0)
        self.members.align(lv.ALIGN.CENTER, 0, 70)

