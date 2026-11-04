# -*- coding: utf-8 -*-
"""全文検索の索引：完成したノートの HTML を「検索結果の1件」ごとの本文に分ける

1件の単位（検索結果に1行ずつ出て、押すとそこへ飛ぶ）：
  章・ボード（section）／ 節（## の見出しから次の見出しまで）／ カード1枚 ／ ひっかけペア1組 ／ 公式1つ
"""
import unicodedata
from html.parser import HTMLParser

class TextIndexer(HTMLParser):
    """ノート本文を、id の付いた区切り（章・節・カード・ペア・公式）ごとのテキストに分ける"""
    ANCHOR_TAGS = {"section", "article", "h1", "h2", "h3", "h4"}
    SKIP = {"script", "style", "nav", "noscript", "template", "button"}
    VOID = {"br", "img", "input", "meta", "link", "hr", "area", "base", "col", "embed", "source", "track", "wbr"}

    def __init__(self, labels):
        super().__init__(convert_charrefs=True)
        self.labels = labels          # id → 目次の名前（章）
        self.secs = [["", "", []]]    # [id, label, [text]]
        self.skip = 0
        self.stack = []
        self.want = 0                 # 名前に使う文字列をあと何個拾うか
        self.prefix = ""              # 名前の頭に付ける言葉（「03-6」「カード」など）
        self.got = []
        self.top = ""                 # 今いる章・ボードの短い名前（節の名前の頭に付ける）
        self.top_open = False         # 章・ボードの名前を、最初の文字列から決める途中か

    def start(self, sid, label, prefix="", want=1):
        self.secs.append([sid, label, []])
        self.want, self.prefix, self.got = (0 if label else want), prefix, []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        self.stack.append(tag)
        if tag in self.SKIP:
            self.skip += 1
        a = dict(attrs)
        sid = a.get("id")
        if not sid or self.skip:
            return
        cls = (a.get("class") or "").split()
        if tag in self.ANCHOR_TAGS or sid in self.labels:
            label = self.labels.get(sid, "")
            self.start(sid, label)
            self.top = label.split(" ", 1)[0] if label else ""   # 章なら「03-6」
            self.top_open = not label
        elif "sec" in cls:
            self.start(sid, "", (self.top + " ") if self.top else "")
        elif "tcard" in cls:
            self.start(sid, "", "カード ")
        elif "fx" in cls:
            self.start(sid, "", "公式 ")
        elif tag == "tr":
            self.start(sid, "", "ペア ", 2)

    def handle_endtag(self, tag):
        if tag in self.VOID or tag not in self.stack:
            return
        while self.stack:
            t = self.stack.pop()
            if t in self.SKIP:
                self.skip -= 1
            if t == tag:
                break

    def handle_data(self, data):
        if self.skip:
            return
        t = " ".join(data.split())
        if not t:
            return
        cur = self.secs[-1]
        if self.want and len(t) > 1:
            self.got.append(t[:40])
            self.want -= 1
            if not self.want:
                cur[1] = self.prefix + " ／ ".join(self.got)
                if self.top_open:  # ボードは見出しの「（」より前を短い名前にする（例：あとから出た疑問）
                    self.top = t.split("（", 1)[0][:16]
                    self.top_open = False
        cur[2].append(t)

def text_index(page, outline):
    labels = {}
    for sid, label in outline:
        labels[sid] = label
    ix = TextIndexer(labels)
    ix.feed(page)
    out = []
    for sid, label, texts in ix.secs:
        body = unicodedata.normalize("NFKC", " ".join(texts))
        if body:
            out.append([sid, label or "表紙", body])
    return out
