# cli.py

import argparse
import sys
from typing import Optional
from password_generator import generate_password


def parse_arguments():
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Программа для шифрования и дешифрования файлов.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt', action='store_true', help='Режим шифрования файла.')
    group.add_argument('--decrypt', action='store_true', help='Режим дешифрования файла.')

    parser.add_argument('--input', '-i', type=str, required=True, help='Путь к входному файлу.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Путь к выходному файлу.')
    parser.add_argument('--password', '-p', type=str, help='Пароль для шифрования/дешифрования.')

    return parser.parse_args()


def get_password(provided_password: Optional[str]) -> str:
    """
    Возвращает предоставленный пароль или генерирует новый.
    """
    if provided_password:
        return provided_password
    else:
        print("Пароль не был предоставлен. Генерируется сложный пароль...")
        password = generate_password()
        print(f"Сгенерированный пароль: {password}")
        return password
