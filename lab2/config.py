# config.py

import os

# Путь к папке с зашифрованными файлами
ENCRYPTED_FILES_DIR = os.path.join(os.getcwd(), 'encrypted_files')

# Путь к папке с открытыми файлами
DECRYPTED_FILES_DIR = os.path.join(os.getcwd(), 'decrypted_files')

# Путь к файлу лицензий
LICENSE_FILE = os.path.join(os.getcwd(), 'licenses.json')

# Секретный ключ для шифрования (в реальной системе храните безопасно!)
SECRET_KEY = b'6tJY1mDExQDibdcOVnnPlt12e4ZqmEu2prIELm6HKFY='