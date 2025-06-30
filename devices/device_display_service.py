import cv2
from devices.device_manager_service import DeviceManagerService
from devices.rtsp_frame_reader import RTSPFrameReader
from ai.hand_detection import HandDetection
from ai.face_detection import FaceDetectionService

class DeviceDisplayService:
    def __init__(self):
        self.device_service = DeviceManagerService()
        self.hand_detection = None
        self.face_detection = None
        self.hand_detection_enabled = True
        self.face_detection_enabled = False
        self.rtsp_readers = {}  # device_id -> RTSPFrameReader
    
    def get_frame(self, device_id):
        """دریافت فریم از دیوایس بدون نمایش آن"""
        device = self.device_service.get_device_by_id(device_id)
        if not device:
            print(f"دیوایس با آیدی {device_id} یافت نشد!")
            return None
        
        rtsp_url = self.device_service.get_rtsp_url(device_id)
        if not rtsp_url:
            print("خطا در ساخت RTSP URL!")
            return None
        
        try:
            # Use cached reader if exists, else create and cache
            if device_id not in self.rtsp_readers:
                print(f"Creating RTSPFrameReader for device {device_id}")
                self.rtsp_readers[device_id] = RTSPFrameReader(rtsp_url)
            reader = self.rtsp_readers[device_id]
            frame = reader.next_frame()
            if frame is None:
                print("خطا در خواندن فریم!")
                return None
            
            # اگر تشخیص دست فعال است، آن را اعمال کن
            if self.hand_detection_enabled:
                if self.hand_detection is None:
                    self.hand_detection = HandDetection()
                frame = self.hand_detection.detect_hands(frame)
            
            # اگر تشخیص چهره فعال است، آن را اعمال کن
            if self.face_detection_enabled:
                if self.face_detection is None:
                    self.face_detection = FaceDetectionService()
                frame = self.face_detection.detect_faces(frame)
            
            return frame
            
        except Exception as e:
            print(f"خطا در دریافت فریم: {e}")
            return None

    def close(self):
        """بستن سرویس و آزاد کردن منابع"""
        for reader in self.rtsp_readers.values():
            reader.release()
        self.rtsp_readers.clear()
        if self.hand_detection:
            self.hand_detection.release()
        if self.face_detection:
            self.face_detection.release()

    def toggle_hand_detection(self):
        """فعال/غیرفعال کردن تشخیص دست"""
        self.hand_detection_enabled = not self.hand_detection_enabled
        status = "فعال" if self.hand_detection_enabled else "غیرفعال"
        print(f"تشخیص دست {status} شد.")

    def toggle_face_detection(self):
        """فعال/غیرفعال کردن تشخیص چهره"""
        self.face_detection_enabled = not self.face_detection_enabled
        status = "فعال" if self.face_detection_enabled else "غیرفعال"
        print(f"تشخیص چهره {status} شد.") 