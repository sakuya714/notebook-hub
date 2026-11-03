"""見た目のチェック（全ノート）。docs/ を作ってから実行する。

  uv run --with playwright python -I tools/qa.py            # はみ出し・段組みの偏り・リンク切れ
  uv run --with playwright python -I tools/qa.py --shots 出力先  # ＋章・ボードごとのスクショ（1200px・ダーク）

見るもの：
- はみ出し：要素の右端が章の枠から出ていないか／overflow で中身が切れていないか（1400〜390px の6通り）
- 段組みの偏り：2段組の左右の下端が 140px 以上（かつ長い方の列の8%以上）ずれていないか（1400・1200px。直前カードのボードは章の順を優先するので除く）
- リンク切れ：ページ内の href="#…" の飛び先があるか
直し方の目安：偏りは部品の順番を入れ替える（左右の高さの合計が近くなる順に）か、長いグループを分ける。
"""
import sys, os, re, html, glob, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SHOTS = sys.argv[sys.argv.index("--shots") + 1] if "--shots" in sys.argv else None

MEASURE = r"""
() => {
  const res = {overflow: [], imbalance: [], hscroll: document.scrollingElement.scrollWidth > innerWidth + 1};
  const scrollable = el => { for (let e = el.parentElement; e; e = e.parentElement) { const o = getComputedStyle(e).overflowX; if (o === 'auto' || o === 'scroll') return true; } return false; };
  document.querySelectorAll('section.sheet, section.board').forEach(sec => {
    const sr = sec.getBoundingClientRect();
    sec.querySelectorAll('*').forEach(el => {
      if (el.closest('mjx-assistive-mml')) return;
      const r = el.getBoundingClientRect();
      if (!r.width) return;
      if (r.right > sr.right + 2 && !scrollable(el) && ![...el.children].some(c => c.getBoundingClientRect().right > sr.right + 2))
        res.overflow.push(`${sec.id} はみ出し ${el.tagName}.${el.className}: ${el.textContent.trim().slice(0, 30)}`);
      const o = getComputedStyle(el).overflowX;
      if (o !== 'visible' && el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0 && !el.classList.contains('tbw') && !el.classList.contains('fig') && !el.classList.contains('eq'))
        res.overflow.push(`${sec.id} 切れ ${el.tagName}.${el.className} ${el.scrollWidth}>${el.clientWidth}: ${el.textContent.trim().slice(0, 30)}`);
    });
    sec.querySelectorAll('.cols').forEach(c => {
      if (c.closest('.tcard') || c.querySelector(':scope > .tcard')) return;  // カードの並びは章の順を優先（下端のずれは許す）
      const cr = c.getBoundingClientRect(), mid = cr.left + cr.width / 2;
      let l = cr.top, r = cr.top, nr = 0;
      [...c.children].forEach(k => { const b = k.getBoundingClientRect(); if (!b.height) return; if (b.left < mid) l = Math.max(l, b.bottom); else { r = Math.max(r, b.bottom); nr++; } });
      const p = c.previousElementSibling, h = p && p.classList.contains('sec') ? p.textContent : '(節の先頭)';
      if (nr && Math.abs(l - r) > 140 && Math.abs(l - r) > 0.08 * (Math.max(l, r) - cr.top)) res.imbalance.push(`${sec.id}「${h.slice(0, 20)}」 左${Math.round(l - cr.top)} 右${Math.round(r - cr.top)}`);
    });
  });
  return res;
}"""

def broken_links(path):
    s = open(path, encoding="utf-8").read()
    ids = {html.unescape(x) for x in re.findall(r'\sid="([^"]+)"', s)}
    return sorted({html.unescape(h) for h in re.findall(r'href="#([^"]+)"', s)} - ids - {"top"})

async def main():
    pages = [p for p in glob.glob(os.path.join(DOCS, "**", "index.html"), recursive=True) if os.path.dirname(p) != DOCS]
    bad = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch(channel="chrome")
        for path in sorted(pages):
            name = os.path.relpath(os.path.dirname(path), DOCS)
            print(f"■ {name}")
            links = broken_links(path)
            if links: print("  リンク切れ:", links[:10]); bad += len(links)
            for w in (1400, 1200, 1000, 900, 820, 390):
                ctx = await b.new_context(viewport={"width": w, "height": 900}, color_scheme="dark", reduced_motion="reduce")
                pg = await ctx.new_page()
                await pg.goto("file://" + path); await pg.wait_for_timeout(1500)
                m = await pg.evaluate(MEASURE)
                show = m["overflow"] + (m["imbalance"] if w in (1400, 1200) else [])
                bad += len(m["overflow"]) + int(m["hscroll"])
                print(f"  {w}px 横スクロール{'あり' if m['hscroll'] else 'なし'}・はみ出し{len(m['overflow'])}・偏り{len(m['imbalance'])}")
                for x in show[:20]: print("    ", x)
                if SHOTS and w == 1200:
                    os.makedirs(SHOTS, exist_ok=True)
                    await pg.add_style_tag(content=".top{position:static !important}")
                    for sid in await pg.evaluate("() => [...document.querySelectorAll('section.sheet, section.board')].map(s => s.id)"):
                        await (await pg.query_selector(f"#{sid}")).screenshot(path=os.path.join(SHOTS, f"{name.replace('/', '_')}_{sid}.png"))
                await ctx.close()
        await b.close()
    print("問題なし" if not bad else f"直すもの {bad} 件（偏りは目安なので数に入れていない）")

asyncio.run(main())
