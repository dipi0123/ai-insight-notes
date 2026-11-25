"""하네스 도구의 수용 시험.

  python3 -I tools/harness/selftest.py [--keep]

저장소를 build/harness/selftest/에 복사하고 그 사본에서만 돈다. 진짜 저장소의 파일은 바꾸지 않는다.
일부러 깨뜨린 장·용어집·참고문헌·미확인 목록·변경분·출처 보관함이 각각 잡히는지,
정상 변경분의 merge 뒤 toc·check가 통과하는지, 근거 대장이 문장과 출처를 제대로 묶는지 본다.
네트워크는 쓰지 않는다(출처 내려받기는 가짜 응답으로 시험한다).
"""

from __future__ import annotations

import argparse
import email.message
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
WORK = REPO / "build" / "harness" / "selftest"
IGNORE = shutil.ignore_patterns(".git", ".venv", "build", "node_modules", "__pycache__", ".DS_Store")
CH13 = "book/part01-big-picture/01-03-model-lifecycle.md"
CH15 = "book/part01-big-picture/01-05-landmark-models.md"
GLOSSARY = "book/appendix/glossary.md"
REFERENCES = "book/appendix/references.md"
OQ = "editorial/open-questions.md"
CURRICULUM = "editorial/curriculum.md"
SHARED = (GLOSSARY, REFERENCES, OQ, CURRICULUM, "book/README.md")
FAKE_HTML = (b"<html><head><title>t</title><script>ignore me</script></head><body>"
             b"<p>Once the cumbersome model has been trained, we can then use a different kind of training, "
             b"which we call distillation, to transfer the knowledge to a small model.</p></body></html>")


