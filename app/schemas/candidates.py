from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.schemas.response import ResponseMeta

class UserBase(BaseModel):
    id: str = Field(..., example="UUID")
    email: str = Field(..., example="name@mail.com")
    name: str = Field(..., example="name")
    position: str = Field(..., example="position")
    status: str = Field(..., example="applied, interviewing, hired, rejected")
    created_date: str = Field(..., example="date time")
    active : int = Field(..., example=1)

class UserBaseDelete(BaseModel):
    id: str = Field(..., example="UUID")
    active : int = Field(..., example=0)

class UserBaseInterviews(BaseModel):
    id: str = Field(..., example="UUID")
    email: str = Field(..., example="name@mail.com")
    name: str = Field(..., example="name")
    position: str = Field(..., example="position")
    status: str = Field(..., example="applied, interviewing, hired, rejected")
    schedule_interview: str = Field(..., example="date time")
    created_date: str = Field(..., example="date time")
    active : int = Field(..., example=1)

class UserBaseFeedback(BaseModel):
    id: str = Field(..., example="UUID")
    email: str = Field(..., example="name@mail.com")
    name: str = Field(..., example="name")
    position: str = Field(..., example="position")
    status: str = Field(..., example="applied, interviewing, hired, rejected")
    rating: int = Field(..., example=5)
    created_date: str = Field(..., example="date time")
    active : int = Field(..., example=1)

class UserResponse(BaseModel):
    message: str
    data: Optional[UserBase] = None
    exception: Optional[str] = None
    meta: ResponseMeta
    
    class Config:
        orm_mode = True

class UserResponseDelete(BaseModel):
    message: str
    data: Optional[UserBaseDelete] = None
    exception: Optional[str] = None
    meta: ResponseMeta
    
    class Config:
        orm_mode = True

class UserResponseInterviews(BaseModel):
    message: str
    data: Optional[UserBaseInterviews] = None
    exception: Optional[str] = None
    meta: ResponseMeta
    
    class Config:
        orm_mode = True

class UserResponseFeedback(BaseModel):
    message: str
    data: Optional[UserBaseFeedback] = None
    exception: Optional[str] = None
    meta: ResponseMeta
    
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name_th: Optional[str]
    last_name_th: Optional[str]
    first_name_en: Optional[str]
    last_name_en: Optional[str]
    phone: Optional[str]
    active: Optional[int]