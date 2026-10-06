# 정원의 기록장 — Flask + PostgreSQL 게시판

필수 CRUD와 역할별 모듈 분리를 구현한 독립 테스트 프로젝트입니다.
기존 mini-watch 소스가 제공되지 않아 기존 코드와의 병합·호환 검증은 아직 하지 않았습니다.
선택 실습인 로그인은 포함하지 않았습니다. 기존 로그인 파일은 유지하세요.

## Windows PowerShell에서 새 테스트 프로젝트 실행

압축을 풀고 mini-watch-board 폴더에서 실행합니다.

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r general/requirements.txt
Copy-Item general/.env.example general/.env
```

`general/.env`에서 PostgreSQL의 DB_NAME, DB_USER, DB_PASSWORD를 실제 값으로 수정합니다.
비밀번호는 Git에 올리지 않습니다. DB_NAME은 이미 존재하는 DB여야 합니다.
새 테스트 DB를 만들려면 pgAdmin에서 Databases → Create → Database로 `mini_watch`를 만드세요.
해당 DB의 Query Tool에서 `general/sql/01_create_posts.sql`을 실행하세요.
기존 수업 DB의 posts 테이블에 연결한다면 준비 SQL을 다시 실행하지 않습니다.

첫 번째 터미널:

```powershell
cd monitor/backend
python app.py
```

두 번째 터미널(프로젝트 루트에서 가상환경 활성화):

```powershell
.\venv\Scripts\Activate.ps1
cd general
python app.py
```

http://127.0.0.1:5100/ 에 접속합니다.
감시 기록은 `monitor/backend/logs/events.jsonl`에 쌓입니다.
일반 서비스 로컬 기록은 `general/logs/requests.jsonl`에 쌓입니다.
감시 서버가 꺼져 있어도 로컬 기록을 저장하고 게시판 응답을 반환합니다.
전송은 동기 방식이고 요청당 최대 1초 대기할 수 있습니다. 운영용 큐·재전송은 범위 밖입니다.

## 기존 mini-watch에 합치기

먼저 기존 폴더를 백업하세요. 이 ZIP을 기존 프로젝트 전체에 덮어쓰지 마세요.

- 기존 `general/db.py`, `.env`, SQL, 연습 파일, 로그인 파일, `monitor` 폴더를 유지합니다.
- `post_rules.py`, `repositories/`, `routes/posts.py`, 게시판 템플릿과 CSS를 복사합니다.
- app.py의 기존 게시판 라우트를 제거하고 `posts_bp`를 import하여 `app.register_blueprint(posts_bp)`로 등록합니다. 로그인 라우트와 기타 설정은 유지합니다.
- 기존 요청 기록 코드를 `request_logging.py`로 옮기고 등록합니다. 제공된 예제는 `/events`로 JSON을 보내므로 기존 감시 서버 주소·JSON 필드가 다르면 그 규격에 맞춰 바꿔야 합니다. 기존 훅과 예제 훅을 함께 등록하면 중복 기록될 수 있습니다.
- 기존 connect_db()가 psycopg Connection을 반환하면 저장소 코드를 사용할 수 있습니다. 기본 tuple과 dict_row를 모두 처리합니다. 다른 row_factory는 별도 확인이 필요합니다.
- 같은 이름의 로그인용 템플릿이나 CSS가 있으면 내용을 병합하세요.
- 기존 requirements.txt에 필요한 패키지를 합칩니다.

정확한 병합에는 기존 app.py, db.py, 요청 기록 코드와 감시 수집 라우트가 필요합니다.

## 직접 확인

1. 빈 목록 안내 → 새 글 작성 → 상세 → 목록의 제목 링크 확인.
2. 저장 응답 303, 상세 새로고침 후 행 수가 늘지 않는지 확인.
3. 제목 또는 내용을 비우거나 공백만 보내면 400, 입력값 재표시, DB 미변경 확인.
4. 수정 GET의 기존 값, 저장 후 상세·목록 변경 확인. 수정 입력만 바꾸고 취소하면 원래 값 유지.
5. 삭제 GET과 취소로 행 유지 → 삭제 POST 303 → 목록에서 제거 확인.
6. 삭제된 글의 상세·수정·삭제 GET과 수정·삭제 POST가 404인지 확인.
7. 일반 서버를 재시작해도 데이터 유지, 감시 JSONL에서 method/path/status 확인.

브라우저 개발자 도구 Network에서 상태 코드를 확인합니다.
이 실습은 로컬 실행용이며 인증·CSRF 보호·공개 운영 설정은 포함하지 않았습니다.

## Git 저장

프로젝트 루트에서:

```powershell
git init
git add .
git status
git commit -m "Implement PostgreSQL board CRUD with Blueprint and request logging"
```

`git status`에 `.env`, venv, logs가 없는지 확인하세요.
기존 mini-watch 저장소에 합쳤다면 git init 없이 해당 저장소에서 커밋합니다.
GitHub에 올릴 때는 기존 원격 주소를 확인한 뒤 실제 저장소 주소로 push하세요.

## 검증 상태

`VALIDATION.md`에 이번 환경에서 실제 수행한 검증과 남은 검증을 기록했습니다.
