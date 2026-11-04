# -*- coding: utf-8 -*-
"""応用情報直前対策の図。部品は engine/figkit.py（全ノート共通）。ここには中身（文字・数字・並び）だけを書く"""
from figkit import *  # noqa: F401,F403

# ───────────────────────── S1 鍵 ─────────────────────────
def keys():
    return (chain("暗号化（隠す）＝受信者の鍵", [("送信者", "暗号化する", "受信者の公開鍵"), ("受信者", "復号する", "受信者の秘密鍵")], "link")
            + chain("デジタル署名（証明する）＝送信者の鍵", [("送信者", "ハッシュ値に署名", "送信者の秘密鍵"), ("受信者", "署名を検証", "送信者の公開鍵")])
            + chain("証明書（公開鍵の身分証）＝CAの鍵", [("認証局（CA）", "証明書に署名", "CAの秘密鍵"), ("利用者", "証明書を検証", "CAの公開鍵")]))

def signenc():
    return chain("", [("送信者・①", "署名を付ける", "送信者の秘密鍵"), ("送信者・②", "まとめて暗号化", "受信者の公開鍵"),
                      ("受信者・③", "復号する", "受信者の秘密鍵"), ("受信者・④", "署名を検証", "送信者の公開鍵")])

# ───────────────────────── N1 送り出す順 ─────────────────────────
def sendorder():
    return (hrow(tile("MAC", "2層・隣の機器", "o s"), tile("IP", "3層・どの端末", "s"), tile("TCP", "4層・どのアプリ（ポート）", "s"), tile("データ", "本文", "s"))
            + ends("← 先頭（一番外の封筒）から送り出す", "後ろ →", "o"))

# ───────────────────────── H1 仮想化・クラウド ─────────────────────────
def virt():
    def col(title, layers, note):
        return column(title, [tile(name, tone="s o" if hot else "s") for name, hot in layers], sub=note, center=True)
    return columns(col("ホストOS型", [("アプリ", 0), ("ゲストOS", 0), ("仮想化ソフト", 1), ("ホストOS", 0), ("ハード", 0)], "OSが2重で遅い（VirtualBox）"),
                   col("ハイパーバイザ型", [("アプリ", 0), ("ゲストOS", 0), ("ハイパーバイザ", 1), ("ハード", 0)], "ホストOSなし・速い（ESXi・KVM）"),
                   col("コンテナ型", [("アプリ", 0), ("コンテナ", 1), ("コンテナエンジン", 0), ("ホストOS", 0), ("ハード", 0)], "ゲストOSなし・一番軽い（Docker）"))

def cloud():
    layers = ("アプリ", "ミドルウェア", "OS", "サーバ・NW")
    def col(title, mine, note):
        return column(title, [tile(name, tone="s o" if k < mine else "s") for k, name in enumerate(layers)], sub=note, center=True)
    return columns(col("オンプレ", 4, "全部自分"), col("IaaS", 3, "空っぽの部屋"), col("PaaS", 1, "家具付きの部屋"), col("SaaS", 0, "ホテル"))

# ───────────────────────── H3 メモリ ─────────────────────────
def memtree():
    return tree(("半導体メモリ", "電源を切ったら消える？", 0, [
        ("RAM", "消える（揮発性）＝作業机", 0, [
            ("DRAM", "コンデンサに電気をためる。漏れるので【リフレッシュ必要】。安い・大容量 → 主記憶", 0, []),
            ("SRAM", "フリップフロップで記憶。【リフレッシュ不要】。速い・高い・小容量 → キャッシュ", 0, [])]),
        ("ROM", "消えない（不揮発性）＝本棚", 0, [
            ("マスクROM", "工場で書き込み。書き換え【不可】", 0, []),
            ("PROM", "あとから書き込める", 0, [
                ("ワンタイムPROM", "1回だけ", 0, []),
                ("UV-EPROM", "紫外線で消す（基板から外す）", 1, []),
                ("EEPROM", "電気で消す（バイト単位）", 1, []),
                ("フラッシュメモリ", "電気で消す（ブロック単位）→ USBメモリ・SSD", 1, [])])])]))

