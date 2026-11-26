# 수정 — 채택된 지적만 고치기

채택된 지적과 그 영향 범위만 고친다. 다른 문장을 다듬지 않는다. [공통 규칙](../README.md#모든-카드-공통)을 따른다.

## 입력
- 장 번호 `N.M`, 회차 `N`, `judge-rN.json`과 그 지적 파일들

## 읽을 것
- 판정 결과와 채택된 지적, stage의 장 파일, `delta.json`, `ledger.json`
- 고칠 사실의 출처(`fetch.py page`·`anchor`)

## 쓸 것
- stage의 장 파일·그림·코드, `delta.json`, `ledger.json`

## 할 일
1. 채택된 `차단` 지적을 모두 고친다. 채택된 `권고`는 다른 문장을 건드리지 않고 고칠 수 있을 때만 고친다.
2. 영향 범위도 함께 고친다: 같은 사실을 되풀이한 「한눈에」·「정리」·확인 문제와 답, 그림과 그림 설명, `delta.json`의 용어집 행.
3. `미확인`으로 판정된 문장은 빼거나 확인된 만큼만 남기고, `open_questions_add`에 한 줄을 더한다.
4. `book.py lint N.M` 오류 0 → `ledger.py sync N.M` → 새 문장 번호에 갈래와 근거를 다시 단다 → `ledger.py validate N.M` 오류 0. 새 문헌은 본문이 인용하면 `references_add`, 근거로만 쓰면 대장 `sources`의 `entry`에 둔다.
5. `delta.json`의 `stage_files` 해시를 새로 적는다.

고친 문장은 다음 회차에 다시 점검받는다. 두 번째 회차에도 고치지 못한 차단 지적이 있으면 억지로 맞추지 않고 `보류`로 돌려준다.

## 돌려줄 것
`{"status", "changed": ["s-…", …], "removed": ["s-…"], "open_questions_add": <수>}`
