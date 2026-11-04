# -*- coding: utf-8 -*-
"""応用情報まとめの図。部品は engine/figkit.py（全ノート共通）"""
from figkit import *  # noqa: F401,F403

def mm1():
    X0, X1, Y0, Y1 = 44, 340, 176, 18
    fx = lambda r: X0 + (X1 - X0) * r
    fy = lambda v: Y0 - (Y0 - Y1) * v / 10
    pts = []
    r = 0.0
    while r <= 0.9091:
        pts.append((fx(r), fy(r / (1 - r))))
        r += 0.005
    b = arrow_defs("mm")
    b += f'<line x1="{X0}" y1="{Y0}" x2="{X1+6}" y2="{Y0}" class="s-ax"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-6}" class="s-ax"/>'
    for v in (1, 4, 9):
        b += f'<line x1="{X0}" y1="{fy(v):.1f}" x2="{X1}" y2="{fy(v):.1f}" class="s-grid"/>'
        b += text(X0 - 6, fy(v) + 4, f"{v}倍", "t-s f-ink3", "end")
    b += f'<path d="{path(pts)}" class="s-main"/>'
    for rr, v in ((0.5, 1), (0.8, 4), (0.9, 9)):
        b += f'<line x1="{fx(rr):.1f}" y1="{Y0}" x2="{fx(rr):.1f}" y2="{fy(v):.1f}" class="s-dash"/>'
        b += f'<circle cx="{fx(rr):.1f}" cy="{fy(v):.1f}" r="3.5" class="f-ou"/>'
        b += text(fx(rr), Y0 + 14, f"ρ={rr}", "t-s f-ink2", "middle")
    b += text(fx(1.0), Y0 + 14, "1", "t-s f-ink3", "middle")
    b += text(X0 + 6, Y1 + 2, "待ち時間 ÷ サービス時間 ＝ ρ/(1−ρ)", "t-s f-ink2")
    b += text(fx(0.55), fy(6.5), "1に近づくと爆発", "t-s f-ou hand")
    return svg(360, 200, b, "M/M/1 待ち時間のグラフ")

def normal():
    X0, X1, Y0, Y1 = 20, 340, 150, 20
    mu, s = (X0 + X1) / 2, (X1 - X0) / 7.4
    f = lambda z: math.exp(-z * z / 2)
    pts = [(mu + z * s, Y0 - (Y0 - Y1) * f(z)) for z in [i / 20 for i in range(-74, 75)]]
    b = ""
    def band(k, cls):
        sub = [(mu + z * s, Y0 - (Y0 - Y1) * f(z)) for z in [i / 20 for i in range(-20 * k, 20 * k + 1)]]
        return f'<path d="{path(sub)} L{mu+k*s:.1f},{Y0} L{mu-k*s:.1f},{Y0} Z" class="{cls}" />'
    b += band(3, "f-oubg") + band(2, "f-oubg") + band(1, "f-oubg")
    b += f'<path d="{path(pts)}" class="s-main"/><line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" class="s-ax"/>'
    for k in (-3, -2, -1, 0, 1, 2, 3):
        x = mu + k * s
        b += f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{Y0+4}" class="s-ax"/>'
        lab = "μ" if k == 0 else (f"{'+' if k>0 else '−'}{abs(k)}σ")
        b += text(x, Y0 + 15, lab, "t-s f-ink3", "middle")
    for k, pct, yy in ((1, "68%", 172), (2, "95%", 186), (3, "99.7%", 200)):
        x1, x2 = mu - k * s, mu + k * s
        b += f'<line x1="{x1:.1f}" y1="{yy-4}" x2="{x2:.1f}" y2="{yy-4}" class="s-2"/>'
        b += text(mu, yy - 7, f"±{k}σ に {pct}", "t-s f-ink2", "middle")
    return svg(360, 206, b, "正規分布 68 95 99.7")

def hufftree():
    nodes = {"r": (180, 18, "100%"), "a": (110, 64, "a 50%"), "n1": (250, 64, "50%"), "b": (190, 110, "b 30%"),
             "n2": (310, 110, "20%"), "c": (270, 156, "c 10%"), "d": (350, 156, "d 10%")}
    edges = [("r", "a", "0"), ("r", "n1", "1"), ("n1", "b", "0"), ("n1", "n2", "1"), ("n2", "c", "0"), ("n2", "d", "1")]
    b = ""
    for p, c, bit in edges:
        x1, y1, _ = nodes[p]; x2, y2, _ = nodes[c]
        b += f'<line x1="{x1}" y1="{y1+8}" x2="{x2}" y2="{y2-10}" class="s-ax"/>'
        b += text((x1 + x2) / 2 + (-9 if bit == "0" else 6), (y1 + y2) / 2 + 2, bit, "t-s f-ou")
    for k, (x, y, s) in nodes.items():
        leaf = k in "abcd"
        b += f'<rect x="{x-24}" y="{y-10}" width="48" height="20" rx="10" class="{"f-sheet3" if leaf else "f-bg"} st-line"/>'
        b += text(x, y + 4, s, "t-s f-ink" if leaf else "t-s f-ink3", "middle")
    b += text(16, 140, "a=0  b=10", "t-m f-ink2 mono")
    b += text(16, 158, "c=110  d=111", "t-m f-ink2 mono")
    b += text(16, 176, "平均 1.7ビット", "t-m f-ou")
    return svg(380, 180, b, "ハフマン木")

