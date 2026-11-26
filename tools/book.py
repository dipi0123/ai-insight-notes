#!/usr/bin/env python3
"""AI Insight Notes 책 도구 — 검사, 목차 생성, 상태 요약, 웹 사이트 원고 생성.

사용법:
  python3 tools/book.py check    규칙 검사(예제 코드 문법 포함). 오류가 있으면 종료 코드 1
  python3 tools/book.py toc      editorial/curriculum.md로 book/README.md 목차를 다시 만든다
  python3 tools/book.py status   장별 진행 상태를 요약한다
  python3 tools/book.py site     검사를 통과하면 웹 사이트용 원고(build/site-src)와
                                 설정(build/zensical.toml)을 만든다. 그다음
                                 zensical build -f build/zensical.toml 로 사이트를 만든다

책 전체 집필(작업 절차 §10)에 쓰는 명령:
  python3 tools/book.py lint 3.7 [--stage 폴더] [--delta 파일] [--json 결과파일]
                                 장 하나를 검토완료 요건·용어 표기·링크·인용까지 검사한다.
                                 --stage를 주면 그 폴더(저장소와 같은 배치)의 초안을 먼저 본다
  python3 tools/book.py sentences 3.7 [--stage 폴더] [--json 결과파일]
                                 장을 문장 단위로 나누고 문장 번호와 장 내용 해시를 낸다
  python3 tools/book.py slice --chapter 3.7 | --before 3.7 | --terms "a,b"
                                 용어집에서 필요한 행만 뽑는다
  python3 tools/book.py hashes [--out 파일]
                                 공유 파일의 sha256을 적는다(묶음을 시작할 때)
  python3 tools/book.py merge 변경분.json ... [--dry-run] [--base 해시파일] [--oq-floor N]
                                 집필 패스가 낸 변경분을 용어집·참고문헌·미확인 목록·curriculum
                                 상태에 반영하고 초안을 book/에 놓는다(통합 패스만 쓴다)
  자세한 쓰임과 변경분 형식은 tools/harness/README.md에 있다.

표준 라이브러리만 쓴다. 규칙의 정본은 AGENTS.md와 editorial/ 문서이고,
이 스크립트는 그중 기계로 확인할 수 있는 것만 확인한다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
CURRICULUM = ROOT / "editorial" / "curriculum.md"
BOOK_README = BOOK / "README.md"
REFERENCES = BOOK / "appendix" / "references.md"
GLOSSARY = BOOK / "appendix" / "glossary.md"
OPEN_QUESTIONS = ROOT / "editorial" / "open-questions.md"

TOC_START = "<!-- TOC:START -->"
TOC_END = "<!-- TOC:END -->"

CODE = BOOK / "code"

STATUSES = ("계획", "초고", "검토완료", "확정")
LEVELS = ("L1", "L2", "L3", "L4", "L5")

# 집필 규칙 §4: 학습 방법·성능 고도화 부의 장은 「구조와의 연결」 절을 둔다.
STRUCTURE_LINK_PARTS = {8, 9, 10, 12}
STRUCTURE_LINK_HEADING = "## 구조와의 연결"
# 집필 규칙 §4: 「직접 만들기:」「프로젝트:」 장의 필수 절.
BUILD_PREFIXES = ("직접 만들기:", "프로젝트:")
BUILD_HEADINGS = ("## 만들 것", "## 준비물", "## 실행 결과", "## 바꿔 보기")

# 링크 검사에서 뺄 경로(저장소 기준 앞부분). 템플릿은 자리표시 링크를 담고, 작업대는 임시 재료이고,
# build/는 site 명령이 만든 산출물이다.
LINK_SKIP = ("workbench/", "editorial/templates/", "build/", "node_modules/")
# 저장소를 훑을 때 들어가지 않는 폴더. 점으로 시작하는 폴더(.git·.venv 등)도 들어가지 않는다.
WALK_SKIP_DIRS = {"build", "node_modules", "__pycache__"}

# 웹 사이트(ED-16). 설정의 정본은 tools/site/config.toml이고, 목차는 curriculum에서 만든다.
SITE_TOOLS = ROOT / "tools" / "site"
SITE_CONFIG = SITE_TOOLS / "config.toml"
SITE_ASSETS = SITE_TOOLS / "assets"
BUILD = ROOT / "build"
SITE_SRC = BUILD / "site-src"
SITE_BUILD_CONFIG = BUILD / "zensical.toml"
SITE_BRANCH = "main"
SITE_GENERATED = ("nav", "docs_dir", "site_dir")

# 책 전체 집필 하네스(작업 절차 §10). 작업 파일은 git에 올리지 않는 build/harness/에 둔다.
HARNESS = BUILD / "harness"
TOOL_VERSION = "2026.11.3"  # lint·sentences·merge 결과에 적는 도구 판. 검사 내용을 바꾸면 올린다

# 집필 규칙 §5: 용어집 「분류」 칸의 값.
CATEGORIES = ("분야", "구조", "과제", "방식", "학습신호", "규모·활용", "학습과정", "평가", "데이터", "수학", "시스템")
GLOSSARY_HEADER = ("표기", "풀이·다른 이름", "한국어", "분류", "한 줄 정의", "본 장")
# 집필 규칙 §4: 강조 상자는 네 가지만 쓴다.
BOXES = ("핵심", "주의", "표준과 관례", "현업 사례")
# 집필 규칙 §3: 시점을 가리키는 말. 「(2026년 기준)」처럼 기준 시점을 적은 줄은 경고하지 않는다.
TIME_WORDS = re.compile(r"최근|요즘|새로 나온|최신")
# 용어집 한국어 칸과 겹치지만 일반 서술로 흔히 쓰는 말. 「번역어 단독 사용」 후보에서 뺀다.
# 임시 목록이다. 정식 허용 목록은 사용자 승인으로 style-guide §5에 둔다(설계안 9절 8).
EVERYDAY_KO = {"구조", "환경", "행동", "표현", "특징", "층", "음성", "손실", "정책", "클래스", "패치", "토큰", "잡음"}

# 개발자 독자에게 직역투로 읽히는 낱말(style-guide §5). (정규식, 표시 이름, 흔히 쓰는 말). lint가 후보로 알리고 렌즈가 판정한다.
# 새로 발견한 말은 여기에 더한다.
LITERAL_KO = [
    (r"한살이", "한살이", "lifecycle"),
    (r"갈래", "갈래", "분야·종류·범주"),
    (r"짝(?!지)", "짝", "쌍"),
    (r"(?<![가-힣])판(?=이다|이|은|을|의|마다|에서|으로|[)\s,.])", "판", "버전"),
    (r"꼬리", "꼬리", "접미사"),
    (r"견[주준줄]", "견주다", "비교하다"),
    (r"걷어\s?[내낸냈낼]", "걷어 내다", "제거하다"),
    (r"되풀이", "되풀이", "반복"),
    (r"짜임", "짜임", "구성"),
    (r"도우미", "도우미", "어시스턴트"),
    (r"지어\s?[올오][리린렸릴]", "지어 올리다", "쌓아 가다"),
]

# book/ 안에서 쓰면 안 되는 표현. 확실한 신호만 둔다(오탐을 피하려고 일반 단어는 넣지 않는다).
FORBIDDEN = [
    (re.compile(r"질문하신|말씀하신|말씀드린|문의하신"), "대화체 — 책은 특정 대화·사람을 가리키지 않는다"),
    (re.compile(r"우리 대화|이 대화에서|앞선 대화|지난 대화"), "대화 언급 — 책에는 대화 이력을 쓰지 않는다"),
    (re.compile(r"(?<![A-Za-z])(TODO|TBD|FIXME)(?![A-Za-z])"), "미완 표시 — 미확인 목록이나 workbench로 보낸다"),
    (re.compile(r"변경 이력|수정 이력|작성일|수정일|작성자\s*:"), "이력·작성 정보 — 이력은 git이 맡는다"),
    (re.compile(r"(Claude|GPT|Gemini|Grok|Codex)\s*(가|이)?\s*(작성|집필|검토|정리)(함|했|한|됨)"), "AI 서명 — 집필·검토 AI는 curriculum 상태 칸에만 적는다"),
]

PART_RE = re.compile(r"^##\s+(\d+)부\.\s+(.+?)\s*$")
CHAPTER_NUM_RE = re.compile(r"^(\d+)\.(\d+)$")
PATH_RE = re.compile(r"^book/part(\d{2})-[a-z0-9-]+/(\d{2})-(\d{2})-[a-z0-9-]+\.md$")
LINK_RE = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
CITE_RE = re.compile(r"\[(@[^\]]+)\]")
REF_ENTRY_RE = re.compile(r"^- \*\*@([A-Za-z][A-Za-z0-9_-]*)\*\*")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
CHAPTER_ITEM_RE = re.compile(r"^(?:\[(\d+\.\d+)\]\(([^)\s]+)\)|(\d+\.\d+))$")
OQ_ID_RE = re.compile(r"OQ-(\d{3})")
REF_ID_RES = (
    re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})"),
    re.compile(r"doi\.org/(10\.[^\s)]+)", re.I),
)
SEP_ROW_RE = re.compile(r"^\|?\s*:?-{3,}")


@dataclass
class Chapter:
    num: str
    part: int
    idx: int
    title: str
    level: str
    prereqs: list
    question: str
    path: str
    status: str
    status_raw: str
    line: int


@dataclass
class Part:
    num: int
    title: str
    chapters: list


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def read(path: Path) -> str:
    return nfc(path.read_text(encoding="utf-8"))


def prose_lines(text: str):
    """코드 블록 밖의 줄만 (줄 번호, 줄)로 돌려준다."""
    in_fence = False
    fence = ""
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            mark = stripped[:3]
            if not in_fence:
                in_fence, fence = True, mark
            elif mark == fence:
                in_fence = False
            continue
        if not in_fence:
            yield i, line


# ---------------------------------------------------------------- curriculum

def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_curriculum(rep: Report) -> list[Part]:
    where = rel(CURRICULUM)
    if not CURRICULUM.exists():
        rep.error(where, "파일이 없다")
        return []
    parts: list[Part] = []
    for i, line in prose_lines(read(CURRICULUM)):
        m = PART_RE.match(line)
        if m:
            parts.append(Part(int(m.group(1)), m.group(2), []))
            continue
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if not cells or not CHAPTER_NUM_RE.match(cells[0]):
            continue
        loc = f"{where}:{i}"
        if len(cells) != 7:
            rep.error(loc, f"장 행의 칸이 7개가 아니라 {len(cells)}개다(칸 안에 | 를 쓰지 않는다)")
            continue
        if not parts:
            rep.error(loc, "부 제목(## N부. 제목) 앞에 장 행이 있다")
            continue
        num, title, level, prereq, question, path, status_raw = cells
        p, c = (int(x) for x in CHAPTER_NUM_RE.match(num).groups())
        path = path.strip("`").strip()
        status = status_raw.split("·")[0].strip()
        prereqs = [] if prereq in ("—", "-", "") else [x.strip() for x in prereq.split(",") if x.strip()]
        parts[-1].chapters.append(
            Chapter(num, p, c, title, level, prereqs, question, path, status, status_raw, i)
        )
    return parts


def check_curriculum(parts: list[Part], rep: Report) -> dict[str, Chapter]:
    where = rel(CURRICULUM)
    chapters: dict[str, Chapter] = {}
    seen_parts: set[int] = set()
    seen_paths: set[str] = set()
    for part in parts:
        if part.num in seen_parts:
            rep.error(where, f"{part.num}부가 두 번 있다")
        seen_parts.add(part.num)
        if not part.chapters:
            rep.warn(where, f"{part.num}부에 장이 없다")
        for ch in part.chapters:
            loc = f"{where}:{ch.line}"
            if ch.num in chapters:
                rep.error(loc, f"장 번호 {ch.num}이 두 번 있다")
            chapters[ch.num] = ch
            if ch.part != part.num:
                rep.error(loc, f"{ch.num}장이 {part.num}부 표에 있다")
            if ch.level not in LEVELS:
                rep.error(loc, f"수준 '{ch.level}'은 L1~L5가 아니다")
            m = PATH_RE.match(ch.path)
            if not m:
                rep.error(loc, f"파일 경로 '{ch.path}'가 book/partNN-슬러그/NN-MM-슬러그.md 형식이 아니다")
            elif (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (ch.part, ch.part, ch.idx):
                rep.error(loc, f"파일 경로 '{ch.path}'의 번호가 장 번호 {ch.num}과 다르다")
            if ch.path in seen_paths:
                rep.error(loc, f"파일 경로 '{ch.path}'가 두 장에 쓰였다")
            seen_paths.add(ch.path)
            check_status(ch, loc, rep)
    for ch in chapters.values():
        loc = f"{where}:{ch.line}"
        for pre in ch.prereqs:
            if pre == ch.num:
                rep.error(loc, f"{ch.num}장이 자기 자신을 선수 장으로 둔다")
            elif pre not in chapters:
                rep.error(loc, f"선수 장 '{pre}'가 curriculum에 없다")
    return chapters


def check_status(ch: Chapter, loc: str, rep: Report) -> None:
    if ch.status not in STATUSES:
        rep.error(loc, f"상태 '{ch.status_raw}'의 첫 값은 {'·'.join(STATUSES)} 중 하나여야 한다")
        return
    exists = (ROOT / ch.path).exists()
    if ch.status == "계획":
        if exists:
            rep.error(loc, f"{ch.num}장 파일이 있는데 상태가 계획이다 — 초고 이상으로 바꾼다")
        return
    if not exists:
        rep.error(loc, f"{ch.num}장 상태가 {ch.status}인데 파일 {ch.path}가 없다")
    people = ch.status_raw.split("·", 1)[1].strip() if "·" in ch.status_raw else ""
    names = [n.strip() for n in people.split("/") if n.strip()]
    if ch.status == "초고":
        if len(names) < 1:
            rep.error(loc, f"{ch.num}장 상태에 집필 AI가 없다(예: 초고 · Claude)")
    else:
        if len(names) != 2:
            rep.error(loc, f"{ch.num}장 상태는 '{ch.status} · 집필AI / 검토AI' 형식이어야 한다")
        elif names[0].lower() == names[1].lower():
            rep.error(loc, f"{ch.num}장의 검토 AI가 집필 AI와 같다(ED-08)")


# ---------------------------------------------------------------- 장 파일

def check_chapter_files(chapters: dict[str, Chapter], rep: Report) -> None:
    listed = {ch.path for ch in chapters.values()}
    for path in sorted(BOOK.glob("part*/**/*.md")):
        if rel(path) not in listed:
            rep.error(rel(path), "curriculum에 없는 장 파일이다 — 구성 변경은 사용자 결정(ED-12)")
    for ch in chapters.values():
        path = ROOT / ch.path
        if ch.status == "계획" or not path.exists():
            continue
        text = read(path)
        lines = text.splitlines()
        first = next((ln for ln in lines if ln.strip()), "")
        want = f"# {ch.num} {ch.title}"
        if first.strip() != want:
            rep.error(f"{ch.path}:1", f"첫 줄이 '{want}'여야 한다(curriculum과 같게)")
        meta = next((ln for ln in lines if ln.startswith("> **수준**")), None)
        want_meta = expected_meta(ch, chapters)
        if meta is None:
            rep.error(ch.path, "메타 줄(> **수준** …)이 없다")
        elif not meta.startswith(f"> **수준** {ch.level}"):
            rep.error(ch.path, f"메타 줄의 수준이 curriculum의 {ch.level}과 다르다")
        elif want_meta and meta.strip() != want_meta:
            rep.error(ch.path, f"메타 줄이 curriculum과 다르다 — 이렇게 쓴다: {want_meta}")
        headings = {ln.strip() for _, ln in prose_lines(text) if ln.startswith("## ")}
        required = ["## 한눈에"]
        if ch.status in ("검토완료", "확정"):
            required += ["## 정리", "## 확인 문제"]
            is_build = ch.title.startswith(BUILD_PREFIXES)
            if is_build:
                required += list(BUILD_HEADINGS)
                if ch.title.startswith("프로젝트:"):
                    required.append("## 설계 결정")
            elif ch.part in STRUCTURE_LINK_PARTS:
                required.append(STRUCTURE_LINK_HEADING)
        for h in required:
            if h not in headings:
                rep.error(ch.path, f"'{h}' 절이 없다(상태 {ch.status})")


def chapter_href(ch: Chapter, src: Path) -> str:
    """src 파일에서 ch장 파일로 가는 상대 경로."""
    return Path(os.path.relpath(ROOT / ch.path, src.parent)).as_posix()


def expected_meta(ch: Chapter, chapters: dict[str, Chapter]) -> str | None:
    """curriculum으로 만든 메타 줄. 선수 장이 curriculum에 없으면 None(그 오류는 따로 난다)."""
    if any(p not in chapters for p in ch.prereqs):
        return None
    src = ROOT / ch.path
    pre = ", ".join(f"[{chapters[p].num} {chapters[p].title}]({chapter_href(chapters[p], src)})" for p in ch.prereqs)
    return f"> **수준** {ch.level} · **선수** {pre or '—'} · **이 장의 질문** {ch.question}"


def check_forbidden(rep: Report) -> None:
    for path in sorted(BOOK.rglob("*.md")):
        for i, line in prose_lines(read(path)):
            for pattern, why in FORBIDDEN:
                m = pattern.search(line)
                if m:
                    rep.error(f"{rel(path)}:{i}", f"'{m.group(0)}' — {why}")


# ---------------------------------------------------------------- 링크와 앵커

def slugify(text: str) -> str:
    """GitHub 방식에 가까운 제목 앵커."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    out = []
    for ch in nfc(text).strip().lower():
        if ch == " ":
            out.append("-")
        elif ch in "-_":
            out.append(ch)
        elif unicodedata.category(ch)[0] in "LNM":
            out.append(ch)
    return "".join(out)


