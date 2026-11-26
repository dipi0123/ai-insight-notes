"""근거 대장 도구 — 책 전체 집필(editorial/workflow.md §10.4)에서 장마다 남기는 근거 대장을 만들고 검사한다.

사용법(언제나 -I로 돌린다):
  python3 -I tools/harness/ledger.py facts 1.5
      조사 패스가 모은 출처와 사실 목록만 검사한다(장 파일이 아직 없어도 된다).
  python3 -I tools/harness/ledger.py sync 1.5 [--stage 폴더] [--writer Claude]
      장의 문장 목록으로 build/harness/1.5/ledger.json을 만들거나 맞춘다.
      새 문장은 빈 행으로 더하고, 사라진 문장의 행은 지우며 그 목록을 보인다(바뀐 문장은 판정을 다시 받는다).
  python3 -I tools/harness/ledger.py validate 1.5 [--stage 폴더] [--final]
      대장을 검사한다. --final은 자체 점검을 마친 뒤의 요건(모든 문장의 판정이 일치)까지 본다.
  python3 -I tools/harness/ledger.py verdicts 1.5 점검.json ... [--judge 판정.json ...]
      자체 점검 렌즈의 문장별 판정을 대장의 판정 칸에 모은다. 회차가 여럿이면 모든 회차의 점검과 판정을 함께 준다.
  python3 -I tools/harness/ledger.py export 1.5 [--stage 폴더]
      검사를 통과한 대장을 workbench/evidence/1.5.md로 내보낸다(통합 패스만).

대장 JSON 형식과 갈래는 tools/harness/README.md에 있다. 표준 라이브러리만 쓴다.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


book = _load("book_tool", ROOT / "tools" / "book.py")
fetch = _load("fetch_tool", HERE / "fetch.py")

KINDS = ("출처", "교과", "계산", "실행", "설명", "연결")
NEEDS_SOURCE = ("출처", "교과")
NEEDS_PATH = ("계산", "실행")
VERDICTS = ("", "일치", "불일치", "미확인", "해당 없음")
# 갈래마다 판정을 맡는 렌즈(§10.2 자체 점검). 연결은 판정하지 않고 수만 센다.
LENS_FOR = {"출처": "출처 대조", "교과": "출처 대조", "계산": "검산·실행", "실행": "검산·실행", "설명": "설명"}
EVIDENCE = ROOT / "workbench" / "evidence"


def ledger_path(num: str) -> Path:
    return book.HARNESS / num / "ledger.json"


def chapter_units(num: str, stage: str | None):
    chapters, ch, src, _ = book.resolve_chapter_file(num, None, stage)
    if ch is None:
        raise SystemExit(f"오류  장 '{num}'이 curriculum에 없다")
    if not src.exists():
        raise SystemExit(f"오류  {ch.path}: 장 파일이 없다(stage에도 없다)")
    units = book.sentence_units(book.read(src))
    return ch, src, units


def load_ledger(num: str) -> dict:
    path = ledger_path(num)
    if not path.is_file():
        raise SystemExit(f"오류  {book.rel(path)}이 없다 — 먼저 sync")
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(num: str, data: dict) -> None:
    book.write_json(str(ledger_path(num)), data)


# ---------------------------------------------------------------- sync

def cmd_sync(args) -> int:
    ch, src, units = chapter_units(args.chapter, args.stage)
    path = ledger_path(ch.num)
    data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {
        "chapter": ch.num, "file": ch.path, "writer": args.writer or "", "sources": {},
        "sentences": {}, "cross_review_priority": [], "open_questions": [],
    }
    if args.writer:
        data["writer"] = args.writer
    old = data.get("sentences", {})
    ids = [u["id"] for u in units]
    new = {}
    for u in units:
        entry = old.get(u["id"], {"kind": "", "refs": [], "verdict": ""})
        entry["line"] = u["line"]
        entry["unit"] = u["kind"]
        new[u["id"]] = entry
    dropped = [sid for sid in old if sid not in new]
    added = [sid for sid in ids if sid not in old]
    data["sentences"] = new
    data["chapter_hash"] = book.chapter_hash(units)
    save_ledger(ch.num, data)
    for sid in dropped:
        print(f"지움  {sid} (문장이 바뀌었거나 없어졌다 — 바뀐 문장은 새 번호로 다시 판정받는다)")
    print(f"sync {ch.num}: 문장 {len(ids)}개, 새로 {len(added)}개, 지움 {len(dropped)}개 → {book.rel(path)}")
    return 0


# ---------------------------------------------------------------- validate

def check_sources(num: str, data: dict, errors: list[str]) -> set[str]:
    """출처는 참고문헌(또는 변경분)에 있는 키이고, 보관함 출처가 내려받은 그대로여야 한다. 쓸 수 있는 키를 돌려준다."""
    keys = {k for _, k in book.reference_entries(book.read(book.REFERENCES).splitlines())}
    delta_path = book.default_delta(num)
    if delta_path:
        delta = json.loads(delta_path.read_text(encoding="utf-8"))
        for line in delta.get("references_add", []):
            m = book.REF_ENTRY_RE.match(line)
            if m:
                keys.add(m.group(1))
    log = fetch.log_entries()
    good = set()
    for key, info in data.get("sources", {}).items():
        entry = info.get("entry", "")
        if entry:
            m = book.REF_ENTRY_RE.match(entry)
            if not m or m.group(1) != key:
                errors.append(f"출처 @{key}: entry는 참고문헌 형식(style-guide §7) 한 줄이고 키가 @{key}여야 한다")
        elif key not in keys:
            errors.append(f"출처 @{key}가 참고문헌에도 변경분(references_add)에도 없다 — "
                          "본문에서 인용하지 않는 근거 문헌이면 sources의 그 키에 entry로 둔다")
        sid = info.get("source_id", "")
        parts = info.get("parts") or {}
        probs = [] if sid else [f"@{key}: source_id가 없다"]
        for one in ([sid] if sid else []) + list(parts):
            probs += fetch.verify(one, log)
        for one, scope in parts.items():
            if not scope:
                errors.append(f"출처 @{key}: parts의 {one}에 scope를 적는다")
        if probs:
            errors += [f"출처 @{key}: {p}" for p in probs]
        else:
            good.add(key)
        if not info.get("scope"):
            errors.append(f"출처 @{key}: scope(전문 또는 초록만 등)를 적는다")
    return good


def check_ref(where: str, r: dict, data: dict, good_sources: set[str], errors: list[str]) -> None:
    key = r.get("key", "")
    if key not in data.get("sources", {}):
        errors.append(f"{where}: sources에 없는 키다")
        return
    if not r.get("loc"):
        errors.append(f"{where}: 위치(loc)가 없다")
    anchor = r.get("anchor", "")
    if not anchor:
        errors.append(f"{where}: 닻(anchor)이 없다")
    elif len(anchor.split()) > fetch.ANCHOR_MAX_WORDS:
        errors.append(f"{where}: 닻은 15단어 미만이다")
    info = data["sources"][key]
    sid = r.get("source_id") or info.get("source_id", "")
    if r.get("source_id") and sid != info.get("source_id") and sid not in (info.get("parts") or {}):
        errors.append(f"{where}: source_id '{sid}'가 @{key}의 source_id·parts에 없다")
    elif anchor and len(anchor.split()) <= fetch.ANCHOR_MAX_WORDS and key in good_sources:
        if not fetch.find_anchor(sid, anchor)["found"]:
            errors.append(f"{where}: 닻 '{anchor}'이 출처 본문에 없다({sid})")


def cmd_facts(args) -> int:
    path = ledger_path(args.chapter)
    if not path.is_file():
        print(f"오류  {book.rel(path)}이 없다")
        return 1
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    good = check_sources(args.chapter, data, errors)
    facts = data.get("facts", [])
    ids = [f.get("id") for f in facts]
    if len(set(ids)) != len(ids) or not all(ids):
        errors.append("사실 id가 비었거나 겹친다")
    for f in facts:
        if not f.get("claim"):
            errors.append(f"{f.get('id')}: claim이 없다")
        check_ref(f"{f.get('id')} @{f.get('key', '')}", f, data, good, errors)
    for e in errors:
        print(f"오류  {e}")
    gaps = data.get("gaps", [])
    for g in gaps:
        print(f"못 구함  {g}")
    print(f"ledger facts {args.chapter}: 출처 {len(data.get('sources', {}))}개, 사실 {len(facts)}개, "
          f"못 구함 {len(gaps)}개, 오류 {len(errors)}건")
    return 1 if errors else 0


def validate(num: str, stage: str | None, final: bool) -> tuple[list[str], list[str], dict]:
    ch, src, units = chapter_units(num, stage)
    data = load_ledger(ch.num)
    errors: list[str] = []
    warnings: list[str] = []
    text_of = {u["id"]: u for u in units}
    sents = data.get("sentences", {})
    if data.get("chapter") != ch.num:
        errors.append(f"대장의 장 번호 '{data.get('chapter')}'가 {ch.num}이 아니다")
    if not data.get("writer"):
        errors.append("writer(집필 AI)가 비었다")
    for sid in sents:
        if sid not in text_of:
            errors.append(f"{sid}: 장에 없는 문장이다 — sync로 맞춘다")
    for sid in text_of:
        if sid not in sents:
            errors.append(f"{sid}: 대장에 없다 — sync로 맞춘다")

    good_sources = check_sources(ch.num, data, errors)

    counts = {k: 0 for k in KINDS}
    for sid, e in sents.items():
        if sid not in text_of:
            continue
        kind = e.get("kind", "")
        if kind not in KINDS:
            errors.append(f"{sid} ({text_of[sid]['line']}행): 갈래가 없거나 '{kind}'는 갈래가 아니다")
            continue
        counts[kind] += 1
        refs = e.get("refs", [])
        cited = set()
        for m in book.CITE_RE.finditer(text_of[sid]["text"]):
            cited |= {p.strip().lstrip("@").strip() for p in m.group(1).split(";") if p.strip()}
        ref_keys = {r.get("key") for r in refs}
        for key in sorted(cited - ref_keys):
            errors.append(f"{sid}: 문장이 [@{key}]를 인용하는데 근거에 @{key}가 없다")
        if kind in NEEDS_SOURCE and not refs:
            errors.append(f"{sid} ({text_of[sid]['line']}행): {kind} 문장인데 근거가 없다")
        for r in refs:
            check_ref(f"{sid} @{r.get('key', '')}", r, data, good_sources, errors)
        if kind in NEEDS_PATH:
            p = e.get("path", "")
            if not p or not (ROOT / p).exists():
                errors.append(f"{sid}: {kind} 문장은 계산·실행 기록 파일(path)을 단다 — '{p}'가 없다")
        verdict = e.get("verdict", "")
        if verdict not in VERDICTS:
            errors.append(f"{sid}: 판정 '{verdict}'는 {VERDICTS[1:]} 중 하나가 아니다")
        if final and (verdict in ("불일치", "미확인") if kind == "연결" else verdict not in ("일치", "해당 없음")):
            errors.append(f"{sid} ({text_of[sid]['line']}행): 판정이 '{verdict or '없음'}'이다 — 자체 점검을 마친 장은 모두 일치여야 한다")
    cited_all = set()
    for u in units:
        for m in book.CITE_RE.finditer(u["text"]):
            cited_all |= {p.strip().lstrip("@").strip() for p in m.group(1).split(";") if p.strip()}
    delta_path = book.default_delta(ch.num)
    if delta_path:
        for line in json.loads(delta_path.read_text(encoding="utf-8")).get("references_add", []):
            m = book.REF_ENTRY_RE.match(line)
            if m and m.group(1) not in cited_all:
                errors.append(f"변경분 references_add의 @{m.group(1)}를 이 장이 인용하지 않는다 — 참고문헌에는 본문이 "
                              "인용하는 문헌만 넣는다. 근거로만 쓰면 references_add에서 빼고 sources의 entry로 둔다")
    if data.get("chapter_hash") != book.chapter_hash(units):
        warnings.append("대장의 장 해시가 지금 장과 다르다 — sync를 다시 돌린다")
    stats = {"sentences": len(units), "kinds": counts}
    return errors, warnings, stats


def cmd_validate(args) -> int:
    errors, warnings, stats = validate(args.chapter, args.stage, args.final)
    for w in warnings:
        print(f"경고  {w}")
    for e in errors:
        print(f"오류  {e}")
    kinds = ", ".join(f"{k} {n}" for k, n in stats["kinds"].items())
    print(f"ledger validate {args.chapter}: 오류 {len(errors)}건 — 문장 {stats['sentences']}개({kinds})")
    return 1 if errors else 0


# ---------------------------------------------------------------- verdicts

def round_of(path: Path, data: dict) -> int:
    r = data.get("round")
    if isinstance(r, int):
        return r
    m = re.search(r"(?:^|-)r(\d+)[-.]", path.name)
    return int(m.group(1)) if m else 1


def cmd_verdicts(args) -> int:
    """회차가 여럿이면 문장마다 렌즈별로 가장 늦은 회차의 판정과 지적만 쓴다(고친 문장은 번호가 바뀌어 새로 점검받는다).
    지적은 (회차, 렌즈/번호)로 가린다. 차단 지적이 열려 있으면 불일치, 판정이 미확인이면 미확인이다.
    권고 지적은 판정을 바꾸지 않는다(수정 패스가 고칠 의무가 없다).
    연결 문장은 맡은 렌즈가 없어 판정 칸이 비지만, 어느 렌즈든 차단·미확인 지적이 열려 있으면 그것을 적는다."""
    data = load_ledger(args.chapter)
    judge: dict[tuple[int, str], str] = {}
    for jp in args.judge or []:
        jd = json.loads(Path(jp).read_text(encoding="utf-8"))
        r = round_of(Path(jp), jd)
        for d in jd.get("decisions", []):
            judge[(r, d.get("finding"))] = d.get("decision")
    checks = []
    for path in args.checks:
        c = json.loads(Path(path).read_text(encoding="utf-8"))
        checks.append((round_of(Path(path), c), path, c))
    last = max(r for r, _, _ in checks)
    # (문장, 렌즈) → 회차 → {"verdict": …, "findings": [(키, 심각도)]}
    seen: dict[tuple[str, str], dict[int, dict]] = {}
    for r, path, c in checks:
        lens = c.get("lens", "")
        if r == last and c.get("chapter_hash") and c["chapter_hash"] != data.get("chapter_hash"):
            print(f"오류  {path}: 다른 판의 장을 점검한 결과다(장 해시가 다르다)")
            return 1
        for sid, v in c.get("verdicts", {}).items():
            seen.setdefault((sid, lens), {}).setdefault(r, {"verdict": "", "findings": []})["verdict"] = v
        for f in c.get("findings", []):
            slot = seen.setdefault((f.get("sentence", ""), lens), {}).setdefault(r, {"verdict": "", "findings": []})
            slot["findings"].append(((r, f"{lens}/{f.get('id')}"), f.get("severity", "차단")))
    lenses = {lens for (_, lens) in seen}
    changed = 0
    for sid, e in data.get("sentences", {}).items():
        kind = e.get("kind", "")
        own = LENS_FOR.get(kind)
        if own is None and kind != "연결":
            continue
        v = ""
        rounds = seen.get((sid, own), {}) if own else {}
        for r in sorted(rounds, reverse=True):
            if rounds[r]["verdict"]:
                v = rounds[r]["verdict"]
                break
        open_block, open_unres, rejected = [], [], []
        for lens in lenses:
            rounds = seen.get((sid, lens), {})
            if not rounds:
                continue
            for key, sev in rounds[max(rounds)]["findings"]:
                dec = judge.get(key)
                if dec == "기각":
                    rejected.append(key)
                elif dec == "미확인":
                    open_unres.append(key)
                elif sev != "권고":
                    open_block.append(key)
        if open_unres:
            v = "미확인"
        elif open_block:
            v = "불일치"
        elif v == "불일치" and rejected:
            v = "일치"
        elif own is None:
            v = ""
        if e.get("verdict") != v:
            e["verdict"] = v
            changed += 1
    save_ledger(args.chapter, data)
    left = sum(1 for e in data["sentences"].values()
               if (e.get("kind") in LENS_FOR and e.get("verdict") not in ("일치", "해당 없음"))
               or (e.get("kind") == "연결" and e.get("verdict") in ("불일치", "미확인")))
    print(f"verdicts {args.chapter}: 회차 {sorted({r for r, _, _ in checks})}, 판정 {changed}곳 바꿈, 일치가 아닌 문장 {left}개")
    return 0


# ---------------------------------------------------------------- export

def cell(text: str) -> str:
    return str(text or "").replace("|", "／").replace("\n", " ").strip() or "—"


def cmd_export(args) -> int:
    errors, _, stats = validate(args.chapter, args.stage, True)
    if errors:
        for e in errors:
            print(f"오류  {e}")
        print("export 중단: 대장 검사(--final)를 통과하지 못했다")
        return 1
    ch, src, units = chapter_units(args.chapter, args.stage)
    data = load_ledger(ch.num)
    out = [f"# 근거 대장: {ch.num} {ch.title}", "",
           f"- 장 파일: {ch.path}",
           f"- 내용 해시: {book.chapter_hash(units)[:12]}",
           f"- 집필 AI: {data.get('writer')}", "",
           "이 대장은 교차 검토자가 「어디를 열어 볼지」 고르는 안내다. 검토 범위를 줄이지 않는다"
           "([작업 절차 §10.5](../../editorial/workflow.md#105-자체-점검과-교차-검토)).", "",
           "## 출처", "| 키 | 읽은 판 | 받은 날 | 범위 | 원본 sha256 |", "|---|---|---|---|---|"]
    for key, info in sorted(data.get("sources", {}).items(), key=lambda kv: kv[0].casefold()):
        for sid, scope in [(info["source_id"], info.get("scope"))] + list((info.get("parts") or {}).items()):
            rec = fetch.load_record(sid)
            out.append(f"| @{key} | {cell(rec.get('final_url'))} | {cell(rec.get('fetched_at', '')[:10])} | "
                       f"{cell(scope)} | {rec.get('sha256', '')[:12]} |")
    k = stats["kinds"]
    out += ["", "## 문장",
            f"문장 {stats['sentences']}개 — " + ", ".join(f"{n} {k[n]}" for n in KINDS) +
            ". 연결(앞뒤 문장을 잇는 서술)은 수만 적는다. 문장 번호는 `python3 tools/book.py sentences "
            f"{ch.num}`로 본문과 맞춘다.", "",
            "| 문장 | 갈래 | 근거 | 위치 | 닻 | 측정 조건 | 판정 |", "|---|---|---|---|---|---|---|"]
    line_of = {u["id"]: u["line"] for u in units}
    for u in units:
        e = data["sentences"][u["id"]]
        if e.get("kind") == "연결":
            continue
        refs = e.get("refs") or [{}]
        for r in refs:
            basis = (f"@{r['key']}" + (f" ({r['source_id']})" if r.get("source_id") else "")) if r.get("key") \
                else (e.get("path") or "—")
            out.append(f"| {u['id']} · {line_of[u['id']]}행 | {e.get('kind')} | {cell(basis)} | {cell(r.get('loc'))} | "
                       f"{cell(r.get('anchor'))} | {cell(r.get('conditions'))} | {cell(e.get('verdict'))} |")
    out += ["", "## 교차 검토 우선 목록"] + ([f"- {x}" for x in data.get("cross_review_priority", [])] or ["- 없음"])
    out += ["", "## 미확인으로 보낸 것"] + ([f"- {x}" for x in data.get("open_questions", [])] or ["- 없음"])
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    dest = EVIDENCE / f"{ch.num}.md"
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"export {ch.num}: {book.rel(dest)}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="tools/harness/ledger.py", description="근거 대장 도구(§10.4)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("facts")
    p.add_argument("chapter")
    p = sub.add_parser("sync")
    p.add_argument("chapter")
    p.add_argument("--stage")
    p.add_argument("--writer")
    p = sub.add_parser("validate")
    p.add_argument("chapter")
    p.add_argument("--stage")
    p.add_argument("--final", action="store_true")
    p = sub.add_parser("verdicts")
    p.add_argument("chapter")
    p.add_argument("checks", nargs="+")
    p.add_argument("--judge", nargs="*", default=[])
    p = sub.add_parser("export")
    p.add_argument("chapter")
    p.add_argument("--stage")
    args = ap.parse_args(argv[1:])
    return {"facts": cmd_facts, "sync": cmd_sync, "validate": cmd_validate, "verdicts": cmd_verdicts, "export": cmd_export}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
