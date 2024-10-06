# controllers/user_controller.py

from controllers.auth_controller import AuthController
from models.certificate import Certificate
from utils.utils import check_password_requirements

class UserController:
    def __init__(self, user, use_certificate=False, usb_label='D:\\'):
        self.user = user
        self.use_certificate = use_certificate
        self.auth_controller = AuthController()
        if usb_label:
            self.certificate = Certificate(usb_label)
        else:
            self.certificate = None
        print(self.certificate)

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

        # Если используется сертификат, обновляем его на USB
        if self.use_certificate and self.certificate:
            user_data = {
                'username': self.user.username,
                'password': self.user.password,
                'min_length': self.user.min_length,
                'blocked': self.user.blocked,
                'use_certificate': self.user.use_certificate
            }
            if not self.certificate.save_certificate(user_data):
                return False, 'Failed to update certificate on USB drive.'
            return True, 'Password changed and updated on USB certificate.'
        
        # Обновление пользователя в списке auth_controller
        self.auth_controller.users[self.user.username] = self.user
        
        # Сохранение списка пользователей в файл
        self.auth_controller.save_users()

        return True, 'Password changed successfully.'

