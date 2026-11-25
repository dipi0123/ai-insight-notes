#!/usr/bin/env python3
"""AI Insight Notes 책 도구 — 검사, 목차 생성, 상태 요약.

사용법:
  python3 tools/book.py check    규칙 검사. 오류가 있으면 종료 코드 1
  python3 tools/book.py toc      editorial/curriculum.md로 book/README.md 목차를 다시 만든다
  python3 tools/book.py status   장별 진행 상태를 요약한다

표준 라이브러리만 쓴다. 규칙의 정본은 AGENTS.md와 editorial/ 문서이고,
이 스크립트는 그중 기계로 확인할 수 있는 것만 확인한다.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
CURRICULUM = ROOT / "editorial" / "curriculum.md"
BOOK_README = BOOK / "README.md"
REFERENCES = BOOK / "appendix" / "references.md"

TOC_START = "<!-- TOC:START -->"
TOC_END = "<!-- TOC:END -->"

STATUSES = ("계획", "초고", "검토완료", "확정")
LEVELS = ("L1", "L2", "L3", "L4", "L5")

# 링크 검사에서 뺄 경로(저장소 기준 앞부분). 템플릿은 자리표시 링크를 담고, 작업대는 임시 재료다.
LINK_SKIP = ("workbench/", "editorial/templates/", ".git/", "node_modules/")

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
        if meta is None:
            rep.error(ch.path, "메타 줄(> **수준** …)이 없다")
        elif not meta.startswith(f"> **수준** {ch.level}"):
            rep.error(ch.path, f"메타 줄의 수준이 curriculum의 {ch.level}과 다르다")
        headings = {ln.strip() for _, ln in prose_lines(text) if ln.startswith("## ")}
        required = ["## 한눈에"]
        if ch.status in ("검토완료", "확정"):
            required += ["## 정리", "## 확인 문제"]
        for h in required:
            if h not in headings:
                rep.error(ch.path, f"'{h}' 절이 없다(상태 {ch.status})")


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
    for path in sorted(ROOT.rglob("*.md")):
        r = rel(path)
        if any(r.startswith(s) for s in LINK_SKIP) or any(part.startswith(".") for part in Path(r).parts):
            continue
        files.append(path)
    return files


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


# ---------------------------------------------------------------- 명령

def print_report(rep: Report) -> None:
    for w in rep.warnings:
        print(f"경고  {w}")
    for e in rep.errors:
        print(f"오류  {e}")


def cmd_check() -> int:
    rep = Report()
    parts = parse_curriculum(rep)
    chapters = check_curriculum(parts, rep)
    check_chapter_files(chapters, rep)
    check_forbidden(rep)
    check_links(rep)
    check_citations(rep)
    check_toc(parts, rep)
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
    commands = {"check": cmd_check, "toc": cmd_toc, "status": cmd_status}
    if len(argv) != 2 or argv[1] not in commands:
        print(__doc__)
        return 2
    return commands[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
