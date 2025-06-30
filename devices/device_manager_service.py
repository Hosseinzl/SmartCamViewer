from database.sqllite.data_context import SessionLocal
from database.sqllite.models.sqllite_device import Device
from sqlalchemy.orm import Session
from typing import Optional

class DeviceManagerService:
    def __init__(self, session: Optional[Session] = None):
        self.session = session or SessionLocal()

    def add_device(self, name, ip, rtsp_port, channel, subtype=None, username=None, password=None, rtsp_url_format=None):
        device = Device(
            name=name,
            ip=ip,
            rtsp_port=rtsp_port,
            channel=channel,
            subtype=subtype,
            username=username,
            password=password,
            rtsp_url_format=rtsp_url_format
        )
        self.session.add(device)
        self.session.commit()
        self.session.refresh(device)
        return device

    def delete_device(self, device_id):
        device = self.session.query(Device).filter(Device.id == device_id).first()
        if device:
            self.session.delete(device)
            self.session.commit()
            return True
        return False

    def get_all_devices(self):
        return self.session.query(Device).all()

    def get_device_by_id(self, device_id):
        return self.session.query(Device).filter(Device.id == device_id).first()

    def close(self):
        self.session.close() 

    def get_rtsp_url(self, device_id):
        device = self.get_device_by_id(device_id)
        if not device:
            return None
        
        # اگر rtsp_url_format وجود نداشت، از فرمت پیش‌فرض استفاده کن
        if device.rtsp_url_format is not None:
            rtsp_url = device.rtsp_url_format.format(
                username=device.username, 
                password=device.password, 
                ip=device.ip, 
                port=device.rtsp_port, 
                channel=device.channel, 
                subtype=device.subtype
            )

        else:
            # فرمت پیش‌فرض

            rtsp_url = f"rtsp://{device.username}:{device.password}@{device.ip}:{device.rtsp_port}/stream?ch={device.channel}&subtype={device.subtype}"
        
        return rtsp_url
