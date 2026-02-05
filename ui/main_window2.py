import logging

from ui.frame_grabber_thread import FrameGrabberThread
logging.disable(logging.INFO)

from PyQt5 import QtWidgets, uic
from qt_material import apply_stylesheet
import sys
import cv2
from ui.add_device_dialog import AddDeviceDialog
from devices.device_manager_service import DeviceManagerService
from devices.device_display_service import DeviceDisplayService
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QSizePolicy

class MainDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("test.ui", self)

        # اجازه تغییر اندازه و فعال‌کردن دکمه‌های مینیمایز/ماکسیمایز
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowSystemMenuHint
        )

        self.hand_detection_toggle.clicked.connect(self.on_hand_detection_toggle)
        self.face_detection_toggle.clicked.connect(self.on_face_detection_toggle)
        self.pushButton_4.clicked.connect(lambda: print("Button 3 clicked"))
        self.add_device_button.clicked.connect(self.add_device)

        self.device_service = DeviceManagerService()
        self.device_display_service = DeviceDisplayService()
        self.current_device_id = None
        self.frame_thread = None

        self.select_device.currentIndexChanged.connect(self.on_device_selected)
        self.load_devices()

        # نوار انتخاب دیوایس همیشه کمی فضا داشته باشد و کاملاً مخفی نشود
        self.device_management_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.device_management_container.setMinimumHeight(60)

        # فریم ویدیو همراه با تغییر اندازهٔ پنجره بزرگ/کوچک شود
        self.frame_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # جلوگیری از بزرگ‌شدن تدریجی لیبل بر اساس اندازه پیکس‌مپ
        # و درخواست کشیدن تصویر داخل فضای فعلی لیبل
        self.frame_container.setScaledContents(True)

    def load_devices(self):
        self.select_device.clear()
        self.devices = self.device_service.get_all_devices()
        for device in self.devices:
            self.select_device.addItem(f"{device.name} ({device.ip})", device.id)
        if self.devices:
            self.select_device.setCurrentIndex(0)

    def on_device_selected(self, index):
        if index < 0 or not self.devices:
            self.frame_container.setText("دیوایسی انتخاب نشده است.")
            self.current_device_id = None
            return

        device_id = self.select_device.itemData(index)
        self.current_device_id = device_id

        # توقف ترد قبلی (اگر وجود داشت)
        if self.frame_thread:
            self.frame_thread.stop()
            self.frame_thread = None

        # ساخت ترد جدید
        self.frame_thread = FrameGrabberThread(
            lambda: self.device_display_service.get_frame(device_id)
        )
        self.frame_thread.frame_received.connect(self.show_frame)
        self.frame_thread.start()

    def add_device(self):
        dialog = AddDeviceDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            device_info = dialog.get_device_data()
            self.device_service.add_device(
                device_info["name"],
                device_info["ip"],
                device_info["port"],
                device_info["channel"],
                device_info["subtype"], 
                device_info["username"], 
                device_info["password"], 
                device_info["format"]
            )
            self.load_devices()

    def show_frame(self, frame):
        if frame is None:
            self.frame_container.setText("خطا در دریافت فریم!")
            return

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # با فعال‌بودن setScaledContents(True)، فقط پیکس‌مپ را تنظیم می‌کنیم
        # و خود لیبل تصویر را در فضای فعلی‌اش می‌کشد، بدون تغییر اندازه تدریجی.
        self.frame_container.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.frame_thread:
            self.frame_thread.stop()
        if hasattr(self, 'device_display_service'):
            self.device_display_service.close()
        event.accept()

    def on_hand_detection_toggle(self):
        self.device_display_service.toggle_hand_detection()

    def on_face_detection_toggle(self):
        self.device_display_service.toggle_face_detection()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())
