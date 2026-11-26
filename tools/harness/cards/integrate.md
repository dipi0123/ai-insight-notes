# 통합 — 묶음을 저장소에 반영하기

저장소(`book/`·공유 파일·`workbench/evidence/`·진행 기록)에 쓰는 유일한 패스다. 한 번에 하나만 돈다(§10.7). 커밋과 push는 하지 않는다. [공통 규칙](../README.md#모든-카드-공통)의 2를 뺀 나머지를 따른다.

## 입력
- 묶음 이름 `batch-NN-K`, 묶음의 장 목록

## 읽을 것
- `workbench/progress/book-harness.md`, `build/harness/batch-NN-K/base.json`
- 장마다 `delta.json`, 마지막 `judge-rN.json`
- `editorial/workflow.md` §10.3·§10.6·§10.7

## 쓸 것
- `merge`가 고치는 파일(`book/`의 그 장 파일·그림·코드, 용어집, 참고문헌, 미확인 목록, curriculum 상태 칸), `toc`가 고치는 `book/README.md`
- `workbench/evidence/<장>.md`(`ledger.py export`), `workbench/progress/book-harness.md`

## 할 일
1. 장마다 통과 조건을 본다: `book.py lint N.M` 오류 0, `ledger.py validate N.M --final` 오류 0, 마지막 판정에 열린 차단 지적 없음. 못 넘은 장은 이번 통합에서 뺀다. 빠진 장을 선수로 둔 장도 뺀다.
2. `git status --porcelain`이 진행 기록에 적힌 변경 말고는 없는지 본다. 다른 변경이 있으면 멈춘다.
3. `python3 -I tools/harness/fetch.py verify`가 오류 0인지 본다.
4. `python3 tools/book.py merge <변경분…> --base build/harness/batch-NN-K/base.json --oq-floor <진행 기록의 다음 미확인 번호 - 1> --dry-run`으로 바뀔 것을 보고, 이상이 없으면 `--dry-run` 없이 돌린다.
5. `python3 tools/book.py toc` → `python3 tools/book.py check`. 오류가 있으면 원인이 통합에서 생긴 기계적인 것(링크 경로 등)일 때만 고친다. 그 밖이면 스냅숏(`build/harness/snapshots/merge-…/`, `manifest.json`)으로 되돌리고 멈춘다. 두 번 연속 실패해도 멈춘다.
6. 장마다 `python3 -I tools/harness/ledger.py export N.M`.
7. 진행 기록을 고친다: 장마다 단계(통합), 통과한 장 해시, 문장 수, 보류한 장과 이유, 다음 미확인 번호.

## 돌려줄 것
`{"status", "merged": ["N.M", …], "held": [{"chapter": "N.M", "reason": "…"}], "check_errors": 0, "snapshot": "build/harness/snapshots/merge-…"}` — `status`는 [공통 규칙 8](../README.md#모든-카드-공통)의 네 값 중 하나다.
