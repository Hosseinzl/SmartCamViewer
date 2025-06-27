# data context for sqllite

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

# اتصال به دیتابیس SQLite
engine = create_engine('sqlite:///devices.db', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()