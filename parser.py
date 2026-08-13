import re
from datetime import datetime

class InvoiceParser:
    @staticmethod
    def get_indonesian_date():
        months = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        today = datetime.now()
        return f"{today.day} {months[today.month]} {today.year}"

    @staticmethod
    def parse(raw_text, config):
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        date_today = InvoiceParser.get_indonesian_date()
        
        current_item = ""
        current_price = 0
        parsed_data = []
        
        # Load default ongkir from config
        default_ongkir_config = int(config.get("default_ongkir", 0))
        
        for line in lines:
            # 1. Category Header
            match_category = re.match(r'(.*?)\s+(\d+)k', line.lower())
            if match_category:
                current_item = match_category.group(1).title()
                current_price = int(match_category.group(2)) * 1000
                continue
            
            # 2. Phone Number
            phone = ""
            phone_match = re.search(r'(\b08\d{8,11}\b|\b628\d{8,11}\b)', line)
            if phone_match:
                phone = phone_match.group(1)
                line = line.replace(phone, "").strip()
                if phone.startswith("08"):
                    phone = "62" + phone[1:]

            # 3. Ongkir Logic
            ongkir_val = default_ongkir_config # Start with default
            
            ongkir_match = re.search(r'\+(\d+)k|\+(\d+)', line.lower())
            if ongkir_match:
                matched_num = ongkir_match.group(1) or ongkir_match.group(2)
                val = int(matched_num)
                ongkir_val = val * 1000 if val < 1000 else val # Override with specific
                line = re.sub(r'\+\d+k?', '', line, flags=re.IGNORECASE).strip()

            # 4. Note / Date
            note = "-"
            note_match = re.search(r'\((.*?)\)', line)
            if note_match:
                note = note_match.group(1)
                line = line.replace(f"({note})", "").strip()
                
            # 5. Quantity
            qty = 1
            qty_match = re.search(r'\b(\d+)\b', line)
            if qty_match:
                qty = int(qty_match.group(1))
                line = line.replace(qty_match.group(1), "").strip()
                
            name = line.title().strip()
            
            # Delivery Date & Pickup Override
            if "pickup" in note.lower():
                ongkir_val = 0
                ongkir_display = "0 (Pickup)"
                delivery_date = "(Pickup)"
            else:
                ongkir_display = f"{ongkir_val:,}".replace(',', '.') if ongkir_val > 0 else "-"
                delivery_date = note.title() if note != "-" else "-"

            # Math & Formatting
            subtotal = qty * current_price
            total = subtotal + ongkir_val
            
            subtotal_str = f"{subtotal:,}".replace(',', '.')
            total_str = f"{total:,}".replace(',', '.')

            # 6. Apply Template
            invoice_text = f"""{config.get('header', '')}
Tanggal: {date_today}
Nama Pemesan: {name}
Tanggal Pengiriman: {delivery_date}
Rincian Harga:
• Item: {current_item}
• Qty: {qty}
• Subtotal: Rp. {subtotal_str}
• Ongkir: Rp. {ongkir_display}
Total: Rp. {total_str}

Pembayaran
{config.get('bank_account', '')}
{config.get('footer', '')}"""

            parsed_data.append({
                "name": name,
                "phone": phone,
                "text": invoice_text
            })
            
        return parsed_data