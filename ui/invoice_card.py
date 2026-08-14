import customtkinter as ctk
import pyperclip

from . import theme


class InvoiceCard:
    """
    A single invoice result: the white bubble showing the customer name,
    plus Copy / Send buttons. Owns its own tkinter widgets and small bit
    of state (sent / not sent).
    """

    def __init__(self, parent, name, invoice_text, phone, phone_valid, bold_font, on_send):
        self.phone = phone
        self.text = invoice_text
        self.sent = False
        self.on_send = on_send

        border_color = theme.PRIMARY_BTN if phone_valid else theme.WARNING_BTN

        self.frame = ctk.CTkFrame(
            parent, fg_color=theme.FRAME_COLOR, corner_radius=15,
            border_width=1, border_color=border_color
        )
        self.frame.pack(fill="x", pady=8, padx=5)

        if phone and not phone_valid:
            display_title = f"⚠️ {name} (invalid number: {phone or '—'})"
        elif phone:
            display_title = f"👤 {name} ({phone})"
        else:
            display_title = f"👤 {name}"

        ctk.CTkLabel(
            self.frame, text=display_title, font=bold_font, text_color=theme.TEXT_COLOR
        ).pack(anchor="w", padx=15, pady=(10, 0))

        if phone and not phone_valid:
            ctk.CTkLabel(
                self.frame,
                text="Number doesn't look valid — auto-send is disabled for this one.",
                font=ctk.CTkFont(family="Helvetica", size=11),
                text_color="#A0522D",
            ).pack(anchor="w", padx=15, pady=(0, 4))

        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame, text="📋 Copy", width=80, corner_radius=15,
            fg_color="#F5F5F5", hover_color="#E0E0E0", text_color=theme.TEXT_COLOR,
            command=lambda: pyperclip.copy(invoice_text)
        ).pack(side="left", padx=5)

        can_auto_send = bool(phone) and phone_valid
        btn_text = "🚀 Auto-Send" if can_auto_send else "💬 Open in WA"
        self.btn = ctk.CTkButton(
            btn_frame, text=btn_text, width=100, corner_radius=15,
            fg_color=theme.WA_BTN, hover_color=theme.WA_HOVER,
            text_color=theme.TEXT_COLOR, font=bold_font,
            command=self._handle_click
        )
        self.btn.pack(side="left", padx=5)

    def _handle_click(self):
        if not self.sent:
            self.on_send(self)

    def mark_sending(self):
        self.btn.configure(state="disabled", text="⏳ Sending...")

    def mark_sent(self):
        self.sent = True
        self.btn.configure(
            text="✅ Sent!", fg_color=theme.DISABLED_BTN,
            hover_color=theme.DISABLED_BTN, text_color="#808080", state="disabled"
        )

    def destroy(self):
        self.frame.destroy()