# ───────────────────────── 01-2 ─────────────────────────
def traversal():
    pos = {1: (180, 20), 2: (110, 72), 3: (250, 72), 4: (70, 124), 5: (150, 124), 6: (290, 124)}
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
    b = ""
    for a, c in edges:
        b += f'<line x1="{pos[a][0]}" y1="{pos[a][1]}" x2="{pos[c][0]}" y2="{pos[c][1]}" class="s-ax"/>'
    for k, (x, y) in pos.items():
        b += f'<circle cx="{x}" cy="{y}" r="12" class="f-sheet3 st-line"/>' + text(x, y + 4, str(k), "t-m f-ink", "middle")
    rows = [("行きがけ 節→左→右", "1 2 4 5 3 6"), ("通りがけ 左→節→右", "4 2 5 1 3 6"), ("帰りがけ 左→右→節", "4 5 2 6 3 1"), ("幅優先（キュー）", "1 2 3 4 5 6")]
    for i, (n, s) in enumerate(rows):
        y = 160 + i * 17
        b += text(20, y, n, "t-s f-ink2") + text(340, y, s, "t-s f-ou mono", "end")
    return svg(360, 226, b, "2分木の走査")

# ───────────────────────── 02-1 ─────────────────────────
def pipeline():
    return timing([f"命令{i + 1}" for i in range(5)], 8, [(i, ["F", "D", "R", "E"]) for i in range(5)], hot_row=0)

def memhier():
    return (stack([("レジスタ", "CPUの中", 0), ("キャッシュ（SRAM）", "L1→L2→L3", 0), ("主記憶（DRAM）", "リフレッシュ要", 0), ("SSD（NANDフラッシュ）／HDD", "補助記憶", 0)])
            + ends("↑ 速い・小さい・高い", "遅い・大きい・安い ↓"))

def memtree():
    return tree(("半導体メモリ", "電源を切ったら消える？", 0, [
        ("RAM", "揮発性：電源OFFで消える＝作業机", 0, [
            ("DRAM", "コンデンサに電気をためる。漏れるので【リフレッシュ必要】。安い・大容量・遅め → 主記憶", 0, []),
            ("SRAM", "フリップフロップ回路で記憶。【リフレッシュ不要】。高い・小容量・速い → キャッシュ", 0, [])]),
        ("ROM", "不揮発性：電源OFFでも消えない＝本棚", 0, [
            ("マスクROM", "工場で書き込み。書き換え【不可】", 0, []),
            ("PROM", "後から書き込める", 0, [
                ("ワンタイムPROM", "1回だけ書ける", 0, []),
                ("UV-EPROM", "紫外線で消去（基板から外す）", 1, []),
                ("EEPROM", "電気で消去（1バイト単位）", 1, []),
                ("フラッシュメモリ", "電気で消去（ブロック単位）→ USBメモリ・SSD・SDカード", 1, [])])])]))

# ───────────────────────── 02-2 ─────────────────────────
def availability():
    # 直列は掛け算、並列は「全部止まる」を1から引く
    def box(x, y, v):
        return f'<rect x="{x}" y="{y}" width="44" height="22" rx="6" class="f-sheet3 st-line"/>' + text(x + 22, y + 15, v, "t-m f-ink mono", "middle")
    b = f'<line x1="0" y1="21" x2="14" y2="21" class="s-ax"/>' + box(14, 10, "0.9") + f'<line x1="58" y1="21" x2="76" y2="21" class="s-ax"/>' + box(76, 10, "0.8")
    b += f'<line x1="120" y1="21" x2="134" y2="21" class="s-ax"/>' + text(146, 25, "直列 ＝ 0.9×0.8 ＝ ", "t-m f-ink mono") + text(286, 25, "0.72", "t-m f-ou mono")
    b += f'<path d="M14,58 L14,94 M58,58 L58,94 M0,76 L14,76 M58,76 L72,76" class="s-ax"/>' + box(14, 47, "0.9") + box(14, 83, "0.8")
    b += text(86, 80, "並列 ＝ 1−(1−0.9)(1−0.8) ＝ ", "t-m f-ink mono") + text(296, 80, "0.98", "t-m f-ou mono")
    return svg(460, 110, b, "直列と並列の稼働率")

def raid():
    g0 = column("RAID0", [hrow(cellcol("A", ["1", "3", "5"]), cellcol("B", ["2", "4", "6"]))], sub="ストライピング<br>速い・冗長なし")
    g1 = column("RAID1", [hrow(cellcol("A", ["1", "2", "3"]), cellcol("B", ["1", "2", "3"]))], sub="ミラーリング<br>容量1/2・1台壊れてもOK")
    g5 = column("RAID5", [hrow(cellcol("A", ["1", "3", "P"], "P"), cellcol("B", ["2", "P", "5"], "P"), cellcol("C", ["P", "4", "6"], "P"))],
                sub="パリティ分散<br>1台までOK・容量(n−1)台分")
    return columns(g0, g1, g5)

