# controllers/admin_controller.py

from controllers.auth_controller import AuthController
from utils.utils import check_password_requirements
from models.user import User

class AdminController:
    def __init__(self, user):
        self.user = user
        self.auth_controller = AuthController()

    def change_password(self, old_password, new_password):
        if not self.user.check_password(old_password):
            return False, 'Incorrect old password.'

        # Check password requirements
        requirements = check_password_requirements(new_password, self.user.min_length, self.user.username)
        if not all(requirements.values()):
            messages = []
            if not requirements['min_length']:
                messages.append(f'- At least {self.user.min_length} characters long.')
            if not requirements['latin_letters']:
                messages.append('- Contains at least one Latin letter.')
            if not requirements['cyrillic_letters']:
                messages.append('- Contains at least one Cyrillic letter.')
            if not requirements['arithmetic_symbols']:
                messages.append('- Contains at least one arithmetic symbol (+, -, *, /, =).')
            if not requirements['no_consecutive_duplicates']:
                messages.append('- Does not contain consecutive identical characters.')
            if not requirements['not_reversed_username']:
                messages.append('- Password should not be the reversed username.')
            return False, 'Password does not meet requirements:\n' + '\n'.join(messages)

        # Set the new password
        self.user.set_password(new_password)

        # Сохранение обновленного пользователя в списке пользователей
        self.auth_controller.users[self.user.username] = self.user

        # Сохранение списка пользователей в файл
        self.auth_controller.save_users()

        return True, 'Password changed successfully.'


    def add_user(self, username, min_length, use_certificate):
        if username in self.auth_controller.users:
            return False, 'User already exists.'

        # Hash the empty password
        hashed_empty_password = User.hash_password('')

        new_user = User(username, hashed_empty_password, min_length, False, use_certificate)
        self.auth_controller.users[username] = new_user
        self.auth_controller.save_users()
        return True, f'User {username} added.'

    def block_user(self, username):
        if username not in self.auth_controller.users:
            return False, 'User not found.'
        self.auth_controller.users[username].blocked = True
        self.auth_controller.save_users()
        return True, f'User {username} has been blocked.'

    def set_min_length(self, username, min_length):
        if username not in self.auth_controller.users:
            return False, 'User not found.'
        self.auth_controller.users[username].min_length = min_length
        self.auth_controller.save_users()
        return True, f'Minimum password length for {username} set to {min_length}.'

    def set_usb_label(self, label):
        self.auth_controller.set_usb_label(label)
        return True, f'USB drive label set to {label}.'
