# 자체 점검: 출처 대조

출처·교과 문장이 원문과 맞는지 본다. 집필 패스의 생각 과정과 다른 렌즈의 결과는 보지 않는다. 이 점검은 교차 검토(ED-08)가 아니다. [공통 규칙](../README.md#모든-카드-공통)을 따른다.

## 입력
- 장 번호 `N.M`, 회차 `N`

## 읽을 것
- `python3 tools/book.py sentences N.M --json build/harness/N.M/checks/rN-sentences.json`의 결과
- stage의 장 파일(문맥 확인용)
- `ledger.json`의 `sources`와 각 문장의 `refs`(키·위치·닻·측정 조건)만. `note`·`gaps` 등 집필 쪽 메모는 읽지 않는다
- 출처 본문: `fetch.py page`·`fetch.py anchor`, `build/harness/sources/<이름>/text.txt`

## 쓸 것
- `build/harness/N.M/checks/rN-source.json`(형식은 [README](../README.md#점검과-판정-형식), `lens`는 `출처 대조`)

## 할 일
출처·교과 문장마다:
1. `fetch.py verify`로 출처가 받은 그대로인지 본다. 아니면 그 문장은 `미확인`.
2. 위치(`loc`)의 원문을 직접 읽는다. 닻만 보고 판정하지 않는다.
3. 주장이 원문과 같은가: 수치, 단위, 측정 조건(데이터셋·지표·설정), 한정어, 시점. 원문의 범위보다 넓혀 말하지 않았나.
4. 인용 키가 그 주장의 출처인가.
5. 교과 문장: 정말 공통 정의인가, 특정 논문·도구의 정의인가. 후자면 「표준과 관례」로 갈라 써야 한다.
6. 갈래가 설명·연결인데 출처가 필요한 사실 주장을 담은 문장도 지적한다(갈래 잘못).

판정: `일치`·`불일치`·`미확인`. 불일치와 미확인에는 지적을 단다. 지적의 근거는 출처의 위치와 닻이다.

## 돌려줄 것
`{"status", "file": "build/harness/N.M/checks/rN-source.json", "blocking": <수>}` — `status`는 [공통 규칙 8](../README.md#모든-카드-공통)의 네 값 중 하나다.
