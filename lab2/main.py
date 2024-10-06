# main.py

import os
import sys
from drm_utils import DRMUtils
from license_manager import LicenseManager
from config import ENCRYPTED_FILES_DIR, DECRYPTED_FILES_DIR

def encrypt_files(drm, input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        drm.encrypt_file(input_path, output_path)
        print(f"Зашифрован {filename}")

def generate_license(license_manager):
    user_info = input("Введите информацию о пользователе: ")
    license_key = license_manager.generate_license_key(user_info)
    print(f"Сгенерирован лицензионный ключ: {license_key}")

def main():
    drm = DRMUtils()
    license_manager = LicenseManager()

    if len(sys.argv) < 2:
        print("Использование: python main.py [encrypt|generate_license]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "encrypt":
        if len(sys.argv) != 4:
            print("Использование: python main.py encrypt <input_dir> <output_dir>")
            sys.exit(1)
        input_dir = sys.argv[2]
        output_dir = sys.argv[3]
        encrypt_files(drm, input_dir, output_dir)
    elif command == "generate_license":
        generate_license(license_manager)
    else:
        print("Неизвестная команда.")

if __name__ == "__main__":
    main()
