import customtkinter as ctk

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
DISABLED_BTN = "#D3D3D3"
DISABLED_HOVER = "#C0C0C0"
WARNING_BTN = "#FFD27D"      # Soft amber, used for invalid-phone warnings


def apply_appearance():
    ctk.set_appearance_mode("Light")


def make_fonts():
    """Returns (custom_font, bold_font) for reuse across tabs."""
    custom_font = ctk.CTkFont(family="Helvetica", size=13)
    bold_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
    return custom_font, bold_font
