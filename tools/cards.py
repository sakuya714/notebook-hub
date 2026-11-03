"""直前カード（@card）の漏れチェック：カードが飛び先にしている節の用語のうち、カードに出てこないものを並べる。

  python3 tools/cards.py

出てきた語のうち、そのカードのテーマに関係するものはカードにも書く（本文の方が詳しい状態にしない）。
テーマが違う語（同じ節にある別の話）はそのままでよい。
"""
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from markup import sec_slug

for note in sorted(glob.glob(os.path.join(ROOT, "notes", "**", "note.json"), recursive=True)):
    d = os.path.join(os.path.dirname(note), "content")
    files = sorted(glob.glob(os.path.join(d, "*.txt")))
    secs, ch, sec, cards = {}, None, None, []
    for f in files:
        text = open(f, encoding="utf-8").read()
        cards += re.findall(r"@card (.+?) \| (\S+?)(?:#(.+?))?\n(.*?)\n@end", text, re.S)
        for l in text.split("\n"):
            s = l.strip()
            if s.startswith("@ch "): ch, sec = s.split("|")[0][4:].strip(), None
            elif s.startswith("@board"): ch = sec = None
            elif s.startswith("## ") and ch: sec = sec_slug(s[3:])
            elif ch and sec:
                m = re.match(r"^[-+]\*?\s+(.*?)\s—\s", s) or re.match(r"^\+?\|\s*([^|]+?)\s*\|", s)
                if m and not s.startswith("| |"):
                    secs.setdefault((ch, sec), []).append(re.sub(r"\*\*", "", m.group(1)))
    if not cards:
        continue
    print("■", os.path.relpath(os.path.dirname(note), os.path.join(ROOT, "notes")))
    for title, cid, h, body in cards:
        plain = re.sub(r"\*\*", "", body + title)
        terms = secs.get((cid, sec_slug(h)) if h else (cid, None), [])
        miss = [x for x in terms if re.split(r"[（(／ ]", x)[0] not in plain]
        if miss:
            print(f"  {title}（{cid}#{h}）カードに無い語: {'、'.join(miss)}")
