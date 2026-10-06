from db import connect_db


def _post(row):
    # 기존 connect_db()가 tuple을 반환해도 사용할 수 있습니다.
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(zip(("id", "title", "body"), row))


def list_posts():
    with connect_db() as conn:
        rows = conn.execute("SELECT id, title, body FROM posts ORDER BY id ASC").fetchall()
    return [_post(row) for row in rows]


def find_post(post_id):
    with connect_db() as conn:
        row = conn.execute("SELECT id, title, body FROM posts WHERE id = %s", (post_id,)).fetchone()
    return _post(row)


def create_post(title, body):
    with connect_db() as conn:
        row = conn.execute(
            "INSERT INTO posts (title, body) VALUES (%s, %s) RETURNING id",
            (title, body),
        ).fetchone()
    return row["id"] if isinstance(row, dict) else row[0]


def update_post(post_id, title, body):
    with connect_db() as conn:
        row = conn.execute(
            "UPDATE posts SET title = %s, body = %s WHERE id = %s RETURNING id, title, body",
            (title, body, post_id),
        ).fetchone()
    return _post(row)


def delete_post(post_id):
    with connect_db() as conn:
        row = conn.execute(
            "DELETE FROM posts WHERE id = %s RETURNING id, title, body", (post_id,)
        ).fetchone()
    return _post(row)
