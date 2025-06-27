from sqlalchemy import Column, Integer, String, Boolean
from database.sqllite.data_context import Base

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    rtsp_port = Column(Integer, nullable=False)
    channel = Column(Integer, nullable=False)
    subtype = Column(String, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    rtsp_url_format = Column(String, nullable=True)

    @classmethod
    def get_all(cls, session):
        """خواندن همه دیوایس‌ها از دیتابیس"""
        return session.query(cls).all()