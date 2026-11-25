# 렌더 확인 — 사이트에서 그림·표·수식 보기

통합한 묶음의 장이 웹 사이트에서 제대로 보이는지 본다. 고치지 않고 지적만 낸다. [공통 규칙](../README.md#모든-카드-공통)을 따른다.

## 입력
- 묶음 이름 `batch-NN-K`, 묶음의 장 목록

## 읽을 것
- 묶음 장들의 `book/` 파일(그림·표·수식이 있는 곳)

## 쓸 것
- `build/`(사이트 산출물), `build/harness/batch-NN-K/render.md`

## 할 일
1. `python3 tools/book.py site` → `.venv/bin/zensical build -f build/zensical.toml --strict`. 경고나 실패는 그대로 지적이다.
2. `build/site/`의 그 장 HTML에서 본다: Mermaid 블록이 그림으로 들어갔나, 수식이 수식 요소로 바뀌었나, 표의 열 수가 맞나, 이미지 경로가 살아 있나, 장 사이 링크가 맞는 페이지로 가나.
3. 브라우저 도구가 있으면 `build/site`를 로컬 서버로 띄우고 그 장을 데스크톱 폭과 375px 폭으로 연다. 그림이 잘리거나 가로로 넘치는 곳, 표가 깨지는 곳, 수식이 날것으로 보이는 곳을 찾는다. 서버는 확인이 끝나면 끈다.
4. 브라우저로 보지 못했으면 「브라우저 확인 못 함」이라고 적는다. 오케스트레이터가 보완한다.

지적마다 장, 위치(절·그림 번호), 무엇이 어떻게 보이는지, 화면 폭을 적는다.

## 돌려줄 것
`{"status", "file": "build/harness/batch-NN-K/render.md", "issues": <수>, "browser_checked": true}`
