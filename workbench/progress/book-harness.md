# 책 전체 집필 하네스

## 목표
책 전체를 작성 → 검토 → 수정 → 최종 리뷰의 단계를 거쳐 완성하는 하네스를 설계하고, 그 준비 단계(규칙 반영, 검사 도구, 역할 카드, 수용 시험)를 마친다. 설계안은 [workbench/drafts/2026-11-25_claude_book-harness.md](../drafts/2026-11-25_claude_book-harness.md)다.

## 현재 상태
- 준비 단계의 도구와 역할 카드가 갖춰졌고, 수용 시험(`python3 -I tools/harness/selftest.py`)이 89개 모두 통과한다.
- 규칙 문구(ED-20, 미정 Q-01, workflow §10, AGENTS.md의 패스 경계 규칙 등)는 사용자가 승인했고 커밋했다.
- 설계안 8절의 결정(워크플로 하나의 에이전트 수, 커밋 방식, 내려받기 허용 호스트와 설치 범위)은 아직 받지 않았다. 받기 전에는 묶음을 돌리지 않는다.
- 아직 어떤 묶음도 돌리지 않았다.

## 준비 단계에서 바꾼 파일
| 파일 | 내용 |
|---|---|
| `editorial/decisions.md` | ED-20(책 전체 집필), 미정 Q-01(교차 검토 시점·모델) |
| `editorial/workflow.md` | §2에서 §10으로 가는 안내, §10 「책 전체 집필」 |
| `AGENTS.md`·`CLAUDE.md`·`README.md`·`workbench/README.md` | 패스의 파일 경계, 하네스 도구와 근거 대장 안내 |
| `editorial/templates/evidence.md` | 근거 대장 템플릿 |
| `tools/book.py` | check 확장, lint·sentences·slice·hashes·merge 명령 |
| `tools/harness/` | fetch.py, ledger.py, selftest.py, README.md, 역할 카드 13장 |
| `workbench/drafts/2026-11-25_claude_book-harness.md` | 설계안. 승인된 부분을 정본으로 다 옮긴 뒤 지운다 |

git 밖(`build/harness/sources/`)에 도구 점검으로 받은 출처 두 개가 있다: `hinton2015-v1`(arXiv PDF), `hinton2015-abs`(arXiv 초록 페이지). `fetch.py verify`를 통과한다.

## 끝난 일
근거 커밋: 이 파일을 처음 올린 커밋(`git log --diff-filter=A --oneline -- workbench/progress/book-harness.md`).
- 설계안 작성. 의존 깊이 18, 부 단위 59묶음, 1.1~1.4의 인용 문장 비율 13% 같은 측정값은 설계안에 있다.
- 규칙 반영(위 표). 사용자 승인.
- `tools/book.py` 확장. 지금 저장소에서 `check` 오류 0, 1.1~1.4의 `lint` 오류 0.
- `tools/harness/` 도구·카드·수용 시험.

## 실패한 접근
- Workflow 도구의 결과 파일(`.output`)은 순수 JSON이 아니라 감싼 형식이라 그대로 파싱되지 않았다. 에이전트별 결과는 실행 폴더의 `journal.jsonl`(type `result`, 라벨은 `started` 항목)에서 읽는다.
- 용어 첫 등장 검사를 대소문자 무시로 하면 고유 이름을 풀어 쓴 곳(「Language-Image Pre-training」)이 용어로 잡혔다. 일반 명사 용어는 문장 첫머리에서도 소문자로 쓰므로(style-guide §5) 대소문자를 가린다.
- lint가 자기 장의 stage만 보면 같은 묶음의 다른 장으로 가는 링크가 깨진 것으로 나왔다. `build/harness/*/stage`를 모두 찾는다.

## 장별 단계
| 장 | 단계 | 장 해시(앞 12자) | 문장 | 비고 |
|---|---|---|---|---|
| 1.1 | 하네스 밖에서 쓴 초고 | 4521e3eff882 | 161 | lint 오류 0, 경고 1(가로 그림 노드 8개), 용어 후보 4 |
| 1.2 | 하네스 밖에서 쓴 초고 | 27fb1b40514f | 162 | lint 오류 0, 용어 후보 4(「AI」 첫 등장 등) |
| 1.3 | 하네스 밖에서 쓴 초고 | cb96d9539bd1 | 186 | lint 오류 0, 용어 후보 4 |
| 1.4 | 하네스 밖에서 쓴 초고 | db81fe0848b0 | 125 | lint 오류 0, 용어 후보 2 |
| 1.5 | 계획 | — | — | 시범 운영 3에서 쓴다 |
| 1.6 | 계획 | — | — | 시범 운영 3에서 쓴다 |

## 기준 장
승인된 기준 장은 아직 없다. 설계안의 유형별 후보: 1부, 2.2·2.4, 3.2, 4.3·5.5, 9.4, 14.2, 14.3.

## 다음 미확인 번호
OQ-001(파일과 git 이력에 쓰인 번호가 없다). merge에는 `--oq-floor 0`.

## 다음 단계
1. **사용자 결정**: 설계안 8절의 워크플로 하나의 에이전트 수, 커밋 방식(가·나·다), 내려받기 허용 호스트와 설치 범위.
2. push는 사용자가 따로 요청할 때 한다.
3. 시범 운영(설계안 11절): 심은 오류 시험 세트를 만들어 자체 점검 렌즈의 검출률을 잰다 → 1.1~1.4 소급 자체 점검(근거 대장을 거꾸로 만든다) → 1.5·1.6을 구성부터 부 리뷰까지.
4. 2부 전: 책 설계도 1판(`editorial/blueprint.md`, 승인 필요), style-guide §6·§7 보강(설계안 9절 7), 일반 서술로 쓰는 한국어 낱말의 허용 목록(9절 8. 지금 `tools/book.py`의 `EVERYDAY_KO`는 임시).
5. 3부 전: 코드 계약(9절 9). 시스템 Python은 3.14이고 torch·numpy가 없다.
6. 하네스를 다 쓰면 결론만 정본으로 옮기고 이 파일과 설계안을 지운다(§9).
