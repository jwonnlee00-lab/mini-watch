# 검증 결과

Python 문법 검사와 Flask test_client를 이용한 동작 검증을 통과했습니다.
DB 저장소는 메모리 대역으로 교체하여 HTTP·화면 흐름을 검증했습니다.
PostgreSQL 서버가 없어 실제 SQL 실행, commit·rollback, 시퀀스 생성과 재시작 후 영속성은 검증하지 않았습니다.
감시 서버는 실제 로컬 HTTP 서버로 실행하여 requests의 JSON 전송과 파일 수집을 확인했습니다.
GitHub의 기존 /posts JSON API를 분리해 유지했고 정상 글과 없는 글의 응답을 검증했습니다.
PC에만 있는 최신 수업 파일은 제공되지 않아 비교하지 못했습니다.

## 통과 항목

- 빈 목록 안내
- 작성 GET
- 잘못된 작성 400 및 DB 변경 없음
- 잘못된 작성 400 및 DB 변경 없음
- 잘못된 작성 400 및 DB 변경 없음
- 작성 303 및 공백 제거
- 상세·목록 표시
- 상세 새로고침 중복 없음
- 수정 폼 기존 값
- 수정 오류 400·입력 재표시·기존 값 유지
- 수정 303 및 내용 반영
- 삭제 확인 GET 보존 및 취소 링크
- 삭제 303 목록 이동
- 삭제 후 get /board/1 404
- 삭제 후 get /board/1/edit 404
- 삭제 후 get /board/1/delete 404
- 삭제 후 post /board/1/edit 404
- 삭제 후 post /board/1/delete 404
- Jinja 자동 HTML 이스케이프
- CSS 제공
- 로컬 JSONL 기록
- requests 실제 HTTP JSON 전송 및 감시 파일 수집

## 추가 완료

- 제출 구조인 루트 general/과 monitor/backend/로 통합.
- 기존 JSON API 정상 응답과 없는 글 404 유지 확인.
- 사용자 승인 가상 general/.env 포함.
- prepare_db.py: 없는 DB·테이블 생성, 기존 데이터·시퀀스 유지.
- verify_board.py: 실제 PostgreSQL CRUD·새 앱 인스턴스 조회·실제 HTTP 감시 전송 검사 제공.
- start-board.ps1: 가상환경 → 설치 → DB 준비 → 검증 → 두 서버 실행 제공.
- 실제 PostgreSQL 검증 실행은 127.0.0.1:5432 연결 거부로 실패. 통과로 표기하지 않음.
- 자동 DB 검증·PowerShell 실행은 사용자의 Windows/PostgreSQL 환경에서 확인 필요.
- 서버 종료·재시작 후 영속성과 브라우저 시각 확인은 직접 확인 필요.

## 체크리스트 32개

구현은 소스 확인이며 실제 DB 검증 통과와 구분합니다.

| 번호 | 기준 | 결과 |
|---:|---|---|
|1|소스 문법|검사 통과|
|2|목록·상세 HTML|구현|
|3|폼 요소|구현|
|4|공통 CSS|구현|
|5|Jinja 출력|구현|
|6|반복문·조건문|구현|
|7|라우팅·GET/POST|DB 대역 검증 통과|
|8|request.form·render_template|구현|
|9|입력 검사·DB 보존|DB 대역 검증 통과, 실제 DB 확인 필요|
|10|400·404·303|DB 대역 검증 통과|
|11|PostgreSQL 저장·재시작 영속성|구현, 실제 DB 확인 필요|
|12|psycopg.connect|구현, 실제 연결 확인 필요|
|13|.env·dotenv|구현·가상 설정 포함|
|14|execute CRUD SQL|구현, 실제 SQL 확인 필요|
|15|fetchall·fetchone|구현|
|16|%s 매개변수|구현|
|17|시퀀스·RETURNING id|구현, 실제 DB 확인 필요|
|18|일반·감시 폴더 분리|구현|
|19|app 역할 분리|구현|
|20|공통 DB 연결|구현|
|21|저장소 SQL 분리|구현|
|22|Blueprint|구현|
|23|데이터와 HTTP 역할 분리|구현|
|24|공통 입력 규칙|구현|
|25|templates·static·sql|구현|
|26|요청 기록 모듈·등록|구현|
|27|패키지·import·실행|확인|
|28|가상환경·requirements|가상환경에서 동작 확인|
|29|링크·버튼 CRUD·취소|템플릿·응답 확인|
|30|requests JSON 감시 수집|실제 HTTP 검증 통과|
|31|분리 후 기존 기능 유지|기존 GitHub API와 대역 CRUD 확인, PC 최신 코드·실제 DB 확인 필요|
|32|Git 커밋|GitHub 테스트 브랜치 반영|
