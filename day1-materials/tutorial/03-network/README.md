# 3교시 — 코드 변경 없이 연결망 익히기
1교시 수정 이미지 m5d1-flask:2와 2교시 수정 이미지 m5d1-next:2를 사용한다.
이 단계는 Dockerfile을 추가하지 않는다. Notion 3교시의 순서대로 실행한다.

```cmd
docker network create m5d1-lab
docker run -d --name m5d1-api --network m5d1-lab -p 127.0.0.1:5500:5000 m5d1-flask:2
docker run --rm --network m5d1-lab curlimages/curl:8.12.1 -sS --connect-timeout 3 http://m5d1-api:5000/api/hello
docker network disconnect m5d1-lab m5d1-api
docker run --rm --network m5d1-lab curlimages/curl:8.12.1 -sS --connect-timeout 3 http://m5d1-api:5000/api/hello
docker network connect m5d1-lab m5d1-api
docker run --rm --network m5d1-lab curlimages/curl:8.12.1 -sS --connect-timeout 3 http://m5d1-api:5000/api/hello
docker run -d --name m5d1-web --network m5d1-lab -p 127.0.0.1:3300:3000 m5d1-next:2
```
중간 실패는 망 연결을 끊은 실험 결과다. 복구 후 두 컨테이너를 실행 상태로 둔다.
