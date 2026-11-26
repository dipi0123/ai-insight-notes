# 책 전체 집필 하네스

## 목표
책 전체를 작성 → 검토 → 수정 → 최종 리뷰의 단계를 거쳐 완성하는 하네스를 설계하고, 그 준비 단계(규칙 반영, 검사 도구, 역할 카드, 수용 시험)를 마친다. 설계안은 [workbench/drafts/2026-11-25_claude_book-harness.md](../drafts/2026-11-25_claude_book-harness.md)다.

## 현재 상태
- 준비 단계의 도구와 역할 카드가 갖춰졌고, 수용 시험(`python3 -I tools/harness/selftest.py`)이 104개 모두 통과한다.
- 규칙 문구(ED-20, 미정 Q-01, workflow §10, AGENTS.md의 패스 경계 규칙 등)는 사용자가 승인했고 커밋했다.
- 설계안 8절의 결정은 사용자가 권고안대로 정했다: 워크플로 하나에 에이전트 25~40개, 커밋 방식 가(부 접점에서 요청받아 커밋), 내려받기는 `tools/harness/allowed-hosts.txt`의 호스트만, 1·2부는 설치 없음. 값은 [하네스 README의 운영 범위](../../tools/harness/README.md#운영-범위)에 있다.
- 시범 운영 1(심은 오류 시험)을 마쳤다. 심은 오류 7개를 모두 잡았고 대조 문장에 헛지적이 없었다. 결과는 [회귀 시험의 기준선](../../tools/harness/regression/README.md#기준선)에 있다.
- 시범 운영 2(1.1~1.4 소급 자체 점검)를 마쳤다. 묶음 `batch-01-1`에서 1.1·1.3·1.4를, 보류했던 1.2는 사용자 결정대로 묶음 `batch-01-2`에서 한 번 더 고쳐 통합했다. 네 장 모두 상태는 `초고 · Claude`다(자체 점검은 교차 검토가 아니다).
- 작업 트리의 미커밋 변경은 모두 하네스의 것이다: `tools/harness/` 아래 파일, 이 기록, 두 묶음의 통합분(1.1~1.4 장 파일, 용어집, 참고문헌, 미확인 목록, `workbench/evidence/1.1~1.4.md`).

## 준비 단계에서 바꾼 파일
| 파일 | 내용 |
|---|---|
| `editorial/decisions.md` | ED-20(책 전체 집필), 미정 Q-01(교차 검토 시점·모델) |
| `editorial/workflow.md` | §2에서 §10으로 가는 안내, §10 「책 전체 집필」 |
| `AGENTS.md`·`CLAUDE.md`·`README.md`·`workbench/README.md` | 패스의 파일 경계, 하네스 도구와 근거 대장 안내 |
| `editorial/templates/evidence.md` | 근거 대장 템플릿 |
| `tools/book.py` | check 확장, lint·sentences·slice·hashes·merge 명령 |
| `tools/harness/` | fetch.py, ledger.py, selftest.py, README.md, 역할 카드 14장(소급 대장 `backfill` 포함) |
| `tools/harness/allowed-hosts.txt` | 내려받기 허용 호스트(사용자 결정) |
| `tools/harness/regression/` | 심은 오류 시험 세트 planted-1과 `run.py build/score` |
| `workbench/evidence/` | 통합한 장의 근거 대장(`ledger.py export`) |
| `workbench/drafts/2026-11-25_claude_book-harness.md` | 설계안. 승인된 부분을 정본으로 다 옮긴 뒤 지운다 |

git 밖 보관함(`build/harness/sources/`)에는 도구 점검과 시범 운영에서 받은 출처가 있다. 쓰지 않는 항목 셋은 지우지 않고 남겼다: `mccarthy1955-aimag2006`(봇 확인 페이지), `samuel1959-abs`·`patterson2022-doi`(빈 응답). ISO/IEC 22989는 iso.org를 허용했지만 HTTP 403(봇 차단)이라 받지 못했다.

## 끝난 일
근거 커밋: 이 파일을 처음 올린 커밋(`git log --diff-filter=A --oneline -- workbench/progress/book-harness.md`).
- 설계안 작성. 의존 깊이 18, 부 단위 59묶음, 1.1~1.4의 인용 문장 비율 13% 같은 측정값은 설계안에 있다.
- 규칙 반영(위 표). 사용자 승인.
- `tools/book.py` 확장. 지금 저장소에서 `check` 오류 0, 1.1~1.4의 `lint` 오류 0.
- `tools/harness/` 도구·카드·수용 시험.
- 설계안 8절 결정 반영(하네스 README 「운영 범위」), `fetch.py`의 허용 목록 검사(받을 때와 `verify`), 수용 시험 91개.
- 시범 운영 2의 회차 1: 소급 대장 카드(`cards/backfill.md`)로 네 장의 대장을 거꾸로 만들고 렌즈 셋과 판정을 돌렸다. 판정을 모은 뒤 일치가 아닌 문장은 1.1 29개, 1.2 22개, 1.3 16개, 1.4 26개다. 사용자는 허용 목록을 넓히는 기준을 「학습에 필요한 내용이면 원문을 구하고, 중복이면 더 공신력 있는 출처 하나」로 정했다(README 「운영 범위」). 그에 따라 McCarthy 제안서(jmc.stanford.edu), Samuel 논문(people.csail.mit.edu), Gama 서베이(eprints.bournemouth.ac.uk)를 받았다.
- `ledger.py verdicts`를 회차를 아는 방식으로 바꿨다. 모든 회차의 점검과 판정을 함께 받고, (문장, 렌즈)마다 늦은 회차가 이기며, 지적은 (회차, 렌즈/번호)로 가린다. 열린 권고는 판정을 바꾸지 않는다. 수용 시험 93개.
- 시범 운영 2의 1.2 다시 점검(batch-01-2): 수정 → 렌즈 셋 → 판정(에이전트 5개, 9분, 하위 에이전트 토큰 약 70만). 차단 지적 0으로 통합했다(merge 스냅숏 `build/harness/snapshots/merge-20261126-085314/`). 용어집 +2행(MLLM, model card), 참고문헌 +4개(Goodfellow2014·Kingma2013·Mitchell2019·Sun2026), 미확인 OQ-004~OQ-007. 사용자가 용어집 기존 6행(GAN·VAE·Transformer·parameter·image-text-to-text·language model) 변경과 @ISO2022 삭제(인용하는 장이 없고 원문을 403으로 받지 못했다)를 승인했다.
- 시범 운영 2 전체 비용: 워크플로 넷, 에이전트 61개(소급 대장·렌즈·판정 16, 수정 1회차 20, 수정 2회차 20, 1.2 다시 5). 회차마다 일치가 아닌 문장: 회차 1 판정 뒤 93개(1.1 29·1.2 22·1.3 16·1.4 26) → 회차 2 뒤 9개 → 회차 3 뒤 2개(1.2) → 0개.
- 시범 운영 2의 회차 3과 통합: 마지막 수정과 회차 3 점검·판정(에이전트 20개, 24분, 하위 에이전트 토큰 약 341만). 1.1·1.3·1.4는 모든 문장이 일치이고 열린 차단 지적이 없어 통합했다(merge 스냅숏 `build/harness/snapshots/merge-20261126-083815/`). 용어집 +2행(validation set, preference-based reinforcement learning), 참고문헌 +6개, 미확인 OQ-001~OQ-003. 사용자가 기존 행 7곳 변경을 승인했다: 용어집 expert system 행 삭제(1.1이 출처대로 knowledge base를 쓴다), reinforcement learning·PEFT·online learning·self-supervised learning 정의, @McCarthy1955·@Samuel1959에 실제로 대조한 판본 주소. 통합 check가 「인용하는 장이 없는 참고문헌」 경고 2건(@Brown2020·@OpenAI2024, 1.3의 교과 근거)을 내서 규칙을 고쳤다: 참고문헌에는 본문이 인용하는 문헌만 넣고, 근거로만 쓰는 문헌은 대장 `sources`의 `entry`에 둔다(`validate`가 막는다, 카드 넷과 README). 수용 시험 104개.
- 시범 운영 2의 회차 2: 장마다 수정 → 렌즈 셋 → 판정(에이전트 20개, 39분, 하위 에이전트 토큰 약 404만). 판정을 모은 뒤 일치가 아닌 문장은 1.1 2개, 1.2 5개, 1.3 1개, 1.4 1개다. 이 과정에서 하네스의 빈틈 둘을 고쳤다. 연결 문장에 채택된 차단 지적이 `verdicts`와 `validate --final`에 보이지 않던 것, 대장이 키 하나에 출처 파일 하나만 받아 1.3이 Goodfellow 5장 대신 Google 용어집으로 받친 것(`parts`와 근거별 `source_id`를 더했다). 수용 시험 101개.
- 시범 운영 1: 심은 오류 시험. 저장소 밖 격리 사본에서 렌즈 셋과 판정을 돌렸고, 에이전트 기록에 원본 저장소 경로를 연 흔적이 없다. 출처 대조와 판정이 「보관함에 허용 목록 밖 출처가 있다」를 짚어 `verify`의 빈틈을 찾았다. 렌즈는 시험 장에 모르고 남긴 오류(temperature를 쓰는 이유의 틀린 설명, 정의 없는 hidden layer·unit·regularization, 번역어만 쓴 지표 이름)도 잡았다. 선수 범위 밖 용어는 용어집에 없으면 lint가 못 잡으므로 설명 렌즈가 맡는다.

## 실패한 접근
- Workflow 도구의 결과 파일(`.output`)은 순수 JSON이 아니라 감싼 형식이라 그대로 파싱되지 않았다. 에이전트별 결과는 실행 폴더의 `journal.jsonl`(type `result`, 라벨은 `started` 항목)에서 읽는다.
- 용어 첫 등장 검사를 대소문자 무시로 하면 고유 이름을 풀어 쓴 곳(「Language-Image Pre-training」)이 용어로 잡혔다. 일반 명사 용어는 문장 첫머리에서도 소문자로 쓰므로(style-guide §5) 대소문자를 가린다.
- lint가 자기 장의 stage만 보면 같은 묶음의 다른 장으로 가는 링크가 깨진 것으로 나왔다. `build/harness/*/stage`를 모두 찾는다.
- `ledger.py verdicts`가 처음에는 회차 하나의 점검만 받아 판정 칸을 덮어썼다. 회차 2를 넣으면 회차 1에서 일치였던 문장의 판정이 지워지고, 회차마다 같은 지적 번호(`F1` 등)가 겹쳤다. 모든 회차를 함께 받는 방식으로 고쳤다.
- 소급 대장의 셸 루프에서 zsh의 `set -- $spec`은 낱말을 나누지 않아 주소에 공백이 섞였고 `fetch.py`가 `http.client.InvalidURL`로 죽었다. 예외 처리에 넣고, 명령은 하나씩 적어 돌린다.
- 워크플로의 에이전트 하나가 API 연결 오류로 실패해도 같은 스크립트를 `resumeFromRunId`로 다시 돌리면 끝난 에이전트는 캐시에서 온다. 판정만 다시 돌았다(실패한 판정은 21분을 쓰고 끊겼다).

## 장별 단계
| 장 | 단계 | 장 해시(앞 12자) | 문장 | 비고 |
|---|---|---|---|---|
| 1.1 | 통합(batch-01-1, 자체 점검 3회차) | af28ddbf8b25 | 177 | lint 오류 0, 후보 1. 근거 대장 `workbench/evidence/1.1.md` |
| 1.2 | 통합(batch-01-2, 자체 점검 4회차) | f98af9de9e10 | 198 | lint 오류 0, 후보 1(메타 줄의 「과제」, curriculum 질문이라 그대로). batch-01-1에서 두 번 고친 뒤 차단 2개가 남아 보류했다가 다시 돌렸다. 근거 대장 `workbench/evidence/1.2.md` |
| 1.3 | 통합(batch-01-1, 자체 점검 3회차) | 4cdb35848441 | 195 | lint 오류 0, 후보 2. 근거 대장 `workbench/evidence/1.3.md` |
| 1.4 | 통합(batch-01-1, 자체 점검 3회차) | eeab3db38b36 | 161 | lint 오류 0, 후보 0. 근거 대장 `workbench/evidence/1.4.md` |
| 1.5 | 계획 | — | — | 시범 운영 3에서 쓴다 |
| 1.6 | 계획 | — | — | 시범 운영 3에서 쓴다 |

## 남은 확인거리(통합 때 나온 것)
- 용어집 SFT 행(「지시 → 좋은 답」 쌍)이 1.2의 SFT 서술(입력과 바라는 출력의 짝, Zhao2023)보다 좁다. noise 행(「데이터에 섞인 무작위 값」)은 GAN 행의 만드는 쪽 입력으로 쓰는 noise를 덮지 못한다. 둘 다 1.2 설명 렌즈의 notes이고 본 장이 다른 장(1.4·9.3)이라 제안하지 않았다. 해당 장을 다룰 때 본다.
- 참고문헌 @Meta2024 제목 「Meta-Llama-3-8B-Instruct 모델 카드」는 그대로 두었다. 용어집 model card의 분류는 변경분대로 「규모·활용」이다.
- 보관함의 쓰지 않는 항목: mccarthy1955-aimag2006(봇 확인 페이지), samuel1959-abs·patterson2022-doi(빈 응답), kingma2014-v11(kingma2013-v11과 같은 PDF).

## 기준 장
승인된 기준 장은 아직 없다. 설계안의 유형별 후보: 1부, 2.2·2.4, 3.2, 4.3·5.5, 9.4, 14.2, 14.3.

## 다음 미확인 번호
OQ-008. merge에는 `--oq-floor 7`.

## 다음 단계
1. push는 사용자가 따로 요청할 때 한다.
2. 시범 운영(설계안 11절) 나머지: 1.5·1.6을 구성부터 부 리뷰까지(구성안은 사용자 승인). 선택: 두 장을 다른 모델로 대조.
3. 2부 전: 책 설계도 1판(`editorial/blueprint.md`, 승인 필요), style-guide §6·§7 보강(설계안 9절 7), 일반 서술로 쓰는 한국어 낱말의 허용 목록(9절 8. 지금 `tools/book.py`의 `EVERYDAY_KO`는 임시).
4. 3부 전: 코드 계약(9절 9). 시스템 Python은 3.14이고 torch·numpy가 없다.
5. 하네스를 다 쓰면 결론만 정본으로 옮기고 이 파일과 설계안을 지운다(§9).
