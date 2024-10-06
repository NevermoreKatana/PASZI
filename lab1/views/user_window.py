# views/user_window.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.user_controller import UserController

class UserWindow:
    def __init__(self, user, use_certificate):
        self.root = tk.Tk()
        self.root.title('User Panel')
        self.user = user
        self.controller = UserController(user, use_certificate)

        self.root.geometry('400x200')
        self.root.resizable(False, False)

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='User', menu=user_menu)
        user_menu.add_command(label='Change Password', command=self.change_password)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=self.show_about)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def change_password(self):
        old_password = simpledialog.askstring('Change Password', 'Enter old password:', show='*')
        new_password = simpledialog.askstring('Change Password', 'Enter new password:', show='*')
        success, message = self.controller.change_password(old_password, new_password)
        if success:
            messagebox.showinfo('Success', message)
        else:
            messagebox.showerror('Error', message)

    def show_about(self):
        about_text = 'Author: Leonid Khodykin\nLab Assignment 1\nAll requirements have been implemented.'
        messagebox.showinfo('About', about_text)

    def on_closing(self):
        self.root.destroy()
        exit()
    