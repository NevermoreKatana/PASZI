# views/admin_window.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.admin_controller import AdminController

class AdminWindow:
    def __init__(self, user):
        self.root = tk.Tk()
        self.root.title('Admin Panel')
        self.user = user
        self.controller = AdminController(user)

        self.root.geometry('400x300')
        self.root.resizable(False, False)

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='User Management', menu=user_menu)
        user_menu.add_command(label='Change Password', command=self.change_password)
        user_menu.add_command(label='View Users', command=self.view_users)
        user_menu.add_command(label='Add User', command=self.add_user)
        user_menu.add_command(label='Block User', command=self.block_user)
        user_menu.add_command(label='Set Min Password Length', command=self.set_min_length)
        user_menu.add_command(label='Set USB Drive Label', command=self.set_usb_label)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=self.show_about)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def change_password(self):
        old_password = simpledialog.askstring('Change Password', 'Enter old password:', show='*')
        new_password = simpledialog.askstring('Change Password', 'Enter new password:', show='*')
        success, message = self.controller.change_password(old_password, new_password,)
        if success:
            messagebox.showinfo('Success', message)
        else:
            messagebox.showerror('Error', message)

    def view_users(self):
        users = self.controller.auth_controller.get_users()
        top = tk.Toplevel(self.root)
        top.title('Registered Users')
        top.geometry('400x300')
        scrollbar = tk.Scrollbar(top)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        user_list = tk.Listbox(top, yscrollcommand=scrollbar.set, width=50)
        for user in users.values():
            user_info = f"User: {user.username}, Min Length: {user.min_length}, Blocked: {user.blocked}"
            user_list.insert(tk.END, user_info)
        user_list.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=user_list.yview)

    def add_user(self):
        new_username = simpledialog.askstring('Add User', 'Enter new username:')
        if not new_username:
            return
        min_length = simpledialog.askinteger('Password Policy', 'Enter minimum password length for the user:', minvalue=4, maxvalue=20)
        if not min_length:
            min_length = 8
        use_certificate = messagebox.askyesno('Certificate', 'Use USB Certificate for this user?')
        success, message = self.controller.add_user(new_username, min_length, use_certificate)
        if success:
            messagebox.showinfo('Success', message)
        else:
            messagebox.showerror('Error', message)

    def block_user(self):
        username = simpledialog.askstring('Block User', 'Enter username to block:')
        if not username:
            return
        success, message = self.controller.block_user(username)
        if success:
            messagebox.showinfo('Success', message)
        else:
            messagebox.showerror('Error', message)

    def set_min_length(self):
        username = simpledialog.askstring('Set Min Password Length', 'Enter username:')
        if not username:
            return
        min_length = simpledialog.askinteger('Password Policy', 'Enter minimum password length for the user:', minvalue=4, maxvalue=20)
        if not min_length:
            return
        success, message = self.controller.set_min_length(username, min_length)
        if success:
            messagebox.showinfo('Success', message)
        else:
            messagebox.showerror('Error', message)

    def set_usb_label(self):
        label = simpledialog.askstring('Set USB Drive Label', 'Enter new USB drive label:')
        if not label:
            return
        success, message = self.controller.set_usb_label(label)
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
