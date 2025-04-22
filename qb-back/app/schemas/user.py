from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime