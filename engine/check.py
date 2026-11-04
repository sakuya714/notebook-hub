# -*- coding: utf-8 -*-
"""ビルド前のチェック（全ノート共通）。エラーが1つでもあればビルドを止める。

1. 書き間違い：知らない @記法・@xxx と @end の数の食い違い・存在しない章へのリンク・note.json の不備
   ＋置き場所：ノート側（本文・figs.py）に見た目（style= ・<style>・var(--…)）を書いていないか
2. 公開してはいけない情報：メール・電話・学籍番号・APIキー・Mac のパス・.private-words に書いた言葉
   （このサイトは GitHub で公開する。.private-words は公開しない＝.gitignore 済み）
"""
import os, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from markup import sec_slug, XREF, split_note

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCKS = {"map", "stack", "mx", "lad", "html", "flows", "box", "card", "fold", "quiz", "ox", "check", "steps", "stats", "routes", "cover"}
SINGLE = {"part", "ch", "board", "pair", "toc", "formulas", "pairs", "legend", "fig", "fig!", "flow", "end"}
BOX_TONES = {"why", "exam", "warn", "goal"}
NOTE_KEYS = {"title", "type", "labels", "macros"}
TYPES = ("整理型", "理解型")

SECRET_PATTERNS = [
    (r"[\w.+-]+@[\w-]+\.[\w.-]+", "メールアドレス"),
    (r"(?<!\d)0\d{1,4}-\d{1,4}-\d{3,4}(?!\d)", "電話番号"),
    (r"(?<!\d)\d{2}-\d-\d{3}-\d{4}(?!\d)", "学籍番号の形"),
    (r"\b(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_\w{20,}|AKIA[0-9A-Z]{16}|xox[bpa]-[\w-]{10,})", "APIキー・トークン"),
    (r"/Users/[^\s\"']+", "Mac のファイルの場所"),
]

def private_words():
    p = os.path.join(ROOT, ".private-words")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as fh:
        return [w.strip() for w in fh if w.strip() and not w.startswith("#")]

def scan_privacy(errors):
    words = private_words()
    targets = []
    for base in ("notes", "theme", "engine"):
        for f in glob.glob(os.path.join(ROOT, base, "**", "*"), recursive=True):
            if os.path.isfile(f) and f.endswith((".txt", ".json", ".py", ".js", ".css", ".html", ".md")) and "/vendor/" not in f:
                targets.append(f)
    targets += [os.path.join(ROOT, f) for f in ("hub.py", "README.md")]
    for f in targets:
        if f.endswith("engine/check.py"):
            continue  # 検出用のパターンそのものが書いてあるため
        with open(f, encoding="utf-8", errors="ignore") as fh:
            for i, line in enumerate(fh, 1):
                for pat, what in SECRET_PATTERNS:
                    m = re.search(pat, line)
                    if m:
                        errors.append(f"{rel(f)}:{i}: 公開NG？（{what}）: {m.group(0)[:40]}")
                for w in words:
                    if w in line:
                        errors.append(f"{rel(f)}:{i}: 公開NG（.private-words の言葉）: {w}")

def rel(f):
    return os.path.relpath(f, ROOT)

def scan_separation(note_dir, errors):
    """ノート側（本文・figs.py）に見た目（CSS）を書かない。見た目は theme/、部品は engine/figkit.py に置く"""
    targets = glob.glob(os.path.join(note_dir, "content", "*.txt")) + glob.glob(os.path.join(note_dir, "figs.py"))
    for f in targets:
        with open(f, encoding="utf-8") as fh:
            for i, line in enumerate(fh, 1):
                for pat, what in ((r"style\s*=", "style="), (r"<style", "<style>"), (r"var\(--", "var(--…)")):
                    if re.search(pat, line):
                        errors.append(f"{rel(f)}:{i}: ノート側に見た目の指定（{what}）がある。theme/blocks.css のクラスか engine/figkit.py の部品を使う")

def read_lines(note_dir):
    lines = []
    for f in sorted(glob.glob(os.path.join(note_dir, "content", "*.txt"))):
        with open(f, encoding="utf-8") as fh:
            lines += [(rel(f), i, l.rstrip("\n")) for i, l in enumerate(fh, 1)]
    return lines

def collect_secs(lines, errors):
    """章の番号と、章ごとの小見出しのアンカー名を集める"""
    chapters, secs, cur = set(), {}, None
    for f, i, l in lines:
        m = re.match(r"@ch\s+([^|]+)\|", l.strip())
        if m:
            cid = m.group(1).strip()
            if cid in chapters:
                errors.append(f"{f}:{i}: 章の番号 {cid} が2回ある")
            chapters.add(cid); cur = cid; secs.setdefault(cid, set())
        elif re.match(r"@board\s", l.strip()):
            cur = None
        elif l.strip().startswith("##") and cur:
            sl = sec_slug(l.strip()[2:])
            if sl in secs[cur]:
                errors.append(f"{f}:{i}: {cur} に同じ小見出し「{sl}」が2つある（リンク先が決まらない）")
            secs[cur].add(sl)
    return chapters, secs

