    # controllers/auth_controller.py

from models.user import User
from models.certificate import Certificate
from utils.signature import check_computer_signature

class AuthController:
    def __init__(self):
        self.users = User.load_users()
        self.certificate = None
        self.attempts = 0

    def set_usb_label(self, label):
        self.certificate = Certificate(label)

    def authenticate(self, username, password):
        check_computer_signature()
        use_certificate = False
        user = None
        print(self.certificate)
        # Check for USB certificate
        if self.certificate:
            cert_data = self.certificate.load_certificate()
            if cert_data and cert_data['username'] == username:
                user = User(
                    username,
                    cert_data['password'],
                    cert_data.get('min_length', 8),
                    cert_data.get('blocked', False),
                    cert_data.get('use_certificate', False)
                )
                use_certificate = True

        if not user and username in self.users:
            user = self.users[username]

        if not user:
            return False, 'User not found.'

        if user.blocked:
            return False, 'User is blocked.'

        if not user.check_password(password):
            self.attempts += 1
            if self.attempts >= 3:
                return False, 'Too many failed attempts.'
            else:
                return False, f'Incorrect password. Attempts left: {3 - self.attempts}'

        # Reset attempts after successful login
        self.attempts = 0
        return True, {'user': user, 'use_certificate': use_certificate}

    def get_users(self):
        return self.users

    def save_users(self):
        User.save_users(self.users)
