"""없으면 DB와 posts를 만들고, 기존 테이블·시퀀스는 변경하지 않습니다."""
import os
from pathlib import Path
import psycopg
from psycopg import sql
from dotenv import load_dotenv
from db import connect_db


def prepare():
    load_dotenv(Path(__file__).with_name(".env"))
    db_name = os.getenv("DB_NAME", "general_db")
    # CREATE DATABASE는 트랜잭션 밖에서 실행해야 합니다.
    with psycopg.connect(host=os.getenv("DB_HOST", "127.0.0.1"),
                         port=os.getenv("DB_PORT", "5432"),
                         dbname="postgres", user=os.getenv("DB_USER", "postgres"),
                         password=os.getenv("DB_PASSWORD", ""), autocommit=True, connect_timeout=5) as conn:
        exists = conn.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,)).fetchone()
        if not exists:
            conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    with connect_db() as conn:
        conn.execute(Path(__file__).parent.joinpath("sql/01_create_posts.sql").read_text(encoding="utf-8"))
        row = conn.execute(
            "SELECT column_default, is_identity FROM information_schema.columns "
            "WHERE table_schema = current_schema() AND table_name = 'posts' AND column_name = 'id'"
        ).fetchone()
        if row is None or not (row["is_identity"] == "YES" or "nextval(" in (row["column_default"] or "")):
            raise RuntimeError("기존 posts.id에 시퀀스가 없습니다. 수업의 시퀀스 설정을 먼저 확인하세요.")
    print("DB와 posts 준비 완료. 기존 데이터와 시퀀스는 유지했습니다.")


if __name__ == "__main__":
    prepare()
