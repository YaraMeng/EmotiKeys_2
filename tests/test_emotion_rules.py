import pytest
from backend.app.emotion_rules import get_emotion_style, map_cell_to_note


def test_get_emotion_style_happy():
    s = get_emotion_style("happy")
    assert s["bpm"] == 115
    assert s["scale"] == "C_ionian"


def test_map_cell_to_note_happy_corner():
    # left-top corner
    note = map_cell_to_note(x=0, y=0, emotion="happy", intensity=1.0, grid_width=20, grid_height=10)
    # degree=0 -> base note 60, octave_offset=0 -> pitch 60
    assert note["pitch"] == 60
    # intensity=1 -> max vel for happy is 100
    assert note["velocity"] == 100
    # duration computed from bpm/step/legato
    assert round(note["duration"], 4) == round((60.0 / 115) * (1.0 / 4) * 0.9, 4)


def test_map_cell_to_note_calm_middle():
    note = map_cell_to_note(x=10, y=5, emotion="calm", intensity=0.5, grid_width=20, grid_height=10)
    # for calm, vel range [55,75], intensity=0.5 -> 65
    assert note["velocity"] == 65
    # pitch should be an integer
    assert isinstance(note["pitch"], int)


def test_map_cell_to_note_tense_bottom_right():
    note = map_cell_to_note(x=19, y=9, emotion="tense", intensity=0.8, grid_width=20, grid_height=10)
    # tense scale exists and pitch is integer
    assert isinstance(note["pitch"], int)
    # velocity in expected range
    assert 70 <= note["velocity"] <= 95