def bathtub():
    X0, X1, Y0, Y1 = 30, 340, 140, 20
    pts = []
    for i in range(0, 301):
        t = i / 300
        v = 0.75 * math.exp(-t * 14) + 0.12 + 0.8 * max(0, t - 0.68) ** 2 * 9
        pts.append((X0 + (X1 - X0) * t, Y0 - (Y0 - Y1) * min(v, 1)))
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" class="s-ax"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-4}" class="s-ax"/>'
    b += f'<path d="{path(pts)}" class="s-main"/>'
    for t in (0.22, 0.7):
        x = X0 + (X1 - X0) * t
        b += f'<line x1="{x:.1f}" y1="{Y1}" x2="{x:.1f}" y2="{Y0}" class="s-dash"/>'
    for t, s1, s2 in ((0.11, "初期故障", "↓下がる"), (0.46, "偶発故障", "→一定"), (0.85, "摩耗故障", "↑上がる")):
        x = X0 + (X1 - X0) * t
        b += text(x, Y0 + 15, s1, "t-s f-ink2", "middle") + text(x, Y0 + 28, s2, "t-s f-ink3", "middle")
    b += text(X0 + 4, Y1 - 6, "故障率", "t-s f-ink3")
    b += text(40, 48, "エージング・", "t-s f-ou hand") + text(40, 62, "バーンインで潰す", "t-s f-ou hand")
    b += text(262, 60, "予防保守で先に交換", "t-s f-ou hand")
    return svg(360, 176, b, "バスタブ曲線")

def virt():
    def col(title, layers, note):
        return column(title, [tile(name, tone="s o" if hot else "s") for name, hot in layers], sub=note, center=True)
    return columns(col("ホスト型", [("アプリ", 0), ("ゲストOS", 0), ("仮想化ソフト", 1), ("ホストOS", 0), ("HW", 0)], "OSが2重で遅い（VirtualBox）"),
                   col("ハイパバイザ型", [("アプリ", 0), ("ゲストOS", 0), ("ハイパバイザ", 1), ("HW", 0)], "ホストOSなし・速い（ESXi・Xen・KVM）"),
                   col("コンテナ型", [("アプリ", 0), ("コンテナ", 1), ("コンテナエンジン", 0), ("ホストOS", 0), ("HW", 0)], "ゲストOSなし・一番軽い（Docker）"))

# ───────────────────────── 02-3 ─────────────────────────
def taskstate():
    R, U, W = (70, 90), (290, 40), (290, 150)
    b = arrow_defs("ts")
    def node(p, s, sub):
        return (f'<rect x="{p[0]-46}" y="{p[1]-17}" width="92" height="34" rx="17" class="f-sheet3 st-line"/>'
                + text(p[0], p[1] - 1, s, "t-m f-ink", "middle") + text(p[0], p[1] + 12, sub, "t-s f-ink3", "middle"))
    b += f'<path d="M{R[0]+30},{R[1]-17} Q170,10 {U[0]-46},{U[1]-6}" class="s-main" marker-end="url(#tso)"/>'
    b += text(165, 22, "ディスパッチ", "t-s f-ou", "middle")
    b += f'<path d="M{U[0]-46},{U[1]+8} Q175,62 {R[0]+46},{R[1]-4}" class="s-ax" marker-end="url(#ts)"/>'
    b += text(176, 74, "プリエンプション", "t-s f-ink2", "middle")
    b += f'<line x1="{U[0]}" y1="{U[1]+17}" x2="{W[0]}" y2="{W[1]-19}" class="s-ax" marker-end="url(#ts)"/>'
    b += text(U[0] + 8, 98, "入出力要求", "t-s f-ink2") + text(U[0] + 8, 111, "(SVC割込み)", "t-s f-ink3")
    b += f'<path d="M{W[0]-46},{W[1]} Q150,160 {R[0]+10},{R[1]+19}" class="s-ax" marker-end="url(#ts)"/>'
    b += text(160, 166, "入出力完了（入出力割込み）", "t-s f-ink2", "middle")
    b += node(R, "実行可能", "Ready") + node(U, "実行", "Run") + node(W, "待ち", "Wait")
    b += text(250, 196, "待ち → 実行 は直接いけない", "t-s f-warn hand", "middle")
    return svg(360, 204, b, "タスクの状態遷移")

# ───────────────────────── 03-2 ─────────────────────────
def recovery():
    X0, X1 = 70, 330
    CP, FL = 150, 300
    b = f'<line x1="{X0-10}" y1="150" x2="{X1}" y2="150" class="s-ax"/>'
    b += f'<line x1="{CP}" y1="12" x2="{CP}" y2="150" class="s-dash"/>' + text(CP, 164, "チェックポイント", "t-s f-ink2", "middle")
    b += f'<line x1="{FL}" y1="12" x2="{FL}" y2="150" class="s-warn"/>' + text(FL, 164, "障害 ✖", "t-s f-warn", "middle")
    rows = [("T1", 80, 130, True, "何もしない", "f-ink3"), ("T2", 110, 220, True, "ロールフォワード", "f-ou"),
            ("T3", 170, 260, True, "ロールフォワード", "f-ou"), ("T4", 100, FL, False, "ロールバック", "f-k"), ("T5", 200, FL, False, "ロールバック", "f-k")]
    for i, (n, s, e, cm, act, cls) in enumerate(rows):
        y = 26 + i * 25
        b += text(X0 - 26, y + 4, n, "t-s f-ink2")
        b += f'<line x1="{s}" y1="{y}" x2="{e}" y2="{y}" class="{"s-main" if cls=="f-ou" else "s-2"}" stroke-linecap="round"/>'
        if cm:
            b += f'<circle cx="{e}" cy="{y}" r="3.5" class="f-ink"/>' + text(e, y - 6, "commit", "t-s f-ink3", "middle")
        b += text(X1 + 2, y + 4, act, f"t-s {cls}", "start")
    return svg(420, 172, b, "障害回復のタイムライン")

