import cv2
import numpy as np
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions import drawing_utils

class HandDetection:
    def __init__(self):
        self.hands = Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = drawing_utils
    
    def detect_hands(self, frame):
        """تشخیص دست‌ها در فریم و رسم نقاط کلیدی"""
        # تبدیل BGR به RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # تشخیص دست‌ها
        results = self.hands.process(rgb_frame)
        
        # اگر دستی تشخیص داده شد
        multi_hand_landmarks = getattr(results, "multi_hand_landmarks", None)
        if multi_hand_landmarks:
            for hand_landmarks in multi_hand_landmarks:
                # رسم نقاط کلیدی دست
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    list(HAND_CONNECTIONS)
                )
                
                # نمایش تعداد دست‌های تشخیص داده شده
                cv2.putText(
                    frame, 
                    f"Hands: {len(multi_hand_landmarks)}", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, 
                    (0, 255, 0), 
                    2
                )
        
        return frame
    
    def get_hand_count(self, frame):
        """تعداد دست‌های تشخیص داده شده را برمی‌گرداند"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        multi_hand_landmarks = getattr(results, "multi_hand_landmarks", None)
        if multi_hand_landmarks:
            return len(multi_hand_landmarks)
        return 0
    
    def release(self):
        """آزاد کردن منابع"""
        self.hands.close() 