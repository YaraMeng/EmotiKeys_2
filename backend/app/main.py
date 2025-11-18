from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import moods, generate_notes

app = FastAPI(title="EmotiKeys Backend (dev)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(moods.router)
app.include_router(generate_notes.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "EmotiKeys backend"}
