import time
import threading

import customtkinter as ctk

from parser import InvoiceParser
from whatsapp import WhatsAppHandler
from . import theme
from .invoice_card import InvoiceCard

PLACEHOLDER_TEXT = (
    "Input the raw data in the format below 💖:\n\n"
    "Personal 40k\n"
    "Ayyash 78 ( 8 September +20k 08xxxxxxx)\n\n"
    "Couple 80k\n"
    "Raula 67 ( 3 July Pickup 08xxxxxxx)"
)


class GeneratorTab:
    """Owns the 'Generator' tab: raw-data input, and the generated invoice cards."""

    def __init__(self, tab, config_manager, bold_font):
        self.tab = tab
        self.config_manager = config_manager
        self.bold_font = bold_font
        self.cards = []

        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        self._build_input_panel()
        self._build_output_panel()

    def _build_input_panel(self):
        self.input_frame = ctk.CTkFrame(self.tab, fg_color=theme.BG_COLOR, corner_radius=15)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.input_frame, text="📝 Paste Raw Data Here:",
            font=self.bold_font, text_color=theme.TEXT_COLOR
        ).pack(pady=10)

        self.textbox = ctk.CTkTextbox(
            self.input_frame, fg_color=theme.FRAME_COLOR, text_color=theme.TEXT_COLOR,
            corner_radius=10, border_width=2, border_color=theme.PRIMARY_BTN
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.textbox.insert("1.0", PLACEHOLDER_TEXT)
        self.textbox.configure(text_color="#A9A9A9")

        self.textbox.bind("<FocusIn>", self._clear_placeholder)
        self.textbox.bind("<FocusOut>", self._add_placeholder)

        self.action_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.action_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkButton(
            self.action_frame, text="✨ Generate", font=self.bold_font, text_color=theme.TEXT_COLOR,
            fg_color=theme.PRIMARY_BTN, hover_color=theme.PRIMARY_HOVER, corner_radius=20,
            command=self.process_data, height=45
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.send_all_btn = ctk.CTkButton(
            self.action_frame, text="💌 Auto-Send All", font=self.bold_font, text_color=theme.TEXT_COLOR,
            command=self.send_all_messages, height=45, corner_radius=20,
            state="disabled", fg_color=theme.DISABLED_BTN, hover_color=theme.DISABLED_HOVER
        )
        self.send_all_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

    def _build_output_panel(self):
        self.output_frame = ctk.CTkScrollableFrame(self.tab, fg_color=theme.BG_COLOR, corner_radius=15)
        self.output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(
            self.output_frame, text="💝 Generated Invoices:",
            font=self.bold_font, text_color=theme.TEXT_COLOR
        ).pack(pady=10)

    def _clear_placeholder(self, event):
        if self.textbox.get("1.0", "end-1c") == PLACEHOLDER_TEXT:
            self.textbox.delete("1.0", "end")
            self.textbox.configure(text_color=theme.TEXT_COLOR)

    def _add_placeholder(self, event):
        if not self.textbox.get("1.0", "end-1c").strip():
            self.textbox.insert("1.0", PLACEHOLDER_TEXT)
            self.textbox.configure(text_color="#A9A9A9")

    def process_data(self):
        raw_text = self.textbox.get("1.0", "end-1c")
        if not raw_text.strip() or raw_text.strip() == PLACEHOLDER_TEXT.strip():
            return

        for card in self.cards:
            card.destroy()
        self.cards.clear()

        parsed_invoices = InvoiceParser.parse(raw_text, self.config_manager.settings)

        has_sendable_phone = False
        for inv in parsed_invoices:
            card = InvoiceCard(
                self.output_frame, inv["name"], inv["text"], inv["phone"],
                inv.get("phone_valid", bool(inv["phone"])), self.bold_font,
                on_send=self.handle_single_send
            )
            self.cards.append(card)
            if inv["phone"]:
                has_sendable_phone = True

        if has_sendable_phone:
            self.send_all_btn.configure(state="normal", fg_color=theme.PURPLE_BTN, hover_color=theme.PURPLE_HOVER)
        else:
            self.send_all_btn.configure(state="disabled", fg_color=theme.DISABLED_BTN, hover_color=theme.DISABLED_HOVER)

    def handle_single_send(self, card):
        delay = self.config_manager.settings.get("auto_send_delay", 2.0)
        auto_press_enter = self.config_manager.settings.get("auto_press_enter", False)
        card.mark_sending()

        def on_complete():
            self.tab.after(0, card.mark_sent)

        WhatsAppHandler.send_single(card.phone, card.text, delay, auto_press_enter, on_complete)

    def send_all_messages(self):
        items_to_send = [card for card in self.cards if card.phone and not card.sent]
        if not items_to_send:
            return

        self.send_all_btn.configure(state="disabled", text="⏳ Sending All...")
        delay = self.config_manager.settings.get("auto_send_delay", 2.0)
        auto_press_enter = self.config_manager.settings.get("auto_press_enter", False)

        def worker():
            for card in items_to_send:
                self.tab.after(0, card.mark_sending)
                WhatsAppHandler.execute_send(card.phone, card.text, delay, auto_press_enter)
                self.tab.after(0, card.mark_sent)
                time.sleep(1.5)

            self.tab.after(0, lambda: self.send_all_btn.configure(
                state="disabled", text="✅ All Sent!", fg_color=theme.DISABLED_BTN
            ))

        threading.Thread(target=worker, daemon=True).start()
