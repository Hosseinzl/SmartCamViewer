from PyQt5.QtCore import QThread, pyqtSignal
import cv2

class FrameGrabberThread(QThread):
    frame_received = pyqtSignal(object)

    def __init__(self, get_frame_callback, parent=None):
        super().__init__(parent)
        self.get_frame = get_frame_callback
        self.running = True

    def run(self):
        while self.running:
            frame = self.get_frame()
            if frame is not None:
                self.frame_received.emit(frame)
            #self.msleep(30)  # حدود 30 فریم بر ثانیه

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