def parity():
    """垂直水平パリティ：1ビットなら交差点が1つに決まる／長方形の4ビットは全部すり抜ける"""
    def grid(ox, title, errs, flag_rows, flag_cols, note):
        c, n = 22, 4
        b = text(ox + n * c / 2, 14, title, "t-s f-ink hand", "middle")
        for r in range(n):
            for k in range(n):
                x, y = ox + k * c, 24 + r * c
                bad = (r, k) in errs
                b += f'<rect x="{x}" y="{y}" width="{c - 2}" height="{c - 2}" rx="3" class="{"f-ou" if bad else "f-sheet3"} st-line"/>'
                if bad:
                    b += text(x + (c - 2) / 2, y + 15, "×", "t-s f-bg", "middle")
        for r in range(n):
            on = r in flag_rows
            b += text(ox + n * c + 8, 24 + r * c + 15, "!" if on else "ok", "t-s f-ou" if on else "t-s f-ink3")
        for k in range(n):
            on = k in flag_cols
            b += text(ox + k * c + (c - 2) / 2, 24 + n * c + 14, "!" if on else "ok", "t-s f-ou" if on else "t-s f-ink3", "middle")
        b += text(ox + n * c / 2, 24 + n * c + 34, note, "t-s f-ink2", "middle")
        return b
    b = grid(40, "1ビットの誤り", {(1, 2)}, {1}, {2}, "交差点が1つ → 訂正できる")
    b += grid(210, "長方形の4ビット", {(0, 0), (0, 2), (2, 0), (2, 2)}, set(), set(), "全部 ok に戻る → 見逃す")
    return svg(360, 176, b, "垂直水平パリティ")

# ───────────────────────── H4 周期タスク ─────────────────────────
def sched():
    """優先度の高いAが割り込む。Bは隙間だけで進む。Bの完了 ≦ Bの周期 なら間に合う"""
    def case(oy, title, a_run, a_per, b_run, b_per, n):
        c = 26
        b = text(10, oy + 12, title, "t-s f-ink hand")
        a = [((t % a_per) < a_run) for t in range(n)]
        left, done = b_run, None
        bcells = []
        for t in range(n):
            if not a[t] and left > 0:
                bcells.append(True); left -= 1
                if left == 0:
                    done = t + 1
            else:
                bcells.append(False)
        for row, (lab, cells, cls) in enumerate((("A", a, "f-k"), ("B", bcells, "f-ou"))):
            y = oy + 22 + row * (c + 4)
            b += text(10, y + 17, lab, "t-m f-ink")
            for t in range(n):
                b += f'<rect x="{30 + t * c}" y="{y}" width="{c - 3}" height="{c - 3}" rx="3" class="{cls if cells[t] else "f-sheet3"} st-line"/>'
        y2 = oy + 22 + 2 * (c + 4)
        for t in range(n + 1):
            b += text(30 + t * c - 1.5, y2 + 12, str(t), "t-s f-ink3 mono", "middle")
        xd = 30 + b_per * c - 1.5
        b += f'<line x1="{xd}" y1="{oy + 18}" x2="{xd}" y2="{y2}" class="s-dash"/>' + text(xd + 3, oy + 12, f"Bの周期 {b_per}", "t-s f-warn")
        ok = done is not None and done <= b_per
        b += text(10, y2 + 30, f"Bは {done} で完了 → {'間に合う' if ok else '間に合わない'}", "t-s f-ou" if ok else "t-s f-warn")
        return b
    b = case(0, "A：2ずつ・周期4 ／ B：3・周期8", 2, 4, 3, 8, 10)
    b += case(118, "A：3ずつ・周期6 ／ B：4・周期9", 3, 6, 4, 9, 11)
    return svg(330, 236, b, "周期タスクのスケジュール")

# ───────────────────────── M2 保守 ─────────────────────────
def hoshu():
    return tree(("バグ（問題）の話？", "まず「訂正」か「改良」かを決める", 0, [
        ("はい → 訂正", "悪いところを直す", 0, [
            ("もう起きた → 是正保守", "報告された問題を直す（ログインできない）", 1, []),
            ("まだ起きていない → 予防保守", "起きる前に先に直す（来月落ちそう）", 1, [])]),
        ("いいえ → 改良", "問題はないが手を入れる", 0, [
            ("外が変わった → 適応保守", "OS・法律・機器の変化に合わせる（iOSの更新）", 1, []),
            ("自分から良くする → 完全化保守", "性能向上・機能追加・文書の改善（仕様書をコードに合わせる）", 1, [])])]))

# ───────────────────────── 順番の図 ─────────────────────────
def riskflow():
    return chain("", [("見つける", "リスク特定", "資産・価値・脅威"), ("測る", "リスク分析", "起こりやすさ・大きさ"),
                      ("決める", "リスク評価", "基準と比べて優先順位"), ("やる", "リスク対応", "回避・低減・移転・保有")])

