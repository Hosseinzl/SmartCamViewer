import cv2
import numpy as np
from mediapipe.python.solutions.face_detection import FaceDetection
from mediapipe.python.solutions import drawing_utils

class FaceDetectionService:
    def __init__(self):
        self.face_detection = FaceDetection(
            model_selection=0,  # 0 for short-range, 1 for full-range
            min_detection_confidence=0.5
        )
        self.mp_draw = drawing_utils

    def detect_faces(self, frame):
        """تشخیص چهره‌ها در فریم و رسم باکس‌ها"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        detections = getattr(results, "detections", None)
        if detections:
            for detection in detections:
                self.mp_draw.draw_detection(frame, detection)

            cv2.putText(
                frame,
                f"Faces: {len(detections)}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

        return frame

    def get_face_count(self, frame):
        """تعداد صورت‌های تشخیص داده شده را برمی‌گرداند"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        detections = getattr(results, "detections", None)
        if detections:
            return len(detections)
        return 0

    def release(self):
        """آزاد کردن منابع"""
        self.face_detection.close()
