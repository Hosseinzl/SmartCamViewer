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

    #def __init__(self, rtsp_url=None):
    #    # self.rtsp_url = rtsp_url
    #    # self.cap = cv2.VideoCapture(rtsp_url)
    #    # if not self.cap.isOpened():
    #    #     raise ValueError(f"Cannot open RTSP stream: {rtsp_url}")
#
    #    # بارگذاری تصویر تست به جای استریم RTSP
    #    self.test_image = cv2.imread("test.jpg")
    #    if self.test_image is None:
    #        raise FileNotFoundError("Cannot load test image: test.jpg")
#
    #def next_frame(self):
    #    # return یک کپی از تصویر برای جلوگیری از دستکاری نسخه‌ی اصلی
    #    return self.test_image
#
    #def release(self):
    #    # در حالت تست کاری لازم نیست انجام بدیم
    #    pass