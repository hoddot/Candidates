from pydantic import BaseModel, Field
from typing import Optional, List, Any
from app.schemas.response import ResponseMeta
from datetime import datetime

# ---------- child objects ----------
class InterviewSchema(BaseModel):
    interviewer: Optional[str] = Field(None, example="John Doe")
    scheduled_at: Optional[datetime] = Field(
        None, example="2025-07-01T14:30:00"
    )

class FeedbackSchema(BaseModel):
    rating: Optional[int] = Field(None, example=4)

# ---------- main user ----------
class UserBase(BaseModel):
    id: str = Field(..., example="UUID")
    email: str = Field(..., example="name@mail.com")
    name: str = Field(..., example="name")
    position: str = Field(..., example="position")
    status: str = Field(..., example="applied, interviewing, hired, rejected")
    created_date: datetime = Field(..., example="2025-06-26T16:44:29")
    active: int = Field(..., example=1)

    interviews: Optional[InterviewSchema] = None
    feedbacks: Optional[FeedbackSchema] = None

# ---------- wrapper objects ----------
class UsersContainer(BaseModel):
    users: List[UserBase]

class ResponseMeta(BaseModel):
    timestamp: str = Field(..., example="2025-06-27 15:05:00")

class PaginationResponse(BaseModel):
    message: str
    data: UsersContainer
    meta: ResponseMeta
    exception: Optional[str] = None

class FirstResponse(BaseModel):
    message: str
    data: UserBase
    meta: ResponseMeta
    exception: Optional[str] = None