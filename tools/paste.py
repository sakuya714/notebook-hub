"""貼られた解説の漏れチェック：解説の太字（**…**）の語が、直前カード（@card）に出てくるかを調べる。

  python3 tools/paste.py notes/learning/応用情報技術者 解説1.md 解説2.md …

貼られた解説はリポジトリの外（作業用のフォルダ）に1件1ファイルで保存して渡す。公開しない。
空白・句読点・カッコ・「・」などを無視して探すので、少しの言い回しの違いは同じとみなす。
出てきた語は目で確かめ、意味ごと抜けていたらカードに足す（言い回しが違うだけなら直さなくてよい）。
"""
import os, re, glob, sys

SKIP = r"[\s、，,・･（）()「」『』【】：:。．.！!？?＝=→←⇄〜~\-／/｜|]+"


def norm(t):
    return re.sub(SKIP, "", t.replace("**", "")).lower()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    note, pastes = sys.argv[1], sys.argv[2:]
    text = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(note, "content", "*.txt"))))
    cards = norm("\n".join(re.findall(r"@card .*?\n@end", text, re.S)))
    bad = 0
    for p in pastes:
        terms = list(dict.fromkeys(re.findall(r"\*\*(.+?)\*\*", open(p, encoding="utf-8").read())))
        miss = [t for t in terms if norm(t) and norm(t) not in cards]
        bad += len(miss)
        print(f"{os.path.basename(p)}：太字 {len(terms)} 語", "→ カードに無い：" + "、".join(miss) if miss else "→ 全部カードにある")
    print("問題なし" if not bad else f"カードに無い語 {bad} 個（言い回し違いか、本当の抜けかを目で確かめる）")


main()
