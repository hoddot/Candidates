from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.core.database import Base
from app.core.config import bangkok_now
from datetime import datetime
from sqlalchemy.orm import relationship

class UserRegister(BaseModel):
    name: str = Field(..., example="name candidates")
    email: str = Field(..., example="name@mail.com")
    position: str = Field(..., example="position")

class UserStatus(BaseModel):
    status: str = Field(..., example="applied, interviewing, hired, rejected")

class ScheduleInterview(BaseModel):
    schedule_interview: datetime
    interviewer: str = Field(..., example="interviewer")

class FeedBack(BaseModel):
    rating: int = Field(..., example=5)
    #rating: int = Field(..., ge=1, le=5, example=5)

class UserUpdate(BaseModel):
    first_name_th: str
    last_name_th: str
    first_name_en: str
    last_name_en: str
    phone: str

class User(Base):
    __tablename__ = "candidate"

    id = Column(String(255), primary_key=True)
    email = Column(String(255))
    name = Column(String(255))
    position = Column(String(255))
    status = Column(String(255))
    active = Column(Integer, default=1)
    created_date = Column(DateTime, default=bangkok_now)
    created_by = Column(String(255))
    updated_date = Column(DateTime, onupdate=bangkok_now)
    updated_by = Column(String(255))

    interviews = relationship("Interview", back_populates="candidate", lazy="selectin")
    feedbacks = relationship("Feedback", back_populates="candidate", lazy="selectin")

class Interview(Base):
    __tablename__ = "interview"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(String(255), ForeignKey("candidate.id"))
    interviewer = Column(String(255))
    scheduled_at = Column(DateTime, default=None)

    candidate = relationship("User", back_populates="interviews")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(String(255), ForeignKey("candidate.id"))
    rating  = Column(Integer, default=None)

    candidate = relationship("User", back_populates="feedbacks")