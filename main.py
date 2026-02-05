import logging

from PyQt5.QtGui import QIcon
# Suppress SQLAlchemy logs completely
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.ERROR)

import sys
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet
from database.sqllite.seed_data import seed_database
from devices.device_selector import DeviceSelector
from devices.device_display_service import DeviceDisplayService
from ui.main_window2 import MainDialog


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icons/icon.png"))
    apply_stylesheet(app, theme='dark_teal.xml')  # اعمال تم متریال
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())