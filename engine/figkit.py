# -*- coding: utf-8 -*-
"""図の部品（全ノート共通）。各ノートの figs.py は `from figkit import *` して、図を返す関数だけを書く。

図の関数は「SVG か HTML の文字列」を返す。色は theme の CSS クラス（s-ax, f-ou など）で付けるので、
ここにもノート側にも色の値は書かない（ダーク／ライトの切替で自動的に変わる）。
"""
import math  # noqa: F401  figs.py から使えるように

__all__ = ["math", "svg", "text", "path", "arrow_defs", "fig",
           "tile", "blank", "grid", "stack", "column", "columns", "rows", "ends", "mono", "bits", "cellcol", "hrow", "chain", "vpairs", "timing"]

def svg(w, h, body, label=""):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

def text(x, y, s, cls="t-s f-ink2", anchor="start", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}" {extra}>{s}</text>'

def path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def arrow_defs(idn="ah"):
    """矢印の先端（id=idn は灰色、idn+'o' はアクセント色）。marker-end="url(#ah)" のように使う"""
    return (f'<defs><marker id="{idn}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" class="f-ink3"/></marker>'
            f'<marker id="{idn}o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" class="f-ou"/></marker></defs>')

def fig(inner, title="", cap="", cls=""):
    """図の枠（タイトル＋本体＋キャプション）。本文の @fig からも使う"""
    t = f'<div class="ttl">{title}</div>' if title else ""
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="fig {cls}">{t}{inner}{c}</div>'


# ───────────── HTML の図の部品（見た目は theme/blocks.css の .fk-*）─────────────
# ノートの figs.py はこれを組み合わせて「中身（文字・数字・並び）」だけを書く。style= や色はノート側に書かない。

def tile(main, sub="", tone=""):
    """箱1つ。tone："" ふつう／"o" アクセントの背景／"oo" アクセントの背景＋枠（中心を目立たせる）／"s" 小さい（"o s" のように組み合わせ可）"""
    sub_h = f"<span>{sub}</span>" if sub else ""
    return f'<div class="fk-tile {tone}"><b>{main}</b>{sub_h}</div>'

def blank():
    """grid の空きマス"""
    return "<div></div>"

def grid(cells, cols=3, center_wide=False):
    """マス目に並べる（cols 列）。center_wide=True なら3列の真ん中を少し広く（ファイブフォースのような中心のある図）"""
    return f'<div class="fk-grid c{cols}{" cw" if center_wide else ""}">{"".join(cells)}</div>'

def column(head="", items=(), note="", sub="", center=False):
    """縦の1列：見出し・補足・中身（箱など）・下の注"""
    h = f'<b class="h">{head}</b>' if head else ""
    n = f'<span class="n">{note}</span>' if note else ""
    b = f'<span class="s">{sub}</span>' if sub else ""
    return f'<div class="fk-col{" c" if center else ""}">{h}{n}{"".join(items)}{b}</div>'

def columns(*cols):
    """縦の列を横に並べる（狭い画面では折り返す）"""
    return f'<div class="fk-cols">{"".join(cols)}</div>'

def rows(items):
    """横長の段を積む：(見出し, 中身, 右端, 左にアクセントの線, 右端をアクセント色)"""
    h = ""
    for label, body, side, hot, side_hot in items:
        h += f'<div class="r{" o" if hot else ""}"><b>{label}</b><span>{body}</span><i class="{"o" if side_hot else ""}">{side}</i></div>'
    return f'<div class="fk-rows">{h}</div>'

def ends(left, right, left_tone=""):
    """左右の端に置く短い説明（↑速い ／ 遅い↓ など）"""
    return f'<div class="fk-ends"><span class="{left_tone}">{left}</span><span>{right}</span></div>'

def mono(html):
    """計算の途中を等幅で"""
    return f'<div class="fk-mono">{html}</div>'

def bits(groups):
    """ビット列：[(文字列, アクセントか)]。文字列の中の空白は小さいすき間、グループの間は少し広いすき間"""
    out = []
    for k, (chars, on) in enumerate(groups):
        if k:
            out.append('<span class="gg"></span>')
        out += ['<span class="g"></span>' if c == " " else f'<span class="b{" o" if on else ""}">{c}</span>' for c in chars]
    return f'<div class="fk-bits">{"".join(out)}</div>'

def cellcol(name, values, hot=()):
    """小さいマスの縦1列（ディスクなど）。hot に入っている値はアクセント色"""
    cs = "".join(f'<div class="fk-cell{" o" if v in hot else ""}">{v}</div>' for v in values)
    return f'<div class="fk-cellcol"><i>{name}</i>{cs}</div>'

def hrow(*items):
    """部品を横に詰めて並べる"""
    return f'<div class="fk-hrow">{"".join(items)}</div>'

def chain(title, steps, tone="o"):
    """→でつないだ箱の列：steps＝[(小さい字, 太字, 色付きの字)]。tone："o" アクセント／"link" 青緑"""
    s = ""
    for k, (small, main, key) in enumerate(steps):
        if k:
            s += "<i>→</i>"
        s += f'<div class="bx"><small>{small}</small><b>{main}</b><em>{key}</em></div>'
    return f'<div class="fk-chain-t">{title}</div><div class="fk-chain {tone}">{s}</div>'

def vpairs(left, right, head=("", ""), bottom=""):
    """V字（左右の対応）：下に行くほど内側に寄る。left[i] と right[i] が点線でつながる。right の最初だけ灰色"""
    hd = f'<div class="hd"><span>{head[0]}</span><span>{head[1]}</span></div>' if any(head) else ""
    rs = "".join(f'<div class="r l{i}{" k" if i == 0 else ""}"><span>{a}</span><span class="ln"></span><span>{b}</span></div>'
                 for i, (a, b) in enumerate(zip(left, right)))
    bt = f'<div class="bt">{bottom}</div>' if bottom else ""
    return f'<div class="fk-v">{hd}<div class="rs">{rs}{bt}</div></div>'

def timing(row_labels, n_cols, spans, hot_row=0):
    """時間割の表（パイプラインなど）：spans[i]＝(始まりの列, [各マスの字])。hot_row の行はアクセント色"""
    head = "<tr><th></th>" + "".join(f"<th>{j + 1}</th>" for j in range(n_cols)) + "</tr>"
    body = ""
    for i, (lab, (start, marks)) in enumerate(zip(row_labels, spans)):
        cells = "".join(f'<td class="on">{marks[j - start]}</td>' if start <= j < start + len(marks) else "<td></td>" for j in range(n_cols))
        body += f'<tr class="{"o" if i == hot_row else ""}"><th>{lab}</th>{cells}</tr>'
    return f'<table class="fk-timing">{head}{body}</table>'

def stack(items):
    """本文の @stack と同じ見た目の段：(見出し, 右の補足, アクセントの線)"""
    return '<div class="stack">' + "".join(f'<div class="r{" o" if hot else ""}"><b>{a}</b><span>{b}</span></div>' for a, b, hot in items) + "</div>"
