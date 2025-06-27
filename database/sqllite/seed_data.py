import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database.sqllite.data_context import SessionLocal, Base
from database.sqllite.models.sqllite_device import Device

def seed_database():
    # ابتدا جداول را ایجاد کن
    Base.metadata.create_all(bind=SessionLocal().bind)
    
    session = SessionLocal()
    
    # بررسی وجود داده در جدول devices
    device_count = session.query(Device).count()
    
    if device_count == 0:
        # اضافه کردن دیوایس تست
        test_device = Device(
            name="test",
            ip="192.168.1.200",
            rtsp_port=554,
            channel=1,
            subtype="0",
            username="admin",
            password="0111215",
            rtsp_url_format="rtsp://{username}:{password}@{ip}:{port}/H264?ch={channel}&subtype={subtype}"
        )
        
        session.add(test_device)
        session.commit()
        print("داده‌های نمونه به دیتابیس اضافه شد.")
    else:
        print("دیتابیس قبلاً دارای داده است.")
    
    session.close()

if __name__ == "__main__":
    seed_database() 