import customtkinter as ctk

from . import theme


class SettingsTab:
    """Owns the 'Settings' tab: header/footer/bank text, delay, and toggles."""

    def __init__(self, tab, config_manager, bold_font):
        self.tab = tab
        self.config_manager = config_manager
        self.bold_font = bold_font

        self.container = ctk.CTkFrame(tab, fg_color=theme.BG_COLOR, corner_radius=15)
        self.container.pack(fill="both", expand=True, padx=40, pady=20)

        if config_manager.load_error:
            self._build_load_error_banner(config_manager.load_error)

        self._build_fields()

    def _build_load_error_banner(self, error_message):
        banner = ctk.CTkFrame(self.container, fg_color=theme.WARNING_BTN, corner_radius=10)
        banner.pack(fill="x", padx=20, pady=(15, 0))
        ctk.CTkLabel(
            banner,
            text=(
                "⚠️ Your saved config.json couldn't be read, so defaults were "
                f"loaded instead ({error_message}). Re-save Settings below to "
                "write a fresh, valid config.json."
            ),
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=theme.TEXT_COLOR,
            wraplength=500,
            justify="left",
        ).pack(padx=15, pady=10, anchor="w")

    def _create_label(self, text):
        ctk.CTkLabel(
            self.container, text=text, font=self.bold_font, text_color=theme.TEXT_COLOR
        ).pack(anchor="w", padx=20, pady=(10, 2))

    def _apply_input_style(self, widget):
        widget.configure(
            fg_color=theme.FRAME_COLOR, text_color=theme.TEXT_COLOR,
            border_width=2, border_color=theme.PRIMARY_BTN, corner_radius=8
        )
        widget.pack(fill="x", padx=20)

    def _build_fields(self):
        settings = self.config_manager.settings

        self._create_label("⏱️ Auto-Send Delay (seconds):")
        self.delay_input = ctk.CTkEntry(self.container)
        self._apply_input_style(self.delay_input)
        self.delay_input.insert(0, str(settings.get("auto_send_delay", 2.0)))

        self._create_label("🛵 Default Ongkir (Rp):")
        self.ongkir_input = ctk.CTkEntry(self.container)
        self._apply_input_style(self.ongkir_input)
        self.ongkir_input.insert(0, str(settings.get("default_ongkir", 0)))

        self._create_label("🎀 Invoice Header:")
        self.header_input = ctk.CTkTextbox(self.container, height=60)
        self._apply_input_style(self.header_input)
        self.header_input.insert("1.0", settings.get("header", ""))

        self._create_label("💳 Bank Details:")
        self.bank_input = ctk.CTkTextbox(self.container, height=40)
        self._apply_input_style(self.bank_input)
        self.bank_input.insert("1.0", settings.get("bank_account", ""))

        self._create_label("🌸 Invoice Footer:")
        self.footer_input = ctk.CTkTextbox(self.container, height=60)
        self._apply_input_style(self.footer_input)
        self.footer_input.insert("1.0", settings.get("footer", ""))

        # Auto-press Enter is on by default; uncheck to require a manual
        # Enter press after WhatsApp opens instead.
        self.auto_press_enter_var = ctk.BooleanVar(value=settings.get("auto_press_enter", True))
        self._create_label("⌨️ Auto-press Enter after opening WhatsApp:")
        ctk.CTkCheckBox(
            self.container,
            text="Enable (sends automatically — uncheck to press Enter yourself instead)",
            variable=self.auto_press_enter_var,
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=theme.TEXT_COLOR,
            fg_color=theme.PRIMARY_BTN,
            hover_color=theme.PRIMARY_HOVER,
        ).pack(anchor="w", padx=20, pady=(2, 0))

        self.save_btn = ctk.CTkButton(
            self.container, text="💾 Save Settings", font=self.bold_font, text_color=theme.TEXT_COLOR,
            fg_color=theme.PRIMARY_BTN, hover_color=theme.PRIMARY_HOVER, corner_radius=20,
            command=self.save_settings, height=45
        )
        self.save_btn.pack(pady=25, padx=20, fill="x")

    def save_settings(self):
        try:
            delay_val = float(self.delay_input.get())
        except ValueError:
            delay_val = 2.0

        try:
            default_ongkir_val = int(self.ongkir_input.get())
        except ValueError:
            default_ongkir_val = 0

        new_config = {
            "header": self.header_input.get("1.0", "end-1c"),
            "footer": self.footer_input.get("1.0", "end-1c"),
            "bank_account": self.bank_input.get("1.0", "end-1c"),
            "auto_send_delay": delay_val,
            "default_ongkir": default_ongkir_val,
            "auto_press_enter": self.auto_press_enter_var.get(),
        }
        self.config_manager.save(new_config)
        self.config_manager.load_error = None
        self.save_btn.configure(text="✅ Saved Successfully!", fg_color=theme.WA_BTN)
        self.tab.after(2000, lambda: self.save_btn.configure(text="💾 Save Settings", fg_color=theme.PRIMARY_BTN))
