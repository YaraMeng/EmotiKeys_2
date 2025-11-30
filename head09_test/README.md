# head09_test — Frontend (static assets)

This folder contains the frontend static assets for the application. The backend mounts this directory with `StaticFiles` (see `backend/app/main.py`). This README is intended as a quick reference for frontend maintenance and local debugging.

## Structure

- `index.html` — frontend entry page
- `app.js` — main JavaScript logic (audio synthesis / interaction)
- `styles.css` — stylesheet
- `assets/` — images, icons, logo and other static assets

## Quick preview (static only)

If you only want to quickly preview the static site (without the backend), you can run a simple static server in this folder:

```powershell
cd head09_test
python -m http.server 8000
# then open http://localhost:8000 in your browser
```

However, the recommended approach is to serve the frontend via the backend (see below).

## Recommended: run via backend (development / integration)

The backend mounts this directory as static files. From the repository root, run:

```powershell
# activate virtual environment
.\.venv\Scripts\Activate.ps1

# start backend (development)
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
# then open http://localhost:8000
```

Advantages:

- Frontend and backend are served from the same host; API requests (using relative paths) automatically target the correct server.
- Avoids cross-origin/CORS issues during development.

## Common operations & notes

- Editing `app.js`: the project sets `API_BASE` to an empty string (`''`), so API calls are sent to the same host that serves the page (recommended). If you change it to a fixed IP, make sure that host is reachable.
- If you previously used a generator script (e.g. `te09.py`) to produce `app.js`, avoid re-running it after manual edits unless you want to overwrite your changes.
- Add or replace `assets/logo.png` to change the browser tab icon — `index.html` already references the favicon.

## Audio debugging (no sound / cannot record)

1. Prefer local (localhost) testing: browsers require a secure context for microphone and screen-capture APIs. To verify audio recording/playback, open the app on the server machine using `http://localhost:8000`.
2. LAN access limitations: accessing via IP (e.g. `http://192.168.x.y:8000`) may restrict microphone or autoplay behavior in some browsers. To enable these features from other devices, use HTTPS (self-signed or CA certificate).
3. AudioContext requires user interaction: browsers allow AudioContext to start only after a user gesture. `app.js` implements logic to start audio on the first user interaction.

## Cache & debugging

- If changes to `app.js` or `styles.css` do not appear, clear the browser cache or enable “Disable cache” in the DevTools Network tab and reload.
- Keep the browser console (F12) open during development to see errors (CORS, 404s, JS exceptions).

## Deployment tips

- In production, put a reverse proxy (nginx, Caddy) in front to provide HTTPS; the backend can then focus on APIs and static files. HTTPS resolves cross-device recording/screen-capture security restrictions.

## Helpful commands

```powershell
# start backend and serve frontend
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# local static preview (optional)
python -m http.server 8000
```

---

If you want, I can:

- add a `run-local.ps1` in `head09_test/` to quickly start a local static server;
- or create a `run-dev.ps1` script at the repository root to activate the venv and run uvicorn with one command;
- or convert the troubleshooting notes into a small FAQ.

Tell me which enhancement you'd like next.
