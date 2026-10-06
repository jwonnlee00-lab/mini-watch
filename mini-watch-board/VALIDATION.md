# 검증 결과

Python 문법 검사와 Flask test_client를 이용한 동작 검증을 통과했습니다.
DB 저장소는 메모리 대역으로 교체하여 HTTP·화면 흐름을 검증했습니다.
PostgreSQL 서버가 없어 실제 SQL 실행, commit·rollback, 시퀀스 생성과 재시작 후 영속성은 검증하지 않았습니다.
감시 서버는 실제 로컬 HTTP 서버로 실행하여 requests의 JSON 전송과 파일 수집을 확인했습니다.
기존 수업 감시 서버와의 호환성은 기존 코드 제공 후 확인해야 합니다.

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
