from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InvoiceIn(BaseModel):
    client_name: str
    amount: int
    status: Optional[str] = "draft"

class InvoiceOut(BaseModel):
    id: int
    user_id: int
    client_name: str
    amount: int
    status: str
    created_at: datetime
    
class InvoiceUpdate(BaseModel):
    client_name: Optional[str]
    amount: Optional[int]
    status: Optional[str]
