from pydantic import BaseModel
from datetime import datetime

    
class CreateTicket(BaseModel):
    ticket_id: int
    client_id: int
    subject: str
    status: str
    priority: str
    tags: str | None = None
    
class UpdateTicket(BaseModel):
    subject: str | None = None
    status: str | None = None
    priority: str | None = None
    tags: str | None = None
    satisfaction_rating: str | None = None
    
class ResponseTicket(BaseModel):
    id: int
    ticket_id: int
    client_id: int
    subject: str
    status: str
    priority: str
    tags: str | None
    created_at: datetime
    resolved_at: datetime | None
    satisfaction_rating: str | None
    
    class Config:
        from_attributes = True