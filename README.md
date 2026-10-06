# mini-watch — PostgreSQL 게시판

기존 `/posts/<번호>` JSON API를 유지하며 `general`에 게시판 CRUD를 추가했습니다.
이번 과제의 가상 DB 설정은 사용자 승인으로 `general/.env`에 포함했습니다.
이 서버는 로컬 실습용입니다. 선택 과제인 로그인은 이번 저장소에 없으며 추가하지 않았습니다.

## 한 번에 실행

PostgreSQL을 실행한 뒤 다운로드한 폴더에서 PowerShell로 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\start-board.ps1
```

가상환경·패키지·DB 준비·실제 DB 검증이 성공하면 감시 서버와 게시판을 실행합니다.
이미 5100 또는 5200을 사용하는 서버가 있으면 먼저 종료하세요.
브라우저가 서버보다 먼저 열려 연결 오류가 뜨면 잠시 뒤 새로고침하세요.

## Windows 수동 실행

`board-crud-test` 브랜치 코드를 다운로드하거나 다음처럼 받으세요.

```powershell
git clone --branch board-crud-test https://github.com/jwonnlee00-lab/mini-watch.git
cd mini-watch
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r general/requirements.txt
cd general
python prepare_db.py
python verify_board.py
python app.py
```

PostgreSQL이 `127.0.0.1:5432`, 계정 `postgres`, 비밀번호 `1234`로 실행 중이어야 합니다.
`prepare_db.py`는 general_db가 없으면 생성하고, posts가 없으면 생성합니다.
기존 테이블·행·시퀀스를 삭제하거나 초기화하지 않습니다.
기존 posts에 시퀀스가 없으면 오류로 알리며 기존 설정을 임의로 변경하지 않습니다.
이미 같은 이름의 DB가 있고 접근 권한이 없다면 접속 설정을 수정하세요.

http://127.0.0.1:5100/ 에서 게시판을 사용합니다.

감시 서비스를 계속 실행하려면 별도 터미널에서 프로젝트 루트 기준으로:

```powershell
.\venv\Scripts\Activate.ps1
cd monitor/backend
python app.py
```

게시글 요청은 `general/logs/requests.jsonl`과 `monitor/backend/logs/events.jsonl`에서 확인합니다.
`verify_board.py`는 테스트 감시 서버를 빈 포트에서 잠깐 실행하고 실제 PostgreSQL CRUD를 검사합니다.
검증 중 생성한 글만 삭제하며 기존 글은 수정·삭제하지 않습니다. 시퀀스 번호에 빈 번호가 생길 수 있습니다.
검증은 독립 테스트 환경에서 실행하세요. 동시에 다른 사용자가 글을 쓰면 행 개수 검증이 실패할 수 있습니다.

## 직접 완료 확인

목록 → 작성 → 상세 → 수정 → 상세 → 삭제 확인 → 취소 → 상세 → 삭제 확인 → 삭제 → 목록 순서로 사용하세요.
개발자 도구 Network에서 입력 오류 400, 없는 글 404, 저장·수정·삭제 303을 확인하세요.
정상 저장 뒤 서버를 종료하고 `python app.py`로 다시 실행해 글이 남는지 확인하세요.
실제 PC에서의 서버 종료·재시작과 시각적 화면 확인은 직접 확인 항목입니다.

## 코드 구조

- general/app.py: 앱 생성·설정·Blueprint·요청 기록 등록·실행
- general/db.py: 환경변수와 psycopg 연결
- general/post_rules.py: 공통 입력 검증
- general/repositories/posts.py: PostgreSQL CRUD
- general/routes/posts.py: 게시판 HTTP 처리
- general/routes/api.py: 기존 JSON API
- general/request_logging.py: 로컬 JSONL 기록과 requests 전송
- general/templates, static, sql: HTML·CSS·DB 준비 SQL
- monitor/backend/app.py: 감시 기록 수집

기존 저장소에 없던 DB·로그인·감시 코드와 PC에만 있는 최신 수업 파일의 호환성은 별도 확인해야 합니다.
GitHub에 확인된 기존 general/app.py와 requirements.txt의 기능은 유지했습니다.
중복 테스트 사본 mini-watch-board 폴더는 정리하고 루트 general만 사용합니다.

## Git

```powershell
git status
git add general monitor README.md VALIDATION.md .gitignore
git commit -m "Update board assignment"
git push origin board-crud-test
```

## 공식 근거

- Psycopg 연결 context manager의 정상 종료는 commit, 예외 종료는 rollback: https://www.psycopg.org/psycopg3/docs/basic/transactions.html
- PostgreSQL identity 컬럼은 내부 시퀀스로 번호 생성: https://www.postgresql.org/docs/17/ddl-identity-columns.html
