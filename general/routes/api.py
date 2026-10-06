from flask import Blueprint

api_bp = Blueprint("api", __name__)
# 기존 Day1 JSON 주소와 응답을 유지합니다.
POSTS = {
    1: {"id": 1, "title": "첫 번째 공지", "body": "일반 서비스를 준비합니다."},
    2: {"id": 2, "title": "실습 안내", "body": "게시글 번호를 바꿔 보세요."},
}

@api_bp.get("/posts/<int:post_id>")
def get_post(post_id):
    post = POSTS.get(post_id)
    if post is None:
        return {"error": "POST_NOT_FOUND"}, 404
    return post, 200
