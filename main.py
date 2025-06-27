import sys
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet
from ui.main_window import MainWindow
from database.sqllite.seed_data import seed_database
from devices.device_selector import DeviceSelector
from devices.device_display_service import DeviceDisplayService
from ui.main_window2 import MainDialog

def main():
    # ابتدا داده‌های نمونه را اضافه کن
    seed_database()
    
    # انتخاب دیوایس
    device_selector = DeviceSelector()
    device_id = device_selector.get_first_device_id()
    
    if device_id is None:
        print("هیچ دیوایسی برای نمایش یافت نشد!")
        return
    
    # نمایش استریم دیوایس
    display_service = DeviceDisplayService()
    success = display_service.display_device_stream(device_id)
    
    if not success:
        print("خطا در نمایش استریم دیوایس!")
    
    # بستن سرویس‌ها
    device_selector.close()
    display_service.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')  # اعمال تم متریال
    window = MainDialog()
    #window = MainWindow()
    window.show()
    sys.exit(app.exec_())