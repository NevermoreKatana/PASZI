# models/certificate.py

import json
import os
import ctypes
import psutil

CERTIFICATE_FILE = 'certificate.json'

class Certificate:
    def __init__(self, usb_label = 'D:/'):
        self.usb_label = usb_label

    def get_usb_drive(self):
        drives = [disk.device for disk in psutil.disk_partitions(all=False) if 'removable' in disk.opts]
        print(drives)
        for drive in drives:
            try:
                drive_label = ctypes.create_unicode_buffer(1024)
                ctypes.windll.kernel32.GetVolumeInformationW(
                    ctypes.c_wchar_p(drive),
                    drive_label,
                    ctypes.sizeof(drive_label),
                    None,
                    None,
                    None,
                    None,
                    0
                )
                if drive_label.value == self.usb_label:
                    return drive
            except Exception:
                continue
        return None

    def load_certificate(self):
        drive = self.get_usb_drive()
        if drive:
            cert_path = os.path.join(drive, CERTIFICATE_FILE)
            print(cert_path)
            if os.path.exists(cert_path):
                with open(cert_path, 'r') as f:
                    certificate = json.load(f)
                return certificate
        return None

    def save_certificate(self, user_data):
        drive = self.get_usb_drive()
        if drive:
            cert_path = os.path.join(drive, CERTIFICATE_FILE)
            with open(cert_path, 'w') as f:
                json.dump(user_data, f, indent=4)
            return True
        return False
