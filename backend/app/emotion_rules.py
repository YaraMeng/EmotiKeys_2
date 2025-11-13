from typing import Dict
from .data import scales

# Minimal emotion styles (kept in sync with routes/moods.py)
MOODS = {
    "happy": {"bpm": 115, "step": 4, "scale": "C_ionian", "vel": [80, 100], "legato": 0.9, "palette": ["#FFD54F", "#FF8A65"]},
    "calm": {"bpm": 78, "step": 6, "scale": "G_pentatonic", "vel": [55, 75], "legato": 1.2, "palette": ["#B2DFDB", "#80CBC4"]},
    "tense": {"bpm": 140, "step": 1, "scale": "E_phrygian", "vel": [70, 95], "legato": 0.5, "palette": ["#FF5252", "#FF1744"]},
    "sad": {"bpm": 88, "step": 3, "scale": "A_aeolian", "vel": [50, 70], "legato": 0.95, "palette": ["#90A4AE", "#546E7A"]},
    "excited": {"bpm": 145, "step": 2, "scale": "D_dorian", "vel": [85, 110], "legato": 0.8, "palette": ["#D05CE3", "#FF4081"]},
}


def get_emotion_style(emotion: str) -> Dict:
    if emotion not in MOODS:
        raise KeyError(f"Unknown emotion: {emotion}")
    return MOODS[emotion]


def map_cell_to_note(x: int, y: int, emotion: str, intensity: float, grid_width: int, grid_height: int) -> Dict:
    if grid_width <= 1 or grid_height <= 1:
        raise ValueError("grid_width and grid_height must be > 1")
    intensity = max(0.0, min(1.0, float(intensity)))

    style = get_emotion_style(emotion)
    scale_name = style["scale"]
    scale_entry = scales.SCALES.get(scale_name)
    if not scale_entry:
        scale_entry = scales.SCALES["C_ionian"]

    notes = scale_entry["notes"]
    degree = int((x / (grid_width - 1)) * (len(notes) - 1))
    degree = max(0, min(len(notes) - 1, degree))

    octave_offset = int((y / (grid_height - 1)) * 2)
    octave_offset = max(0, min(2, octave_offset))

    pitch = notes[degree] + octave_offset * 12

    minv, maxv = style.get("vel", [60, 100])
    velocity = int(round(minv + intensity * (maxv - minv)))

    bpm = style.get("bpm", 90)
    step = max(1, style.get("step", 4))
    legato = style.get("legato", 1.0)
    duration = round((60.0 / bpm) * (1.0 / step) * legato, 4)

    return {"pitch": int(pitch), "velocity": int(velocity), "duration": float(duration)}
