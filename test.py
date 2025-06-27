from PyQt5.QtWidgets import QApplication, QPushButton
import qt_material
import sys

app = QApplication(sys.argv)
qt_material.apply_stylesheet(app, theme='dark_blue.xml')
btn = QPushButton("Test Button")
btn.show()
sys.exit(app.exec_())