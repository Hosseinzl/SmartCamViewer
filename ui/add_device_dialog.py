from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class AddDeviceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("add_device_dialog.ui", self)
        # وصل شدن دکمه‌های استاندارد OK و Cancel به متدها
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


    def get_device_data(self):
        return {
            "name": self.name_input.text(),
            "ip": self.ip_input.text(),
            "port": self.port_input.text() or "554",  # مقدار پیش‌فرض
            "username": self.username_input.text(),
            "password": self.password_input.text(),
            "format": self.rtsp_format_input.text(),  # فرض بر اینکه کمبوباکس هست
            "channel": self.channel_input.value(),
            "subtype": self.subtype_input.value()
        }