def star():
    return grid([blank(), tile("顧客", "名前・住所"), blank(),
                 tile("商品", "商品名・単価"), tile("売上（ファクト）", "いつ・誰が・何を・<b>何個</b>・いくら", "oo"), tile("店舗", "店名・地域"),
                 blank(), tile("日付", "年・月・曜日"), blank()], 3)

# ───────────────────────── 03-3 ─────────────────────────
def osi():
    # 層・よく出るプロトコル・中継装置を1枚に。試験に出る 7・4・3・2 層は左にアクセントの線
    return rows([("7 アプリケーション", "HTTP（80）・SMTP（25）・POP3（110）・IMAP（143）・FTP（20/21）・DNS（53）・DHCP（67/68）・SNMP（161/162）・NTP（123）・SSH（22）", "ゲートウェイ", 1, 1),
                 ("6 プレゼンテーション", "文字コード・圧縮・暗号化（データの形式）", "↑", 0, 0),
                 ("5 セッション", "通信の開始〜終了の管理", "↑", 0, 0),
                 ("4 トランスポート", "TCP・UDP（ポート番号でアプリへ）", "↑", 1, 0),
                 ("3 ネットワーク", "IP・ICMP・ARP・RARP・IPsec・RIP・OSPF・BGP・VRRP（IPアドレスで遠くへ）", "ルータ・L3SW", 1, 1),
                 ("2 データリンク", "イーサネット・PPP・VLAN・STP（MACアドレスで隣へ）", "ブリッジ・L2SW", 1, 1),
                 ("1 物理", "ケーブル・電気信号", "リピータ・ハブ", 0, 1)])

def handshake():
    C, S = 70, 290
    b = arrow_defs("hs")
    b += f'<line x1="{C}" y1="22" x2="{C}" y2="178" class="s-dash"/><line x1="{S}" y1="22" x2="{S}" y2="178" class="s-dash"/>'
    b += text(C, 14, "クライアント", "t-m f-ink", "middle") + text(S, 14, "サーバ", "t-m f-ink", "middle")
    msgs = [(C, S, 40, 70, "① SYN", "seq=100"), (S, C, 84, 114, "② SYN/ACK", "seq=200, ack=101"), (C, S, 128, 158, "③ ACK", "seq=101, ack=201")]
    for x1, x2, y1, y2, a, s in msgs:
        b += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="s-main" marker-end="url(#hso)"/>'
        b += text((x1 + x2) / 2, (y1 + y2) / 2 - 6, a, "t-m f-ou", "middle")
        b += text((x1 + x2) / 2, (y1 + y2) / 2 + 14, s, "t-s f-ink3 mono", "middle")
    return svg(360, 186, b, "3ウェイハンドシェイク")

# ───────────────────────── 03-4 ─────────────────────────
def subnet():
    return (bits([("11000000 10101000 00000001 10", True), ("000010", False)])
            + ends("ネットワーク部 26ビット（/26）", "ホスト部 6ビット", "o")
            + mono('192.168.1.130/26<br>NW ＝ AND → 192.168.1.<b class="hl">128</b>　BC ＝ ホスト全部1 → .<b class="hl">191</b><br>'
                   'ホスト数 ＝ 2⁶−2 ＝ <b class="hl">62</b>（.129〜.190）'))

# ───────────────────────── 03-5 ─────────────────────────
def keys():
    return (chain("暗号化（盗聴対策）", [("送信者", "暗号化", "受信者の公開鍵"), ("受信者", "復号", "受信者の秘密鍵")], "link")
            + chain("デジタル署名（改ざん・なりすまし・否認対策）", [("送信者", "ハッシュ値を署名", "送信者の秘密鍵"), ("受信者", "署名を検証", "送信者の公開鍵")])
            + chain("証明書の検証", [("認証局", "証明書に署名", "CAの秘密鍵"), ("利用者", "証明書を検証", "CAの公開鍵")]))

