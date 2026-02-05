import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import qt_material

from devices.device_manager_service import DeviceManagerService
from devices.rtsp_frame_reader import RTSPFrameReader
from ui.frame_grabber_thread import FrameGrabberThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مدیریت و نمایش دوربین‌ها")
        self.setGeometry(200, 100, 900, 600)

        self.device_service = DeviceManagerService()
        self.rtsp_reader = None
        self.current_device_id = None
        self.frame_thread = None
        self.latest_frame = None

        self.init_ui()
        self.load_devices()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header: Device Management Button
        header_layout = QHBoxLayout()
        self.manage_btn = QPushButton("مدیریت دیوایس‌ها")
        self.manage_btn.clicked.connect(self.on_manage_devices)
        header_layout.addWidget(self.manage_btn)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Device selection
        device_layout = QHBoxLayout()
        self.device_combo = QComboBox()
        self.device_combo.currentIndexChanged.connect(self.on_device_selected)
        device_layout.addWidget(QLabel("انتخاب دیوایس:"))
        device_layout.addWidget(self.device_combo)
        device_layout.addStretch()
        main_layout.addLayout(device_layout)

        # Camera image display
        self.image_label = QLabel("تصویر دوربین اینجا نمایش داده می‌شود")
        self.image_label.setFixedSize(800, 600)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Timer for updating camera frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def load_devices(self):
        self.device_combo.clear()
        self.devices = self.device_service.get_all_devices()
        for device in self.devices:
            self.device_combo.addItem(f"{device.name} ({device.ip})", device.id)
        if self.devices:
            self.device_combo.setCurrentIndex(1)

    def on_manage_devices(self):
        QMessageBox.information(self, "مدیریت دیوایس‌ها", "این بخش بعداً پیاده‌سازی می‌شود.")

    def on_device_selected(self, index):
        # توقف هر استریم قبلی و ترد مربوط به آن
        print("try to stop the last device stream")
        if self.frame_thread:
            self.frame_thread.stop()
            self.frame_thread = None
            print("the last device stream stopped")

        print("try to release the last device stream")
        if self.rtsp_reader:
            self.rtsp_reader.release()
            self.rtsp_reader = None
            print("the last device stream released")

        print("try to stop the timer")  
        self.timer.stop()
        self.latest_frame = None
        print("the timer stopped")

        print("try to check if the index is valid")
        if index < 0 or not self.devices:
            self.image_label.setText("دیوایسی انتخاب نشده است.")
            return

        # log the index
        print(index)
        device_id = self.device_combo.itemData(index)
        rtsp_url = self.device_service.get_rtsp_url(device_id)
        if not rtsp_url:
            self.image_label.setText("خطا در دریافت RTSP URL!")
            return
        try:
            self.rtsp_reader = RTSPFrameReader(rtsp_url)

            # ترد جدا برای گرفتن فریم‌ها با حداقل تأخیر
            self.frame_thread = FrameGrabberThread(self.rtsp_reader.next_frame, self)
            self.frame_thread.frame_received.connect(self.on_frame_received)
            self.frame_thread.start()

            # تایمر فقط آخرین فریم دریافت‌شده را نمایش می‌دهد
            self.timer.start(30)  # حدود 30 فریم بر ثانیه
        except Exception as e:
            self.image_label.setText(f"خطا در اتصال به دوربین: {e}")

    def on_frame_received(self, frame):
        """
        این اسلات در ترد پس‌زمینه هنگام رسیدن هر فریم جدید صدا زده می‌شود.
        فقط آخرین فریم نگه داشته می‌شود تا تأخیر به حداقل برسد.
        """
        self.latest_frame = frame

    def update_frame(self):
        # فقط آخرین فریم موجود را نمایش بده؛
        # فریم‌گیری در ترد جدا انجام می‌شود تا تأخیر کم بماند.
        if self.latest_frame is None:
            return

        frame = self.latest_frame
        # تبدیل فریم OpenCV (BGR) به QImage (RGB)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        

        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.width(), self.image_label.height(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        ))

    def closeEvent(self, event):
        if self.frame_thread:
            self.frame_thread.stop()
            self.frame_thread = None

        if self.rtsp_reader:
            self.rtsp_reader.release()
        self.device_service.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()  # ← اول پنجره رو بساز
    qt_material.apply_stylesheet(app, theme='dark_blue')  # ← بعدش تم رو اعمال کن
    window.show()
    sys.exit(app.exec_())
