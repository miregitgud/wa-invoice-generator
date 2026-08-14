# ✨ WA Invoice Generator ✨

A small desktop app that turns quick, shorthand order notes into formatted
Indonesian-language invoices and sends them straight to customers on
WhatsApp.

Paste in a batch of orders, hit Generate, and get one invoice card per
customer — each with a Copy button and a one-click "send to WhatsApp"
button (with optional auto-send).

## Features

- Parses shorthand order text into full invoices (date, item, qty,
  subtotal, ongkir, total, bank details)
- Per-category pricing — set a price once, apply it to every order
  underneath
- Auto-detects Indonesian phone numbers and normalizes them to the
  `62...` format WhatsApp expects
- Flags phone numbers that don't look valid instead of silently
  mis-sending
- Pickup orders (no delivery) are handled automatically — ongkir zeroes out
- One-click "Open in WhatsApp" per customer, or "Auto-Send All" to go
  through the whole batch
- Optional auto-press-Enter after WhatsApp opens (on by default — toggle
  off in Settings if you'd rather press Enter yourself)
- Configurable header, footer, bank account, default ongkir, and send
  delay — saved to `config.json`

## Requirements

- Python 3.10+
- WhatsApp Desktop installed (the app opens `whatsapp://` links)
- Dependencies in `requirements.txt`:
  ```
  customtkinter>=5.2.2
  pyperclip>=1.8.2
  pyautogui>=0.9.54
  pyinstaller>=6.22.0
  ```

## Setup

```bash
pip install -r requirements.txt
python main.py
```

On first run, a `config.json` is created next to the app with sensible
defaults — edit it directly or use the in-app Settings tab.

## Input format

One line per order. A line ending in a price like `40k` sets the current
category — every order line under it uses that price until the next
category line:

```
Personal 40k
Ayyash 78 ( 8 September +20k 08123456789)

Couple 80k
Raula 67 ( 3 July Pickup 08987654321)
```

Each order line can include, in any combination:

| Piece | Example | Notes |
|---|---|---|
| Customer name | `Ayyash` | Whatever text is left after everything else is stripped out |
| Quantity | `78` | Defaults to `1` if no number is present |
| Phone number | `08123456789` or `628123456789` | Normalized to `62...`; auto-detected in WhatsApp's format |
| Extra delivery fee (ongkir) | `+20k` (Rp 20,000) or `+20000` | Overrides the default ongkir from Settings for that order |
| Note / delivery date | `(8 September)` | Anything in parentheses; shown as "Tanggal Pengiriman" |
| Pickup | `(Pickup)` or `(3 July Pickup)` | Zeroes out ongkir and marks the order as pickup |

The generated invoice looks like:

```
<your configured header>
Tanggal: 14 Agustus 2026
Nama Pemesan: Ayyash
Tanggal Pengiriman:  8 September
Rincian Harga:
• Item: Personal
• Qty: 78
• Subtotal: Rp. 3.120.000
• Ongkir: Rp. 20.000
Total: Rp. 3.140.000

Pembayaran
<your configured bank account>
<your configured footer>
```

## Settings

Available in the app's ⚙️ Settings tab, saved to `config.json`:

- **Auto-Send Delay** — seconds to wait after WhatsApp opens before
  auto-pressing Enter
- **Default Ongkir** — delivery fee used when an order doesn't specify
  its own `+Nk`
- **Invoice Header / Footer** — the greeting and closing message wrapped
  around every invoice
- **Bank Details** — payment info shown on every invoice
- **Auto-press Enter** — on by default; when enabled, the app presses
  Enter for you after opening WhatsApp so the message sends without
  further action. Turn this off if you'd rather review each message
  before pressing Enter yourself.

## A note on auto-send

Auto-press-Enter sends a real keystroke to whatever window has focus
after the configured delay. If WhatsApp Desktop is slow to open or loses
focus, that keystroke can land somewhere else. If you hit that, either
increase the Auto-Send Delay or turn Auto-press Enter off in Settings.

Only phone numbers that pass validation (`62` + 8xx + a plausible number
of digits) are eligible for auto-send — anything that doesn't match falls
back to a manual "Open in WhatsApp" button instead.

## Project structure

```
main.py              # Entry point
config.py            # Loads/saves config.json
parser.py            # Turns raw order text into invoice data
whatsapp.py          # Opens WhatsApp and (optionally) sends
ui/
  app.py             # Root window, composes tabs
  generator_tab.py   # Input box, generate, send-all
  settings_tab.py    # Settings form
  invoice_card.py     # Single invoice result card
  theme.py           # Shared colors/fonts
```

## Building a standalone executable

```bash
pyinstaller main.spec
```

Output goes to `dist/`. `config.json` is read from next to the built
executable, so it can be edited without rebuilding.