def dmz():
    b = arrow_defs("dz")
    def bx(x, y, w, s, sub="", cls="f-sheet3"):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="8" class="{cls} st-line"/>' + text(x + w / 2, y + 15, s, "t-s f-ink", "middle")
                + (text(x + w / 2, y + 29, sub, "t-s f-ink3", "middle") if sub else ""))
    b += bx(4, 70, 96, "インターネット")
    b += bx(122, 70, 44, "FW", "", "f-oubg")
    b += '<line x1="100" y1="88" x2="122" y2="88" class="s-ax"/>'
    b += '<path d="M166,80 L190,40" class="s-ax"/><path d="M166,96 L190,136" class="s-ax"/>'
    b += bx(190, 18, 166, "DMZ", "Webサーバ・メールサーバ")
    b += bx(190, 118, 166, "内部ネットワーク", "DBサーバ・社員PC")
    b += text(273, 74, "公開サーバはここ", "t-s f-ou hand", "middle")
    b += text(273, 106, "外から直接は入れない", "t-s f-ink3 hand", "middle")
    return svg(360, 160, b, "DMZの構成")

# ───────────────────────── 04-1 ─────────────────────────
def ftatree():
    return tree(("車が動かない", "トップ事象：悪い結果を一番上に置く", 1, [
        ("OR ゲート", "下のどれか1つでも起きたらアウト", 0, [
            ("バッテリー切れ", "", 0, []),
            ("ガス欠", "", 0, []),
            ("エンジン故障", "", 0, [
                ("AND ゲート", "下が全部そろったらアウト", 0, [
                    ("部品A破損", "", 0, []),
                    ("部品B破損", "", 0, [])])])])]))

def vmodel():
    return vpairs(["業務要件定義", "システム要件定義", "システム方式設計", "ソフトウェア要件定義", "ソフトウェア方式設計", "ソフトウェア詳細設計"],
                  ["運用テスト", "システム適格性確認テスト", "システム結合テスト", "ソフトウェア適格性確認テスト", "ソフトウェア結合テスト", "単体テスト"],
                  head=("決める（作り込み）↓", "↑ 確かめる（検証）"), bottom="＼ プログラミング ／")

# ───────────────────────── 05-1 ─────────────────────────
def crash():
    # 計画 A3日→B5日→C5日＝13日、完了予定日は11日目。クラッシング＝B・Cに人を足して短く、ファストトラッキング＝Cを前倒しして重ねる
    X0, D, DUE = 70, 26, 11
    def bar(day0, days, row_y, label, hot=False):
        x, w = X0 + day0 * D, days * D - 2
        return (f'<rect x="{x}" y="{row_y}" width="{w}" height="20" rx="4" class="{"f-oubg st-ou" if hot else "f-sheet3"}"/>'
                + text(x + w / 2, row_y + 14, label, "t-s f-ou" if hot else "t-s f-ink", "middle"))
    def due(y0, y1):
        x = X0 + DUE * D - 1
        return f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" class="s-dash"/>' + text(x, y1 + 12, "完了予定日（11日目）", "t-s f-ink3", "middle")
    b = text(4, 14, "クラッシング：人や資源を足して、1つ1つを短くする", "t-m f-ink hand")
    b += text(4, 38, "計画", "t-s f-ink3") + bar(0, 3, 24, "A 3日") + bar(3, 5, 24, "B 5日") + bar(8, 5, 24, "C 5日")
    b += text(4, 64, "短縮後", "t-s f-ink3") + bar(0, 3, 50, "A 3日") + bar(3, 4, 50, "B 4日", True) + bar(7, 3, 50, "C 3日", True)
    b += due(20, 76)
    y = 108
    b += text(4, y + 14, "ファストトラッキング：順番の作業を重ねて並行に進める", "t-m f-ink hand")
    b += text(4, y + 38, "計画", "t-s f-ink3") + bar(0, 3, y + 24, "A 3日") + bar(3, 5, y + 24, "B 5日") + bar(8, 5, y + 24, "C 5日")
    b += text(4, y + 64, "短縮後", "t-s f-ink3") + bar(0, 3, y + 50, "A 3日") + bar(3, 5, y + 50, "B 5日") + bar(6, 5, y + 76, "C 5日（前倒し）", True)
    b += due(y + 20, y + 102)
    return svg(460, y + 120, b, "クラッシングとファストトラッキング")

