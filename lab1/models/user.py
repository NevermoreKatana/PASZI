# models/user.py

import hashlib
import json
import os

USER_FILE = 'data/users.json'

class User:
    def __init__(self, username, password='', min_length=8, blocked=False, use_certificate=False):
        self.username = username
        self.password = password  # hashed password
        self.min_length = min_length
        self.blocked = blocked
        self.use_certificate = use_certificate

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def load_users(cls):
        if not os.path.exists(USER_FILE):
            os.makedirs('data', exist_ok=True)
            # Создаем учетную запись администратора с хэшированным пустым паролем
            hashed_empty_password = cls.hash_password('')
            admin = cls('ADMIN', hashed_empty_password, 8, False, False)
            cls.save_users({'ADMIN': admin})
            return {'ADMIN': admin}
        else:
            with open(USER_FILE, 'r') as f:
                users_data = json.load(f)
            users = {}
            for username, data in users_data.items():
                users[username] = cls(
                    username,
                    data['password'],
                    data.get('min_length', 8),
                    data.get('blocked', False),
                    data.get('use_certificate', False)
                )
            return users

    @classmethod
    def save_users(cls, users):
        users_data = {}
        for username, user in users.items():
            users_data[username] = {
                'password': user.password,
                'min_length': user.min_length,
                'blocked': user.blocked,
                'use_certificate': user.use_certificate
            }
        with open(USER_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)

    def check_password(self, password):
        return self.password == self.hash_password(password)

    def set_password(self, new_password):
        self.password = self.hash_password(new_password)