_anchor_cache: dict[Path, set[str]] = {}


def anchors_of(path: Path) -> set[str]:
    if path not in _anchor_cache:
        found: set[str] = set()
        counts: dict[str, int] = {}
        for _, line in prose_lines(read(path)):
            m = HEADING_RE.match(line)
            if not m:
                continue
            base = slugify(m.group(2))
            n = counts.get(base, 0)
            found.add(base if n == 0 else f"{base}-{n}")
            counts[base] = n + 1
        _anchor_cache[path] = found
    return _anchor_cache[path]


def markdown_files() -> list[Path]:
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in WALK_SKIP_DIRS]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = Path(dirpath) / name
            if not any(rel(path).startswith(s) for s in LINK_SKIP):
                files.append(path)
    return sorted(files)


def check_links(rep: Report) -> None:
    for src in markdown_files():
        for i, line in prose_lines(read(src)):
            for m in LINK_RE.finditer(INLINE_CODE_RE.sub("", line)):
                target = m.group(1)
                if "://" in target or target.startswith("mailto:"):
                    continue
                path_part, _, anchor = target.partition("#")
                dest = src if not path_part else (src.parent / unquote(path_part)).resolve()
                loc = f"{rel(src)}:{i}"
                if not dest.exists():
                    rep.error(loc, f"링크 대상 '{target}'이 없다")
                    continue
                if anchor and dest.suffix == ".md" and dest.is_file():
                    if nfc(unquote(anchor)).lower() not in anchors_of(dest):
                        rep.error(loc, f"링크 '{target}'의 앵커가 {rel(dest)}에 없다")


# ---------------------------------------------------------------- 인용

def check_citations(rep: Report) -> None:
    if not REFERENCES.exists():
        rep.error(rel(REFERENCES), "파일이 없다")
        return
    keys: dict[str, int] = {}
    for i, line in prose_lines(read(REFERENCES)):
        m = REF_ENTRY_RE.match(line)
        if not m:
            continue
        key = m.group(1)
        loc = f"{rel(REFERENCES)}:{i}"
        if key in keys:
            rep.error(loc, f"참고문헌 키 @{key}가 두 번 있다")
        keys[key] = i
        if "http" not in line and "doi" not in line.lower():
            rep.error(loc, f"@{key}에 URL이나 DOI가 없다(ED-10)")
    used: set[str] = set()
    for path in sorted(BOOK.rglob("*.md")):
        if path == REFERENCES:
            continue
        for i, line in prose_lines(read(path)):
            for m in CITE_RE.finditer(INLINE_CODE_RE.sub("", line)):
                for part in m.group(1).split(";"):
                    key = part.strip().lstrip("@").strip()
                    if not key:
                        continue
                    used.add(key)
                    if key not in keys:
                        rep.error(f"{rel(path)}:{i}", f"인용 키 @{key}가 참고문헌에 없다")
    for key, i in keys.items():
        if key not in used:
            rep.warn(f"{rel(REFERENCES)}:{i}", f"@{key}를 인용하는 장이 없다")


# ---------------------------------------------------------------- 예제 코드

