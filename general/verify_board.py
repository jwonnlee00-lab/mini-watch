"""실제 PostgreSQL CRUD 및 실제 HTTP 감시 전송 검증. 만든 테스트 글만 삭제합니다."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
from uuid import uuid4
from werkzeug.serving import make_server
from app import create_app
from repositories import posts


def verify():
    created = []
    checks = []
    def check(name, passed):
        if not passed:
            raise AssertionError(name)
        checks.append(name)
        print("PASS", name)
    root = Path(__file__).parent.parent
    marker = "verify-" + uuid4().hex
    with tempfile.TemporaryDirectory() as directory:
        os.environ["REQUEST_LOG_PATH"] = str(Path(directory) / "requests.jsonl")
        spec = importlib.util.spec_from_file_location("test_monitor", root / "monitor/backend/app.py")
        monitor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(monitor)
        monitor.log_path = Path(directory) / "events.jsonl"
        server = make_server("127.0.0.1", 0, monitor.app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        os.environ["MONITOR_LOG_URL"] = f"http://127.0.0.1:{server.server_port}/events"
        app = create_app()
        app.testing = True
        client = app.test_client()
        try:
            count = len(posts.list_posts())
            check("목록·작성 화면", client.get("/").status_code == 200 and client.get("/board/new").status_code == 200)
            for data in [{"title": " ", "body": marker}, {"title": marker, "body": " "}, {}]:
                response = client.post("/board/new", data=data)
                check("잘못된 작성 400·DB 행 증가 없음", response.status_code == 400 and len(posts.list_posts()) == count)
            response = client.post("/board/new", data={"title": " " + marker + " ", "body": " 원래 내용 "})
            check("작성 303", response.status_code == 303)
            post_id = int(response.location.rsplit("/", 1)[1])
            created.append(post_id)
            post = posts.find_post(post_id)
            check("실제 INSERT·시퀀스·공백 제거", post["title"] == marker and post["body"] == "원래 내용")
            check("목록·상세 연결", f"/board/{post_id}" in client.get("/").text and marker in client.get(response.location).text)
            client.get(response.location)
            check("상세 새로고침 중복 없음", len(posts.list_posts()) == count + 1)
            other_client = create_app().test_client()
            check("앱 재생성·새 DB 연결에서 저장 내용 유지", marker in other_client.get(response.location).text)
            check("수정 폼 기존 값", marker in client.get(f"/board/{post_id}/edit").text)
            response = client.post(f"/board/{post_id}/edit", data={"title": " ", "body": "입력값"})
            check("잘못된 수정 400·입력값 표시·DB 보존", response.status_code == 400 and "입력값" in response.text and posts.find_post(post_id)["body"] == "원래 내용")
            client.get(f"/board/{post_id}/edit")
            check("수정 GET만으로 DB 변경 없음", posts.find_post(post_id)["title"] == marker)
            response = client.post(f"/board/{post_id}/edit", data={"title": marker + "-edited", "body": "새 내용"})
            check("UPDATE·303·목록과 상세 반영", response.status_code == 303 and marker + "-edited" in client.get("/").text and "새 내용" in client.get(response.location).text)
            response = client.get(f"/board/{post_id}/delete")
            check("삭제 GET·취소 링크·글 보존", response.status_code == 200 and f'href="/board/{post_id}"' in response.text and posts.find_post(post_id) is not None)
            response = client.post(f"/board/{post_id}/delete")
            check("DELETE·303·목록 제거", response.status_code == 303 and response.location == "/" and posts.find_post(post_id) is None and marker not in client.get("/").text)
            for method, suffix in [("get", ""), ("get", "/edit"), ("get", "/delete"), ("post", "/edit"), ("post", "/delete")]:
                check("삭제 후 " + method + suffix + " 404", getattr(client, method)(f"/board/{post_id}{suffix}").status_code == 404)
            check("기존 JSON API 보존", client.get("/posts/1").json["title"] == "첫 번째 공지" and client.get("/posts/999999").status_code == 404)
            events = [json.loads(line) for line in monitor.log_path.read_text(encoding="utf-8").splitlines()]
            check("실제 HTTP JSON 감시 수집", any(e["path"] == f"/board/{post_id}" and e["status"] == 404 for e in events))
            check("로컬 요청 기록", Path(directory, "requests.jsonl").exists())
            print(f"총 {len(checks)}개 검증 통과")
        finally:
            for post_id in created:
                posts.delete_post(post_id)
            server.shutdown()
            thread.join()
            server.server_close()


if __name__ == "__main__":
    try:
        verify()
    except Exception as exc:
        print("검증 실패:", str(exc), file=sys.stderr)
        print("PostgreSQL 실행, .env 설정, python prepare_db.py 결과를 확인하세요.", file=sys.stderr)
        sys.exit(1)
