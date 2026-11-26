#!/usr/bin/env python3
"""심은 오류 시험 세트 — 자체 점검 렌즈의 검출률을 잰다(설계안 11절의 1).

    python3 -I tools/harness/regression/run.py build 사본폴더 [--set planted-1]
    python3 -I tools/harness/regression/run.py score 사본폴더 [--set planted-1]

build는 저장소 밖의 빈 폴더에 격리된 사본을 만든다. 사본에는 git 이력·이 폴더(답)·작업 초안이 없다.
사본의 curriculum에 시험 장을 넣고, 장 초안을 stage에, 가짜 출처를 fetch.py로 보관함에, 근거 대장과
변경분을 build/harness/<장>/에 둔 뒤 lint·대장 검사·check가 통과하는지 본다. 렌즈와 판정은 그 사본에서
역할 카드대로 돌린다(README). score는 사본의 checks/r1-*.json과 judge-r1.json을 답과 맞춰 본다.
"""
from __future__ import annotations

import argparse
import email.message
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
SKIP_NAMES = {".git", ".venv", ".claude", "build", "node_modules", "__pycache__", ".DS_Store"}
SKIP_PATHS = {"tools/harness/regression", "workbench/drafts", "workbench/progress", "workbench/inbox"}


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def ignore(dirpath: str, names: list[str]) -> set[str]:
    rel = Path(dirpath).resolve().relative_to(REPO)
    out = set()
    for n in names:
        if n in SKIP_NAMES or (rel / n).as_posix() in SKIP_PATHS:
            out.add(n)
    return out