def check_code(rep: Report) -> None:
    """book/code/의 Python 파일이 문법 오류 없이 컴파일되는지 본다(실행은 하지 않는다)."""
    if not CODE.exists():
        return
    for path in sorted(CODE.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as e:
            rep.error(f"{rel(path)}:{e.lineno}", f"Python 문법 오류 — {e.msg}")


# ---------------------------------------------------------------- 공유 파일 형식

def chapter_order(chapters: dict[str, Chapter]) -> dict[str, int]:
    """장 번호 → 책 순서(curriculum 순서)."""
    return {num: i for i, num in enumerate(chapters)}


def glossary_table(lines: list[str]):
    """용어집 표의 (머리줄 인덱스, 끝 인덱스(제외), [(줄 인덱스, 칸 목록)]). 표가 없으면 None."""
    head = next((i for i, ln in enumerate(lines) if ln.startswith("| 표기 |")), None)
    if head is None:
        return None
    rows = []
    j = head + 2
    while j < len(lines) and lines[j].lstrip().startswith("|"):
        rows.append((j, split_row(lines[j])))
        j += 1
    return head, j, rows


def parse_chapter_items(cell: str):
    """용어집 「본 장」 칸을 [(장 번호, 링크 또는 None)]로 나눈다. 형식이 틀리면 None."""
    if cell in ("", "—"):
        return []
    out = []
    for item in cell.split(", "):
        m = CHAPTER_ITEM_RE.match(item.strip())
        if not m:
            return None
        out.append((m.group(1), m.group(2)) if m.group(1) else (m.group(3), None))
    return out


def check_glossary(chapters: dict[str, Chapter], rep: Report) -> None:
    where = rel(GLOSSARY)
    if not GLOSSARY.exists():
        rep.error(where, "파일이 없다")
        return
    lines = read(GLOSSARY).splitlines()
    table = glossary_table(lines)
    if table is None:
        rep.error(where, "용어집 표의 머리줄(| 표기 | …)이 없다")
        return
    head, end, rows = table
    if tuple(split_row(lines[head])) != GLOSSARY_HEADER:
        rep.error(f"{where}:{head + 1}", "머리줄이 '| " + " | ".join(GLOSSARY_HEADER) + " |'가 아니다")
    if any(ln.strip() for ln in lines[end:]):
        rep.error(f"{where}:{end + 1}", "용어집 표 뒤에 다른 내용이 있다(표에 빈 줄을 넣지 않는다)")
    order = chapter_order(chapters)
    seen: dict[str, int] = {}
    prev = None
    for idx, cells in rows:
        loc = f"{where}:{idx + 1}"
        if len(cells) != len(GLOSSARY_HEADER):
            rep.error(loc, f"칸이 {len(GLOSSARY_HEADER)}개가 아니라 {len(cells)}개다(칸 안에 | 를 쓰지 않는다)")
            continue
        term, alias, ko, cat, definition, home = cells
        key = term.casefold()
        if key in seen:
            rep.error(loc, f"'{term}'이 {seen[key]}행에도 있다")
        seen[key] = idx + 1
        if prev is not None and key < prev:
            rep.error(loc, f"'{term}'이 알파벳순(대소문자 무시)에서 벗어났다")
        prev = key
        if cat not in CATEGORIES:
            rep.error(loc, f"분류 '{cat}'은 style-guide §5의 값이 아니다")
        for name, val in (("표기", term), ("풀이·다른 이름", alias), ("한국어", ko), ("한 줄 정의", definition)):
            if not val:
                rep.error(loc, f"{name} 칸이 비었다(없으면 —)")
        items = parse_chapter_items(home)
        if items is None:
            rep.error(loc, f"본 장 칸 '{home}'은 '[N.M](경로), N.M' 형식이 아니다")
            continue
        nums = [n for n, _ in items]
        if len(set(nums)) != len(nums):
            rep.error(loc, "본 장 칸에 같은 장이 두 번 있다")
        for n, link in items:
            ch = chapters.get(n)
            if ch is None:
                rep.error(loc, f"본 장 {n}이 curriculum에 없다")
                continue
            if link is not None:
                want = chapter_href(ch, GLOSSARY)
                if link != want:
                    rep.error(loc, f"본 장 {n}의 링크는 '{want}'여야 한다")
            elif (ROOT / ch.path).exists():
                rep.warn(loc, f"본 장 {n}은 파일이 있으니 링크로 건다")
        known = [order[n] for n in nums if n in order]
        if known != sorted(known):
            rep.error(loc, "본 장 칸의 장 번호가 책 순서가 아니다")


def reference_entries(lines: list[str]) -> list[tuple[int, str]]:
    """참고문헌 항목의 (줄 인덱스, 키)."""
    out = []
    for i, ln in enumerate(lines):
        m = REF_ENTRY_RE.match(ln)
        if m:
            out.append((i, m.group(1)))
    return out


def reference_line_problems(line: str) -> list[str]:
    """참고문헌 항목 한 줄의 형식 문제(style-guide §7)."""
    m = REF_ENTRY_RE.match(line)
    if not m:
        return ["'- **@키** · …'로 시작하지 않는다"]
    key = m.group(1)
    problems = []
    if not line.startswith(f"- **@{key}** · "):
        problems.append("키 뒤에 ' · '를 둔다")
    if "「" not in line or "」" not in line:
        problems.append("제목을 「」로 감싼다")
    if not re.search(r"https?://\S+$", line.rstrip()):
        problems.append("끝에 URL이나 DOI 링크를 둔다(ED-10)")
    if "|" in line:
        problems.append("| 를 쓰지 않는다")
    return problems


def reference_ids(line: str) -> list[str]:
    ids = []
    for rx in REF_ID_RES:
        ids += [m.group(1).lower().rstrip(".") for m in rx.finditer(line)]
    return ids


def check_reference_format(rep: Report) -> None:
    if not REFERENCES.exists():
        return
    lines = read(REFERENCES).splitlines()
    where = rel(REFERENCES)
    prev = None
    ids: dict[str, str] = {}
    entries = reference_entries(lines)
    for i, key in entries:
        loc = f"{where}:{i + 1}"
        for p in reference_line_problems(lines[i]):
            rep.error(loc, f"@{key}: {p}")
        if prev is not None and key.casefold() < prev:
            rep.error(loc, f"@{key}가 키의 알파벳순에서 벗어났다")
        prev = key.casefold()
        for ident in reference_ids(lines[i]):
            if ident in ids and ids[ident] != key:
                rep.error(loc, f"@{key}와 @{ids[ident]}가 같은 문헌({ident})이다")
            ids[ident] = key
    if entries:
        first, last = entries[0][0], entries[-1][0]
        if last - first + 1 != len(entries):
            rep.error(f"{where}:{first + 1}", "참고문헌 항목 사이에 다른 줄이 있다")


def oq_rows(lines: list[str]) -> list[tuple[int, list[str]]]:
    return [(i, split_row(ln)) for i, ln in enumerate(lines) if ln.lstrip().startswith("| OQ-")]


def check_open_questions(rep: Report) -> None:
    where = rel(OPEN_QUESTIONS)
    if not OPEN_QUESTIONS.exists():
        rep.error(where, "파일이 없다")
        return
    lines = read(OPEN_QUESTIONS).splitlines()
    if not any(ln.startswith("| ID |") for ln in lines):
        rep.error(where, "미확인 표의 머리줄(| ID | …)이 없다")
    seen: set[str] = set()
    for i, cells in oq_rows(lines):
        loc = f"{where}:{i + 1}"
        if len(cells) != 4:
            rep.error(loc, f"칸이 4개가 아니라 {len(cells)}개다(칸 안에 | 를 쓰지 않는다)")
            continue
        if not re.fullmatch(r"OQ-\d{3}", cells[0]):
            rep.error(loc, f"ID '{cells[0]}'는 OQ-세 자리 번호가 아니다")
        if cells[0] in seen:
            rep.error(loc, f"{cells[0]}이 두 번 있다")
        seen.add(cells[0])
        if not all(cells):
            rep.error(loc, "빈 칸이 있다")


# ---------------------------------------------------------------- 목차

def build_toc(parts: list[Part]) -> str:
    out: list[str] = []
    for part in parts:
        out.append(f"### {part.num}부. {part.title}")
        out.append("")
        for ch in part.chapters:
            label = f"{ch.num} {ch.title}"
            if ch.status != "계획" and (ROOT / ch.path).exists():
                link = Path(ch.path).relative_to("book").as_posix()
                out.append(f"- [{label}]({link}) · {ch.level}")
            else:
                out.append(f"- {label} · {ch.level}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def readme_toc_block(text: str) -> tuple[int, int] | None:
    start = text.find(TOC_START)
    end = text.find(TOC_END)
    if start < 0 or end < 0 or end < start:
        return None
    return start + len(TOC_START), end


def check_toc(parts: list[Part], rep: Report) -> None:
    text = read(BOOK_README)
    span = readme_toc_block(text)
    if span is None:
        rep.error(rel(BOOK_README), f"목차 표시 {TOC_START} / {TOC_END}가 없다")
        return
    current = text[span[0]:span[1]].strip("\n")
    if current != build_toc(parts).strip("\n"):
        rep.error(rel(BOOK_README), "목차가 curriculum과 다르다 — python3 tools/book.py toc 를 실행한다")


def cmd_toc() -> int:
    rep = Report()
    parts = parse_curriculum(rep)
    check_curriculum(parts, rep)
    if rep.errors:
        print_report(rep)
        print("curriculum 오류 때문에 목차를 만들지 않았다.")
        return 1
    text = read(BOOK_README)
    span = readme_toc_block(text)
    if span is None:
        print(f"{rel(BOOK_README)}: 목차 표시 {TOC_START} / {TOC_END}가 없다")
        return 1
    new = text[: span[0]] + "\n" + build_toc(parts) + text[span[1]:]
    if new != text:
        BOOK_README.write_text(new, encoding="utf-8")
        print(f"{rel(BOOK_README)} 목차를 갱신했다.")
    else:
        print("목차가 이미 최신이다.")
    return 0


# ---------------------------------------------------------------- 웹 사이트

def toml_key(key: str) -> str:
    return key if re.fullmatch(r"[A-Za-z0-9_-]+", key) else json.dumps(key, ensure_ascii=False)


def toml_value(value) -> str:
    """사이트 설정에 필요한 만큼만 TOML로 쓴다. 표는 한 줄짜리 인라인 표로 쓴다."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{toml_key(k)} = {toml_value(v)}" for k, v in value.items()) + " }"
    raise TypeError(f"TOML로 쓸 수 없는 값: {value!r}")


def toml_dump(config: dict) -> str:
    out = [f"# tools/book.py site가 만든 파일이다. 고치지 말고 {rel(SITE_CONFIG)} 파일과 curriculum을 고친다."]
    for table, items in config.items():
        out.append(f"[{toml_key(table)}]")
        out += [f"{toml_key(k)} = {toml_value(v)}" for k, v in items.items()]
    return "\n".join(out) + "\n"


def title_of(path: Path) -> str:
    for line in read(path).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def site_nav(parts: list[Part]) -> list:
    """사이트 목차: 처음 → 실린 장이 있는 부 → 부록. 계획 상태의 장은 넣지 않는다."""
    nav: list = [{"처음": "index.md"}]
    for part in parts:
        items = [
            {f"{ch.num} {ch.title}": Path(ch.path).relative_to("book").as_posix()}
            for ch in part.chapters
            if ch.status != "계획" and (ROOT / ch.path).exists()
        ]
        if items:
            nav.append({f"{part.num}부. {part.title}": items})
    appendix = [
        {title_of(p): p.relative_to(BOOK).as_posix()}
        for p in sorted((BOOK / "appendix").glob("*.md"), key=lambda p: p.name)
    ]
    if (CODE / "README.md").exists():
        appendix.append({title_of(CODE / "README.md"): "code/index.md"})
    if appendix:
        nav.append({"부록": appendix})
    return nav


def in_dir(path: Path, folder: Path) -> bool:
    return path == folder or folder in path.parents


def site_link(target: str, src: Path, repo_url: str) -> str:
    """책 안의 Markdown 링크는 그대로(README.md는 index.md로) 두고, 사이트에 실리지 않는 곳
    (책 밖, 예제 코드 파일·폴더)을 가리키는 링크는 GitHub 주소로 바꾼다."""
    if "://" in target or target.startswith(("mailto:", "#")):
        return target
    path_part, sharp, anchor = target.partition("#")
    dest = (src.parent / unquote(path_part)).resolve()
    if in_dir(dest, BOOK) and dest.suffix == ".md":
        if dest.name == "README.md" and path_part.endswith("README.md"):
            path_part = path_part[: -len("README.md")] + "index.md"
        return path_part + sharp + anchor
    if in_dir(dest, BOOK) and not in_dir(dest, CODE) and dest.is_file():
        return target
    kind = "tree" if dest.is_dir() else "blob"
    return f"{repo_url.rstrip('/')}/{kind}/{SITE_BRANCH}/{rel(dest)}" + sharp + anchor


def site_prose(text: str, src: Path, repo_url: str, ref_rel: str) -> str:
    """코드가 아닌 글 조각에서 링크를 고치고 [@키] 인용을 참고문헌 링크로 바꾼다."""
    text = LINK_RE.sub(
        lambda m: m.group(0).replace(m.group(1), site_link(m.group(1), src, repo_url), 1), text
    )

    def cite(m: re.Match) -> str:
        keys = [k.strip().lstrip("@").strip() for k in m.group(1).split(";")]
        return "\\[" + "; ".join(f"[{k}]({ref_rel}#ref-{k})" for k in keys if k) + "\\]"

    return CITE_RE.sub(cite, text)


def site_markdown(text: str, src: Path, repo_url: str) -> str:
    ref_rel = Path(os.path.relpath(REFERENCES, src.parent)).as_posix()
    prose = dict(prose_lines(text))
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if i in prose:
            ref = REF_ENTRY_RE.match(line) if src == REFERENCES else None
            if ref:
                # 인용 링크(#ref-키)가 닿을 자리를 항목 앞에 만든다.
                line = f'- <span id="ref-{ref.group(1)}"></span>' + line[2:]
            elif re.match(r"^\s*<details>\s*$", line):
                # GitHub처럼 접힌 답 안의 Markdown도 그려지게 한다(md_in_html).
                line = line.replace("<details>", '<details markdown="1">')
            else:
                pieces, last = [], 0
                for m in INLINE_CODE_RE.finditer(line):
                    pieces.append(site_prose(line[last:m.start()], src, repo_url, ref_rel))
                    pieces.append(m.group(0))
                    last = m.end()
                pieces.append(site_prose(line[last:], src, repo_url, ref_rel))
                line = "".join(pieces)
        out.append(line)
    return "\n".join(out) + "\n"


def cmd_site() -> int:
    rep = Report()
    parts = run_checks(rep)
    if rep.errors:
        print_report(rep)
        print("검사 오류 때문에 사이트 원고를 만들지 않았다.")
        return 1
    config = tomllib.loads(SITE_CONFIG.read_text(encoding="utf-8"))
    project = config.get("project", {})
    for key in SITE_GENERATED:
        if key in project:
            print(f"{rel(SITE_CONFIG)}: {key}는 쓰지 않는다 — site 명령이 채운다")
            return 1
    repo_url = project.get("repo_url")
    if not repo_url:
        print(f"{rel(SITE_CONFIG)}: repo_url이 없다 — 책 밖을 가리키는 링크를 바꿀 수 없다")
        return 1

    if SITE_SRC.exists():
        shutil.rmtree(SITE_SRC)
    for path in sorted(BOOK.rglob("*")):
        if path.is_dir() or path.name.startswith(".") or "__pycache__" in path.parts:
            continue
        if in_dir(path, CODE) and path.suffix != ".md":
            continue  # 예제 코드 파일은 GitHub에서 본다(링크는 site_link가 바꾼다)
        target = path.relative_to(BOOK)
        if path.name == "README.md":
            target = target.with_name("index.md")
        dest = SITE_SRC / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".md":
            dest.write_text(site_markdown(read(path), path, repo_url), encoding="utf-8")
        else:
            shutil.copy2(path, dest)
    if SITE_ASSETS.exists():
        shutil.copytree(SITE_ASSETS, SITE_SRC, dirs_exist_ok=True)

    config["project"] = {**project, "docs_dir": SITE_SRC.name, "site_dir": "site", "nav": site_nav(parts)}
    SITE_BUILD_CONFIG.write_text(toml_dump(config), encoding="utf-8")
    zensical = ROOT / ".venv" / "bin" / "zensical"
    cmd = rel(zensical) if zensical.exists() else "zensical"
    print(f"{rel(SITE_SRC)}/와 {rel(SITE_BUILD_CONFIG)}을 만들었다.")
    print(f"  사이트 만들기: {cmd} build -f {rel(SITE_BUILD_CONFIG)}   (결과: {rel(BUILD)}/site/)")
    print(f"  미리 보기:     {cmd} serve -f {rel(SITE_BUILD_CONFIG)}")
    return 0


# ---------------------------------------------------------------- 하네스: 공통

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_chapters() -> dict[str, Chapter]:
    """curriculum의 장 목록. 하네스 명령은 curriculum 오류를 따로 보고하지 않는다(check가 맡는다)."""
    return check_curriculum(parse_curriculum(Report()), Report())


def in_repo(path: Path) -> Path | None:
    try:
        return path.resolve().relative_to(ROOT)
    except ValueError:
        return None


def staged(path: Path, stage: Path | None) -> Path:
    """저장소 경로 path에 대응하는 stage 안 파일이 있으면 그것을, 없으면 저장소 파일을 돌려준다.
    stage는 저장소와 같은 배치다(예: stage/book/part01-…/01-05-….md)."""
    if stage is not None:
        r = in_repo(path)
        if r is not None and (stage / r).exists():
            return stage / r
    return path


def staged_any(path: Path, stage: Path | None) -> Path:
    """staged()와 같되, 같은 묶음의 다른 장 초안(build/harness/*/stage)도 찾는다."""
    found = staged(path, stage)
    if found is not path:
        return found
    r = in_repo(path)
    if r is not None and HARNESS.is_dir():
        for other in sorted(HARNESS.glob("*/stage")):
            if (other / r).exists():
                return other / r
    return path


def default_stage(num: str) -> Path | None:
    d = HARNESS / num / "stage"
    return d if d.is_dir() else None


def default_delta(num: str) -> Path | None:
    f = HARNESS / num / "delta.json"
    return f if f.is_file() else None


def write_json(path: str, data) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fenced_blocks(lines: list[str]):
    """코드 블록의 (시작 인덱스, 끝 인덱스, 언어, 본문 줄)."""
    i = 0
    while i < len(lines):
        s = lines[i].lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            mark, lang = s[:3], s[3:].strip()
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith(mark):
                j += 1
            yield i, j, lang, lines[i + 1:j]
            i = j + 1
        else:
            i += 1


# ---------------------------------------------------------------- 하네스: 문장 단위

LIST_MARK_RE = re.compile(r"^(?:[-*+]|\d+\.)\s+")
SENT_SPLIT_RE = re.compile(r"(?<=[가-힣A-Za-z0-9)」\"'\]$*`][.?!])\s+(?=\S)")
TAG_LINE_RE = re.compile(r"^(?:</?details>|<summary>.*</summary>|</?[a-zA-Z][^>]*>)$")


def norm_unit(text: str) -> str:
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"<[^>]+>", "", text)
    return nfc(re.sub(r"\s+", " ", text).strip())


def sentence_units(text: str) -> list[dict]:
    """장을 문장 단위로 나눈다. 문단·목록은 문장으로, 표는 본문 행으로, 코드·Mermaid는 블록 하나로.
    제목·메타 줄·구분선·표 머리줄·HTML 태그 줄은 세지 않는다."""
    lines = text.splitlines()
    units: list[dict] = []
    para: list[tuple[int, str]] = []
    kind = "문단"

    def flush() -> None:
        if not para:
            return
        joined = " ".join(t.strip() for _, t in para)
        for s in SENT_SPLIT_RE.split(joined):
            if s.strip():
                units.append({"line": para[0][0], "kind": kind, "raw": s.strip()})
        para.clear()

    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("```") or s.startswith("~~~"):
            flush()
            mark, lang = s[:3], s[3:].strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(mark):
                j += 1
            units.append({"line": i + 1, "kind": "그림" if lang == "mermaid" else "코드",
                          "raw": "\n".join(lines[i + 1:j])})
            i = j + 1
            continue
        if (not s or s.startswith("#") or s.startswith("> **수준**") or TAG_LINE_RE.match(s)
                or re.fullmatch(r"-{3,}|\*{3,}", s)):
            flush()
            i += 1
            continue
        if s.startswith("|"):
            flush()
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if not SEP_ROW_RE.match(s) and not SEP_ROW_RE.match(nxt):
                units.append({"line": i + 1, "kind": "표", "raw": " | ".join(split_row(s))})
            i += 1
            continue
        content = re.sub(r"^(?:>\s?)+", "", s) if s.startswith(">") else s
        if not content:
            flush()
            i += 1
            continue
        m = LIST_MARK_RE.match(content)
        if m:
            flush()
            kind = "목록"
            para.append((i + 1, content[m.end():]))
        else:
            if not para:
                kind = "상자" if s.startswith(">") else "문단"
            para.append((i + 1, content))
        i += 1
    flush()

    counts: dict[str, int] = {}
    out = []
    for u in units:
        norm = norm_unit(u["raw"]) if u["kind"] not in ("코드", "그림") else u["raw"].strip()
        if not norm:
            continue
        base = "s-" + sha256_bytes(norm.encode("utf-8"))[:6]
        counts[base] = counts.get(base, 0) + 1
        sid = base if counts[base] == 1 else f"{base}-{counts[base]}"
        out.append({"id": sid, "line": u["line"], "kind": u["kind"], "text": norm})
    return out


def chapter_hash(units: list[dict]) -> str:
    return sha256_bytes("\n".join(u["text"] for u in units).encode("utf-8"))


def resolve_chapter_file(num: str | None, file: str | None, stage_arg: str | None):
    """(장, 읽을 파일, stage). 장 번호나 파일 중 하나로 찾는다."""
    chapters = load_chapters()
    if file:
        path = Path(file).resolve()
        ch = next((c for c in chapters.values() if (ROOT / c.path).resolve() == path), None)
        return chapters, ch, path, None
    ch = chapters.get(num or "")
    if ch is None:
        return chapters, None, None, None
    stage = Path(stage_arg).resolve() if stage_arg else default_stage(ch.num)
    return chapters, ch, staged(ROOT / ch.path, stage), stage


def cmd_sentences(args) -> int:
    chapters, ch, src, _ = resolve_chapter_file(args.chapter, args.file, args.stage)
    if src is None:
        print(f"오류  장 '{args.chapter}'이 curriculum에 없다")
        return 2
    if not src.exists():
        print(f"오류  {rel(src)}: 파일이 없다")
        return 1
    units = sentence_units(read(src))
    digest = chapter_hash(units)
    if args.json:
        write_json(args.json, {
            "tool": "book.py sentences", "version": TOOL_VERSION,
            "chapter": ch.num if ch else None, "file": ch.path if ch else rel(src), "source": rel(src),
            "hash": digest, "units": units,
        })
    else:
        for u in units:
            print(f"{u['id']}\t{u['line']}\t{u['kind']}\t" + u["text"].replace("\n", " ⏎ "))
    print(f"문장 {len(units)}개, 장 해시 {digest[:12]} ({rel(src)})", file=sys.stderr if not args.json else sys.stdout)
    return 0


# ---------------------------------------------------------------- 하네스: lint

KNOWN_TAIL = [STRUCTURE_LINK_HEADING, "## 헷갈리기 쉬운 점", "## 정리", "## 확인 문제", "## 더 읽을거리"]
BUILD_ORDER = ["## 만들 것", "## 준비물", "## 설계 결정", "## 실행 결과", "## 바꿔 보기"]
MERMAID_KEYWORDS = {"flowchart", "graph", "subgraph", "end", "style", "classDef", "class", "direction",
                    "click", "linkStyle", "LR", "RL", "TB", "TD", "BT"}
MERMAID_NODE_RE = re.compile(r"(?<![\w-])([A-Za-z_][\w]*)\s*(?:\[|\(|\{|>)")
MERMAID_EDGE_RE = re.compile(r"(?<![\w-])([A-Za-z_][\w]*)\s*(?:-->|---|-\.->|==>|--\s|-\.-)"
                             r"|(?:-->|---|-\.->|==>|-\.-)\s*(?:\|[^|]*\|\s*)?([A-Za-z_][\w]*)")
LATIN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[-'][A-Za-z0-9]+)*")
READ_LIMIT_CHARS = 13500  # 이론 장 분량 경고선(시범 운영에서 1부 장 30~40분 읽기에 해당). 넘으면 경고만 한다


def section_range(heads: list[tuple[int, str]], name: str, n_lines: int):
    """heads는 (줄 인덱스, 제목). name 절의 (시작, 끝(제외)) 인덱스."""
    for k, (i, h) in enumerate(heads):
        if h == name:
            end = heads[k + 1][0] if k + 1 < len(heads) else n_lines
            return i, end
    return None


def glossary_entries(delta: dict | None = None) -> list[dict]:
    rows = []
    if GLOSSARY.exists():
        table = glossary_table(read(GLOSSARY).splitlines())
        if table:
            for _, cells in table[2]:
                if len(cells) == len(GLOSSARY_HEADER):
                    rows.append({"표기": cells[0], "풀이": cells[1], "한국어": cells[2], "분류": cells[3],
                                 "정의": cells[4], "본장": cells[5]})
    for add in (delta or {}).get("glossary_add", []):
        rows.append({"표기": add.get("표기", ""), "풀이": add.get("풀이", "—"), "한국어": add.get("한국어", "—"),
                     "분류": add.get("분류", ""), "정의": add.get("정의", ""), "본장": ""})
    return rows


def split_variants(cell: str) -> list[str]:
    if cell in ("", "—"):
        return []
    return [v.strip() for v in re.split(r"\s*[·,/]\s*", cell) if v.strip()]


def term_pattern(term: str) -> re.Pattern:
    """대소문자를 가린다. 일반 명사 용어는 문장 첫머리에서도 소문자로 쓰므로(style-guide §5),
    「Language-Image Pre-training」처럼 고유 이름을 풀어 쓴 곳은 용어로 세지 않는다."""
    return re.compile(r"(?<![A-Za-z0-9-])" + re.escape(term) + r"(?:s|es)?(?![A-Za-z0-9-])")


def clean_for_terms(line: str) -> str:
    """용어 검사용으로 줄을 정리한다. 글자 위치를 바꾸지 않도록 지울 부분은 공백으로 덮는다."""
    def blank(m: re.Match) -> str:
        return " " * len(m.group(0))
    line = INLINE_CODE_RE.sub(blank, line)
    line = re.sub(r"\$[^$]*\$", blank, line)
    line = re.sub(r"\]\([^)]*\)", lambda m: "]" + " " * (len(m.group(0)) - 1), line)
    line = re.sub(r"\[@[^\]]*\]", blank, line)
    line = re.sub(r"<[^>]+>", blank, line)
    return line


def paren_spans(text: str) -> list[tuple[int, int]]:
    """괄호 쌍 (여는 위치, 닫는 위치)."""
    spans, stack = [], []
    for i, c in enumerate(text):
        if c == "(":
            stack.append(i)
        elif c == ")" and stack:
            spans.append((stack.pop(), i))
    return spans



def literal_candidates(lines: list[str]) -> list[dict]:
    """직역투 낱말 후보(style-guide §5). 제목도 본다. Mermaid 밖의 코드 블록과 링크 주소는 뺀다."""
    found: dict[str, list[int]] = {}
    fence = None
    for i, ln in enumerate(lines):
        s = ln.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = None if fence is not None else (s[3:].strip().split() or [""])[0].lower()
            continue
        if fence is not None and fence != "mermaid":
            continue
        text = re.sub(r"\]\([^)]*\)", "]", ln)
        for rx, name, _ in LITERAL_KO:
            for _m in re.finditer(rx, text):
                found.setdefault(name, []).append(i + 1)
    out = []
    for rx, name, better in LITERAL_KO:
        where = found.get(name)
        if where:
            more = f" 외 {len(where) - 1}곳" if len(where) > 1 else ""
            out.append({"line": where[0], "msg": f"직역투 낱말 '{name}'{more} — 개발 문서에서 흔히 쓰는 말({better})이나 영어를 쓴다(style-guide §5)"})
    return out

def term_candidates(lines: list[str], body_start: int, rows: list[dict]) -> tuple[list[dict], dict]:
    """용어 표기 후보: 첫 등장에 한국어가 없음, 괄호 한국어를 다시 닮, 번역어 단독 사용, 용어집에 없는 영어 낱말.
    Mermaid 블록 안의 글도 본문처럼 센다(그림 노드가 첫 등장일 수 있다). 다른 코드 블록은 뺀다."""
    segs = []  # (줄 번호, 정리한 줄, 표 행인가)
    fence = None  # 열린 코드 블록의 언어
    for i, ln in enumerate(lines):
        s = ln.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = None if fence is not None else (s[3:].strip().split() or [""])[0].lower()
            continue
        if fence is not None and fence != "mermaid":
            continue
        if fence == "mermaid" and re.match(r"(flowchart|graph|sequenceDiagram|classDiagram|stateDiagram|erDiagram|subgraph|end\b|%%)", s):
            continue
        if i < body_start or not s or (fence is None and (s.startswith("#") or TAG_LINE_RE.match(s.strip()))):
            continue
        segs.append((i + 1, clean_for_terms(ln), s.startswith("|")))
    out: list[dict] = []

    # 1) 첫 등장: 긴 표기부터 찾아 가린다(supervised fine-tuning 안의 fine-tuning을 따로 세지 않게).
    variants = []
    for k, r in enumerate(rows):
        for v in [r["표기"]] + split_variants(r["풀이"]):
            variants.append((len(v), v, k))
    variants.sort(reverse=True)
    masked = [list(t) for _, t, _ in segs]
    occ: dict[int, list[tuple[int, int, int]]] = {}  # 행 → [(seg, start, end)]
    for _, v, k in variants:
        rx = term_pattern(v)
        for si in range(len(segs)):
            text = "".join(masked[si])
            for m in rx.finditer(text):
                occ.setdefault(k, []).append((si, m.start(), m.end()))
                for p in range(m.start(), m.end()):
                    masked[si][p] = "\0"

    def gloss_group(text: str, start: int, end: int) -> str | None:
        """용어 바로 뒤의 괄호, 또는 용어를 감싼 가장 안쪽 괄호."""
        if end < len(text) and text[end] == "(":
            close = next((c for o, c in paren_spans(text) if o == end), len(text))
            return text[end:close + 1]
        enclosing = [(o, c) for o, c in paren_spans(text) if o < start and end <= c]
        if enclosing:
            o, c = max(enclosing)
            return text[o:c + 1]
        return None

    for k, places in occ.items():
        r = rows[k]
        kos = split_variants(r["한국어"])
        if not kos:
            continue
        places.sort()
        si, start, end = places[0]
        text = segs[si][1]
        # 같은 줄(표 행)에서 용어를 다시 쓰며 한국어를 단 것도 첫 등장의 풀이로 친다.
        groups = [gloss_group(text, st, en) for sj, st, en in places if sj == si]
        if not any(g and any(ko in g for ko in kos) for g in groups):
            found = text[start:end]
            also = f" — 표기는 '{r['표기']}'" if found.casefold() != r["표기"].casefold() else ""
            out.append({"line": segs[si][0], "msg": f"'{found}'의 첫 등장에 한국어 '{r['한국어']}'가 없다{also}"})
        # 괄호 한국어를 다시 단 곳: 첫 등장 뒤, 표 밖에서 용어 바로 뒤 괄호에 한국어가 또 있다.
        again = []
        for sj, st, en in places[1:]:
            if sj == si:
                continue
            t = segs[sj][1]
            if segs[sj][2] or not (en < len(t) and t[en] == "("):
                continue
            g = gloss_group(t, st, en)
            if g and any(ko in g for ko in kos):
                again.append(segs[sj][0])
        if again:
            more = f" 외 {len(again) - 1}곳" if len(again) > 1 else ""
            out.append({"line": again[0], "msg": f"'{r['표기']}'의 괄호 한국어를 첫 등장({segs[si][0]}행) 뒤에 다시 달았다{more} — 그다음부터는 영어만 쓴다(style-guide §5)"})

    # 2) 번역어 단독 사용: 괄호 밖·표 밖에서 한국어만 쓴 곳.
    kos = []
    for r in rows:
        for ko in split_variants(r["한국어"]):
            if ko not in EVERYDAY_KO and len(ko) >= 2:
                kos.append((len(ko), ko, r["표기"]))
    kos.sort(reverse=True)
    kmask = [list(t) for _, t, _ in segs]
    alone: dict[str, list[int]] = {}
    for _, ko, term in kos:
        for si, (lno, text, is_table) in enumerate(segs):
            cur = "".join(kmask[si])
            spans = paren_spans(text)
            for m in re.finditer(re.escape(ko), cur):
                for p in range(m.start(), m.end()):
                    kmask[si][p] = "\0"
                if is_table or any(o < m.start() < c for o, c in spans):
                    continue
                alone.setdefault(f"{ko}\t{term}", []).append(lno)
    for key, lnos in alone.items():
        ko, term = key.split("\t")
        more = f" 외 {len(lnos) - 1}곳" if len(lnos) > 1 else ""
        out.append({"line": lnos[0], "msg": f"번역어 '{ko}'를 괄호 밖에 홀로 썼다{more} — 표기는 '{term}'"})

    # 3) 용어집에 없는 영어 낱말(참고용).
    known = set()
    for r in rows:
        for v in [r["표기"]] + split_variants(r["풀이"]):
            known.update(w.casefold() for w in LATIN_RE.findall(v))
    unknown: dict[str, int] = {}
    for _, text, _ in segs:
        for w in LATIN_RE.findall(text):
            base = re.sub(r"(?:es|s)$", "", w.casefold())
            if w.casefold() in known or base in known or len(w) < 2:
                continue
            unknown[w] = unknown.get(w, 0) + 1
    out.sort(key=lambda c: c["line"])
    return out, dict(sorted(unknown.items(), key=lambda kv: (-kv[1], kv[0].casefold())))


def lint_chapter(ch: Chapter, chapters: dict[str, Chapter], src: Path, stage: Path | None, delta: dict) -> dict:
    text = read(src)
    lines = text.splitlines()
    final = (ROOT / ch.path).resolve()
    res = {"errors": [], "warnings": [], "candidates": []}

    def err(line: int, msg: str) -> None:
        res["errors"].append({"line": line, "msg": msg})

    def warn(line: int, msg: str) -> None:
        res["warnings"].append({"line": line, "msg": msg})

    # 제목과 메타 줄
    first = next((i for i, ln in enumerate(lines) if ln.strip()), 0)
    want = f"# {ch.num} {ch.title}"
    if not lines or lines[first].strip() != want:
        err(first + 1, f"첫 줄이 '{want}'여야 한다(curriculum과 같게)")
    meta_i = next((i for i, ln in enumerate(lines) if ln.startswith("> **수준**")), None)
    want_meta = expected_meta(ch, chapters)
    if meta_i is None:
        err(1, "메타 줄(> **수준** …)이 없다")
    elif want_meta and lines[meta_i].strip() != want_meta:
        err(meta_i + 1, f"메타 줄이 curriculum과 다르다 — 이렇게 쓴다: {want_meta}")
    for i, ln in prose_lines(text):
        if ln.startswith("# ") and i - 1 != first:
            err(i, "# 제목은 장 제목 하나만 둔다")

    # 절 구성(검토완료 요건까지)
    heads = [(i - 1, ln.strip()) for i, ln in prose_lines(text) if ln.startswith("## ")]
    names = [h for _, h in heads]
    is_build = ch.title.startswith(BUILD_PREFIXES)
    required = ["## 한눈에", "## 정리", "## 확인 문제", "## 더 읽을거리"]
    if is_build:
        required += list(BUILD_HEADINGS)
        if ch.title.startswith("프로젝트:"):
            required.append("## 설계 결정")
    elif ch.part in STRUCTURE_LINK_PARTS:
        required.append(STRUCTURE_LINK_HEADING)
    for h in required:
        if h not in names:
            err(1, f"'{h}' 절이 없다(검토완료 요건)")
    for h in sorted(set(names)):
        if names.count(h) > 1:
            err(heads[names.index(h)][0] + 1, f"'{h}' 절이 두 번 있다")
    known_named = set(KNOWN_TAIL) | set(BUILD_ORDER) | {"## 한눈에"}
    numbered = [(i, h) for i, h in heads if re.match(r"## \d+\. \S", h)]
    for i, h in heads:
        if h not in known_named and (i, h) not in numbered:
            err(i + 1, f"'{h}' — 본문 절은 '## N. 제목'으로 쓰고, 그 밖의 절 이름은 style-guide §4의 것만 쓴다")
    if heads and names[0] != "## 한눈에":
        err(heads[0][0] + 1, "첫 절은 '## 한눈에'다")
    if heads and names[-1] != "## 더 읽을거리":
        err(heads[-1][0] + 1, "마지막 절은 '## 더 읽을거리'다")
    tail_pos = [names.index(h) for h in KNOWN_TAIL if h in names]
    if tail_pos != sorted(tail_pos):
        err(1, "끝 절 순서는 구조와의 연결 → 헷갈리기 쉬운 점 → 정리 → 확인 문제 → 더 읽을거리다")
    for k, (i, h) in enumerate(numbered, 1):
        if int(re.match(r"## (\d+)\.", h).group(1)) != k:
            err(i + 1, f"본문 절 번호는 1부터 차례로 붙인다 — 여기는 {k}")
            break
    if not is_build and not numbered:
        err(1, "본문 절(## 1. …)이 없다")
    if numbered and tail_pos and names.index(numbered[-1][1]) > min(tail_pos):
        err(numbered[-1][0] + 1, "본문 절은 끝 절(구조와의 연결·헷갈리기 쉬운 점·정리…)보다 앞에 둔다")
    if is_build:
        bpos = [names.index(h) for h in BUILD_ORDER if h in names]
        if bpos != sorted(bpos):
            err(1, "직접 만들기·프로젝트 장의 절 순서는 만들 것 → 준비물 → (설계 결정) → 구현 절 → 실행 결과 → 바꿔 보기다")
        if numbered and "## 실행 결과" in names and names.index(numbered[-1][1]) > names.index("## 실행 결과"):
            err(numbered[-1][0] + 1, "구현 절은 '## 실행 결과'보다 앞에 둔다")

    # 확인 문제
    sec = section_range(heads, "## 확인 문제", len(lines))
    if sec:
        body = lines[sec[0] + 1:sec[1]]
        d0 = next((k for k, ln in enumerate(body) if ln.strip().startswith("<details")), None)
        qs = [ln for ln in (body if d0 is None else body[:d0]) if re.match(r"\d+\. ", ln)]
        if not 3 <= len(qs) <= 5:
            err(sec[0] + 1, f"확인 문제는 3~5개다 — 지금 {len(qs)}개")
        if d0 is None:
            err(sec[0] + 1, "답을 <details>로 접는다")
        else:
            d1 = next((k for k in range(d0, len(body)) if body[k].strip().startswith("</details")), None)
            if d1 is None:
                err(sec[0] + d0 + 2, "</details>가 없다")
                d1 = len(body)
            if not any(ln.strip().startswith("<summary>") for ln in body[d0:d1]):
                err(sec[0] + d0 + 2, "<details> 안에 <summary>답</summary>를 둔다")
            ans = [ln for ln in body[d0:d1] if re.match(r"\d+\. ", ln)]
            if len(ans) != len(qs):
                err(sec[0] + d0 + 2, f"답 {len(ans)}개가 문제 {len(qs)}개와 다르다")

    # 상자 라벨, 금지 표현, 시점 표현
    prev = ""
    for i, ln in prose_lines(text):
        m = re.match(r"^>\s*\*\*([^*]+)\*\*", ln)
        if m and not prev.startswith(">") and m.group(1) != "수준" and m.group(1) not in BOXES:
            err(i, f"상자 라벨 '{m.group(1)}'은 쓰지 않는다 — {'·'.join(BOXES)}만 쓴다")
        prev = ln
        for pattern, why in FORBIDDEN:
            fm = pattern.search(ln)
            if fm:
                err(i, f"'{fm.group(0)}' — {why}")
        tm = TIME_WORDS.search(INLINE_CODE_RE.sub("", ln))
        if tm and "기준)" not in ln:
            warn(i, f"'{tm.group(0)}' — 시점을 가리키는 말은 「(2026년 기준)」처럼 기준 시점을 적는다(style-guide §3)")

    # 인용 키
    keys = {k for _, k in reference_entries(read(REFERENCES).splitlines())} if REFERENCES.exists() else set()
    for line in delta.get("references_add", []):
        m = REF_ENTRY_RE.match(line)
        if m:
            keys.add(m.group(1))
    for i, ln in prose_lines(text):
        for m in CITE_RE.finditer(INLINE_CODE_RE.sub("", ln)):
            for part in m.group(1).split(";"):
                key = part.strip().lstrip("@").strip()
                if key and key not in keys:
                    err(i, f"인용 키 @{key}가 참고문헌에도 변경분에도 없다")

    # 링크와 앵커(최종 위치 기준, stage를 먼저 본다)
    for i, ln in prose_lines(text):
        for m in LINK_RE.finditer(INLINE_CODE_RE.sub("", ln)):
            target = m.group(1)
            if "://" in target or target.startswith("mailto:"):
                continue
            path_part, _, anchor = target.partition("#")
            dest = final if not path_part else (final.parent / unquote(path_part)).resolve()
            real = src if dest == final else staged_any(dest, stage)
            if not real.exists():
                err(i, f"링크 대상 '{target}'이 없다")
                continue
            if anchor and real.suffix == ".md" and real.is_file():
                if nfc(unquote(anchor)).lower() not in anchors_of(real):
                    err(i, f"링크 '{target}'의 앵커가 없다")

    # 그림: 가로 Mermaid의 노드 수, 그림 설명
    for start, end, lang, body in fenced_blocks(lines):
        if lang == "mermaid":
            head = next((b.strip() for b in body if b.strip()), "")
            if re.search(r"\b(LR|RL)\b", head):
                nodes = set()
                groups = {m for b in body for m in re.findall(r"^\s*subgraph\s+([A-Za-z_]\w*)", b)}
                for b in body[1:]:
                    nodes.update(x for x in MERMAID_NODE_RE.findall(b) if x not in MERMAID_KEYWORDS)
                    for a, c in MERMAID_EDGE_RE.findall(b):
                        nodes.update(x for x in (a, c) if x and x not in MERMAID_KEYWORDS)
                nodes -= groups
                if len(nodes) > 5:
                    warn(start + 1, f"가로(LR·RL) 그림의 노드가 {len(nodes)}개다 — 좁은 화면에서는 세로(TB)가 낫다")
            nxt = next((lines[k].strip() for k in range(end + 1, len(lines)) if lines[k].strip()), "")
            if not nxt.startswith("그림"):
                warn(start + 1, "그림 아래에 '그림: …' 한 줄 설명을 단다(style-guide §6)")
    for i, ln in prose_lines(text):
        if re.match(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$", ln):
            nxt = next((lines[k].strip() for k in range(i, len(lines)) if lines[k].strip()), "")
            if not nxt.startswith("그림"):
                warn(i, "그림 아래에 '그림: …' 한 줄 설명을 단다(style-guide §6)")

    # 더 읽을거리
    sec = section_range(heads, "## 더 읽을거리", len(lines))
    if sec:
        items = [(k, ln) for k, ln in enumerate(lines[sec[0] + 1:sec[1]], sec[0] + 2) if ln.startswith("- ")]
        if not items:
            warn(sec[0] + 1, "더 읽을거리에 항목이 없다")
        for k, ln in items:
            if "[@" not in ln:
                warn(k, "더 읽을거리 항목은 [@키]로 인용한다")

    if len(text) > READ_LIMIT_CHARS:
        warn(1, f"{len(text):,}자 — 경고선 {READ_LIMIT_CHARS:,}자를 넘는다. 40분 안에 읽기 어려울 수 있으니 줄일 곳을 본다(작업 절차 §2의 5)")

    body_start = (meta_i + 1) if meta_i is not None else 0
    cands, unknown = term_candidates(lines, body_start, glossary_entries(delta))
    res["candidates"] = cands + literal_candidates(lines)
    units = sentence_units(text)
    res["stats"] = {
        "chars": len(text), "sentences": len(units), "chapter_hash": chapter_hash(units),
        "cited_units": sum(1 for u in units if "[@" in u["text"]),
        "latin_not_in_glossary": unknown,
    }
    return res


def cmd_lint(args) -> int:
    chapters = load_chapters()
    ch = chapters.get(args.chapter)
    if ch is None:
        print(f"오류  장 '{args.chapter}'이 curriculum에 없다")
        return 2
    stage = Path(args.stage).resolve() if args.stage else default_stage(ch.num)
    delta_path = Path(args.delta) if args.delta else default_delta(ch.num)
    src = staged(ROOT / ch.path, stage)
    if not src.exists():
        print(f"오류  {ch.path}: 장 파일이 없다" + (f"(stage {rel(stage)}에도 없다)" if stage else ""))
        return 1
    delta = json.loads(delta_path.read_text(encoding="utf-8")) if delta_path else {}
    res = lint_chapter(ch, chapters, src, stage, delta)
    hashes = {"chapter": sha256_file(src)}
    for name, path in (("glossary", GLOSSARY), ("references", REFERENCES), ("curriculum", CURRICULUM)):
        if path.exists():
            hashes[name] = sha256_file(path)
    if delta_path:
        hashes["delta"] = sha256_file(delta_path)
    if args.json:
        write_json(args.json, {
            "tool": "book.py lint", "version": TOOL_VERSION, "chapter": ch.num, "file": ch.path,
            "source": rel(src), "stage": rel(stage) if stage else None,
            "delta": rel(delta_path) if delta_path else None, "sha256": hashes, **res,
        })
    for kind, label in (("warnings", "경고"), ("errors", "오류"), ("candidates", "후보")):
        for item in res[kind]:
            print(f"{label}  {ch.path}:{item['line']}: {item['msg']}")
    unknown = res["stats"]["latin_not_in_glossary"]
    if unknown:
        shown = ", ".join(f"{w}({n})" for w, n in list(unknown.items())[:30])
        more = f" 외 {len(unknown) - 30}개" if len(unknown) > 30 else ""
        print(f"참고  용어집에 없는 영어 낱말: {shown}{more}")
    st = res["stats"]
    print(f"lint {ch.num}: 오류 {len(res['errors'])}건, 경고 {len(res['warnings'])}건, 후보 {len(res['candidates'])}건 "
          f"— {st['chars']:,}자, 문장 {st['sentences']}개, 장 해시 {st['chapter_hash'][:12]} ({rel(src)})")
    return 1 if res["errors"] else 0


# ---------------------------------------------------------------- 하네스: slice

def cmd_slice(args) -> int:
    if not (args.chapter or args.before or args.terms):
        print("오류  --chapter, --before, --terms 중 하나 이상을 준다")
        return 2
    chapters = load_chapters()
    order = chapter_order(chapters)
    for num in (args.chapter, args.before):
        if num and num not in order:
            print(f"오류  장 '{num}'이 curriculum에 없다")
            return 2
    lines = read(GLOSSARY).splitlines()
    table = glossary_table(lines)
    if table is None:
        print("오류  용어집 표가 없다")
        return 1
    head, _, rows = table
    terms = {t.strip().casefold() for t in (args.terms or "").split(",") if t.strip()}
    picked = []
    for idx, cells in rows:
        if len(cells) != len(GLOSSARY_HEADER):
            continue
        nums = [n for n, _ in (parse_chapter_items(cells[5]) or [])]
        hit = False
        if args.chapter and args.chapter in nums:
            hit = True
        if args.before:
            known = [order[n] for n in nums if n in order]
            if known and min(known) < order[args.before]:
                hit = True
        if terms and (cells[0].casefold() in terms or any(v.casefold() in terms for v in split_variants(cells[1]))):
            hit = True
        if hit:
            picked.append(lines[idx])
    print(lines[head])
    print(lines[head + 1])
    for ln in picked:
        print(ln)
    print(f"행 {len(picked)}개", file=sys.stderr)
    return 0


# ---------------------------------------------------------------- 하네스: hashes · merge

SHARED_FILES = (GLOSSARY, REFERENCES, OPEN_QUESTIONS, CURRICULUM, BOOK_README)
DELTA_KEYS = {"chapter", "stage", "status", "stage_files", "glossary_add", "glossary_link",
              "references_add", "open_questions_add", "note"}
STATUS_DRAFT_RE = re.compile(r"초고 · [A-Za-z][A-Za-z0-9.+-]*")


def shared_hashes() -> dict[str, str]:
    return {rel(p): sha256_file(p) for p in SHARED_FILES if p.exists()}


def cmd_hashes(args) -> int:
    data = shared_hashes()
    if args.out:
        write_json(args.out, data)
        print(f"공유 파일 {len(data)}개의 해시를 {args.out}에 적었다")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def allowed_stage_path(ch: Chapter, relp: str) -> bool:
    """변경분이 book/에 놓을 수 있는 파일: 그 장 파일, 그 장의 그림, 그 장의 코드 폴더."""
    p = Path(relp)
    if p.is_absolute() or ".." in p.parts:
        return False
    relp = p.as_posix()
    stem = Path(ch.path).stem
    prefix = f"{ch.part:02d}-{ch.idx:02d}-"
    if relp == ch.path:
        return True
    if relp.startswith("book/figures/") and len(p.parts) == 3 and p.name.startswith(prefix):
        return True
    return relp.startswith(f"book/code/part{ch.part:02d}/{stem}/")


def render_items(nums: list[str], chapters: dict[str, Chapter], exists) -> str:
    order = chapter_order(chapters)
    uniq = sorted(set(nums), key=lambda n: order.get(n, 10 ** 6))
    out = []
    for n in uniq:
        ch = chapters[n]
        out.append(f"[{n}]({chapter_href(ch, GLOSSARY)})" if exists(ch) else n)
    return ", ".join(out) if out else "—"


def oq_history_max() -> int:
    """git 이력에 나온 가장 큰 OQ 번호(지운 번호를 다시 쓰지 않기 위해). git이 없으면 0."""
    try:
        res = subprocess.run(["git", "log", "-p", "--format=", "--", rel(OPEN_QUESTIONS)],
                             cwd=ROOT, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return 0
    return max((int(x) for x in OQ_ID_RE.findall(res.stdout)), default=0)


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def cmd_merge(args) -> int:
    chapters = load_chapters()
    errors: list[str] = []
    warnings: list[str] = []

    if args.base:
        base = json.loads(Path(args.base).read_text(encoding="utf-8"))
        now = shared_hashes()
        changed = sorted(k for k in set(base) | set(now) if base.get(k) != now.get(k))
        if changed:
            print("오류  묶음을 시작한 뒤 공유 파일이 바뀌었다 — 통합하지 않고 멈춘다(작업 절차 §10.3): " + ", ".join(changed))
            return 1

    gl_lines = read(GLOSSARY).splitlines()
    ref_lines = read(REFERENCES).splitlines()
    oq_lines = read(OPEN_QUESTIONS).splitlines()
    cur_lines = read(CURRICULUM).splitlines()
    table = glossary_table(gl_lines)
    if table is None:
        print("오류  용어집 표가 없다")
        return 1
    g_head, g_end, g_rows = table
    old_rows = [cells for _, cells in g_rows]
    rows = [list(c) for c in old_rows]
    index = {c[0].casefold(): k for k, c in enumerate(rows)}
    old_refs = {key: ref_lines[i] for i, key in reference_entries(ref_lines)}
    new_refs: dict[str, str] = {}
    old_oq = oq_rows(oq_lines)
    oq_texts = {cells[1] for _, cells in old_oq if len(cells) == 4}
    new_oq: list[list[str]] = []
    placements: list[tuple[Path, Path]] = []
    new_status: dict[str, str] = {}
    placed: set[str] = set()
    relinked: set[int] = set()
    added_gl = 0

    deltas = []
    for dp in args.deltas:
        try:
            deltas.append((dp, json.loads(Path(dp).read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError) as e:
            errors.append(f"{dp}: 변경분을 읽지 못했다 — {e}")

    for dp, d in deltas:
        where = dp
        extra = set(d) - DELTA_KEYS
        if extra:
            errors.append(f"{where}: 모르는 키 {sorted(extra)}")
        ch = chapters.get(d.get("chapter", ""))
        if ch is None:
            errors.append(f"{where}: 장 '{d.get('chapter')}'이 curriculum에 없다")
            continue
        stage = (ROOT / d["stage"]).resolve() if d.get("stage") else (HARNESS / ch.num / "stage")
        try:
            stage.relative_to(HARNESS.resolve())
        except ValueError:
            errors.append(f"{where}: stage {stage}는 {rel(HARNESS)}/ 안이어야 한다")
            continue
        files = d.get("stage_files", {})
        for relp, digest in files.items():
            if not allowed_stage_path(ch, relp):
                errors.append(f"{where}: {relp} — {ch.num}장이 놓을 수 있는 파일이 아니다(장 파일·book/figures/{ch.part:02d}-{ch.idx:02d}-*·book/code/part{ch.part:02d}/{Path(ch.path).stem}/)")
                continue
            sf = stage / relp
            if not sf.is_file():
                errors.append(f"{where}: stage에 {relp}가 없다")
            elif sha256_file(sf) != digest:
                errors.append(f"{where}: {relp}가 변경분을 낸 뒤 바뀌었다(sha256 불일치)")
            else:
                placements.append((sf, ROOT / relp))
        if stage.is_dir():
            for f in sorted(stage.rglob("*")):
                if f.is_file() and f.relative_to(stage).as_posix() not in files:
                    errors.append(f"{where}: stage의 {f.relative_to(stage).as_posix()}가 stage_files에 없다")
        if ch.path in files:
            placed.add(ch.num)

        status = d.get("status")
        if status:
            if not STATUS_DRAFT_RE.fullmatch(status):
                errors.append(f"{where}: status는 '초고 · 집필AI'만 쓴다 — 검토완료·확정은 merge가 정하지 않는다(ED-08)")
            else:
                if ch.status in ("검토완료", "확정"):
                    warnings.append(f"{ch.num}장 상태를 {ch.status_raw}에서 {status}로 낮춘다")
                new_status[ch.num] = status
        elif ch.path in files and ch.status == "계획":
            errors.append(f"{where}: {ch.num}장 파일을 처음 놓으면 status('초고 · 집필AI')가 필요하다")
        elif ch.path in files and ch.status in ("검토완료", "확정"):
            warnings.append(f"{ch.num}장은 {ch.status}인데 본문을 바꾼다 — 상태를 그대로 둘지 사용자에게 확인한다")

        for add in d.get("glossary_add", []):
            need = ("표기", "풀이", "한국어", "분류", "정의", "본장")
            miss = [k for k in need if k not in add]
            if miss:
                errors.append(f"{where}: glossary_add에 {miss}가 없다 — {add}")
                continue
            vals = [str(add[k]).strip() for k in need[:5]]
            if any("|" in v or not v for v in vals):
                errors.append(f"{where}: glossary_add '{add['표기']}'의 칸이 비었거나 | 가 있다")
                continue
            if add["분류"] not in CATEGORIES:
                errors.append(f"{where}: '{add['표기']}'의 분류 '{add['분류']}'은 style-guide §5의 값이 아니다")
                continue
            bad = [n for n in add["본장"] if n not in chapters]
            if bad or not add["본장"]:
                errors.append(f"{where}: '{add['표기']}'의 본장 {add['본장']}이 비었거나 curriculum에 없는 장이 있다")
                continue
            cells = vals + [list(add["본장"])]
            key = vals[0].casefold()
            if key in index:
                cur = rows[index[key]]
                if cur[:5] == vals:
                    nums = [n for n, _ in (parse_chapter_items(cur[5]) or [])]
                    rows[index[key]][5] = nums + [n for n in add["본장"] if n not in nums]
                    relinked.add(index[key])
                    warnings.append(f"'{vals[0]}'는 용어집에 같은 행이 있어 본 장만 더한다")
                else:
                    errors.append(f"{where}: '{vals[0]}'가 용어집에 다른 내용으로 있다 — 표기·정의를 고치는 일은 사용자 확인 뒤 사람이 한다")
                continue
            rows.append(cells)
            index[key] = len(rows) - 1
            relinked.add(len(rows) - 1)
            added_gl += 1

        for link in d.get("glossary_link", []):
            term, num = link.get("표기", ""), link.get("장", "")
            if term.casefold() not in index:
                errors.append(f"{where}: glossary_link '{term}'이 용어집에 없다")
                continue
            if num not in chapters:
                errors.append(f"{where}: glossary_link '{term}'의 장 '{num}'이 curriculum에 없다")
                continue
            k = index[term.casefold()]
            cur = rows[k][5]
            nums = cur if isinstance(cur, list) else [n for n, _ in (parse_chapter_items(cur) or [])]
            rows[k][5] = nums + ([num] if num not in nums else [])
            relinked.add(k)

        for line in d.get("references_add", []):
            line = nfc(line.strip())
            probs = reference_line_problems(line)
            if probs:
                errors.append(f"{where}: 참고문헌 '{line[:40]}…' — " + "; ".join(probs))
                continue
            key = REF_ENTRY_RE.match(line).group(1)
            if key in old_refs or key in new_refs:
                if (old_refs.get(key) or new_refs.get(key)) != line:
                    errors.append(f"{where}: @{key}가 참고문헌에 다른 내용으로 있다")
                continue
            ids = set(reference_ids(line))
            clash = [k for k, ln in {**old_refs, **new_refs}.items() if ids & set(reference_ids(ln))]
            if clash:
                errors.append(f"{where}: @{key}는 @{clash[0]}와 같은 문헌이다")
                continue
            new_refs[key] = line

        for oq in d.get("open_questions_add", []):
            vals = [str(oq.get(k, "")).strip() for k in ("확인할 것", "관련 장", "확인 방법")]
            if any("|" in v or not v for v in vals):
                errors.append(f"{where}: open_questions_add의 칸이 비었거나 | 가 있다 — {oq}")
                continue
            if vals[0] in oq_texts:
                continue
            oq_texts.add(vals[0])
            new_oq.append(vals)

    # 본 장 칸 다시 쓰기: 이번에 놓는 장은 링크로 올린다.
    def exists(ch: Chapter) -> bool:
        return ch.num in placed or (ROOT / ch.path).exists()

    for k, cells in enumerate(rows):
        if k in relinked:
            cells[5] = render_items(cells[5] if isinstance(cells[5], list) else
                                    [n for n, _ in (parse_chapter_items(cells[5]) or [])], chapters, exists)
        elif placed:
            items = parse_chapter_items(cells[5])
            if items and any(n in placed and link is None for n, link in items):
                cells[5] = render_items([n for n, _ in items], chapters, exists)

    if errors:
        for w in warnings:
            print(f"경고  {w}")
        for e in errors:
            print(f"오류  {e}")
        print(f"merge 중단: 오류 {len(errors)}건 — 아무 파일도 바꾸지 않았다")
        return 1

    # 새 내용 만들기
    rows.sort(key=lambda c: c[0].casefold())
    new_gl = gl_lines[:g_head + 2] + ["| " + " | ".join(c) + " |" for c in rows] + gl_lines[g_end:]

    entries = reference_entries(ref_lines)
    all_refs = {**old_refs, **new_refs}
    ref_block = [all_refs[k] for k in sorted(all_refs, key=str.casefold)]
    if entries:
        new_ref = ref_lines[:entries[0][0]] + ref_block + ref_lines[entries[-1][0] + 1:]
    else:
        new_ref = ref_lines + [""] + ref_block

    floor = max([args.oq_floor or 0, oq_history_max()] +
                [int(m) for _, c in old_oq for m in OQ_ID_RE.findall(c[0])])
    oq_new_lines = [f"| OQ-{floor + n + 1:03d} | {v[0]} | {v[1]} | {v[2]} |" for n, v in enumerate(new_oq)]
    if old_oq:
        at = old_oq[-1][0] + 1
    else:
        hdr = next((i for i, ln in enumerate(oq_lines) if ln.startswith("| ID |")), None)
        if hdr is None:
            print("오류  미확인 목록의 표 머리줄이 없다")
            return 1
        at = hdr + 2
    new_oq_lines = oq_lines[:at] + oq_new_lines + oq_lines[at:]

    new_cur = list(cur_lines)
    for num, status in new_status.items():
        ch = chapters[num]
        line = new_cur[ch.line - 1].rstrip()
        inner = line[:-1] if line.endswith("|") else line
        cut = inner.rfind("|")
        new_line = inner[:cut + 1] + f" {status} |"
        if split_row(new_line)[:6] != split_row(line)[:6]:
            print(f"오류  curriculum {ch.num}행의 상태 칸만 바꾸지 못했다")
            return 1
        new_cur[ch.line - 1] = new_line

    # 불변식: 지운 행이 없고, 행 수가 더한 만큼만 늘고, 옛 칸은 본 장 말고는 그대로다.
    t2 = glossary_table(new_gl)
    after = {c[0].casefold(): c for _, c in t2[2]}
    bad = [c[0] for c in old_rows if c[0].casefold() not in after or after[c[0].casefold()][:5] != c[:5]]
    if len(t2[2]) != len(old_rows) + added_gl or bad:
        print(f"오류  용어집 불변식이 깨졌다(행 {len(old_rows)}+{added_gl}≠{len(t2[2])}, 바뀐 행 {bad[:5]})")
        return 1
    if len(reference_entries(new_ref)) != len(old_refs) + len(new_refs) or not set(old_refs.values()) <= set(new_ref):
        print("오류  참고문헌 불변식이 깨졌다")
        return 1
    if len(oq_rows(new_oq_lines)) != len(old_oq) + len(new_oq):
        print("오류  미확인 목록 불변식이 깨졌다")
        return 1
    changed_cur = [i for i, (a, b) in enumerate(zip(cur_lines, new_cur)) if a != b]
    if len(new_cur) != len(cur_lines) or len(changed_cur) > len(new_status):
        print("오류  curriculum 불변식이 깨졌다")
        return 1

    def joined(ls: list[str], orig: Path) -> bytes:
        tail = "\n" if read(orig).endswith("\n") else ""
        return ("\n".join(ls) + tail).encode("utf-8")

    writes: list[tuple[Path, bytes]] = []
    for path, ls in ((GLOSSARY, new_gl), (REFERENCES, new_ref), (OPEN_QUESTIONS, new_oq_lines), (CURRICULUM, new_cur)):
        data = joined(ls, path)
        if data != path.read_bytes():
            writes.append((path, data))
    for sf, dest in placements:
        data = sf.read_bytes()
        if not dest.exists() or dest.read_bytes() != data:
            writes.append((dest, data))

    old_home = {c[0].casefold(): c[5] for c in old_rows}
    rehomed = sum(1 for k, c in after.items() if k in old_home and old_home[k] != c[5])
    summary = [
        f"용어집 +{added_gl}행, 본 장 칸 바뀐 행 {rehomed}개",
        f"참고문헌 +{len(new_refs)}개",
        f"미확인 +{len(new_oq)}개" + (f" (OQ-{floor + 1:03d}~OQ-{floor + len(new_oq):03d})" if new_oq else ""),
    ] + [f"curriculum {n}: {chapters[n].status_raw} → {s}" for n, s in new_status.items()]
    for w in warnings:
        print(f"경고  {w}")
    for line in summary:
        print(f"  {line}")
    for path, _ in writes:
        print(f"  {'바꿈' if path.exists() else '새로'}  {rel(path)}")
    if args.dry_run:
        print(f"merge --dry-run: 파일 {len(writes)}개를 바꿀 예정 — 아무것도 쓰지 않았다")
        return 0
    if not writes:
        print("merge: 바꿀 것이 없다")
        return 0

    snap = HARNESS / "snapshots" / ("merge-" + time.strftime("%Y%m%d-%H%M%S"))
    manifest = {"deltas": [str(dp) for dp, _ in deltas], "files": {}}
    for path, _ in writes:
        r = rel(path)
        manifest["files"][r] = "existed" if path.exists() else "new"
        if path.exists():
            (snap / r).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, snap / r)
    write_json(str(snap / "manifest.json"), manifest)
    for path, data in writes:
        atomic_write(path, data)
    print(f"merge: 파일 {len(writes)}개를 바꿨다. 되돌릴 사본: {rel(snap)}/")
    print("다음: python3 tools/book.py toc → python3 tools/book.py check")
    return 0


# ---------------------------------------------------------------- 명령

def print_report(rep: Report) -> None:
    for w in rep.warnings:
        print(f"경고  {w}")
    for e in rep.errors:
        print(f"오류  {e}")


def run_checks(rep: Report) -> list[Part]:
    parts = parse_curriculum(rep)
    chapters = check_curriculum(parts, rep)
    check_chapter_files(chapters, rep)
    check_forbidden(rep)
    check_links(rep)
    check_citations(rep)
    check_reference_format(rep)
    check_glossary(chapters, rep)
    check_open_questions(rep)
    check_code(rep)
    check_toc(parts, rep)
    return parts


def cmd_check() -> int:
    rep = Report()
    parts = run_checks(rep)
    print_report(rep)
    total = sum(len(p.chapters) for p in parts)
    print(f"검사 끝: 장 {total}개, 오류 {len(rep.errors)}건, 경고 {len(rep.warnings)}건")
    return 1 if rep.errors else 0


def cmd_status() -> int:
    rep = Report()
    parts = parse_curriculum(rep)
    check_curriculum(parts, rep)
    counts = {s: 0 for s in STATUSES}
    active: list[Chapter] = []
    for part in parts:
        for ch in part.chapters:
            if ch.status in counts:
                counts[ch.status] += 1
            if ch.status != "계획":
                active.append(ch)
    total = sum(counts.values())
    print(f"전체 {total}장 — " + ", ".join(f"{s} {n}" for s, n in counts.items()))
    for ch in active:
        print(f"  {ch.num:>5} {ch.title} [{ch.status_raw}]")
    if rep.errors:
        print_report(rep)
        return 1
    return 0


def main(argv: list[str]) -> int:
    simple = {"check": cmd_check, "toc": cmd_toc, "status": cmd_status, "site": cmd_site}
    ap = argparse.ArgumentParser(prog="tools/book.py", add_help=True,
                                 description="AI Insight Notes 책 도구. 명령 없이 실행하면 사용법을 보인다.")
    sub = ap.add_subparsers(dest="cmd")
    for name in simple:
        sub.add_parser(name)
    p = sub.add_parser("lint", help="장 하나를 검토완료 요건·용어 표기까지 검사한다")
    p.add_argument("chapter")
    p.add_argument("--stage", help="저장소와 같은 배치의 초안 폴더(기본: build/harness/<장>/stage)")
    p.add_argument("--delta", help="변경분 JSON(기본: build/harness/<장>/delta.json). 새 인용 키·용어를 인정한다")
    p.add_argument("--json", help="결과를 JSON으로 적을 파일")
    p = sub.add_parser("sentences", help="장을 문장 단위로 나누고 문장 번호와 장 해시를 낸다")
    p.add_argument("chapter", nargs="?")
    p.add_argument("--file", help="장 번호 대신 파일을 직접 준다")
    p.add_argument("--stage")
    p.add_argument("--json")
    p = sub.add_parser("slice", help="용어집에서 필요한 행만 뽑는다")
    p.add_argument("--chapter", help="본 장 칸에 이 장이 있는 행")
    p.add_argument("--before", help="책 순서상 이 장보다 앞 장에서 다룬 행")
    p.add_argument("--terms", help="쉼표로 나눈 표기·풀이")
    p = sub.add_parser("merge", help="변경분을 공유 파일과 book/에 반영한다(통합 패스만)")
    p.add_argument("deltas", nargs="+")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--oq-floor", type=int, default=0, help="이 번호보다 큰 OQ 번호만 쓴다(진행 기록의 다음 번호 - 1)")
    p.add_argument("--base", help="묶음 시작 때 hashes로 적은 공유 파일 해시. 다르면 멈춘다")
    p = sub.add_parser("hashes", help="공유 파일의 sha256을 적는다(묶음 시작 때)")
    p.add_argument("--out")
    if len(argv) < 2:
        print(__doc__)
        return 2
    args = ap.parse_args(argv[1:])
    if args.cmd in simple:
        return simple[args.cmd]()
    return {"lint": cmd_lint, "sentences": cmd_sentences, "slice": cmd_slice,
            "merge": cmd_merge, "hashes": cmd_hashes}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
