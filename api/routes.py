# qms-backend/api/routes.py

import os
import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
import httpx
from sqlalchemy.orm import Session
from datetime import datetime, date

# Import the Pydantic models from the models directory
from models.event import QMSEvent, AIPrompt
from database import get_db
from models.event import Event

# Create an APIRouter instance. This is like a mini-FastAPI app.
router = APIRouter()

# --- AI Assistance Endpoint ---

@router.post("/ai/assist")
async def get_ai_assistance(payload: AIPrompt):
    # Ensure all event date fields are Python date objects for AI context
    def parse_date(val):
        if not val:
            return None
        if isinstance(val, date):
            return val
        try:
            return datetime.strptime(val, "%Y-%m-%dT%H:%M:%S").date()
        except Exception:
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except Exception:
                return None

    def fix_event_dates(event):
        event = dict(event)
        for k in ["event_date", "due_date", "date"]:
            if k in event:
                event[k] = parse_date(event[k])
        return event
    """
    Receives a prompt and event data, sends it to the Gemini API,
    and returns the AI's response.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found in .env file.")

    system_prompt = (
        "You are an expert AI assistant for a Quality Management System (QMS) in a life sciences company. "
        "Your role is to analyze the provided QMS event data and answer user questions accurately and concisely. "
        f"The current date is {date.today().strftime('%B %d, %Y')}. The data is provided as a JSON list of events."
    )
    
    events_as_dicts = [fix_event_dates(event) if isinstance(event, dict) else fix_event_dates(event.dict()) for event in payload.events_context]
    full_prompt = f"{system_prompt}\n\nHere is the current list of QMS events:\n{events_as_dicts}\n\nUser's request: '{payload.prompt}'"
    
    gemini_payload = {"contents": [{"role": "user", "parts": [{"text": full_prompt}]}]}
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=gemini_payload, headers={'Content-Type': 'application/json'}, timeout=30.0)
            response.raise_for_status()
            result = response.json()

            if (result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts") and result["candidates"][0]["content"]["parts"][0].get("text")):
                return {"response": result["candidates"][0]["content"]["parts"][0]["text"]}
            else:
                raise HTTPException(status_code=500, detail="Invalid response structure from AI service.")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"AI service request failed: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# --- Database Event Endpoint ---

@router.post("/events", response_model=dict)
def create_event(event: dict, db: Session = Depends(get_db)):
    # Convert string date fields to Python date objects if needed
    def parse_date(val):
        if not val:
            return None
        if isinstance(val, date):
            return val
        try:
            # Try parsing as full datetime first
            return datetime.strptime(val, "%Y-%m-%dT%H:%M:%S").date()
        except Exception:
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except Exception:
                return None

    event_date = parse_date(event.get('event_date'))
    due_date = parse_date(event.get('due_date'))

    new_event = Event(
        title=event['title'],
        description=event.get('description', ''),
        event_type=event.get('event_type'),
        status=event.get('status'),
        initiator=event.get('initiator'),
        department=event.get('department'),
        reporter=event.get('reporter'),
        severity=event.get('severity'),
        priority=event.get('priority'),
        event_date=event_date,
        responsible_person=event.get('responsible_person'),
        due_date=due_date,
        risk_rationale=event.get('risk_rationale'),
        preliminary_root_cause=event.get('preliminary_root_cause'),
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return {
        "id": new_event.id,
        "title": new_event.title,
        "description": new_event.description,
        "event_type": new_event.event_type,
        "status": new_event.status,
        "initiator": new_event.initiator,
        "department": new_event.department,
        "reporter": new_event.reporter,
        "severity": new_event.severity,
        "priority": new_event.priority,
        "event_date": new_event.event_date,
        "responsible_person": new_event.responsible_person,
        "due_date": new_event.due_date,
        "risk_rationale": new_event.risk_rationale,
        "preliminary_root_cause": new_event.preliminary_root_cause,
        "date": new_event.date
    }

@router.get("/events", response_model=List[dict])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return [{
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_type": event.event_type,
        "status": event.status,
        "initiator": event.initiator,
        "department": event.department,
        "reporter": event.reporter,
        "severity": event.severity,
        "priority": event.priority,
        "event_date": event.event_date,
        "responsible_person": event.responsible_person,
        "due_date": event.due_date,
        "risk_rationale": event.risk_rationale,
        "preliminary_root_cause": event.preliminary_root_cause,
        "date": event.date
    } for event in events]

@router.get("/events/{event_id}", response_model=dict)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_type": event.event_type,
        "status": event.status,
        "initiator": event.initiator,
        "department": event.department,
        "reporter": event.reporter,
        "severity": event.severity,
        "priority": event.priority,
        "event_date": event.event_date,
        "responsible_person": event.responsible_person,
        "due_date": event.due_date,
        "risk_rationale": event.risk_rationale,
        "preliminary_root_cause": event.preliminary_root_cause,
        "date": event.date
    }

@router.put("/events/{event_id}", response_model=dict)
def update_event(event_id: int, event_data: dict, db: Session = Depends(get_db)):
    """Update an existing event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update event fields
    if 'title' in event_data:
        event.title = event_data['title']
    if 'description' in event_data:
        event.description = event_data['description']
    if 'event_type' in event_data:
        event.event_type = event_data['event_type']
    if 'status' in event_data:
        event.status = event_data['status']
    if 'initiator' in event_data:
        event.initiator = event_data['initiator']
    if 'department' in event_data:
        event.department = event_data['department']
    if 'reporter' in event_data:
        event.reporter = event_data['reporter']
    if 'severity' in event_data:
        event.severity = event_data['severity']
    if 'priority' in event_data:
        event.priority = event_data['priority']
    if 'event_date' in event_data:
        event.event_date = event_data['event_date']
    if 'responsible_person' in event_data:
        event.responsible_person = event_data['responsible_person']
    if 'due_date' in event_data:
        event.due_date = event_data['due_date']
    if 'risk_rationale' in event_data:
        event.risk_rationale = event_data['risk_rationale']
    if 'preliminary_root_cause' in event_data:
        event.preliminary_root_cause = event_data['preliminary_root_cause']
    
    db.commit()
    db.refresh(event)
    
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_type": event.event_type,
        "status": event.status,
        "initiator": event.initiator,
        "department": event.department,
        "reporter": event.reporter,
        "severity": event.severity,
        "priority": event.priority,
        "event_date": event.event_date,
        "responsible_person": event.responsible_person,
        "due_date": event.due_date,
        "risk_rationale": event.risk_rationale,
        "preliminary_root_cause": event.preliminary_root_cause,
        "date": event.date
    }