def cpm():
    N = {1: (28, 105), 2: (130, 38), 3: (130, 172), 4: (250, 38), 5: (250, 172), 6: (338, 105)}
    T = {1: "0/0", 2: "1/2", 3: "5/5", 4: "9/10", 5: "9/9", 6: "14/14"}
    E = [(1, 2, "A1", 0, 0), (1, 3, "B5", 1, 0), (2, 3, "C3", 0, 0), (2, 4, "D3", 0, 0), (3, 5, "E4", 1, 0), (5, 4, "F", 0, 1), (4, 6, "H4", 0, 0), (5, 6, "G5", 1, 0)]
    b = arrow_defs("cp")
    r = 14
    for a, c, lab, crit, dummy in E:
        (x1, y1), (x2, y2) = N[a], N[c]
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        sx, sy, ex, ey = x1 + ux * r, y1 + uy * r, x2 - ux * (r + 2), y2 - uy * (r + 2)
        cls = "s-main" if crit else ("s-dash" if dummy else "s-ax")
        mk = "cpo" if crit else "cp"
        b += f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" class="{cls}" marker-end="url(#{mk})"/>'
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if abs(ux) < 0.2:
            b += text(mx + (8 if dummy else -8), my + 4, lab + ("（ダミー）" if dummy else ""), "t-s " + ("f-ou" if crit else "f-ink2"), "start" if dummy else "end")
        else:
            b += text(mx, my - 6, lab, "t-s " + ("f-ou" if crit else "f-ink2"), "middle")
    for k, (x, y) in N.items():
        crit = k in (1, 3, 5, 6)
        b += f'<circle cx="{x}" cy="{y}" r="{r}" class="f-sheet3 {"st-ou" if crit else "st-line"}"/>'
        b += text(x, y + 4, str(k), "t-m f-ink", "middle")
        b += text(x, y + (30 if y > 100 else -20), T[k], "t-s f-ink3 mono", "middle")
    b += text(190, 224, "最早/最遅が一致する点を結ぶ＝クリティカルパス", "t-s f-ou hand", "middle")
    return svg(366, 232, b, "アローダイアグラムとクリティカルパス")

def evm():
    X0, X1, Y0, Y1 = 40, 330, 170, 16
    fx = lambda t: X0 + (X1 - X0) * t
    fy = lambda v: Y0 - (Y0 - Y1) * v / 100
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X1+8}" y2="{Y0}" class="s-ax"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-6}" class="s-ax"/>'
    b += f'<line x1="{X0}" y1="{fy(100):.1f}" x2="{X1}" y2="{fy(100):.1f}" class="s-grid"/>' + text(X0 - 4, fy(100) + 4, "BAC", "t-s f-ink3", "end")
    b += f'<line x1="{fx(0)}" y1="{fy(0)}" x2="{fx(1)}" y2="{fy(100):.1f}" class="s-2"/>' + text(fx(1) - 4, fy(100) - 6, "PV（計画）", "t-s f-k", "end")
    b += f'<line x1="{fx(0)}" y1="{fy(0)}" x2="{fx(.5)}" y2="{fy(60):.1f}" class="s-warn"/>'
    b += f'<line x1="{fx(0)}" y1="{fy(0)}" x2="{fx(.5)}" y2="{fy(40):.1f}" class="s-main"/>'
    b += f'<line x1="{fx(.5)}" y1="{Y1}" x2="{fx(.5)}" y2="{Y0}" class="s-dash"/>' + text(fx(.5), Y0 + 14, "いま", "t-s f-ink2", "middle")
    for v, s, cls in ((60, "AC 60（実際に払った）", "f-warn"), (50, "PV 50", "f-k"), (40, "EV 40（できた分）", "f-ou")):
        b += f'<circle cx="{fx(.5):.1f}" cy="{fy(v):.1f}" r="3.5" class="{cls}"/>' + text(fx(.5) + 8, fy(v) + 4, s, f"t-s {cls}")
    b += text(fx(.5) - 8, fy(70) + 4, "SV＝EV−PV＝−10 遅れ", "t-s f-ink2", "end")
    b += text(fx(.5) - 8, fy(82) + 4, "CV＝EV−AC＝−20 超過", "t-s f-ink2", "end")
    return svg(360, 186, b, "EVM")

# ───────────────────────── 06-1 ─────────────────────────
def plc():
    X0, X1, Y0, Y1 = 20, 340, 120, 14
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" class="s-ax"/>'
    sales = [(X0 + (X1 - X0) * t, Y0 - (Y0 - Y1) * (math.exp(-((t - 0.62) / 0.24) ** 2))) for t in [i / 200 for i in range(201)]]
    prof = [(X0 + (X1 - X0) * t, Y0 - (Y0 - Y1) * (0.75 * math.exp(-((t - 0.58) / 0.2) ** 2) - 0.12)) for t in [i / 200 for i in range(201)]]
    b += f'<path d="{path(sales)}" class="s-main"/><path d="{path(prof)}" class="s-2"/>'
    b += text(X0 + (X1 - X0) * .62, Y1 - 2, "売上", "t-s f-ou", "middle") + text(X0 + (X1 - X0) * .44, Y1 + 40, "利益", "t-s f-k", "middle")
    seps = [0.25, 0.5, 0.78]
    for t in seps:
        x = X0 + (X1 - X0) * t
        b += f'<line x1="{x:.1f}" y1="{Y1}" x2="{x:.1f}" y2="{Y0+40}" class="s-dash"/>'
    labs = [(0.125, "導入期", "問題児"), (0.375, "成長期", "花形"), (0.64, "成熟期", "金のなる木"), (0.89, "衰退期", "負け犬")]
    for t, a, p in labs:
        x = X0 + (X1 - X0) * t
        b += text(x, Y0 + 16, a, "t-s f-ink", "middle") + text(x, Y0 + 31, p, "t-s f-ink3", "middle")
    return svg(360, 160, b, "プロダクトライフサイクル")

def fiveforce():
    return grid([blank(), tile("新規参入の脅威"), blank(),
                 tile("売り手（サプライヤ）の交渉力"), tile("業界内の競争", tone="oo"), tile("買い手（バイヤ）の交渉力"),
                 blank(), tile("代替品の脅威"), blank()], 3, center_wide=True)