def bcpflow():
    return chain("", [("動く", "BCP発動", "初期対応して発動"), ("とりあえず", "業務再開", "代替手段で再開"),
                      ("広げる", "業務回復", "再開する範囲を広げる"), ("元に戻す", "全面復旧", "通常運用へ")])

def auditflow():
    return chain("", [("決める", "監査計画", "何をいつ調べる"), ("ざっと見る", "予備調査", "全体をつかむ"),
                      ("証拠を集める", "本調査", "＝監査手続"), ("伝える", "監査報告", "結論・指摘・改善勧告"), ("確かめる", "フォローアップ", "直ったか")])

def procure():
    return chain("", [("聞く", "RFI", "どんな技術・実績が？"), ("頼む", "RFP", "提案書と見積りを"),
                      ("決める", "契約", "業者を選んで契約"), ("変える", "RFC", "契約後の変更依頼")])

def vrflow():
    return chain("", [("追う", "トラッキング", "センサーで人の動き"), ("動かす", "モデリング変換", "物理法則・時間経過"),
                      ("合わせる", "幾何学的レジストレーション", "現実と仮想の座標"), ("描く", "レンダリング", "画面の画像に")])

# ───────────────────────── T4 知的財産 ─────────────────────────
def ipr():
    return columns(column("産業財産権", [tile("特許権", "発明・出願から20年", "o"), tile("実用新案権", "形・構造の工夫・10年", "o"),
                                         tile("意匠権", "デザイン・25年", "o"), tile("商標権", "ロゴ・名前・10年（更新できる）", "o")],
                          note="特許庁に出願・登録が必要"),
                   column("著作権", [tile("著作権", "表現（文章・音楽・プログラム）・死後70年")], note="登録不要。作った瞬間に発生"),
                   column("その他", [tile("営業秘密", "不正競争防止法"), tile("回路配置利用権", "半導体の回路"), tile("育成者権", "植物の新品種")],
                          note="法律がそれぞれ別"))

# ───────────────────────── K1 EVM ─────────────────────────
def evm():
    """壁10枚・予算10万円の例：今日までに PV 5万、EV 3万、AC 4万"""
    X0, X1, Y0, Y1 = 40, 300, 168, 18
    fx = lambda t: X0 + (X1 - X0) * t
    fy = lambda v: Y0 - (Y0 - Y1) * v / 100
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X1 + 8}" y2="{Y0}" class="s-ax"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1 - 6}" class="s-ax"/>'
    b += f'<line x1="{X0}" y1="{fy(100):.1f}" x2="{X1}" y2="{fy(100):.1f}" class="s-grid"/>' + text(X0 - 4, fy(100) + 4, "BAC", "t-s f-ink3", "end")
    b += f'<line x1="{fx(0)}" y1="{fy(0)}" x2="{fx(1)}" y2="{fy(100):.1f}" class="s-2"/>' + text(fx(1) - 2, fy(100) - 6, "PV（予定）", "t-s f-k", "end")
    b += f'<line x1="{fx(0)}" y1="{fy(0)}" x2="{fx(.5)}" y2="{fy(40):.1f}" class="s-warn"/>'
    b += f'<line x1="{fx(0)}" y1="{fy(0)}" x2="{fx(.5)}" y2="{fy(30):.1f}" class="s-main"/>'
    b += f'<line x1="{fx(.5)}" y1="{Y1 + 30}" x2="{fx(.5)}" y2="{Y0}" class="s-dash"/>' + text(fx(.5), Y0 + 14, "いま", "t-s f-ink2", "middle")
    for v, s, cls in ((50, "PV 5万 予定", "f-k"), (40, "AC 4万 使ったお金", "f-warn"), (30, "EV 3万 できた分", "f-ou")):
        b += f'<circle cx="{fx(.5):.1f}" cy="{fy(v):.1f}" r="3.5" class="{cls}"/>' + text(fx(.5) + 8, fy(v) + 4, s, f"t-s {cls}")
    b += text(fx(.5) - 8, fy(62), "コスト：EV と AC", "t-s f-ink2", "end")
    b += text(fx(.5) - 8, fy(74), "進み：EV と PV", "t-s f-ink2", "end")
    b += text(fx(.5) - 8, fy(86), "比べる相手は必ず EV", "t-s f-ou hand", "end")
    return svg(330, 186, b, "EVM")
