# crypto_utils.py

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Генерирует ключ из пароля и соли с использованием PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 бит для AES-256
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    """
    Шифрует файл с использованием AES-GCM.
    """
    salt = os.urandom(16)
    key = derive_key(password, salt)
    nonce = os.urandom(12)  # Для AES GCM

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_path, 'rb') as f:
        data = f.read()

    ciphertext = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag

    with open(output_path, 'wb') as f:
        f.write(salt + nonce + tag + ciphertext)


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    """
    Дешифрует файл, зашифрованный с использованием AES-GCM.
    """
    with open(input_path, 'rb') as f:
        file_data = f.read()

    salt = file_data[:16]
    nonce = file_data[16:28]
    tag = file_data[28:44]
    ciphertext = file_data[44:]

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception:
        raise ValueError("Ошибка дешифрования. Возможно, неверный пароль или поврежденный файл.")

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
