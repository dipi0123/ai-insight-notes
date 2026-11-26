# 집필 — 장 하나 쓰기

근거 대장에 있는 사실로 장을 쓰고, 문장마다 갈래를 단다. 공유 파일에 넣을 것은 변경분으로 낸다. [공통 규칙](../README.md#모든-카드-공통)을 따른다.

## 입력
- 장 번호 `N.M`, 승인된 구성안의 그 장 부분, 기준 장(같은 유형) 경로

## 읽을 것
- 구성안의 그 장 부분, `build/harness/N.M/ledger.json`, `build/harness/N.M/delta.json`
- `editorial/style-guide.md` §3~§10, `editorial/templates/chapter.md`
- `python3 tools/book.py slice --before N.M --chapter N.M`
- 선수 장 전체, 같은 유형의 기준 장. 그 밖의 앞 장은 링크·앵커를 확인할 때만 연다

## 쓸 것
- `build/harness/N.M/stage/` 아래 저장소와 같은 경로: 장 파일, `book/figures/NN-MM-*`, `book/code/partNN/<장 파일 이름>/`
- `build/harness/N.M/delta.json`, `build/harness/N.M/ledger.json`의 `writer`·`sentences`
- 계산 기록: `build/harness/N.M/runs/`

## 할 일
1. 구성안의 절 구성대로 쓴다. 절을 바꾸면 `delta.json`의 `note`에 이유를 적는다.
2. 출처가 필요한 문장은 `facts`에 있는 사실로만 쓴다. 대장에 없는 사실이 필요하면 쓰지 않고 `gaps`에 더한 뒤 돌려준다.
3. 용어: 표기는 용어집과 같게, 한 장에서 처음 나올 때 `영어(한국어)`. 새 용어는 `glossary_add`, 이 장이 본 장인 기존 용어는 `glossary_link`.
4. 링크: 앞 장은 절 앵커까지 링크한다. 아직 파일이 없는 장은 링크하지 않고 장 번호만 쓴다. 선수 칸에 없는 앞 장의 개념은 한 줄로 되짚고 링크한다.
5. 숫자 예시는 `runs/`에 계산을 돌려 기록을 남긴다. 「직접 만들기」 장은 코드를 먼저 돌리고 실행 기록으로 쓴다(§10.2).
6. 장 안에 AI 이름·날짜·작업 경위를 쓰지 않는다.
7. `python3 tools/book.py lint N.M`을 오류 0으로 만든다. 후보는 하나씩 보고 실제 위반만 고친다.
8. `python3 -I tools/harness/ledger.py sync N.M --writer <모델 계열>`. `references_add`에는 본문이 인용하는 문헌만 남긴다. 인용 표시 없이 교과 문장의 근거로만 쓰는 문헌은 그 줄을 대장 `sources`의 그 키에 `entry`로 옮긴다. 모든 문장에 갈래를 달고, 출처·교과 문장에는 `refs`를, 계산·실행 문장에는 `path`를 단다. `cross_review_priority`에 같은 계열 모델로는 가리기 어려운 곳(교과 판정, 비유와 번역어, 책 고유의 분류, 초록만 읽은 주장)을 적는다.
9. `python3 -I tools/harness/ledger.py validate N.M`을 오류 0으로 통과시킨다.
10. `delta.json`: `status`는 `초고 · <모델 계열>`, `stage_files`는 놓을 파일마다 `shasum -a 256` 값.

## 돌려줄 것
`{"status", "chars": <자>, "sentences": <수>, "lint_errors": 0, "gaps": ["…"], "note": "…"}` — `status`는 [공통 규칙 8](../README.md#모든-카드-공통)의 네 값 중 하나다.
