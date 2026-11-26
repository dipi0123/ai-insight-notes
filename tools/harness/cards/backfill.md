# 소급 대장 — 하네스 밖에서 쓴 장의 근거 대장을 거꾸로 만들기

하네스 전에 쓴 장을 자체 점검에 올리려고, 이미 있는 장에서 출발해 근거 대장·변경분·stage를 만든다. 조사와 집필의 대장 부분을 거꾸로 하는 패스다. 장을 고치지 않고 판정하지 않는다. 근거를 찾지 못한 문장은 맞추지 말고 그대로 드러낸다. [공통 규칙](../README.md#모든-카드-공통)을 따른다.

## 입력
- 장 번호 `N.M`

## 읽을 것
- 저장소의 장 파일(curriculum의 경로)
- `book/appendix/references.md`, `tools/harness/allowed-hosts.txt`
- `editorial/style-guide.md` §7, [README](../README.md)의 「근거 대장 형식」
- 출처 본문: `fetch.py anchor`·`page`, `build/harness/sources/<이름>/text.txt`(필요한 곳만 찾아 읽는다)

## 쓸 것
- `build/harness/N.M/stage/<장 경로>`: 저장소 장 파일을 그대로 복사한 것. 고치지 않는다
- `build/harness/N.M/ledger.json`: `writer`·`sources`·`facts`·`gaps`·`sentences`·`cross_review_priority`
- `build/harness/N.M/delta.json`: `chapter`, `status`(`초고 · Claude`), `stage_files`, `note`(「소급 대장」). 장이 이미 인용하는데 참고문헌에 없는 문헌만 `references_add`에 넣는다
- 계산 기록: `build/harness/N.M/runs/`
- 출처는 `fetch.py get`으로만 받는다

## 할 일
1. 장 파일을 stage의 같은 경로로 복사하고 `python3 -I tools/harness/ledger.py sync N.M --writer Claude`.
2. 문장마다 갈래를 단다. 인용 표시가 있는지가 아니라 문장이 무엇을 주장하는지로 정한다. 특정 문헌이 주장하거나 잰 것(정의, 연도, 수치, 결과, 「처음 제안했다」)은 출처, 교과서·공식 문서에 공통으로 실린 정의는 교과, 본문의 숫자 예시는 계산이다. 설명과 연결은 새 사실 주장이 없는 문장만이다.
3. 출처를 받는다. 장이 인용한 키마다 참고문헌의 주소에서 시작해 허용 목록 안에서 전문을 찾는다.
   - arXiv는 판이 있는 PDF(`https://arxiv.org/pdf/<번호>vN`)를 받는다. 장이 인용한 판을 모르면 v1과 최신판 중 학회 판에 가까운 것을 고르고 `scope`에 적는다.
   - DOI·학회 페이지가 초록만 주면, 같은 문헌의 전문을 저자·기관이 허용 목록 안의 호스트(예: 기관 연구 페이지, 학회 proceedings)에 공개했는지 찾는다. 웹 검색은 주소를 찾는 데만 쓴다.
   - 이름은 `<키 소문자>-<판>`(예: `hinton2015-v1`, `sutton2018-book`, `iso2022-abs`). `fetch.py list`로 이미 받은 것을 먼저 본다. `get`이 「이미 있다」고 하면 있는 것을 쓴다.
   - 허용 목록 밖에서만 구할 수 있으면 받지 않고 `gaps`에 「허용 목록 밖: 주소 — 사용자 결정 필요」로 적는다.
4. 교과 문장에 인용 표시가 없으면 허용 목록 안의 교과서·공식 문서에서 같은 정의를 찾는다. 참고문헌에 없는 문헌이면 받은 문서 자체로 저자·제목·연도를 확인해 style-guide §7 형식 한 줄을 만든다. 장이 인용하지 않는 문헌이므로 `references_add`가 아니라 대장 `sources`의 그 키에 `entry`로 둔다(참고문헌에는 본문이 인용하는 문헌만 들어간다).
5. 출처·교과 문장마다 원문에서 그 주장이 있는 곳을 찾아 `refs`(키·위치·닻·측정 조건)를 단다. 닻은 본문에 그대로 있는 15단어 미만 구절이고 `fetch.py anchor`로 확인한다.
   - 주장 전체가 원문에 있을 때만 근거로 단다. 비슷한 말이 있는 곳에 닻을 걸어 맞추지 않는다.
   - 일부만 있거나 찾지 못하면 찾은 만큼만 `refs`에 두고(없으면 빈 목록), `gaps`에 「s-…: 무엇을 찾지 못했나(찾아본 곳)」를 적는다.
   - 받은 출처가 초록만이면 `scope`를 `초록만`으로 하고, 초록에 없는 주장은 찾지 못한 것으로 둔다.
6. 계산 문장은 `runs/calc-N.py`로 다시 계산하고 출력을 `runs/calc-N.txt`에 남겨 `path`에 단다. 본문과 다르면 고치지 말고 `gaps`에 적는다.
7. `facts`에는 근거를 단 주장을 한 줄씩 옮긴다(조사 카드의 형식). `cross_review_priority`에 같은 계열 모델로는 가리기 어려운 곳(교과 판정, 비유와 번역어, 책 고유의 분류, 초록만 읽은 주장)을 적는다.
8. `delta.json`의 `stage_files`에 stage 장 파일의 `shasum -a 256` 값을 적는다.
9. `python3 -I tools/harness/ledger.py validate N.M`. 오류는 `gaps`에 적은 문장의 「근거가 없다」만 남아야 한다. 그 밖의 오류는 고친다.

## 돌려줄 것
`{"status", "sentences": <수>, "kinds": {"출처": <수>, …}, "sources": ["키(source_id, scope)", …], "gaps": ["…"], "validate_errors": <수>}` — `status`는 [공통 규칙 8](../README.md#모든-카드-공통)의 네 값 중 하나다.
