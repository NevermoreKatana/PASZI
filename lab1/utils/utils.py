# utils/utils.py

import string
import re

def check_password_requirements(password, min_length, username):
    # Define character sets
    latin_letters = re.compile(r'[A-Za-z]')
    cyrillic_letters = re.compile(r'[А-Яа-яЁё]')
    arithmetic_symbols = set('+-*/=')

    requirements = {
        'min_length': len(password) >= min_length,
        'latin_letters': bool(latin_letters.search(password)),
        'cyrillic_letters': bool(cyrillic_letters.search(password)),
        'arithmetic_symbols': any(c in arithmetic_symbols for c in password),
        'no_consecutive_duplicates': not re.search(r'(.)\1', password),
        'not_reversed_username': password != username[::-1]
    }
    return requirements