def run(out: Path, *cmd: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-I", *cmd], cwd=out, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def find_unit(units: list[dict], has: str) -> dict:
    hits = [u for u in units if has in u["text"]]
    if len(hits) != 1:
        raise SystemExit(f"오류  '{has}'에 맞는 문장이 {len(hits)}개다(하나여야 한다)")
    return hits[0]


# ---------------------------------------------------------------- build

def fake_fetch(fetch, src: dict, body: bytes) -> None:
    class Resp:
        status = 200

        def __init__(self) -> None:
            self.headers = email.message.Message()
            self.headers["Content-Type"] = src["content_type"]

        def geturl(self) -> str:
            return src["url"]

        def read(self, n: int = -1) -> bytes:
            return body

        def __enter__(self):
            return self

        def __exit__(self, *a) -> None:
            return None

    saved = (fetch.check_host, fetch.check_allowed, fetch.HOST_INTERVAL, fetch.urllib.request.urlopen)
    fetch.check_host = lambda url: None
    fetch.check_allowed = lambda url: None
    fetch.HOST_INTERVAL = 0
    fetch.urllib.request.urlopen = lambda req, timeout=0: Resp()
    try:
        fetch.get(src["url"], src["id"])
    finally:
        fetch.check_host, fetch.check_allowed, fetch.HOST_INTERVAL, fetch.urllib.request.urlopen = saved


def cmd_build(args) -> int:
    setdir = HERE / args.set
    setup = json.loads((setdir / "setup.json").read_text(encoding="utf-8"))
    out = Path(args.out).resolve()
    if out == REPO or REPO in out.parents:
        raise SystemExit("오류  사본은 저장소 밖에 만든다(렌즈가 답과 git 이력을 보지 못하게)")
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"오류  {out}이 비어 있지 않다")
    if out.exists():
        out.rmdir()
    shutil.copytree(REPO, out, ignore=ignore)
    num = setup["chapter"]

    # curriculum: 시험 장의 행을 바꿔 넣는다
    cur = out / "editorial/curriculum.md"
    lines = cur.read_text(encoding="utf-8").splitlines()
    idx = [i for i, ln in enumerate(lines) if ln.startswith(f"| {num} |")]
    if len(idx) != 1:
        raise SystemExit(f"오류  curriculum에 {num} 행이 {len(idx)}개다")
    lines[idx[0]] = setup["curriculum_row"]
    cur.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # 하네스 README에서 이 세트를 가리키는 절을 뺀다(사본에는 이 폴더가 없다)
    readme = out / "tools/harness/README.md"
    body = readme.read_text(encoding="utf-8")
    start = body.index("## 회귀 시험")
    end = body.index("\n## ", start + 1)
    readme.write_text(body[:start] + body[end + 1:], encoding="utf-8")

    book = load("regression_book", out / "tools/book.py")
    fetch = load("regression_fetch", out / "tools/harness/fetch.py")
    chapters = book.load_chapters()
    meta = book.expected_meta(chapters[num], chapters)
    text = (setdir / "chapter.md").read_text(encoding="utf-8").replace("{META}", meta)
    work = out / "build/harness" / num
    chap = work / "stage" / setup["chapter_file"]
    chap.parent.mkdir(parents=True, exist_ok=True)
    chap.write_text(text, encoding="utf-8")

    # 출처: 저장소 보관함의 진짜 출처는 장부 줄과 함께 옮기고, 가짜 출처는 fetch.py로 받는다
    src_root = REPO / "build/harness/sources"
    log = {}
    if (src_root / "fetch-log.jsonl").is_file():
        for line in (src_root / "fetch-log.jsonl").read_text(encoding="utf-8").splitlines():
            log[json.loads(line)["id"]] = line
    fetch.SOURCES.mkdir(parents=True, exist_ok=True)
    for src in setup["copy_sources"]:
        sid = src["id"]
        if sid not in log or not (src_root / sid).is_dir():
            raise SystemExit(f"오류  저장소 보관함에 {sid}가 없다. 먼저 받는다: "
                             f"python3 -I tools/harness/fetch.py get {src['url']} --id {sid}")
        shutil.copytree(src_root / sid, fetch.SOURCES / sid)
        with fetch.LOG.open("a", encoding="utf-8") as f:
            f.write(log[sid] + "\n")
    hosts = out / "tools/harness/allowed-hosts.txt"
    for src in setup["fake_sources"]:
        host = src["url"].split("/")[2]
        hosts.write_text(hosts.read_text(encoding="utf-8") + host + "\n", encoding="utf-8")
        fake_fetch(fetch, src, (setdir / src["file"]).read_bytes())

    # 변경분과 계산 기록
    delta = {"chapter": num, **setup["delta"],
             "stage_files": {setup["chapter_file"]: book.sha256_file(chap)}}
    book.write_json(str(work / "delta.json"), delta)
    for rel, body in setup["calc_records"].items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")

    # 근거 대장: sync로 문장 행을 만들고 규칙대로 갈래·근거를 단다
    led = setup["ledger"]
    rc, msg = run(out, "tools/harness/ledger.py", "sync", num, "--writer", led["writer"])
    if rc:
        raise SystemExit(msg)
    lpath = work / "ledger.json"
    data = json.loads(lpath.read_text(encoding="utf-8"))
    data["sources"] = led["sources"]
    units = book.sentence_units(chap.read_text(encoding="utf-8"))
    ruled = {}
    for rule in led["rules"]:
        u = find_unit(units, rule["has"])
        ruled[u["id"]] = rule
    for u in units:
        e = data["sentences"][u["id"]]
        rule = ruled.get(u["id"])
        if rule:
            e["kind"] = rule["kind"]
            e["refs"] = rule.get("refs", [])
            if "path" in rule:
                e["path"] = rule["path"]
        else:
            e["kind"] = led["default_kind"]
            e["refs"] = []
    book.write_json(str(lpath), data)

    rc, msg = run(out, "tools/book.py", "toc")
    if rc:
        raise SystemExit(msg)
    problems = []
    for name, cmd, good in (
        ("lint", ["tools/book.py", "lint", num], "오류 0건"),
        ("ledger validate", ["tools/harness/ledger.py", "validate", num], "오류 0건"),
        ("fetch verify", ["tools/harness/fetch.py", "verify"], "문제 0개"),
        ("check", ["tools/book.py", "check"], "오류 0건"),
    ):
        rc, msg = run(out, *cmd)
        last = [ln for ln in msg.strip().splitlines() if ln.strip()][-1:] or [""]
        print(f"{name}: {last[0]}")
        if rc or good not in msg:
            problems.append(f"{name}:\n{msg[-3000:]}")
    for p in problems:
        print(p)
    if problems:
        return 1
    print(f"사본 {out}: 장 {num}, 문장 {len(units)}개. 렌즈는 이 사본 안에서만 돌린다.")
    return 0


# ---------------------------------------------------------------- score

