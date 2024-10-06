# license_manager.py

import json
import uuid
import hashlib
import platform
import socket
from datetime import datetime, timedelta
from config import LICENSE_FILE

class LicenseManager:
    def __init__(self):
        self.licenses = self.load_licenses()

    def load_licenses(self):
        try:
            with open(LICENSE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_licenses(self):
        with open(LICENSE_FILE, 'w') as f:
            json.dump(self.licenses, f, indent=4)

    def generate_license_key(self, user_info, validity_days=30):
        license_id = str(uuid.uuid4())
        expiration_date = (datetime.now() + timedelta(days=validity_days)).isoformat()
        system_info = self.get_system_info()
        license_data = {
            'license_id': license_id,
            'user_info': user_info,
            'system_info': system_info,
            'expiration_date': expiration_date
        }
        license_key = self.create_license_key(license_data)
        self.licenses[license_key] = license_data
        self.save_licenses()
        return license_key

    def create_license_key(self, license_data):
        data_string = f"{license_data['license_id']}{license_data['user_info']}{license_data['system_info']}{license_data['expiration_date']}"
        return hashlib.sha256(data_string.encode()).hexdigest()

    def validate_license_key(self, license_key):
        license_data = self.licenses.get(license_key)
        print(license_key)
        if not license_data:
            return False, "Лицензия не найдена."

        if datetime.fromisoformat(license_data['expiration_date']) < datetime.now():
            return False, "Лицензия истекла."

        current_system_info = self.get_system_info()
        if license_data['system_info'] != current_system_info:
            return False, "Лицензия привязана к другому устройству."

        return True, "Лицензия действительна."

    def get_system_info(self):
        hostname = socket.gethostname()
        os_info = platform.platform()
        return hashlib.sha256(f"{hostname}{os_info}".encode()).hexdigest()
