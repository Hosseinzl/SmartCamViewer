import cv2

class RTSPFrameReader:
    #def __init__(self, rtsp_url):
    #    print(rtsp_url)
    #    self.rtsp_url = rtsp_url
    #    self.cap = cv2.VideoCapture(rtsp_url)
    #    if not self.cap.isOpened():
    #        raise ValueError(f"Cannot open RTSP stream: {rtsp_url}")
#
    #def next_frame(self):
    #    print(0)
    #    if not self.cap.isOpened():
    #        print(1)
    #        return None
    #    ret, frame = self.cap.read()
    #    print(2)
#
    #    if not ret:
    #        print(3)
#
    #        return None
    #    print(4)
    #
    #    return frame
#
    #def release(self):
    #    if self.cap:
    #        self.cap.release()

    def __init__(self, rtsp_url=None):
        # self.rtsp_url = rtsp_url
        # self.cap = cv2.VideoCapture(rtsp_url)
        # if not self.cap.isOpened():
        #     raise ValueError(f"Cannot open RTSP stream: {rtsp_url}")

        # بارگذاری تصویر تست به جای استریم RTSP
        self.test_image = cv2.imread("test.jpg")
        if self.test_image is None:
            raise FileNotFoundError("Cannot load test image: test.jpg")

    def next_frame(self):
        # return یک کپی از تصویر برای جلوگیری از دستکاری نسخه‌ی اصلی
        return self.test_image

    def release(self):
        # در حالت تست کاری لازم نیست انجام بدیم
        pass