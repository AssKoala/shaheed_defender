from __future__ import annotations

import os
import time
import uuid

from flask import Flask, jsonify, render_template, request, session

from game_engine import GameEngine

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "shaheed-defender-local-dev")

_sessions: dict[str, dict[str, object]] = {}


def _get_or_create_game() -> dict[str, object]:
    sid = session.get("sid")
    if not sid:
        sid = str(uuid.uuid4())
        session["sid"] = sid
    data = _sessions.get(sid)
    if data is None:
        data = {"engine": GameEngine(), "last_update": time.monotonic()}
        _sessions[sid] = data
    return data


def _advance_game(data: dict[str, object]) -> None:
    now = time.monotonic()
    last = float(data["last_update"])
    elapsed = now - last
    steps = min(10, max(0, int(elapsed / 0.05)))
    engine = data["engine"]
    for _ in range(steps):
        engine.tick()
    data["last_update"] = now


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/state")
def state():
    data = _get_or_create_game()
    _advance_game(data)
    engine = data["engine"]
    return jsonify(engine.state())


@app.post("/api/action")
def action():
    payload = request.get_json(silent=True) or {}
    data = _get_or_create_game()
    _advance_game(data)
    engine = data["engine"]
    action_name = str(payload.get("action", "")).lower()

    if action_name == "move":
        dx = int(payload.get("dx", 0))
        dy = int(payload.get("dy", 0))
        engine.move_cursor(dx, dy)
    elif action_name == "fire":
        engine.fire()
    elif action_name == "click_fire":
        x = int(payload.get("x", engine.cx))
        y = int(payload.get("y", engine.cy))
        engine.click_fire(x, y)

    return jsonify(engine.state())


@app.post("/api/restart")
def restart():
    data = _get_or_create_game()
    engine = data["engine"]
    engine.reset()
    data["last_update"] = time.monotonic()
    return jsonify(engine.state())


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)