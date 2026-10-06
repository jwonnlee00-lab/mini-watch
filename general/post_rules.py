def validate_post(title, body):
    title = (title or "").strip()
    body = (body or "").strip()
    error = "제목과 내용을 모두 입력해 주세요." if not title or not body else None
    return title, body, error
