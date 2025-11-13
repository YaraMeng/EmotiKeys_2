import pytest
from httpx import AsyncClient
from backend.app.main import app


@pytest.mark.asyncio
async def test_get_moods():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/moods")
        assert r.status_code == 200
        data = r.json()
        assert "happy" in data


@pytest.mark.asyncio
async def test_get_scale_existing():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/scale?name=C_ionian")
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "C_ionian"


@pytest.mark.asyncio
async def test_get_scale_notfound():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/scale?name=NONEXISTENT")
        assert r.status_code == 404
