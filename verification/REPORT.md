# 필수 20개 검증 보고서

검증일: 2026-10-12 (Asia/Seoul). 기준: 사용자가 첨부한 6교시 미션 전문의 필수 20개.
PASS는 실제 빌드·컨테이너·HTTP·브라우저·SQL 결과와 설정 확인을 함께 근거로 판정했다.
필수 결과: PASS 20 / FAIL 0 / NOT VERIFIED 0. 선택 심화 4개는 NOT VERIFIED이다.
Docker 적용 및 실행 증거 커밋: 4cc50d1d6c1d1b70d7c9e27b9264efaa36f6cf26.

| # | 필수 기준 | 판정 | 실제 근거 |
|---|---|---|---|
| 1 | 프로젝트 이름 구분, 파일별 시작·종료 | PASS | infrastructure.txt, recreate.txt의 각각 config/up/down |
| 2 | 일반 PostgreSQL·Flask·gateway 함께 실행 | PASS | general-build.txt, final-checks.txt의 3개 Up 및 HTTP 200 |
| 3 | 감시 PostgreSQL·Flask·Next.js·gateway 실행 | PASS | monitor-build.txt, final-checks.txt의 4개 Up 및 화면 접근 |
| 4 | 두 Flask Dockerfile 빌드, 외부 요청 주소·포트 | PASS | 빌드 2개 성공, logs-before.txt의 0.0.0.0:5000, gateway HTTP 응답 |
| 5 | Next.js production build 및 빌드 결과 실행 | PASS | monitor-build.txt build 성공, logs-before/after.txt next start, 브라우저 화면 |
| 6 | .dockerignore에 로컬 생성물 제외 | PASS | 세 파일 확인, 빌드 로그 context 및 final-checks.txt 컨테이너 생성물 제외 확인 |
| 7 | gateway만 8081/8082 공개, 화면·API 접근 | PASS | infrastructure.txt 포트, final-checks.txt 네 URL 200 |
| 8 | DB 내부망만 참여, 공유망 제외 | PASS | infrastructure.txt DB network inspect 각 한 내부망, Compose internal:true |
| 9 | 같은 실제 외부망, 두 API만 참여 | PASS | infrastructure.txt m5d1-events inspect의 API 두 개 |
| 10 | 각 API 자기 DB 서비스·포트·계정 일치 | PASS | Compose 환경, final-checks.txt SQL current_database/current_user 성공 |
| 11 | 감시 API 서비스 이름·내부 포트로 이벤트 전송 | PASS | MONITOR_URL, DNS 조회 및 감시 로그의 POST /api/events 201 |
| 12 | DB healthcheck·API 준비 대기, 감시 준비 후 실험 | PASS | build 로그 DB Healthy 후 API 시작, readiness.txt 200 후 일반 빌드·로그인 |
| 13 | 두 DB 초기 SQL·volume, 수명 구분 | PASS | 최초 초기화 로그, infrastructure.txt mount, recreate.txt 같은 볼륨·자료 유지 |
| 14 | 일반 gateway 로그인 후 게시글 접근 | PASS | general-success.png student 로그인 및 Docker 실행 확인 게시글, 로그인 200 로그 |
| 15 | 이번 실패·성공 종류와 상태를 감시 화면 확인 | PASS | monitor-before.png/UI, SQL ID 7 failure/401·8 success/200 |
| 16 | 새 메모 저장 후 새로고침 조회 | PASS | monitor-before.png/UI: 새로고침→현재 로그인 확인→목록 조회, 메모 ID 1 |
| 17 | -v 없이 종료·재실행 후 기록·메모 유지 | PASS | recreate.txt 전후 동일 SQL, 컨테이너 ID 변경, monitor-after.png 재로그인 조회 |
| 18 | config·ps·망·이름조회 실제 결과 및 범위 구분 | PASS | infrastructure.txt, final-checks.txt, README의 DNS와 앱 응답 구분 |
| 19 | Git 커밋, 식별자·변경 내용 제출물 기록 | PASS | 위 full SHA의 구현·검증 커밋, README 변경 목록 |
| 20 | 소스·설정·README 재현 절차 제출 | PASS | 기존 앱 소스/잠금 파일 보존, README 최초 실행·계정·검증·종료, Git archive 제출 |

## 최초 소스 검사와 수정 범위

처음 지정한 m5d1-sample은 messages 샘플이며 Git 저장소가 아니고 대상 기능이 없어 수정하지 않았다.
사용자가 추가로 지정한 day06-start를 새 mini-watch-day06 폴더에 clone했다. 원본은 Git 변경 없음이었다.
루트 Docker 설정은 없었지만 general의 로그인·게시글 및 monitor/backend의 인증·이벤트·메모와
monitor/next-frontend 화면을 확인했다. DB repository와 starter SQL 테이블·컬럼이 일치했다.
원본 Flask는 127.0.0.1:5100/5200, 이벤트 URL은 localhost:5200, Next rewrite도 localhost:5200이었다.
따라서 제공 starter의 실행 주소·환경변수·Dockerfile·SQL·gateway를 재사용하고 DB만 있는 Compose를 직접 완성했다.
전체 기능 신규 개발이나 route/repository/UI 수정은 하지 않았다.

최초 필수 기준별 상태: 1~13은 Docker 구조 미적용으로 FAIL(5·6의 제공 자료는 실제 빌드 전 NOT VERIFIED),
14~18은 컨테이너 실행 검증 전 NOT VERIFIED, 19는 작업 커밋 전 FAIL, 20은 Docker 재현 문서 미완성 FAIL이었다.
이는 소스 기능 존재만으로 통과 판정을 하지 않은 결과이다.

## 실행 증거와 제한

실제 명령은 README의 코드 블록에, 해당 출력은 이 폴더의 txt 파일에 남겼다.
BuildKit/Compose 진행 메시지에는 같은 진행 줄이 반복될 수 있다. 예시 출력을 실제 결과로 대체하지 않았다.
브라우저에서 오류 문구 확인→성공 로그인→이벤트 조회→메모 등록→새로고침 조회를 수행했다.
재생성 이후에는 일반 로그아웃/재로그인, 감시 로그아웃/재로그인을 수행하고 이전 메모를 조회했다.
메모는 삭제하지 않았다. 기존 샘플 컨테이너와 데이터는 유지했다. 최종 두 프로젝트는 실행 중이다.

[일반 로그인 화면](general-success.png), [새로고침 후 감시 화면](monitor-before.png),
[컨테이너 재생성 후 감시 화면](monitor-after.png).
필수 20개에는 미검증 항목이 없지만 선택 심화 4개 및 실제 운영 보안·부하·장기 운용은 검증하지 않았다.
npm ci에서 보고된 high 취약점 5개는 별도 의존성 점검 대상으로 남겼다.