def valuechain():
    # 支援活動（4本の帯）＋主活動（5つの箱）＋右端のマージン。幅は1段まるごとの図（760）に合わせる
    W, X0, X1 = 760, 34, 690
    b = (text(14, 64, "支援活動", "t-m f-ink3", "middle", 'writing-mode="vertical-rl"')
         + text(14, 150, "主活動", "t-m f-ink3", "middle", 'writing-mode="vertical-rl"'))
    for k, name in enumerate(["全般管理（インフラストラクチャ）", "人事・労務管理", "技術開発", "調達活動"]):
        y = 6 + k * 28
        b += f'<rect x="{X0}" y="{y}" width="{X1 - X0 - 6}" height="24" rx="4" class="f-sheet3"/>' + text((X0 + X1 - 6) / 2, y + 16, name, "t-m f-ink", "middle")
    w = (X1 - X0 - 6 - 4 * 6) / 5
    for k, name in enumerate(["購買物流", "製造", "出荷物流", "販売・マーケ", "サービス"]):
        x = X0 + k * (w + 6)
        b += f'<rect x="{x:.1f}" y="122" width="{w:.1f}" height="52" rx="4" class="f-sheet3"/>' + text(x + w / 2, 152, name, "t-m f-ink", "middle")
    b += (f'<path d="M{X1},6 L{W - 30},6 L{W - 6},90 L{W - 30},174 L{X1},174 Z" class="f-oubg"/>'
          + text(W - 34, 90, "マージン", "t-m f-ou", "middle", 'writing-mode="vertical-rl"'))
    return svg(W, 180, b, "バリューチェーン")

# ───────────────────────── 06-2 ─────────────────────────
def eoq():
    X0, X1, Y0, Y1 = 44, 340, 160, 14
    qmax, ymax = 600, 3000
    fx = lambda q: X0 + (X1 - X0) * q / qmax
    fy = lambda v: Y0 - (Y0 - Y1) * min(v, ymax) / ymax
    order = [(fx(q), fy(120000 / q)) for q in range(40, 601, 4)]
    hold = [(fx(q), fy(3 * q)) for q in range(0, 601, 10)]
    tot = [(fx(q), fy(120000 / q + 3 * q)) for q in range(60, 601, 4)]
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X1+6}" y2="{Y0}" class="s-ax"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-4}" class="s-ax"/>'
    b += f'<path d="{path(order)}" class="s-2"/><path d="{path(hold)}" class="s-3"/><path d="{path(tot)}" class="s-main"/>'
    b += f'<line x1="{fx(200):.1f}" y1="{fy(1200):.1f}" x2="{fx(200):.1f}" y2="{Y0}" class="s-dash"/><circle cx="{fx(200):.1f}" cy="{fy(1200):.1f}" r="3.5" class="f-ou"/>'
    b += f'<circle cx="{fx(200):.1f}" cy="{fy(600):.1f}" r="3" class="f-ink"/>'
    b += text(fx(200), Y0 + 14, "EOQ", "t-s f-ou", "middle")
    b += text(fx(560), fy(1950), "総費用", "t-s f-ou", "end") + text(fx(560), fy(1500), "保管費用", "t-s f-link", "end") + text(fx(70), fy(2700), "発注費用", "t-s f-k")
    b += text(fx(215), fy(600) + 16, "発注費＝保管費のとき最小", "t-s f-ink2 hand")
    b += text(X1, Y0 + 14, "1回の発注量", "t-s f-ink3", "end")
    return svg(360, 180, b, "経済的発注量")

def oc():
    X0, X1, Y0, Y1 = 40, 340, 150, 16
    n, c = 50, 2
    def L(p):
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(c + 1))
    pmax = 0.16
    fx = lambda p: X0 + (X1 - X0) * p / pmax
    fy = lambda v: Y0 - (Y0 - Y1) * v
    pts = [(fx(p), fy(L(p))) for p in [i / 1000 for i in range(0, 161)]]
    p1, p2 = 0.02, 0.10
    L1, L2 = L(p1), L(p2)
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X1+6}" y2="{Y0}" class="s-ax"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-4}" class="s-ax"/>'
    b += f'<line x1="{X0}" y1="{fy(1):.1f}" x2="{X1}" y2="{fy(1):.1f}" class="s-grid"/>' + text(X0 - 4, fy(1) + 4, "1.0", "t-s f-ink3", "end")
    b += f'<path d="{path(pts)}" class="s-main"/>'
    for p, Lv in ((p1, L1), (p2, L2)):
        b += f'<line x1="{fx(p):.1f}" y1="{fy(Lv):.1f}" x2="{fx(p):.1f}" y2="{Y0}" class="s-dash"/><line x1="{X0}" y1="{fy(Lv):.1f}" x2="{fx(p):.1f}" y2="{fy(Lv):.1f}" class="s-dash"/>'
    b += f'<line x1="{fx(p1)+6:.1f}" y1="{fy(1):.1f}" x2="{fx(p1)+6:.1f}" y2="{fy(L1):.1f}" class="s-warn"/>'
    b += text(fx(p1) + 12, fy((1 + L1) / 2) + 4, "生産者危険 α（良品ロットが不合格）", "t-s f-warn")
    b += f'<line x1="{fx(p2)+6:.1f}" y1="{fy(L2):.1f}" x2="{fx(p2)+6:.1f}" y2="{Y0}" class="s-3"/>'
    b += text(fx(p2) + 12, fy(L2 / 2) - 8, "消費者危険 β", "t-s f-link") + text(fx(p2) + 12, fy(L2 / 2) + 6, "（不良ロットが合格）", "t-s f-link")
    b += text(fx(p1), Y0 + 14, "p1(AQL)", "t-s f-ink2", "middle") + text(fx(p2), Y0 + 14, "p2", "t-s f-ink2", "middle")
    b += text(X1, Y0 + 14, "ロットの不良率", "t-s f-ink3", "end") + text(X0 + 4, Y1 - 4, "合格率", "t-s f-ink3")
    return svg(360, 170, b, "OC曲線")

