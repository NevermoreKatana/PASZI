# drm_utils.py

from cryptography.fernet import Fernet
from config import SECRET_KEY

class DRMUtils:
    def __init__(self):
        self.cipher = Fernet(SECRET_KEY)

    def encrypt_file(self, file_path, output_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = self.cipher.encrypt(data)
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

    def decrypt_file(self, file_path, output_path):
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.cipher.decrypt(encrypted_data)
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
