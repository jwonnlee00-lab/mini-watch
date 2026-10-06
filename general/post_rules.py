def validate_post(title, body):
    if not title or not body:
        return "제목과 본문을 빠짐없이 작성해 주세요."
    return None