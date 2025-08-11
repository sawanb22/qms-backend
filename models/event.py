# qms-backend/models/qms_event.py

from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

# This model defines the structure for a single QMS event.
# Pydantic uses this for data validation.
class QMSEvent(BaseModel):
    id: Optional[str] = None
    event_type: str = Field(..., min_length=3, example="Internal Audit")
    title: str = Field(..., min_length=5, example="Annual GMP Audit of Facility X")
    description: str = Field(..., min_length=10, example="Detailed description of the event.")
    status: str = Field(default="Open", example="Open")
    severity: Optional[str] = Field(default="Medium", example="High")
    priority: Optional[str] = Field(default="Medium", example="High")
    initiator: Optional[str] = Field(default="System", example="John Doe")
    department: Optional[str] = Field(None, example="Quality Assurance")
    created_at: Optional[datetime.datetime] = None

# This model defines the structure for the AI prompt payload.
class AIPrompt(BaseModel):
    prompt: str
    events_context: List[dict]  # Accept any dict structure for flexibility

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    event_type = Column(String, index=True)
    status = Column(String, index=True)
    initiator = Column(String, index=True)
    department = Column(String, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    # Additional fields for full event details
    reporter = Column(String, index=True)
    severity = Column(String, index=True)
    priority = Column(String, index=True)
    event_date = Column(DateTime(timezone=True))
    responsible_person = Column(String, index=True)
    due_date = Column(DateTime(timezone=True))
    risk_rationale = Column(String)
    preliminary_root_cause = Column(String)
