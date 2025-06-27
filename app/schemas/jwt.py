from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.schemas.response import ResponseMeta

class Token(BaseModel):
    access_token: str
    refresh_token: str
    
    class Config:
        orm_mode = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenVerify(BaseModel):
    access_token: str
    
class TokenResponse(BaseModel):
    message: str
    data: Optional[Token] = None
    exception: Optional[str] = None
    meta: ResponseMeta
    
    class Config:
        orm_mode = True