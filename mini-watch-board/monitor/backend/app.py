"""기존 감시 서비스가 없는 새 테스트 프로젝트용 수집 서버입니다."""
import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from flask import Flask, jsonify, request

app = Flask(__name__)
log_path = Path(__file__).parent / "logs" / "events.jsonl"
lock = Lock()

@app.post("/events")
def collect():
    event = request.get_json(silent=True)
    if not isinstance(event, dict) or not {"method", "path", "status"}.issubset(event):
        return jsonify(error="요청 기록 형식이 잘못되었습니다."), 400
    event["received_at"] = datetime.now(timezone.utc).isoformat()
    with lock:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")
    return jsonify(received=True), 201

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5200)
