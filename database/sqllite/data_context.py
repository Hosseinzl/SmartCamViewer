# data context for sqllite

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
import logging

# Suppress SQLAlchemy engine logs
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)

# اتصال به دیتابیس SQLite
engine = create_engine('sqlite:///devices.db', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()