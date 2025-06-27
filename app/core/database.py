import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "./my_database.sqlite3")  # default = ไฟล์ในโฟลเดอร์นี้
DATABASE_URL = f"sqlite:///{DB_PATH}"

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# สร้าง session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# สร้าง Base สำหรับ declarative models
Base = declarative_base()

# ฟังก์ชันสำหรับให้ session ของฐานข้อมูล
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise  # ส่งต่อ exception ออกไป
    finally:
        db.close()