def cmd_score(args) -> int:
    setdir = HERE / args.set
    answers = json.loads((setdir / "answers.json").read_text(encoding="utf-8"))
    out = Path(args.out).resolve()
    num = answers["chapter"]
    book = load("regression_book", out / "tools/book.py")
    _, ch, src, _ = book.resolve_chapter_file(num, None, None)
    units = book.sentence_units(src.read_text(encoding="utf-8"))
    text_of = {u["id"]: u["text"] for u in units}
    work = out / "build/harness" / num
    rnd = args.round

    findings = []
    verdicts: dict[str, dict[str, str]] = {}
    for f in sorted((work / "checks").glob(f"r{rnd}-*.json")):
        if f.name.endswith("-sentences.json"):
            continue
        c = json.loads(f.read_text(encoding="utf-8"))
        lens = c.get("lens", f.stem)
        for sid, v in c.get("verdicts", {}).items():
            verdicts.setdefault(sid, {})[lens] = v
        for x in c.get("findings", []):
            findings.append({**x, "lens": lens, "key": f"{lens}/{x.get('id')}"})
    judge = {}
    jpath = work / f"judge-r{rnd}.json"
    if jpath.is_file():
        for d in json.loads(jpath.read_text(encoding="utf-8")).get("decisions", []):
            judge[d.get("finding")] = d.get("decision")

    def words(x: dict) -> str:
        return " ".join(str(x.get(k, "")) for k in ("claim", "fix"))

    expected = {}
    for x in findings:
        for e in answers.get("expected", []):
            if any(k in words(x) for k in e["keywords"]):
                expected[x["key"]] = e["id"]
    planted_ids = set()
    rows = []
    for a in answers["planted"]:
        sid = find_unit(units, a["has"])["id"]
        planted_ids.add(sid)
        on = [x for x in findings if x.get("sentence") == sid and x["key"] not in expected]
        diag = [x for x in on if any(k in words(x) for k in a["keywords"])]
        lens_v = verdicts.get(sid, {})
        rows.append({
            "id": a["id"], "type": a["type"], "sentence": sid,
            "found": bool(on) or "불일치" in lens_v.values(),
            "diagnosed": bool(diag),
            "blocking": any(x.get("severity") == "차단" for x in diag),
            "accepted": any(judge.get(x["key"]) == "채택" for x in diag),
            "unresolved": any(judge.get(x["key"]) == "미확인" for x in diag),
            "by": sorted({x["lens"] for x in diag}),
        })
    control_ids = {find_unit(units, c["has"])["id"]: c["id"] for c in answers["controls"]}
    known_ids = {find_unit(units, h)["id"]: k["id"] for k in answers.get("known", []) for h in k["has"]}
    others = [x for x in findings if x.get("sentence") not in planted_ids and x["key"] not in expected]
    unknown = [x for x in others if x.get("sentence") not in text_of]

    print(f"점수 {num} 회차 {rnd}: 지적 {len(findings)}개, 판정 {len(judge)}개")
    print("| 오류 | 유형 | 지적 | 진단 맞음 | 차단 | 판정 채택 | 렌즈 |")
    print("|---|---|---|---|---|---|---|")
    yes = lambda b: "O" if b else "—"
    for r in rows:
        print(f"| {r['id']} | {r['type']} | {yes(r['found'])} | {yes(r['diagnosed'])} | {yes(r['blocking'])} | "
              f"{yes(r['accepted']) if not r['unresolved'] else '미확인'} | {', '.join(r['by']) or '—'} |")
    n = len(rows)
    print(f"검출(진단 맞음) {sum(r['diagnosed'] for r in rows)}/{n}, 판정 뒤 남음 "
          f"{sum(r['accepted'] or r['unresolved'] for r in rows)}/{n}")
    for eid in sorted(set(expected.values())):
        keys = [k for k, v in expected.items() if v == eid]
        print(f"설계상 예상한 지적 {eid}: {len(keys)}개 ({', '.join(keys)})")
    for kid in [k["id"] for k in answers.get("known", [])]:
        hit = [x["key"] for x in others if known_ids.get(x.get("sentence")) == kid]
        print(f"알려진 문제 {kid}: {'검출 ' + ', '.join(hit) if hit else '못 잡음'}")
    blocking_fp = [x for x in others if x.get("severity") == "차단" and x.get("sentence") not in known_ids]
    print(f"심지 않은 문장의 지적 {len(others)}개 — 알려진 문제 밖의 차단 {len(blocking_fp)}개(판정 채택 "
          f"{sum(judge.get(x['key']) == '채택' for x in blocking_fp)}개, 대조 문장 {sum(x.get('sentence') in control_ids for x in blocking_fp)}개), "
          f"장에 없는 문장 번호 {len(unknown)}개")
    for x in others:
        tag = known_ids.get(x.get("sentence")) or control_ids.get(x.get("sentence"), "")
        print(f"  - {x['key']} [{x.get('severity')}] {tag + ' ' if tag else ''}{judge.get(x['key'], '판정 없음')}: "
              f"{str(x.get('claim', ''))[:160]}")
    result = {"set": answers["set"], "round": rnd, "planted": rows, "expected": expected,
              "other_findings": [{"finding": x["key"], "sentence": x.get("sentence"), "severity": x.get("severity"),
                                  "control": control_ids.get(x.get("sentence")), "known": known_ids.get(x.get("sentence")),
                                  "decision": judge.get(x["key"]),
                                  "claim": x.get("claim")} for x in others]}
    book.write_json(str(out / f"score-r{rnd}.json"), result)
    print(f"→ {out / f'score-r{rnd}.json'}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="tools/harness/regression/run.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "score"):
        p = sub.add_parser(name)
        p.add_argument("out", help="저장소 밖의 사본 폴더")
        p.add_argument("--set", default="planted-1")
        if name == "score":
            p.add_argument("--round", type=int, default=1)
    args = ap.parse_args(argv[1:])
    return cmd_build(args) if args.cmd == "build" else cmd_score(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
