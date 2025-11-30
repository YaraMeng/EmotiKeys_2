# Backend — EmotiKeys (FastAPI)

This document explains how to run and develop the EmotiKeys backend (FastAPI) that serves both API endpoints and the frontend static files.

---

## Purpose

The backend provides:

- REST API endpoints used by the frontend (sessions, moods, generate notes, etc.)
- Static file hosting for the frontend directory (`head09_test`) via `StaticFiles`
- A Swagger/OpenAPI UI available at `/docs` for exploring APIs during development

Location: `backend/app/` contains the FastAPI application. The backend mounts `head09_test` as static files so the project can be served from a single process.

## Quick start (local development)

1.  Open a terminal at the repository root:

```powershell
cd "D:\PolyU\semester_1\SD5913 programming\EmotiKeys_2_myy\EmotiKeys_2"
```

2.  Activate the virtual environment and install dependencies (if not already installed):

```powershell
# activate
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

3.  Run the backend using uvicorn (development mode):

```powershell
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Notes:

- `--reload` enables auto-reload on source changes (dev only).
- `--host 0.0.0.0` allows other devices on your LAN to access the service.
- The backend is configured to serve static files from the `head09_test` folder. Access the app in a browser at `http://localhost:8000`.

## API documentation

- Interactive OpenAPI / Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` (if enabled)

Use the docs to inspect available routes such as `/moods`, `/scale`, and session-related endpoints. The frontend uses these endpoints to retrieve scale/mood data and to post session/cell events.

## Important files

- `backend/app/main.py` — FastAPI app setup, CORS, static files mount, and router includes.
- `backend/app/routes/` — API route modules (moods, generate_notes, sessions).
- `head09_test/` — Frontend static files served by the backend (index.html, app.js, styles.css, assets/).
- `requirements.txt` — Python dependency list for the project (root-level).

## Development notes

- When changing frontend static files, you do not need a separate `python -m http.server`; the backend serves those files when running uvicorn as above.
- If you previously had a generator script (`te09.py`) that produces `app.js`, avoid running it unless you intend to regenerate/overwrite the hand-edited `app.js`.

## Testing

If there are tests in the repository, run them from the project root. Example (pytest):

```powershell
pytest
```

Adjust to your test setup if needed.

## Running with HTTPS (optional, for testing secure context)

Browsers require a secure context for microphone and screen-capture APIs when accessed over a network. If you need LAN devices to be able to record audio, consider enabling HTTPS for local development.

Quick dev approach (self-signed cert):

1.  Generate a self-signed certificate (PowerShell example uses OpenSSL or other tool).
2.  Start uvicorn with TLS:

```powershell
uvicorn backend.app.main:app --host 0.0.0.0 --port 8443 --ssl-keyfile path/to/key.pem --ssl-certfile path/to/cert.pem
```

3.  Access `https://<server-ip>:8443` from the client device and accept the self-signed cert (browser will warn).

For production, use a proper CA-signed certificate and a reverse proxy (nginx, Caddy, Traefik) to terminate TLS.

## Deployment suggestions

- Use a process manager (systemd, pm2, supervisor) or containerize the app (Docker) and run behind a reverse proxy.
- Expose only necessary ports and add firewall rules.
- For multi-instance deployments, consider a shared storage or database for session persistence if sessions are required to survive process restarts or load balancing.

## Troubleshooting

- If the frontend is not loading the latest `app.js`, clear browser cache or open DevTools and enable "Disable cache" while reloading.
- If microphone access is denied in the browser when accessing via IP, try `http://localhost:8000` on the server machine first to confirm behavior locally.
- If uvicorn fails to start due to port conflict, choose a different `--port` or stop the process using that port.