import json
import os
import sys

class ConfigManager:
    def __init__(self):
        self.config_path = self._get_config_path()
        self.settings = self.load()

    def _get_config_path(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, 'config.json')

    def load(self):
        default_config = {
            "header": "Hai! Terima kasih sudah melakukan pemesanan 🫶🏻\nBerikut aku kirimkan invoice untuk pesanannya yaa ✨",
            "footer": "Kirim bukti transfer yaa 💛\nTerima kasih sudah order! 🫶🏻",
            "bank_account": "BCA: 7401855576 a/n Raula Saffanah Putri",
            "auto_send_delay": 2.0,
            "default_ongkir": 0  # Added default ongkir
        }

        if not os.path.exists(self.config_path):
            self.save(default_config)
            return default_config
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default_config

    def save(self, config_dict):
        self.settings = config_dict
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)