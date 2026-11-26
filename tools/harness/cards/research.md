# 조사 — 장 하나의 사실을 1차 출처에서 찾기

구성안이 요구하는 사실을 1차 출처에서 찾아 근거 대장의 출처와 사실을 채운다. 글은 쓰지 않는다. [공통 규칙](../README.md#모든-카드-공통)을 따른다.

## 입력
- 장 번호 `N.M`, 승인된 구성안의 그 장 부분

## 읽을 것
- 구성안의 그 장 부분
- `book/appendix/references.md`(이미 있는 키)
- `editorial/style-guide.md` §7
- [README](../README.md)의 「근거 대장 형식」

## 쓸 것
- `build/harness/N.M/ledger.json`의 `sources`·`facts`·`gaps`
- `build/harness/N.M/delta.json`의 `chapter`와 `references_add`(새 문헌만)
- 출처는 `fetch.py get`으로만 받는다. 보관함에 직접 쓰지 않는다.

## 할 일
1. 구성안이 요구하는 사실을 목록으로 만든다.
2. 사실마다 1차 출처(원 논문, 공식 문서, 표준 교과서)를 찾는다. 웹 검색은 URL을 찾는 데만 쓴다.
3. `python3 -I tools/harness/fetch.py get URL --id <키 소문자>-<판>`으로 받는다. 판이 있는 주소(arXiv의 `vN`, DOI)를 쓰고, 초록보다 전문(PDF)을 받는다.
4. 받은 본문(`build/harness/sources/<이름>/text.txt`, `fetch.py page`)에서 그 사실이 있는 곳을 찾는다.
5. `facts`에 한 줄씩 적는다.
   - `claim`: 한국어 한 줄. 한정어(약·최대·특정 조건에서)를 빼지 않는다.
   - `key`·`loc`(절·쪽·표·그림)·`anchor`(본문에 그대로 있는 15단어 미만 구절)·`conditions`(데이터셋·지표·설정·시점)
   - `fetch.py anchor`로 닻이 찾히는지 확인한다.
6. `sources`에 키마다 `source_id`와 `scope`(`전문`·`초록만`·`해당 절만`)를 적는다.
7. 새 문헌은 style-guide §7 형식으로 `references_add`에 넣는다. 저자·제목·연도·학회는 받은 문서 자체(첫 쪽, arXiv 초록 페이지)에서 확인한다. 학회를 확인하지 못하면 「arXiv, 연도」로 쓴다. 집필 패스가 본문에서 인용하지 않기로 한 문헌은 그 패스가 `sources`의 `entry`로 옮긴다.
8. 찾지 못한 사실, 출처끼리 다투는 사실은 메우지 않고 `gaps`에 적는다.
9. `python3 -I tools/harness/ledger.py facts N.M`을 오류 0으로 통과시킨다.

조건이 다른 수치를 한 사실로 묶지 않는다. 블로그와 요약 글은 1차 출처를 찾는 길잡이로만 쓴다.

## 돌려줄 것
`{"status", "facts": <수>, "sources": [키…], "gaps": ["…"]}` — `status`는 [공통 규칙 8](../README.md#모든-카드-공통)의 네 값 중 하나다.
