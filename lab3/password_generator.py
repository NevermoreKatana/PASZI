# password_generator.py

import string
import random
import getpass


def get_username() -> str:
    """
    Получает имя пользователя текущей системы.
    """
    try:
        return getpass.getuser()
    except Exception:
        return "user"


def generate_password(length: int = 16) -> str:
    """
    Генерирует сложный пароль, соответствующий требованиям.
    """
    username = get_username()
    reversed_username = username[::-1]

    # Наборы символов
    latin_lower = string.ascii_lowercase
    latin_upper = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation
    arithmetic_ops = '+-*/='
    # Кириллические буквы (А-я)
    cyrillic_letters = ''.join([chr(code) for code in range(0x0410, 0x044F + 1)])

    all_chars = latin_lower + latin_upper + digits + punctuation + arithmetic_ops + cyrillic_letters

    if len(all_chars) < length:
        raise ValueError("Недостаточно уникальных символов для генерации пароля заданной длины.")

    while True:
        # Генерация пароля без повторяющихся символов
        password = ''.join(random.sample(all_chars, length))

        # Проверка наличия хотя бы одного символа из каждой категории
        if (any(c in latin_lower for c in password) and
            any(c in latin_upper for c in password) and
            any(c in digits for c in password) and
            any(c in punctuation for c in password) and
            any(c in cyrillic_letters for c in password) and
            any(c in arithmetic_ops for c in password)):

            # Проверка отсутствия подряд одинаковых символов
            if all(password[i] != password[i + 1] for i in range(len(password) - 1)):

                # Проверка, что пароль не совпадает с перевернутым именем пользователя
                if password != reversed_username:
                    return password