def breakeven():
    X0, X1, Y0, Y1 = 46, 330, 160, 14
    smax = 1000
    fx = lambda s: X0 + (X1 - X0) * s / smax
    fy = lambda v: Y0 - (Y0 - Y1) * v / smax
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X1+6}" y2="{Y0}" class="s-ax"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-4}" class="s-ax"/>'
    b += f'<line x1="{fx(0)}" y1="{fy(500):.1f}" x2="{fx(1000):.1f}" y2="{fy(500):.1f}" class="s-dash"/>' + text(fx(990), fy(500) - 4, "固定費 500", "t-s f-ink3", "end")
    b += f'<line x1="{fx(0)}" y1="{fy(0)}" x2="{fx(1000):.1f}" y2="{fy(1000):.1f}" class="s-main"/>' + text(fx(905), fy(1000) + 2, "売上高", "t-s f-ou", "end")
    b += f'<line x1="{fx(0)}" y1="{fy(500):.1f}" x2="{fx(1000):.1f}" y2="{fy(700):.1f}" class="s-2"/>' + text(fx(1000), fy(700) + 16, "総費用＝500＋0.2×売上", "t-s f-k", "end")
    b += f'<circle cx="{fx(625):.1f}" cy="{fy(625):.1f}" r="4" class="f-ou"/><line x1="{fx(625):.1f}" y1="{fy(625):.1f}" x2="{fx(625):.1f}" y2="{Y0}" class="s-dash"/>'
    b += text(fx(625), Y0 + 14, "625", "t-s f-ou mono", "middle")
    b += text(fx(625) - 8, fy(625) - 8, "損益分岐点", "t-s f-ou hand", "end")
    b += text(fx(250), fy(430), "損失", "t-s f-warn", "middle") + text(fx(880), fy(770), "利益", "t-s f-ou", "middle")
    return svg(360, 178, b, "損益分岐点")

# ───────────────────────── 06-3 ─────────────────────────
def ipr():
    return columns(column("産業財産権", [tile("特許権", "発明", "o"), tile("実用新案権", "考案（形・構造）", "o"), tile("意匠権", "デザイン", "o"), tile("商標権", "ロゴ・名前", "o")],
                          note="特許庁に出願・登録が必要"),
                   column("著作権", [tile("著作権", "表現（文章・音楽・プログラム）")], note="登録不要。作った瞬間に発生"),
                   column("その他", [tile("営業秘密", "不正競争防止法"), tile("回路配置利用権", "半導体の回路"), tile("育成者権", "植物の新品種")], note="登録の要らないものも"))

def contracts():
    b = arrow_defs("ct")
    def bx(x, y, s, cls="f-sheet3"):
        return f'<rect x="{x-34}" y="{y-13}" width="68" height="26" rx="7" class="{cls} st-line"/>' + text(x, y + 4, s, "t-s f-ink", "middle")
    def panel(ox, t1, t2, title, cmd_from_client):
        s = text(ox + 85, 14, title, "t-m f-ink hand", "middle")
        A, B, W = (ox + 40, 46), (ox + 130, 46), (ox + 85, 130)
        s += f'<line x1="{A[0]+34}" y1="{A[1]}" x2="{B[0]-34}" y2="{B[1]}" class="s-ax"/>' + text(ox + 85, 40, "契約", "t-s f-ink3", "middle")
        s += f'<line x1="{A[0]}" y1="{A[1]+13}" x2="{W[0]-14}" y2="{W[1]-13}" class="s-ax" marker-end="url(#ct)"/>'
        lab = "雇用" if cmd_from_client else "雇用＋指揮命令"
        s += text(A[0] - 6, 96, lab, "t-s f-ink2", "middle")
        if cmd_from_client:
            s += f'<line x1="{B[0]}" y1="{B[1]+13}" x2="{W[0]+14}" y2="{W[1]-13}" class="s-main" marker-end="url(#cto)"/>' + text(B[0] + 8, 96, "指揮命令", "t-s f-ou", "middle")
        else:
            s += f'<line x1="{B[0]}" y1="{B[1]+13}" x2="{W[0]+14}" y2="{W[1]-13}" class="s-dash"/>' + text(B[0] + 10, 96, "✕指示NG", "t-s f-warn", "middle")
        s += bx(A[0], A[1], t1) + bx(B[0], B[1], t2, "f-oubg" if cmd_from_client else "f-sheet3") + bx(W[0], W[1], "労働者")
        return s
    b += panel(0, "派遣元", "派遣先", "労働者派遣", True)
    b += panel(180, "請負元", "発注者", "請負", False)
    return svg(360, 150, b, "派遣と請負の指揮命令")

