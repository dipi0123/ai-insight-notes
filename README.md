# AI Insight Notes

AI 모델을 입문부터 전문가 수준까지 공부하며 한 권의 책으로 엮는 프로젝트다. 질문하고, 답을 듣고, 확정된 지식만 책에 쌓는다. 여러 AI(Claude·GPT·Gemini·Grok 등)를 섞어 써도 같은 규칙으로 일하도록 규칙을 한 곳([AGENTS.md](AGENTS.md))에 모았다.

- 책(최종 산출물): [book/README.md](book/README.md)
- 편찬 계획과 진행 상태: [editorial/curriculum.md](editorial/curriculum.md)
- AI 작업 규칙: [AGENTS.md](AGENTS.md)

## 폴더
```text
AGENTS.md            모든 AI 공통 규칙 (정본)
CLAUDE.md            Claude Code 입구 → AGENTS.md를 불러온다
GEMINI.md            Gemini CLI 입구 → AGENTS.md를 불러온다
book/                최종 산출물 — 책
  README.md          표지·읽는 법·목차(목차는 자동 생성)
  partNN-…/          부 폴더, 그 안에 NN-MM-….md 장 파일
  appendix/          용어집·참고문헌
  figures/           그림(SVG 등)
editorial/           편집실 — 책을 만드는 규칙과 계획
  curriculum.md      부·장 구성, 수준, 선수 장, 장별 상태 (정본)
  style-guide.md     집필 규칙
  workflow.md        질문 응답·반영·검토·확정 절차
  decisions.md       편집 결정 대장(ED-xx)과 미정 항목
  open-questions.md  확인이 필요한 주장·문헌
  web-chat-kit.md    웹 채팅 AI용 첨부 목록·시작 프롬프트
  templates/         장·검토 템플릿
workbench/           작업대 — 반영 전 재료 (임시)
tools/book.py        검사·목차 생성·상태 요약
```

## AI별 시작 방법
| AI 도구 | 자동으로 읽는 규칙 파일 | 시작 |
|---|---|---|
| Claude Code (터미널·데스크톱 앱) | `CLAUDE.md` → `AGENTS.md` | 이 폴더를 열고 질문 |
| Codex (CLI·앱) | `AGENTS.md` | 이 폴더를 열고 질문 |
| Gemini CLI | `GEMINI.md` → `AGENTS.md` | 이 폴더에서 실행하고 질문 |
| 그 밖에 AGENTS.md를 읽는 도구(Cursor 등) | `AGENTS.md` | 이 폴더를 열고 질문 |
| 웹 채팅(ChatGPT·Gemini·Grok·Claude.ai 등) | 없음 | [웹 채팅 키트](editorial/web-chat-kit.md)의 파일을 첨부하고 시작 프롬프트를 붙여 넣는다 |

## 자주 쓰는 요청
| 이렇게 말하면 | AI가 하는 일 |
|---|---|
| 「F1은 공식 용어야?」 | 대화로 답하고, 책에 들어갈 내용은 해당 장에 반영한 뒤 바꾼 곳을 알린다 |
| 「반영 보류. ○○가 뭐야?」 | 답만 한다 |
| 「5.2장 써 줘」 | 장 전체를 집필한다([작업 절차 §2](editorial/workflow.md#2-장-집필)) |
| 「5.2장 교차 검토해 줘」 | 집필하지 않은 AI가 검토한다([작업 절차 §3](editorial/workflow.md#3-교차-검토)) |
| 「inbox 반영해 줘」 | `workbench/inbox/`의 재료를 확인해서 책에 반영한다([작업 절차 §5](editorial/workflow.md#5-웹-채팅다른-세션-결과-들여오기)) |
| 「5.2장 확정」 | 장 상태를 확정으로 바꾼다 |
| 「진행 상황 알려 줘」 | `python3 tools/book.py status` 결과를 요약한다 |

## 검사
```bash
python3 tools/book.py toc
python3 tools/book.py check
```
