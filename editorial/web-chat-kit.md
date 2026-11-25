# 웹 채팅 키트

ChatGPT·Gemini·Grok·Claude.ai 같은 웹 채팅에서 이 책 작업을 할 때 쓴다. 웹 채팅 AI는 저장소 파일을 열거나 고칠 수 없으므로, 사용자가 규칙 파일을 첨부하고 결과를 저장소로 가져온다.

## 1. 첨부할 파일
프로젝트·지식 파일 기능이 있는 서비스는 아래 파일을 그 기능에 올려 두고, 없으면 대화를 시작할 때 첨부한다.

| 언제 | 파일 |
|---|---|
| 항상 | `AGENTS.md`, `editorial/style-guide.md`, `editorial/curriculum.md`, `book/appendix/glossary.md` |
| 특정 장을 다룰 때 | 그 장 파일과 선수 장 파일 |
| 장을 검토할 때 | 위에 더해 `editorial/workflow.md`, `editorial/templates/review.md`, `book/appendix/references.md` |

저장소의 파일이 바뀌면 서비스에 올려 둔 사본도 바꾼다. 사본이 낡으면 규칙과 용어가 어긋난다.

## 2. 시작 프롬프트
아래를 복사해 대화 첫머리에 붙여 넣는다.

```text
너는 "AI Insight Notes" 책 편찬 프로젝트의 협업 AI다.
첨부한 AGENTS.md가 규칙의 정본이고, style-guide.md·curriculum.md·glossary.md를 따른다.
너는 저장소 파일을 직접 고칠 수 없다. 그래서 다음처럼 일한다.
1. 내 질문에는 style-guide §2(대화 답변) 규칙으로 답한다.
2. 답 뒤에, 책에 넣을 내용이 있으면 web-chat-kit의 「반영 블록」 형식으로 따로 출력한다.
   반영 블록의 본문은 style-guide §3~§8(책 본문 규칙)을 따른다.
3. 확인하지 못한 사실과 문헌은 본문에 넣지 말고 반영 블록의 「미확인」에 적는다.
   문헌은 실재를 확인한 것만 URL이나 DOI와 함께 쓴다.
4. 내 요청이 첨부한 규칙과 부딪치면 먼저 그 점을 알려 준다.
5. 내가 "반영 보류"라고 하면 반영 블록을 만들지 않는다.
```

## 3. 반영 블록 형식
```text
=== 반영 블록 ===
작성 AI: Grok
대상 장: 3.7 혼동행렬·정밀도·재현율·F1 (book/part03-ml-basics/03-07-precision-recall-f1.md)
대상 절: ## 3. F1 점수 — 새 절
본문:
(책 본문 그대로. 해라체, 강조 상자, 수식, 인용 키 포함)
용어집 추가:
| F1 점수 | F1 score | 평가 | 정밀도와 재현율의 조화평균 | 3.7 |
참고문헌 추가:
- **@키** · 저자. 「제목」. 학회·저널, 연도. URL
미확인:
- (확인하지 못한 주장과 확인 방법)
=== 끝 ===
```
- 「대상 절」에는 새 절인지, 기존 절을 보강하는지 적는다.
- 맞는 장이 curriculum에 없으면 「대상 장: 없음 — 제안: …」으로 적고 본문을 쓰지 않는다.

## 4. 저장소로 가져오기
1. 반영 블록을 `workbench/inbox/YYYY-MM-DD_<ai>_<주제>.md`로 저장한다. 예: `workbench/inbox/2026-11-25_grok_f1-score.md`.
2. 저장소를 여는 AI(Claude Code, Codex, Gemini CLI 등)에게 「inbox 반영해 줘」라고 한다.
3. 그 AI가 [작업 절차 §5](workflow.md#5-웹-채팅다른-세션-결과-들여오기)대로 다시 확인하고 반영한다.
