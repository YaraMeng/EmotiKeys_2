# Simple scale definitions used by /scale endpoint
SCALES = {
    "C_ionian": {
        "name": "C_ionian",
        "notes": [60, 62, 64, 65, 67, 69, 71],
        "suggested_octaves": [3, 4, 5],
    },
    "G_pentatonic": {
        "name": "G_pentatonic",
        "notes": [55, 57, 59, 62, 64],
        "suggested_octaves": [3, 4],
    },
    "E_phrygian": {
        "name": "E_phrygian",
        "notes": [64, 65, 67, 69, 71, 72, 74],
        "suggested_octaves": [4, 5],
    },
    "A_aeolian": {
        "name": "A_aeolian",
        "notes": [57, 59, 60, 62, 64, 65, 67],
        "suggested_octaves": [3, 4],
    },
    "D_dorian": {
        "name": "D_dorian",
        "notes": [62, 64, 65, 67, 69, 71, 72],
        "suggested_octaves": [3, 4],
    },
    # Front-end fallback scales (explicitly added to backend)
    "C_major": {
        "name": "C_major",
        "notes": [60, 62, 64, 65, 67, 69, 71, 72],
        "type": "major",
        "suggested_octaves": [3, 4],
    },
    "G_major": {
        "name": "G_major",
        "notes": [55, 57, 59, 60, 62, 64, 66, 67],
        "type": "major",
        "suggested_octaves": [3, 4],
    },
    "E_minor": {
        "name": "E_minor",
        "notes": [52, 54, 55, 57, 59, 60, 62, 64],
        "type": "minor",
        "suggested_octaves": [3, 4],
    },
    "A_minor": {
        "name": "A_minor",
        "notes": [57, 59, 60, 62, 64, 65, 67, 69],
        "type": "minor",
        "suggested_octaves": [3, 4],
    },
}
