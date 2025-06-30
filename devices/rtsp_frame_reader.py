import cv2

class RTSPFrameReader:
    def __init__(self, rtsp_url):
        print(rtsp_url)
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(rtsp_url)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open RTSP stream: {rtsp_url}")

    def next_frame(self):
        if not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        return frame

    def release(self):
        if self.cap:
            self.cap.release()

    def is_connected(self):
        return self.cap is not None and self.cap.isOpened()

    def reconnect(self):
        """Attempt to reconnect to the RTSP stream"""
        self.release()
        self.cap = cv2.VideoCapture(self.rtsp_url)
        return self.cap.isOpened()