import threading
import time
import customtkinter as ctk
import pyperclip
from config import ConfigManager
from parser import InvoiceParser
from whatsapp import WhatsAppHandler

# 1. Switch to Light Mode by default
ctk.set_appearance_mode("Light")  

# Cute Color Palette
BG_COLOR = "#FFF0F5"         # Lavender Blush (Main Background)
FRAME_COLOR = "#FFFFFF"      # Pure White (Cards & Panels)
TEXT_COLOR = "#5C4033"       # Mocha Brown (Softer than black)
PRIMARY_BTN = "#FFB6C1"      # Light Pink
PRIMARY_HOVER = "#FF99A8"    # Slightly darker pink
WA_BTN = "#A8E6CF"           # Pastel Mint Green
WA_HOVER = "#88D4AB"         # Darker Mint
PURPLE_BTN = "#DDA0DD"       # Plum/Pastel Purple
PURPLE_HOVER = "#D8BFD8"     # Thistle

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✨ WA Invoice Generator ✨")
        self.geometry("900x650")
        self.configure(fg_color=BG_COLOR) # Set main background
        
        # Soft, rounded font
        self.custom_font = ctk.CTkFont(family="Helvetica", size=13)
        self.bold_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        
        self.config_manager = ConfigManager()
        
        # Style the Tabview to be cute
        self.tabview = ctk.CTkTabview(self, 
                                      fg_color=FRAME_COLOR, 
                                      segmented_button_fg_color=BG_COLOR,
                                      segmented_button_selected_color=PRIMARY_BTN,
                                      segmented_button_selected_hover_color=PRIMARY_HOVER,
                                      text_color=TEXT_COLOR)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.tab_gen = self.tabview.add("🎀 Generator")
        self.tab_set = self.tabview.add("⚙️ Settings")

        self.invoice_cards = [] 
        
        self.placeholder_text = (
            "Input the raw data in the format below 💖:\n\n"
            "Personal 40k\n"
            "Ayyash 78 ( 8 September +20k 08xxxxxxx)\n\n"
            "Couple 80k\n"
            "Raula 67 ( 3 July Pickup 08xxxxxxx)"
        )
        
        self._setup_generator_tab()
        self._setup_settings_tab()

    def _setup_generator_tab(self):
        self.tab_gen.grid_columnconfigure(0, weight=1)
        self.tab_gen.grid_columnconfigure(1, weight=1)
        self.tab_gen.grid_rowconfigure(0, weight=1)

        self.input_frame = ctk.CTkFrame(self.tab_gen, fg_color=BG_COLOR, corner_radius=15)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.input_frame, text="📝 Paste Raw Data Here:", font=self.bold_font, text_color=TEXT_COLOR).pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self.input_frame, fg_color=FRAME_COLOR, text_color=TEXT_COLOR, corner_radius=10, border_width=2, border_color=PRIMARY_BTN)
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.textbox.insert("1.0", self.placeholder_text)
        self.textbox.configure(text_color="#A9A9A9") # Gray placeholder
        
        self.textbox.bind("<FocusIn>", self._clear_placeholder)
        self.textbox.bind("<FocusOut>", self._add_placeholder)
        
        self.action_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.action_frame.pack(pady=10, padx=10, fill="x")
        
        # Bubbly Buttons (corner_radius=20)
        ctk.CTkButton(self.action_frame, text="✨ Generate", font=self.bold_font, text_color=TEXT_COLOR, 
                      fg_color=PRIMARY_BTN, hover_color=PRIMARY_HOVER, corner_radius=20, 
                      command=self.process_data, height=45).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.send_all_btn = ctk.CTkButton(self.action_frame, text="💌 Auto-Send All", font=self.bold_font, text_color=TEXT_COLOR, 
                                          command=self.send_all_messages, height=45, corner_radius=20, 
                                          state="disabled", fg_color="#D3D3D3", hover_color="#C0C0C0")
        self.send_all_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.output_frame = ctk.CTkScrollableFrame(self.tab_gen, fg_color=BG_COLOR, corner_radius=15)
        self.output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.output_frame, text="💝 Generated Invoices:", font=self.bold_font, text_color=TEXT_COLOR).pack(pady=10)

    def _clear_placeholder(self, event):
        if self.textbox.get("1.0", "end-1c") == self.placeholder_text:
            self.textbox.delete("1.0", "end")
            self.textbox.configure(text_color=TEXT_COLOR)

    def _add_placeholder(self, event):
        if not self.textbox.get("1.0", "end-1c").strip():
            self.textbox.insert("1.0", self.placeholder_text)
            self.textbox.configure(text_color="#A9A9A9")

    def _setup_settings_tab(self):
        settings_container = ctk.CTkFrame(self.tab_set, fg_color=BG_COLOR, corner_radius=15)
        settings_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        settings = self.config_manager.settings

        # Inputs styling wrapper
        def create_label(text):
            ctk.CTkLabel(settings_container, text=text, font=self.bold_font, text_color=TEXT_COLOR).pack(anchor="w", padx=20, pady=(10, 2))
            
        def apply_input_style(widget):
            widget.configure(fg_color=FRAME_COLOR, text_color=TEXT_COLOR, border_width=2, border_color=PRIMARY_BTN, corner_radius=8)
            widget.pack(fill="x", padx=20)

        create_label("⏱️ Auto-Send Delay (seconds):")
        self.delay_input = ctk.CTkEntry(settings_container)
        apply_input_style(self.delay_input)
        self.delay_input.insert(0, str(settings.get("auto_send_delay", 2.0)))

        create_label("🛵 Default Ongkir (Rp):")
        self.ongkir_input = ctk.CTkEntry(settings_container)
        apply_input_style(self.ongkir_input)
        self.ongkir_input.insert(0, str(settings.get("default_ongkir", 0)))

        create_label("🎀 Invoice Header:")
        self.header_input = ctk.CTkTextbox(settings_container, height=60)
        apply_input_style(self.header_input)
        self.header_input.insert("1.0", settings.get("header", ""))

        create_label("💳 Bank Details:")
        self.bank_input = ctk.CTkTextbox(settings_container, height=40)
        apply_input_style(self.bank_input)
        self.bank_input.insert("1.0", settings.get("bank_account", ""))

        create_label("🌸 Invoice Footer:")
        self.footer_input = ctk.CTkTextbox(settings_container, height=60)
        apply_input_style(self.footer_input)
        self.footer_input.insert("1.0", settings.get("footer", ""))

        self.save_btn = ctk.CTkButton(settings_container, text="💾 Save Settings", font=self.bold_font, text_color=TEXT_COLOR,
                                      fg_color=PRIMARY_BTN, hover_color=PRIMARY_HOVER, corner_radius=20,
                                      command=self.save_settings, height=45)
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
            "default_ongkir": default_ongkir_val
        }
        self.config_manager.save(new_config)
        self.save_btn.configure(text="✅ Saved Successfully!", fg_color=WA_BTN)
        self.after(2000, lambda: self.save_btn.configure(text="💾 Save Settings", fg_color=PRIMARY_BTN))

    def process_data(self):
        raw_text = self.textbox.get("1.0", "end-1c")
        if not raw_text.strip() or raw_text.strip() == self.placeholder_text.strip():
            return

        for item in self.invoice_cards:
            item["frame"].destroy()
        self.invoice_cards.clear()

        parsed_invoices = InvoiceParser.parse(raw_text, self.config_manager.settings)
        
        has_phone = False
        for inv in parsed_invoices:
            self._create_card(inv["name"], inv["text"], inv["phone"])
            if inv["phone"]:
                has_phone = True
                
        if has_phone:
            self.send_all_btn.configure(state="normal", fg_color=PURPLE_BTN, hover_color=PURPLE_HOVER)
        else:
            self.send_all_btn.configure(state="disabled", fg_color="#D3D3D3", hover_color="#C0C0C0")

    def _create_card(self, name, invoice_text, phone):
        # White bubbles for invoice cards
        card = ctk.CTkFrame(self.output_frame, fg_color=FRAME_COLOR, corner_radius=15, border_width=1, border_color=PRIMARY_BTN)
        card.pack(fill="x", pady=8, padx=5)
        
        item_data = {
            "frame": card,
            "btn": None,
            "phone": phone,
            "text": invoice_text,
            "sent": False
        }
        self.invoice_cards.append(item_data)
        
        display_title = f"👤 {name} ({phone})" if phone else f"👤 {name}"
        ctk.CTkLabel(card, text=display_title, font=self.bold_font, text_color=TEXT_COLOR).pack(anchor="w", padx=15, pady=(10, 0))
        
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        # Small pill buttons
        ctk.CTkButton(btn_frame, text="📋 Copy", width=80, corner_radius=15, 
                      fg_color="#F5F5F5", hover_color="#E0E0E0", text_color=TEXT_COLOR,
                      command=lambda: pyperclip.copy(invoice_text)).pack(side="left", padx=5)
        
        btn_text = "🚀 Auto-Send" if phone else "💬 Open in WA"
        wa_btn = ctk.CTkButton(btn_frame, text=btn_text, width=100, corner_radius=15,
                               fg_color=WA_BTN, hover_color=WA_HOVER, text_color=TEXT_COLOR, font=self.bold_font,
                               command=lambda: self.handle_single_send(item_data))
        wa_btn.pack(side="left", padx=5)
        
        item_data["btn"] = wa_btn

    def handle_single_send(self, item):
        if item["sent"]: return
        
        delay = self.config_manager.settings.get("auto_send_delay", 2.0)
        item["btn"].configure(state="disabled", text="⏳ Sending...")
        
        def on_complete():
            self.after(0, self.mark_as_sent, item)
            
        WhatsAppHandler.send_single(item["phone"], item["text"], delay, on_complete)

    def send_all_messages(self):
        items_to_send = [item for item in self.invoice_cards if item["phone"] and not item["sent"]]
        if not items_to_send:
            return
            
        self.send_all_btn.configure(state="disabled", text="⏳ Sending All...")
        delay = self.config_manager.settings.get("auto_send_delay", 2.0)
        
        def worker():
            for item in items_to_send:
                self.after(0, lambda i=item: i["btn"].configure(state="disabled", text="⏳ Sending..."))
                WhatsAppHandler.execute_send(item["phone"], item["text"], delay)
                self.after(0, self.mark_as_sent, item)
                time.sleep(1.5)
                
            self.after(0, lambda: self.send_all_btn.configure(state="disabled", text="✅ All Sent!", fg_color="#D3D3D3"))
            
        threading.Thread(target=worker, daemon=True).start()

    def mark_as_sent(self, item):
        item["sent"] = True
        item["btn"].configure(text="✅ Sent!", fg_color="#D3D3D3", hover_color="#D3D3D3", text_color="#808080", state="disabled")