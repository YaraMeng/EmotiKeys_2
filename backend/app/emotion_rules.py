from typing import Dict
from .data import scales

# Minimal emotion styles (kept in sync with routes/moods.py)
MOODS = {
    # Move frontend fallback (兜底) music rules into backend
    "happy": {"bpm": 120, "step": 1, "scale": "C_major", "vel": [70, 85], "legato": 0.7, "palette": ["#FFD54F", "#FF8A65"]},
    "calm": {"bpm": 80, "step": 2, "scale": "G_major", "vel": [50, 65], "legato": 1.2, "palette": ["#4FC3F7", "#81D4FA"]},
    "tense": {"bpm": 100, "step": 1, "scale": "E_minor", "vel": [60, 75], "legato": 0.5, "palette": ["#F44336", "#E57373"]},
    "sad": {"bpm": 70, "step": 2, "scale": "A_minor", "vel": [45, 60], "legato": 1.0, "palette": ["#5C6BC0", "#7986CB"]},
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