def check_note(note_dir, errors, warns):
    name = rel(note_dir)
    try:
        with open(os.path.join(note_dir, "note.json"), encoding="utf-8") as fh:
            cfg = json.load(fh)
    except Exception as e:
        errors.append(f"{name}/note.json: 読めない（{e}）"); return
    if not cfg.get("title"):
        errors.append(f"{name}/note.json: title がない")
    if cfg.get("type") not in TYPES:
        errors.append(f"{name}/note.json: type は 整理型 か 理解型")
    for k in set(cfg) - NOTE_KEYS:
        warns.append(f"{name}/note.json: 知らない項目 \"{k}\"（使える項目：{', '.join(sorted(NOTE_KEYS))}）")
    files = sorted(glob.glob(os.path.join(note_dir, "content", "*.txt")))
    if not files:
        errors.append(f"{name}: content/*.txt がない"); return
    lines = read_lines(note_dir)
    figs = set()
    chapters, secs = collect_secs(lines, errors)

    def check_link(f, i, spec):
        note, rest = split_note(spec)
        chs, ss, out = chapters, secs, errors
        if note:
            # 別のノートへのリンク：そのノートの章・小見出しで確かめる。
            # 相手のノートの書き直しでこちらのビルドが止まらないよう、ずれは「注意」にする（飛び先はページの先頭になる）
            out = warns
            other = os.path.join(ROOT, "notes", note)
            if not glob.glob(os.path.join(other, "content", "*.txt")):
                warns.append(f"{f}:{i}: {{{{{spec}}}}} のノート notes/{note} がない"); return
            chs, ss = collect_secs(read_lines(other), [])
        cid, _, h = rest.partition("#")
        cid = cid.strip()
        if cid not in chs:
            out.append(f"{f}:{i}: {{{{{spec}}}}} の章がない")
        elif h.strip() and sec_slug(h) not in ss.get(cid, set()):
            out.append(f"{f}:{i}: {{{{{spec}}}}}：{cid} に小見出し「{sec_slug(h)}」がない")
    if os.path.exists(os.path.join(note_dir, "figs.py")):
        with open(os.path.join(note_dir, "figs.py"), encoding="utf-8") as fh:
            figs = set(re.findall(r"^def ([A-Za-z]\w*)\(", fh.read(), re.M))
    depth, opened, in_code, in_html = 0, [], False, False
    for f, i, l in lines:
        s = l.strip()
        if s.startswith("```"):
            in_code = not in_code; continue
        if in_code:
            continue
        if in_html and s != "@end":
            continue
        m = re.match(r"@(\w+!?)", s)
        if m:
            tag = m.group(1)
            if tag in BLOCKS:
                depth += 1; opened.append((f, i, tag)); in_html = tag == "html"
                if tag == "box":
                    tone = s[4:].strip().split(" ")[0] if s[4:].strip() else ""
                    if tone not in BOX_TONES:
                        errors.append(f"{f}:{i}: @box の種類は {' / '.join(sorted(BOX_TONES))}（「{tone}」になっている）")
            elif tag == "end":
                if depth == 0:
                    errors.append(f"{f}:{i}: 対応する @xxx がない @end")
                else:
                    depth -= 1; opened.pop(); in_html = False
            elif tag not in SINGLE:
                errors.append(f"{f}:{i}: 知らない記法 @{tag}（書き間違い？ 一覧は README）")
            if tag in ("fig", "fig!"):
                fname = s.split(None, 1)[1].split("|")[0].strip() if len(s.split(None, 1)) > 1 else ""
                if fname not in figs:
                    errors.append(f"{f}:{i}: @fig {fname} が figs.py にない")
            if tag == "pair":
                cid = (s[6:].split("|") + [""] * 5)[4].strip()
                if cid and cid not in chapters:
                    errors.append(f"{f}:{i}: @pair の章 {cid} がない")
        for spec in XREF.findall(s):
            check_link(f, i, spec)
        if re.match(r"@card\b", s) and "|" in s:
            check_link(f, i, s.split("|", 1)[1].strip())
        if opened and opened[-1][2] == "routes" and not s.startswith("@"):
            for st in (s.split("|") + ["", "", ""])[2].split(","):
                cid = st.strip().split(" ")[0]
                if cid and cid not in chapters:
                    errors.append(f"{f}:{i}: 路線図の駅 {cid} の章がない")
        body = re.sub(r"\\\$", "", s)
        if s.count("**") % 2:
            warns.append(f"{f}:{i}: ** の数が奇数（太字の閉じ忘れ？）")
        if not s.startswith("$$") and body.count("$") % 2:
            warns.append(f"{f}:{i}: $ の数が奇数（数式の閉じ忘れ？）")
    for f, i, tag in opened:
        errors.append(f"{f}:{i}: @{tag} が @end で閉じられていない")

def run(note_dirs):
    errors, warns = [], []
    for d in note_dirs:
        check_note(d, errors, warns)
        scan_separation(d, errors)
    scan_privacy(errors)
    for w in warns:
        print("  注意:", w)
    for e in errors:
        print("  エラー:", e)
    return errors, warns
