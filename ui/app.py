import customtkinter as ctk

from config import ConfigManager
from . import theme
from .generator_tab import GeneratorTab
from .settings_tab import SettingsTab

theme.apply_appearance()


class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✨ WA Invoice Generator ✨")
        self.geometry("900x650")
        self.configure(fg_color=theme.BG_COLOR)

        self.custom_font, self.bold_font = theme.make_fonts()

        self.config_manager = ConfigManager()

        self.tabview = ctk.CTkTabview(
            self,
            fg_color=theme.FRAME_COLOR,
            segmented_button_fg_color=theme.BG_COLOR,
            segmented_button_selected_color=theme.PRIMARY_BTN,
            segmented_button_selected_hover_color=theme.PRIMARY_HOVER,
            text_color=theme.TEXT_COLOR,
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        tab_gen = self.tabview.add("🎀 Generator")
        tab_set = self.tabview.add("⚙️ Settings")

        self.generator_tab = GeneratorTab(tab_gen, self.config_manager, self.bold_font)
        self.settings_tab = SettingsTab(tab_set, self.config_manager, self.bold_font)
