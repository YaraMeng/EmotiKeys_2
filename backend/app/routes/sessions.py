from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from uuid import uuid4

router = APIRouter()


class CreateSessionRequest(BaseModel):
    grid_width: int
    grid_height: int


class CellEvent(BaseModel):
    x: int
    y: int
    value: Optional[Any] = None


# Simple in-memory session store (ephemeral)
SESSIONS: Dict[str, Dict[str, Any]] = {}


@router.post("/sessions")
async def create_session(payload: CreateSessionRequest):
    session_id = str(uuid4())
    SESSIONS[session_id] = {
        "grid_width": payload.grid_width,
        "grid_height": payload.grid_height,
        "cells": [],
    }
    return {"session_id": session_id}


@router.post("/sessions/{session_id}/cells")
async def add_cells(session_id: str, events: List[CellEvent]):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="session not found")
    for ev in events:
        SESSIONS[session_id]["cells"].append(ev.dict())
    return {"status": "ok", "count": len(events)}


@router.post("/sessions/{session_id}/clear")
async def clear_session(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="session not found")
    SESSIONS[session_id]["cells"] = []
    return {"status": "cleared"}
