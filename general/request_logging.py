import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
import requests
from flask import g, request


def register_request_logging(app):
    @app.before_request
    def start_timer():
        g.request_started = time.perf_counter()

    @app.after_request
    def record_request(response):
        if request.endpoint == "static":
            return response
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": round((time.perf_counter() - g.request_started) * 1000, 2),
        }
        log_path = Path(os.getenv("REQUEST_LOG_PATH", "logs/requests.jsonl"))
        if not log_path.is_absolute():
            log_path = Path(app.root_path) / log_path
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(event, ensure_ascii=False) + "\n")
        except OSError:
            app.logger.exception("요청 기록 파일 저장 실패")
        target = os.getenv("MONITOR_LOG_URL", "")
        if target:
            try:
                requests.post(target, json=event, timeout=1).raise_for_status()
            except requests.RequestException:
                app.logger.warning("감시 서버 전송 실패: 로컬 요청 기록을 확인하세요.")
        return response
