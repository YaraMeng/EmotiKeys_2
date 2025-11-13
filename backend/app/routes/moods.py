from fastapi import APIRouter, HTTPException
from ..data import scales

router = APIRouter()

MOODS = {
    "happy": {"bpm": 115, "step": 4, "scale": "C_ionian", "vel": [80, 100], "legato": 0.9, "palette": ["#FFD54F", "#FF8A65"]},
    "calm": {"bpm": 78, "step": 6, "scale": "G_pentatonic", "vel": [55, 75], "legato": 1.2, "palette": ["#B2DFDB", "#80CBC4"]},
    "tense": {"bpm": 140, "step": 1, "scale": "E_phrygian", "vel": [70, 95], "legato": 0.5, "palette": ["#FF5252", "#FF1744"]},
    "sad": {"bpm": 88, "step": 3, "scale": "A_aeolian", "vel": [50, 70], "legato": 0.95, "palette": ["#90A4AE", "#546E7A"]},
    "excited": {"bpm": 145, "step": 2, "scale": "D_dorian", "vel": [85, 110], "legato": 0.8, "palette": ["#D05CE3", "#FF4081"]},
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
