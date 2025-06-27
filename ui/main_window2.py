from PyQt5 import QtWidgets, uic
from qt_material import apply_stylesheet
import sys
import cv2
from devices.device_manager_service import DeviceManagerService
from devices.rtsp_frame_reader import RTSPFrameReader
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QSizePolicy

class MainDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("test.ui", self)

        # مثال ساده از اتصال دکمه‌ها
        self.pushButton_2.clicked.connect(lambda: print("Button 1 clicked"))
        self.pushButton_3.clicked.connect(lambda: print("Button 2 clicked"))
        self.pushButton_4.clicked.connect(lambda: print("Button 3 clicked"))

        self.add_device_button.clicked.connect(self.add_device)

        # --- Camera feed logic ---

        self.device_service = DeviceManagerService()
        self.rtsp_reader = None
        self.current_device_id = None

        self.select_device.currentIndexChanged.connect(self.on_device_selected)
        self.load_devices()  # یا آدرس RTSP واقعی

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
        if self.rtsp_reader:
            self.rtsp_reader.release()
            self.rtsp_reader = None
            self.timer.stop()
        if index < 0 or not self.devices:
            self.frame_container.setText("دیوایسی انتخاب نشده است.")
            return
        device_id = self.select_device.itemData(index)
        rtsp_url = self.device_service.get_rtsp_url(device_id)
        if not rtsp_url:
            self.frame_container.setText("خطا در دریافت RTSP URL!")
            return
        try:
            self.rtsp_reader = RTSPFrameReader(rtsp_url)
            # Remove dynamic resizing based on frame size
            self.timer.start(30)  # حدود 30 فریم بر ثانیه
        except Exception as e:
            self.frame_container.setText(f"خطا در اتصال به دوربین: {e}")


    def add_device(self):
        device_name = self.comboBox.currentText()
        print(f"Adding device: {device_name}")

    def update_frame(self):
        if not self.rtsp_reader:
            print('t')
            return
        frame = self.rtsp_reader.next_frame()
        print(frame)
        if frame is None:
            self.image_label.setText("خطا در دریافت فریم!")
            return
        print('y')
        print(frame.shape)
        
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        # print pixmap to sure there is some data
        
        #print(self.frame_container.width(), self.frame_container.height())
        self.frame_container.setPixmap(pixmap.scaled(
            self.frame_container.width(), self.frame_container.height(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        ))
        #print("\n")

    def closeEvent(self, event):
        if hasattr(self, 'rtsp_reader') and self.rtsp_reader:
            self.rtsp_reader.release()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')  # اعمال تم متریال
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())
