# Shaheed Defender

Browser-playable missile-defense game with an optional terminal mode.

The browser version now renders with canvas-based pixel art using PNG sprite assets.
Generated sprite PNGs are not checked in; they are created by Docker build, VS Code launch, or automatically on first web-service startup.

## Quick Start

### Windows (PowerShell) Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python web_service.py
```

### macOS / Linux Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python web_service.py
```

Then open `http://127.0.0.1:8000`.

## Features

- Browser game served by Flask at `http://localhost:8000`
- Canvas renderer with PNG sprite art scaled to fit the viewport
- Per-browser game sessions
- Optional terminal (Textual) version
- Docker image support for easy deployment

## Prerequisites

- Python 3.13+
- pip
- Optional: Docker Desktop / Docker Engine

## Local Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment.
4. Install dependencies.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Web Service

```bash
python web_service.py
```

Open your browser to:

- `http://127.0.0.1:8000`

## Regenerate Starter Sprite Art

The starter browser art is generated as 64x64 PNG sprites from ASCII glyphs.

```bash
python generate_pixel_sprites.py
```

The generated files are written to `static/sprites/`.

## VS Code Launch

The included VS Code launch configurations regenerate sprites before starting either the web service or the terminal app.

- [/.vscode/launch.json](.vscode/launch.json)
- [/.vscode/tasks.json](.vscode/tasks.json)

## Run the Terminal Version (Optional)

```bash
python shaheed_defender.py
```

## Docker Setup

### Build the image

```bash
docker build -t shaheed-defender:latest .
```

### Run the container

```bash
docker run -d \
  --name shaheed-defender \
  -p 8000:8000 \
  -e SECRET_KEY="change-this-secret" \
  shaheed-defender:latest
```

### Open from browser

- Local machine: `http://127.0.0.1:8000`
- Other machines on your network: `http://<host-ip>:8000`

## Configuration

The web service supports these environment variables:

- `HOST` (default: `0.0.0.0`)
- `PORT` (default: `8000`)
- `FLASK_DEBUG` (`1` to enable debug mode)
- `SECRET_KEY` (recommended to set in non-dev use)

Example:

```bash
HOST=0.0.0.0 PORT=8080 SECRET_KEY=my-secret python web_service.py
```

## Exposing to Other Users

To allow other users to connect:

1. Run on `0.0.0.0` (already default in `web_service.py`).
2. Open firewall port `8000` on the host.
3. Share the host IP and port with users.
4. If users are outside your local network, configure router port forwarding or deploy to a cloud host.

## Troubleshooting

- Port already in use:
  - Change port with `PORT=8080` (or another free port).
- Browser cannot connect from another machine:
  - Check host firewall and verify both machines are on the same network.
- Missing dependency errors:
  - Re-activate your virtual environment and run `pip install -r requirements.txt` again.
