from typing import List, Optional, Dict
from fastapi import APIRouter
from pydantic import BaseModel

from ..emotion_rules import map_cell_to_note

router = APIRouter()


class Event(BaseModel):
    x: int
    y: int
    emotion: str
    intensity: float
    timestamp: Optional[str] = None


class GenerateRequest(BaseModel):
    session_id: Optional[str] = None
    events: Optional[List[Event]] = None
    grid_width: Optional[int] = 20
    grid_height: Optional[int] = 10


class Note(BaseModel):
    pitch: int
    velocity: int
    duration: float


class GenerateResponse(BaseModel):
    notes: List[Note]
    meta: Optional[Dict] = None


@router.post("/generate-notes", response_model=GenerateResponse)
async def generate_notes(req: GenerateRequest):
    notes = []
    source_event_index = []

    events = req.events or []
    if not events:
        return {"notes": [], "meta": {"info": "no events provided"}}

    gw = req.grid_width or 20
    gh = req.grid_height or 10

    for i, e in enumerate(events):
        try:
            n = map_cell_to_note(e.x, e.y, e.emotion, e.intensity, gw, gh)
            notes.append(n)
            source_event_index.append(i)
        except Exception:
            # skip invalid event but continue
            continue

    return {"notes": notes, "meta": {"source_event_index": source_event_index}}
