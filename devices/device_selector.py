from devices.device_manager_service import DeviceManagerService

class DeviceSelector:
    def __init__(self):
        self.device_service = DeviceManagerService()
    
    def get_first_device_id(self):
        """اولین دیوایس موجود در دیتابیس را برمی‌گرداند"""
        devices = self.device_service.get_all_devices()
        if not devices:
            print("هیچ دیوایسی در دیتابیس یافت نشد!")
            return None
        
        first_device = devices[0]
        print(f"دیوایس انتخاب شده: {first_device.name} (ID: {first_device.id})")
        return first_device.id
    
    def get_device_by_name(self, name):
        """دیوایس را با نام برمی‌گرداند"""
        devices = self.device_service.get_all_devices()
        for device in devices:
            if device.name == name:
                return device.id
        return None
    
    def list_all_devices(self):
        """لیست همه دیوایس‌ها را نمایش می‌دهد"""
        devices = self.device_service.get_all_devices()
        if not devices:
            print("هیچ دیوایسی در دیتابیس یافت نشد!")
            return
        
        print("لیست دیوایس‌های موجود:")
        for device in devices:
            print(f"ID: {device.id}, Name: {device.name}, IP: {device.ip}")
    
    def close(self):
        """بستن سرویس"""
        self.device_service.close() 