class Suite:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.results: list[tuple[str, bool, str]] = []

    def run(self, *cmd: str) -> tuple[int, str]:
        p = subprocess.run([sys.executable, "-I", *cmd], cwd=self.root, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    def expect(self, name: str, cmd: list[str], code: int | None, *has: str, absent: tuple = ()) -> str:
        rc, out = self.run(*cmd)
        ok = (code is None or rc == code) and all(h in out for h in has) and not any(a in out for a in absent)
        why = "" if ok else f"종료 코드 {rc}(기대 {code}), 출력:\n{out[-1500:]}"
        self.results.append((name, ok, why))
        return out

    def check(self, name: str, ok: bool, why: str = "") -> None:
        self.results.append((name, ok, "" if ok else why))

    def path(self, rel: str) -> Path:
        return self.root / rel

    def hashes(self) -> dict[str, str]:
        return {r: hashlib.sha256(self.path(r).read_bytes()).hexdigest() for r in SHARED}


def rep(old: str, new: str):
    def fn(text: str) -> str:
        assert old in text, f"변형할 곳이 없다: {old[:50]}"
        return text.replace(old, new, 1)
    return fn


@contextmanager
def patched(path: Path, fn):
    orig = path.read_text(encoding="utf-8")
    new = fn(orig)
    assert new != orig, f"변형이 적용되지 않았다: {path}"
    path.write_text(new, encoding="utf-8")
    try:
        yield
    finally:
        path.write_text(orig, encoding="utf-8")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- 시험

def lint_cases(s: Suite) -> None:
    stage = s.path("build/harness/1.3/stage") / CH13
    write(stage, s.path(CH13).read_text(encoding="utf-8"))
    lint = ["tools/book.py", "lint", "1.3"]
    s.expect("lint: 1.3 사본은 오류 0", lint, 0, "오류 0건", "build/harness/1.3/stage")
    cases = [
        ("제목", rep("# 1.3 ", "# 1.3 틀린 "), 1, "첫 줄이"),
        ("메타 줄", rep("**이 장의 질문** ", "**이 장의 질문** 바뀐 "), 1, "메타 줄이 curriculum과 다르다"),
        ("정리 없음", rep("## 정리\n", "정리\n"), 1, "'## 정리' 절이 없다"),
        ("끝 절 순서", lambda t: t.replace("## 헷갈리기 쉬운 점", "@@").replace("## 정리", "## 헷갈리기 쉬운 점").replace("@@", "## 정리"), 1, "끝 절 순서"),
        ("절 번호", rep("## 2. ", "## 3. "), 1, "본문 절 번호"),
        ("모르는 절", rep("## 정리\n", "## 덤\n\n덤이다.\n\n## 정리\n"), 1, "'## 덤'"),
        ("답 수", lambda t: t.replace("\n4. 앞의 것은", "\n앞의 것은"), 1, "답 3개가 문제 4개와 다르다"),
        ("문제 수", lambda t: t.replace("\n3. test set", "\ntest set").replace("\n4. 「전날", "\n「전날"), 1, "확인 문제는 3~5개다"),
        ("상자 라벨", rep("> **핵심** 문제 정의가", "> **팁** 문제 정의가"), 1, "상자 라벨 '팁'"),
        ("금지 표현", rep("## 정리\n", "질문하신 내용이다.\n\n## 정리\n"), 1, "대화체"),
        ("인용 키", rep("[@Sculley2015]", "[@Nobody2020]"), 1, "@Nobody2020"),
        ("링크 대상", rep("(01-01-ai-ml-dl.md", "(01-01-missing.md"), 1, "링크 대상"),
        ("앵커", rep("## 정리\n", "[1.1](01-01-ai-ml-dl.md#없는-절)\n\n## 정리\n"), 1, "앵커가 없다"),
        ("시점 표현", rep("## 정리\n", "최근 모델은 크다.\n\n## 정리\n"), 0, "경고", "'최근'"),
        ("그림 설명", lambda t: "\n".join(ln for ln in t.splitlines() if not ln.startswith("그림: 모델의 한살이")) + "\n", 0, "그림: …"),
        ("더 읽을거리 인용", lambda t: t.rstrip("\n") + "\n- 아무 문헌\n", 0, "[@키]로 인용"),
    ]
    for name, fn, code, *has in cases:
        with patched(stage, fn):
            s.expect(f"lint: {name}", lint, code, *has)
    # 변경분의 새 참고문헌 키는 인용으로 인정한다.
    delta = s.path("build/harness/1.3/delta.json")
    write(delta, json.dumps({"chapter": "1.3", "references_add": [
        "- **@Nobody2020** · A. 「T」. arXiv, 2020. https://arxiv.org/abs/2001.00001"]}))
    with patched(stage, rep("[@Sculley2015]", "[@Nobody2020]")):
        s.expect("lint: 변경분의 새 키 인정", lint, 0, "오류 0건")
    delta.unlink()
    # 같은 묶음의 다른 장 초안으로 가는 링크는 그 장의 stage에서 찾는다.
    write(s.path("build/harness/1.5/stage") / CH15, "# 1.5 임시\n")
    with patched(stage, rep("## 정리\n", "[1.5](01-05-landmark-models.md)\n\n## 정리\n")):
        s.expect("lint: 다른 장 stage로 가는 링크", lint, 0, "오류 0건")
    shutil.rmtree(s.path("build/harness/1.5"))
    shutil.rmtree(s.path("build/harness/1.3"))


def check_cases(s: Suite) -> None:
    check = ["tools/book.py", "check"]
    s.expect("check: 사본은 오류 0", check, 0, "오류 0건")
    gl, refs, oq = s.path(GLOSSARY), s.path(REFERENCES), s.path(OQ)

    def swap_rows(text: str) -> str:
        lines = text.splitlines()
        i = next(k for k, ln in enumerate(lines) if ln.startswith("| action |"))
        lines[i], lines[i + 1] = lines[i + 1], lines[i]
        return "\n".join(lines) + "\n"

    def dup_row(text: str) -> str:
        lines = text.splitlines()
        i = next(k for k, ln in enumerate(lines) if ln.startswith("| action |"))
        lines.insert(i + 1, lines[i])
        return "\n".join(lines) + "\n"

    def swap_refs(text: str) -> str:
        lines = text.splitlines()
        i = next(k for k, ln in enumerate(lines) if ln.startswith("- **@"))
        lines[i], lines[i + 1] = lines[i + 1], lines[i]
        return "\n".join(lines) + "\n"

    cases = [
        ("용어집 순서", gl, swap_rows, 1, "알파벳순"),
        ("용어집 중복", gl, dup_row, 1, "행에도 있다"),
        ("용어집 분류", gl, rep("| 학습신호 |", "| 신호 |"), 1, "분류 '신호'"),
        ("용어집 본 장 링크", gl, rep("[1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1 |", "[1.4](01-04-training-methods-map.md), 10.1 |"), 1, "의 링크는"),
        ("용어집 본 장 순서", gl, rep("[1.4](../part01-big-picture/01-04-training-methods-map.md), 10.1", "10.1, [1.4](../part01-big-picture/01-04-training-methods-map.md)"), 1, "책 순서가 아니다"),
        ("용어집 링크 없는 번호", gl, rep("[1.3](../part01-big-picture/01-03-model-lifecycle.md)", "1.3"), 0, "링크로 건다"),
        ("참고문헌 순서", refs, swap_refs, 1, "알파벳순에서 벗어났다"),
        ("참고문헌 「」", refs, rep("「Software Engineering", "Software Engineering"), 1, "「」로 감싼다"),
        ("참고문헌 같은 문헌", refs, lambda t: t.rstrip("\n") + "\n- **@Zz2099** · X. 「Y」. arXiv, 2099. https://arxiv.org/abs/1503.02531\n", 1, "같은 문헌"),
        ("미확인 번호", oq, lambda t: t.rstrip("\n") + "\n| OQ-1 | a | 1.1 | b |\n", 1, "OQ-세 자리"),
        ("미확인 칸 수", oq, lambda t: t.rstrip("\n") + "\n| OQ-001 | a | b |\n", 1, "칸이 4개가 아니라"),
        ("장 메타 줄", s.path("book/part01-big-picture/01-04-training-methods-map.md"), rep("**이 장의 질문** ", "**이 장의 질문** 바뀐 "), 1, "메타 줄이 curriculum과 다르다"),
    ]
    for name, path, fn, code, *has in cases:
        with patched(path, fn):
            s.expect(f"check: {name}", check, code, *has)


def fake_chapter(s: Suite) -> str:
    book = load("book_copy", s.path("tools/book.py"))
    chapters = book.load_chapters()
    meta = book.expected_meta(chapters["1.5"], chapters)
    return f"""# 1.5 대표 모델 지도

{meta}

## 한눈에

- distillation(증류)은 큰 모델이 배운 것을 작은 모델로 옮기는 학습이다 [@Hinton2015].

## 1. 시험 절

시험용 문장이다. 2 더하기 3은 5다.

## 정리

- 시험용 문장이다.

## 확인 문제

1. 첫 문제?
2. 둘째 문제?
3. 셋째 문제?

<details>
<summary>답</summary>

1. 첫 답.
2. 둘째 답.
3. 셋째 답.

</details>

## 더 읽을거리

- [@Hinton2015] distillation을 처음 제안한 논문
"""


def merge_cases(s: Suite) -> None:
    h = s.path("build/harness")
    stage = h / "1.5/stage"
    chap = stage / CH15
    write(chap, fake_chapter(s))
    gl = s.path(GLOSSARY)
    vit = "| ViT | Vision Transformer | — | 구조 | 이미지를 patch로 잘라 token처럼 늘어놓고 Transformer에 넣는 구조 | [1.2](../part01-big-picture/01-02-naming-axes.md), 6.3 |"
    gl.write_text(rep(vit, vit.replace("), 6.3 |", "), 1.5, 6.3 |"))(gl.read_text(encoding="utf-8")), encoding="utf-8")
    s.expect("check: 링크 없는 1.5 언급은 통과", ["tools/book.py", "check"], 0, "오류 0건")
    good = {
        "chapter": "1.5", "status": "초고 · Claude",
        "stage_files": {CH15: sha(chap)},
        "glossary_add": [{"표기": "zeta test", "풀이": "—", "한국어": "제타 시험", "분류": "평가",
                          "정의": "수용 시험용 행", "본장": ["1.5"]}],
        "glossary_link": [{"표기": "weight", "장": "1.5"}],
        "references_add": ["- **@Aaa2001** · A. 「Test Title」. arXiv, 2001. https://arxiv.org/abs/0101.00001"],
        "open_questions_add": [{"확인할 것": "수용 시험 항목", "관련 장": "1.5", "확인 방법": "시험"}],
    }
    dpath = h / "1.5/delta.json"
    base = h / "batch-01-1/base.json"
    s.expect("hashes", ["tools/book.py", "hashes", "--out", str(base.relative_to(s.root))], 0)
    merge = ["tools/book.py", "merge", str(dpath.relative_to(s.root))]

    def bad(name: str, delta: dict, *has: str, extra=None, args=()) -> None:
        write(dpath, json.dumps(delta, ensure_ascii=False))
        if extra:
            extra()
        before = s.hashes()
        s.expect(f"merge 거부: {name}", merge + list(args), 1, *has)
        s.check(f"merge 거부 뒤 그대로: {name}", s.hashes() == before and not s.path(CH15).exists(), "공유 파일이나 book/이 바뀌었다")

    bad("상태 검토완료", {**good, "status": "검토완료 · Claude / GPT"}, "초고 · 집필AI")
    bad("상태 없음", {k: v for k, v in good.items() if k != "status"}, "status('초고 · 집필AI')가 필요하다")
    bad("모르는 키", {**good, "extra": 1}, "모르는 키")
    bad("용어집 충돌", {**good, "glossary_add": [{**good["glossary_add"][0], "표기": "weight"}]}, "다른 내용으로 있다")
    bad("같은 문헌", {**good, "references_add": ["- **@Bbb2015** · B. 「X」. arXiv, 2015. https://arxiv.org/abs/1503.02531"]}, "같은 문헌")
    bad("참고문헌 형식", {**good, "references_add": ["- **@Ccc2001** · C. Title. arXiv, 2001. https://x.org/a"]}, "「」로 감싼다")
    other = "book/part02-math-and-tools/02-01-vectors-matrices-tensors.md"
    write(stage / other, "x\n")
    bad("남의 장 파일", {**good, "stage_files": {**good["stage_files"], other: sha(stage / other)}}, "놓을 수 있는 파일이 아니다")
    (stage / other).unlink()
    shutil.rmtree(stage / "book/part02-math-and-tools")
    write(stage / "book/figures/01-05-x.svg", "<svg/>")
    bad("목록에 없는 stage 파일", good, "stage_files에 없다")
    (stage / "book/figures/01-05-x.svg").unlink()
    shutil.rmtree(stage / "book/figures")
    orig = chap.read_text(encoding="utf-8")
    write(chap, orig + "\n덧붙임.\n")
    bad("판정 뒤 바뀐 초안", good, "sha256 불일치")
    write(chap, orig)
    oqp = s.path(OQ)
    oq_orig = oqp.read_text(encoding="utf-8")
    bad("묶음 시작 뒤 공유 파일 변경", good, "공유 파일이 바뀌었다",
        extra=lambda: oqp.write_text(oq_orig.replace("확인되면", "확인이 되면", 1), encoding="utf-8"),
        args=("--base", str(base.relative_to(s.root))))
    oqp.write_text(oq_orig, encoding="utf-8")

    write(dpath, json.dumps(good, ensure_ascii=False))
    s.expect("merge --dry-run은 쓰지 않는다", merge + ["--dry-run"], 0, "아무것도 쓰지 않았다")
    s.check("dry-run 뒤 book/에 없다", not s.path(CH15).exists())
    s.expect("merge 정상", merge + ["--base", str(base.relative_to(s.root)), "--oq-floor", "7"], 0,
             "용어집 +1행", "참고문헌 +1개", "OQ-008", "curriculum 1.5: 계획 → 초고 · Claude")
    gtext = gl.read_text(encoding="utf-8")
    link15 = "[1.5](../part01-big-picture/01-05-landmark-models.md)"
    s.check("merge: 장 파일을 놓았다", s.path(CH15).read_text(encoding="utf-8") == chap.read_text(encoding="utf-8"))
    s.check("merge: 새 용어 행", f"| zeta test | — | 제타 시험 | 평가 | 수용 시험용 행 | {link15} |" in gtext)
    s.check("merge: glossary_link", f"[1.4](../part01-big-picture/01-04-training-methods-map.md), {link15}, 4.2 |" in gtext)
    s.check("merge: 링크 없는 언급을 링크로 올림", f"[1.2](../part01-big-picture/01-02-naming-axes.md), {link15}, 6.3 |" in gtext)
    rtext = s.path(REFERENCES).read_text(encoding="utf-8")
    s.check("merge: 참고문헌 키 순서", rtext.index("@Aaa2001") < rtext.index("@Amershi2019"))
    s.check("merge: 미확인 번호", "| OQ-008 | 수용 시험 항목 | 1.5 | 시험 |" in s.path(OQ).read_text(encoding="utf-8"))
    s.check("merge: curriculum 상태 칸만", "| `book/part01-big-picture/01-05-landmark-models.md` | 초고 · Claude |" in s.path(CURRICULUM).read_text(encoding="utf-8"))
    snaps = sorted((h / "snapshots").glob("merge-*/manifest.json"))
    s.check("merge: 스냅숏", bool(snaps) and CH15 in json.loads(snaps[-1].read_text(encoding="utf-8"))["files"])
    s.expect("merge 다시 돌려도 바뀌지 않음", merge, 0, "바꿀 것이 없다")
    s.expect("merge 뒤 toc", ["tools/book.py", "toc"], 0)
    s.expect("merge 뒤 check 오류 0", ["tools/book.py", "check"], 0, "오류 0건")


def fetch_and_ledger_cases(s: Suite) -> None:
    fetch = load("fetch_copy", s.path("tools/harness/fetch.py"))

    class Resp:
        status = 200

        def __init__(self) -> None:
            self.headers = email.message.Message()
            self.headers["Content-Type"] = "text/html; charset=utf-8"

        def geturl(self) -> str:
            return "https://example.org/hinton"

        def read(self, n: int = -1) -> bytes:
            return FAKE_HTML

        def __enter__(self):
            return self

        def __exit__(self, *a) -> None:
            return None

    fetch.check_host = lambda url: None
    fetch.HOST_INTERVAL = 0
    fetch.urllib.request.urlopen = lambda req, timeout=0: Resp()
    rec = fetch.get("https://example.org/hinton", "hinton2015-test")
    s.check("fetch: 가짜 응답 받기", rec["kind"] == "html" and rec.get("text_sha256") is not None)
    s.check("fetch: script 본문 제외", "ignore me" not in (fetch.SOURCES / "hinton2015-test/text.txt").read_text(encoding="utf-8"))
    F = ["tools/harness/fetch.py"]
    s.expect("fetch verify 정상", F + ["verify"], 0, "문제 0개")
    s.expect("fetch anchor", F + ["anchor", "hinton2015-test", "which we call distillation"], 0, '"found": true')
    stray = fetch.SOURCES / "hinton2015-test/note.md"
    stray.write_text("x", encoding="utf-8")
    s.expect("fetch verify: 섞인 파일", F + ["verify"], 1, "도구가 만들지 않은 파일")
    stray.unlink()

    L = ["tools/harness/ledger.py"]
    led = s.path("build/harness/1.5/ledger.json")
    data = {"chapter": "1.5", "sources": {"Hinton2015": {"source_id": "hinton2015-test", "scope": "전문"}},
            "facts": [{"id": "f1", "claim": "distillation이라는 이름", "key": "Hinton2015", "loc": "1쪽",
                       "anchor": "which we call distillation"}], "gaps": []}
    write(led, json.dumps(data, ensure_ascii=False))
    s.expect("ledger facts 정상", L + ["facts", "1.5"], 0, "오류 0건")
    data["facts"][0]["anchor"] = "which we name distillation"
    write(led, json.dumps(data, ensure_ascii=False))
    s.expect("ledger facts: 없는 닻", L + ["facts", "1.5"], 1, "출처 본문에 없다")
    data["facts"][0]["anchor"] = "which we call distillation"
    write(led, json.dumps(data, ensure_ascii=False))

    out = s.expect("ledger sync", L + ["sync", "1.5", "--writer", "Claude"], 0, "새로")
    s.expect("ledger validate: 갈래 없음", L + ["validate", "1.5"], 1, "갈래가 없거나")
    rc, sent = s.run("tools/book.py", "sentences", "1.5", "--json", "build/harness/1.5/sentences.json")
    units = json.loads(s.path("build/harness/1.5/sentences.json").read_text(encoding="utf-8"))["units"]
    ids = [u["id"] for u in units]
    s.check("sentences: 같은 문장은 -2", any(i.endswith("-2") for i in ids), str(ids))
    calc = s.path("build/harness/1.5/runs/calc-1.txt")
    write(calc, "2 + 3 = 5\n")
    led_data = json.loads(led.read_text(encoding="utf-8"))
    for u in units:
        e = led_data["sentences"][u["id"]]
        if "[@Hinton2015]" in u["text"]:
            e.update(kind="출처", refs=[{"key": "Hinton2015", "loc": "1쪽", "anchor": "which we call distillation"}])
        elif "2 더하기 3" in u["text"]:
            e.update(kind="계산", path="build/harness/1.5/runs/calc-1.txt")
        elif u["kind"] in ("목록", "문단"):
            e.update(kind="설명")
        else:
            e.update(kind="연결")
    write(led, json.dumps(led_data, ensure_ascii=False))
    s.expect("ledger validate 정상", L + ["validate", "1.5"], 0, "오류 0건")
    cited = next(u["id"] for u in units if "[@Hinton2015]" in u["text"] and u["kind"] == "목록")
    broken = json.loads(led.read_text(encoding="utf-8"))
    broken["sentences"][cited]["refs"] = []
    write(led, json.dumps(broken, ensure_ascii=False))
    s.expect("ledger validate: 인용에 근거 없음", L + ["validate", "1.5"], 1, "근거에 @Hinton2015가 없다")
    write(led, json.dumps(led_data, ensure_ascii=False))
    s.expect("ledger validate --final: 판정 없음", L + ["validate", "1.5", "--final"], 1, "판정이")
    h = json.loads(led.read_text(encoding="utf-8"))["chapter_hash"]
    checks = s.path("build/harness/1.5/checks")
    source_ids = {sid: "일치" for sid, e in led_data["sentences"].items() if e["kind"] == "출처"}
    write(checks / "r1-source.json", json.dumps({"lens": "출처 대조", "chapter_hash": h,
          "verdicts": source_ids, "findings": []}, ensure_ascii=False))
    explain_ids = {sid: "일치" for sid, e in led_data["sentences"].items() if e["kind"] in ("설명", "계산")}
    write(checks / "r1-explain.json", json.dumps({"lens": "설명", "chapter_hash": h,
          "verdicts": explain_ids, "findings": [{"id": "F1", "sentence": cited, "severity": "차단",
                                                 "claim": "시험", "evidence": {"type": "규칙"}}]}, ensure_ascii=False))
    calc_ids = {sid: "일치" for sid, e in led_data["sentences"].items() if e["kind"] == "계산"}
    write(checks / "r1-calc.json", json.dumps({"lens": "검산·실행", "chapter_hash": h, "verdicts": calc_ids,
          "findings": []}, ensure_ascii=False))
    V = L + ["verdicts", "1.5", "build/harness/1.5/checks/r1-source.json", "build/harness/1.5/checks/r1-explain.json",
             "build/harness/1.5/checks/r1-calc.json"]
    s.expect("ledger verdicts: 열린 지적은 불일치", V, 0, "일치가 아닌 문장 1개")
    write(s.path("build/harness/1.5/judge-r1.json"), json.dumps({"decisions": [{"finding": "설명/F1", "decision": "기각"}]},
                                                               ensure_ascii=False))
    s.expect("ledger verdicts: 기각되면 일치", V + ["--judge", "build/harness/1.5/judge-r1.json"], 0, "일치가 아닌 문장 0개")
    s.expect("ledger validate --final 정상", L + ["validate", "1.5", "--final"], 0, "오류 0건")
    s.expect("ledger export", L + ["export", "1.5"], 0, "workbench/evidence/1.5.md")
    ev = s.path("workbench/evidence/1.5.md").read_text(encoding="utf-8")
    s.check("export: 출처 표와 닻", "| @Hinton2015 | https://example.org/hinton |" in ev and "which we call distillation" in ev)
    s.expect("export 뒤 check 오류 0", ["tools/book.py", "check"], 0, "오류 0건")

    txt = fetch.SOURCES / "hinton2015-test/text.txt"
    orig = txt.read_text(encoding="utf-8")
    txt.write_text(orig + "forged\n", encoding="utf-8")
    s.expect("ledger validate: 바뀐 출처 본문", L + ["validate", "1.5"], 1, "본문 텍스트가 기록과 다르다")
    txt.write_text(orig, encoding="utf-8")
    chap = s.path("build/harness/1.5/stage") / CH15
    with patched(chap, rep("시험용 문장이다. 2 더하기", "고친 문장이다. 2 더하기")):
        s.expect("ledger validate: 바뀐 문장", L + ["validate", "1.5"], 1, "대장에 없다", "장에 없는 문장")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="tools/harness/selftest.py")
    ap.add_argument("--keep", action="store_true", help="시험이 끝나도 사본을 지우지 않는다")
    args = ap.parse_args(argv[1:])
    if WORK.exists():
        shutil.rmtree(WORK)
    shutil.copytree(REPO, WORK / "repo", ignore=IGNORE)
    s = Suite(WORK / "repo")
    for group in (lint_cases, check_cases, merge_cases, fetch_and_ledger_cases):
        try:
            group(s)
        except Exception as e:  # 시험 준비가 깨지면 그 묶음 전체를 실패로 센다
            s.check(f"{group.__name__} 준비", False, f"{type(e).__name__}: {e}")
    failed = [r for r in s.results if not r[1]]
    for name, ok, why in s.results:
        print(f"{'통과' if ok else '실패'}  {name}")
        if not ok:
            print("      " + why.replace("\n", "\n      "))
    print(f"selftest: {len(s.results)}개 중 실패 {len(failed)}개" + ("" if args.keep else " (사본을 지웠다)"))
    if not args.keep:
        shutil.rmtree(WORK)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
