from fastapi import APIRouter, HTTPException
from ..data import scales

router = APIRouter()

MOODS = {
    "happy": {"bpm": 120, "step": 1, "scale": "C_major", "vel": [70, 85], "legato": 0.7, "palette": ["#FFD54F", "#FF8A65"]},
    "calm": {"bpm": 80, "step": 2, "scale": "G_major", "vel": [50, 65], "legato": 1.2, "palette": ["#4FC3F7", "#81D4FA"]},
    "tense": {"bpm": 100, "step": 1, "scale": "E_minor", "vel": [60, 75], "legato": 0.5, "palette": ["#F44336", "#E57373"]},
    "sad": {"bpm": 70, "step": 2, "scale": "A_minor", "vel": [45, 60], "legato": 1.0, "palette": ["#5C6BC0", "#7986CB"]},
}


@router.get("/moods")
async def get_moods():
    return MOODS


@router.get("/scale")
async def get_scale(name: str):
    s = scales.SCALES.get(name)
    if not s:
        raise HTTPException(status_code=404, detail={"error": "scale not found", "name": name})
    return s
