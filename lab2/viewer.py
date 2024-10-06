# viewer.py

import os
import sys
from drm_utils import DRMUtils
from license_manager import LicenseManager
from config import ENCRYPTED_FILES_DIR, DECRYPTED_FILES_DIR

class Viewer:
    def __init__(self, license_key):
        self.drm = DRMUtils()
        self.license_manager = LicenseManager()
        self.license_key = license_key

    def view_file(self, filename):
        is_valid, message = self.license_manager.validate_license_key(self.license_key)
        if not is_valid:
            print(f"Ошибка лицензии: {message}")
            return

        encrypted_path = os.path.join(ENCRYPTED_FILES_DIR, filename)
        print(encrypted_path)
        decrypted_path = os.path.join(DECRYPTED_FILES_DIR, filename)

        if not os.path.exists(encrypted_path):
            print("Файл не найден.")
            return

        self.drm.decrypt_file(encrypted_path, decrypted_path)
        self.open_file(decrypted_path)

    def open_file(self, file_path):
        if sys.platform.startswith('darwin'):
            os.system(f'open "{file_path}"')
        elif os.name == 'nt':
            os.startfile(file_path)
        elif os.name == 'posix':
            os.system(f'xdg-open "{file_path}"')
        else:
            print("Неизвестная операционная система. Не могу открыть файл.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python viewer.py <license_key> <filename>")
        sys.exit(1)
    license_key = sys.argv[1]
    filename = sys.argv[2]
    viewer = Viewer(license_key)
    viewer.view_file(filename)
