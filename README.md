# 5과목 Day1 공통 시작본

4과목 day05-start의 일반 Flask·감시 Flask·React 소스와 Day5 Next.js 부록을 바탕으로 준비했다.
기존 파일은 별도 원본에 보존하며 이 폴더에서만 합쳤다.
감시 백엔드는 기존 세션 부록의 app/auth/notes/events/auth_helpers를 사용한다.
Next.js에는 기존 메모 CRUD를 유지하면서 로그인·CSRF·요청 기록 화면을 연결했다.

이 시작본의 프로젝트 루트에는 Dockerfile·Compose·게이트웨이 설정을 아직 적용하지 않았다. 5교시에서 작은 샘플을 완성한 뒤 6교시에서 추가한다.
로컬 개발 주소는 일반 5100, 감시 API 5200, Next.js 3000이다.
Docker 적용 결과는 같은 저장소의 day07-start 브랜치에서 비교한다.
실제 계정 비밀값과 .env, DB 데이터, node_modules는 포함하지 않는다.
공개 교육 예시 계정 student/operator는 create_user.py로 만든다. 비밀번호 Learn123!은 수업 예시이다.

## 수업 순서와 Git 시작점

1~5교시는 교안의 작은 코드를 직접 작성하고 같은 폴더의 compose.yaml 하나를 확장한다.
Flask·Next.js·DB·게이트웨이의 요청과 응답을 확인한 뒤 6교시 프로젝트 적용을 시작한다.
실프로젝트는 compose-general.yaml과 compose-monitor.yaml 두 파일을 각각 실행한다.
두 API는 외부 네트워크 m5d1-events로 연결한다.

시작 코드: https://github.com/zeroskill2400/mini-watch/tree/day06-start

```cmd
cd /d C:\work
git clone --branch day06-start https://github.com/zeroskill2400/mini-watch.git mini-watch-day06
cd mini-watch-day06
```

general·monitor는 기존 앱이며 day1-materials는 비교 코드와 적용할 설정이다.
설정 적용·공유망 생성·각 프로젝트 실행 순서는 day1-materials/README.md와 6교시 교안을 따른다.

완성 비교 코드: https://github.com/zeroskill2400/mini-watch/tree/day07-start
비교가 필요하면 기존 작업 폴더를 유지하고 별도 폴더로 받는다.

```cmd
cd /d C:\work
git clone --branch day07-start https://github.com/zeroskill2400/mini-watch.git mini-watch-day07-compare
```

교안: https://www.notion.so/3f6ae3d1800c81c59d93e70132b2157f
