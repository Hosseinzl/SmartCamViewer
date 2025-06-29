import logging
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

        # مثال ساده از اتصال دکمه‌ها
        self.hand_detection_toggle.clicked.connect(self.on_hand_detection_toggle)
        self.face_detection_toggle.clicked.connect(self.on_face_detection_toggle)
        self.pushButton_4.clicked.connect(lambda: print("Button 3 clicked"))

        self.add_device_button.clicked.connect(self.add_device)

        # --- Camera feed logic ---
        self.device_service = DeviceManagerService()
        self.device_display_service = DeviceDisplayService()
        self.current_device_id = None

        self.select_device.currentIndexChanged.connect(self.on_device_selected)
        self.load_devices()

        self.frame_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.frame_container.setMaximumSize(800, 454)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # حدود 30 فریم بر ثانیه

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

    def add_device(self):
        dialog = AddDeviceDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            device_info = dialog.get_device_data()
            print("New device info:", device_info)
            # You can handle dialog result here if needed

    def update_frame(self):
        if not self.current_device_id:
            return
        
        frame = self.device_display_service.get_frame(self.current_device_id)
        if frame is None:
            self.frame_container.setText("خطا در دریافت فریم!")
            return
        
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        self.frame_container.setPixmap(pixmap.scaled(
            self.frame_container.width(), self.frame_container.height(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        ))

    def closeEvent(self, event):
        if hasattr(self, 'device_display_service'):
            self.device_display_service.close()
        event.accept()

    def on_hand_detection_toggle(self):
        self.device_display_service.toggle_hand_detection()

    def on_face_detection_toggle(self):
        self.device_display_service.toggle_face_detection()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')  # اعمال تم متریال
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())
