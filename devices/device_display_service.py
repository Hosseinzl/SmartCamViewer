import cv2
from devices.device_manager_service import DeviceManagerService
from devices.rtsp_frame_reader import RTSPFrameReader
from ai.hand_detection import HandDetection

class DeviceDisplayService:
    def __init__(self):
        self.device_service = DeviceManagerService()
        self.hand_detection = None
        self.hand_detection_enabled = True  # به صورت پیش‌فرض فعال
    
    def display_device_stream(self, device_id):
        """نمایش استریم یک دیوایس با استفاده از آیدی"""
        # دیوایس را از دیتابیس بگیر
        device = self.device_service.get_device_by_id(device_id)
        if not device:
            print(f"دیوایس با آیدی {device_id} یافت نشد!")
            return False
        
        print(f"دیوایس انتخاب شده: {device.name} - {device.ip}")
        
        # RTSP URL را بساز
        rtsp_url = self.device_service.get_rtsp_url(device_id)
        if not rtsp_url:
            print("خطا در ساخت RTSP URL!")
            return False
        
        print(f"RTSP URL: {rtsp_url}")
        print("دستورات:")
        print("  'q' - خروج")
        print("  'h' - فعال/غیرفعال کردن تشخیص دست")
        
        # شروع خواندن فریم‌ها
        try:
            reader = RTSPFrameReader(rtsp_url)
            print("اتصال به دوربین برقرار شد.")
            
            while True:
                frame = reader.next_frame()
                if frame is None:
                    print("خطا در خواندن فریم!")
                    break
                
                # اگر تشخیص دست فعال است، آن را اعمال کن
                if self.hand_detection_enabled:
                    if self.hand_detection is None:
                        self.hand_detection = HandDetection()
                    frame = self.hand_detection.detect_hands(frame)
                
                # فریم را نمایش بده
                cv2.imshow('Camera Feed', frame)
                
                # بررسی کلیدهای فشرده شده
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('h'):
                    self.toggle_hand_detection()
                    
        except Exception as e:
            print(f"خطا در اتصال به دوربین: {e}")
            return False
        finally:
            # منابع را آزاد کن
            if 'reader' in locals():
                reader.release()
            if self.hand_detection:
                self.hand_detection.release()
            cv2.destroyAllWindows()
        
        return True
    
    def toggle_hand_detection(self):
        """فعال/غیرفعال کردن تشخیص دست"""
        self.hand_detection_enabled = not self.hand_detection_enabled
        status = "فعال" if self.hand_detection_enabled else "غیرفعال"
        print(f"تشخیص دست {status} شد.")
    
    def close(self):
        """بستن سرویس و آزاد کردن منابع"""
        if self.hand_detection:
            self.hand_detection.release()
        self.device_service.close() 