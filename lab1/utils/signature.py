# utils/signature.py

import os
import hashlib
import platform
import psutil
import getpass
import json
from tkinter import messagebox
import sys

SIGNATURE_FILE = 'data/settings.json'

def generate_computer_signature():
    user_name = getpass.getuser()
    computer_name = platform.node()
    windows_directory = os.environ.get('WINDIR', 'C:\\Windows')
    screen_width = 800  # Placeholder, replace with actual value if needed
    screen_height = 600  # Placeholder, replace with actual value if needed
    total_memory = psutil.virtual_memory().total
    hdd_info = psutil.disk_usage('/')
    hdd_total = hdd_info.total
    hdd_fs_type = ''
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            hdd_fs_type = part.fstype
            break

    signature_data = f"{user_name}{computer_name}{windows_directory}{screen_width}{screen_height}{total_memory}{hdd_total}{hdd_fs_type}"
    signature_hash = hashlib.sha256(signature_data.encode()).hexdigest()
    return signature_hash

def save_computer_signature(signature):
    os.makedirs('data', exist_ok=True)
    settings = {'signature': signature}
    with open(SIGNATURE_FILE, 'w') as f:
        json.dump(settings, f)

def load_computer_signature():
    if not os.path.exists(SIGNATURE_FILE):
        return None
    with open(SIGNATURE_FILE, 'r') as f:
        settings = json.load(f)
    return settings.get('signature')

def check_computer_signature():
    saved_signature = load_computer_signature()
    current_signature = generate_computer_signature()
    if not saved_signature:
        save_computer_signature(current_signature)
    elif saved_signature != current_signature:
        messagebox.showerror('Unauthorized Use', 'The program has detected unauthorized copying or use.\nSignature mismatch.')
        sys.exit()
