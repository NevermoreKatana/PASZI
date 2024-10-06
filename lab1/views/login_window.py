# views/login_window.py

import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController
from views.admin_window import AdminWindow
from views.user_window import UserWindow

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Login')
        self.auth_controller = AuthController()
        self.attempts = 0

        self.root.geometry('300x150')
        self.root.resizable(False, False)

        tk.Label(self.root, text='Username:').pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text='Password:').pack(pady=5)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text='Login', command=self.login).pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, result = self.auth_controller.authenticate(username, password)

        if success:
            self.root.destroy()
            user = result['user']
            use_certificate = result['use_certificate']
            if username == 'ADMIN':
                AdminWindow(user)
            else:
                UserWindow(user, use_certificate)
        else:
            if result == 'Too many failed attempts.':
                messagebox.showerror('Error', result)
                self.root.destroy()
            else:
                messagebox.showerror('Error', result)

    def on_closing(self):
        self.root.destroy()
        exit()
