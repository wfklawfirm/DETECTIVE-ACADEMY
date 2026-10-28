"""Text cleaning and excerpt-window helpers for build_heritage.py (pure functions, read-only)."""
import re

CJK = re.compile(r"[぀-ヿ㐀-鿿]")
# sentence boundary = terminal punctuation (+ closing quotes) followed by whitespace and an opening character
_EN = re.compile(r"""([.!?…]["”’')\]]*)\s+(?=["“‘'(\[A-Z0-9])""")
_FR = re.compile(r"""([.!?…»]["”’')\]]*)\s+(?=["«“‘'(\[A-ZÀ-Ý0-9—-])""")
_CJK_END = re.compile("[。！？；]+[」』”’）]*")


def _split(rx, p):
    out, last = [], 0
    for m in rx.finditer(p):
        out.append(p[last:m.end(1)]); last = m.end()
    out.append(p[last:])
    return out


MAX_WORDS = 120
MAX_CJK_CHARS = 200  # ~ 100-120 "words" for CJK; word totals for CJK are reported as chars/2


def strip_pg(t: str) -> str:
    m = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG[^\n]*\n", t)
    if m: t = t[m.end():]
    e = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG", t)
    if e: t = t[:e.start()]
    return t


def clean(text: str, kind: str) -> str:
    text = text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
    if kind == "pg":
        text = strip_pg(text)
        text = re.sub(r"\[Illustration[^\]]*\]", "", text)
        text = re.sub(r"(?<![\w])_([^_\n]{1,80})_(?![\w])", r"\1", text)
    elif kind == "se" or kind == "wiki" or kind == "ia":
        i = text.find("=" * 20)
        if i >= 0: text = text[text.find("\n", i):]
    if kind == "aozora":
        parts = re.split(r"-{20,}", text)
        if len(parts) >= 3: text = "".join(parts[2:])
        text = re.split(r"\n底本[:：]", text)[0]
        text = re.sub(r"《[^》]*》", "", text)
        text = text.replace("｜", "")
        text = re.sub(r"［＃[^］]*］", "", text)
    if kind == "wiki":
        text = re.sub(r"\{\{[^{}]*\}\}", "", text)
        text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)
        text = re.sub(r"'{2,}", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"^=+\s*(.*?)\s*=+\s*$", r"\1", text, flags=re.M)
        text = re.sub(r"^[*:#]+\s*", "", text, flags=re.M)
    return text


def paragraphs(text: str, lang: str, wrapped: bool = False):
    """List of paragraph strings (whitespace-normalised). CJK/line-based texts use single newlines."""
    blank = text.count("\n\n")
    if wrapped and lang in ("ja", "zh"):
        raw = re.split(r"\n\s*\n", text)  # hard-wrapped e-text: blank line = paragraph break
    elif lang in ("ja", "zh") or blank < len(text) / 4000:
        raw = text.split("\n")
    else:
        raw = re.split(r"\n\s*\n", text)
    out = []
    for p in raw:
        p = re.sub(r"\s+", " ", p).strip() if lang not in ("ja", "zh") else (re.sub(r"\s+", "", p) if wrapped else re.sub(r"[ \t　]+", "", p)).strip()
        if not p or re.search(r"Standard Ebooks|Uncopyright|CC0 1\.0|Project Gutenberg|Faded Page|Internet Archive|ATHAR W2|wikisource", p, re.I):
            out.append(""); continue
        out.append(p)
    return out


def _cjk_split(p):
    out, last = [], 0
    for m in _CJK_END.finditer(p):
        out.append(p[last:m.end()]); last = m.end()
    out.append(p[last:])
    return out


def sentences(p: str, lang: str):
    parts = _split(_FR, p) if lang == "fr" else _cjk_split(p) if lang in ("ja", "zh") else _split(_EN, p)
    s = [x.strip() for x in parts if x and x.strip()]
    return s or [p]


def wcount(s: str, lang: str) -> float:
    if lang in ("ja", "zh"): return len(CJK.findall(s)) / 2.0
    return len(s.split())


def over(s: str, lang: str) -> bool:
    if lang in ("ja", "zh"): return len(s) > MAX_CJK_CHARS
    return len(s.split()) > MAX_WORDS


def window(paras, loc: str, lang: str) -> str:
    """loc 'p:s:n' = start paragraph index, first sentence in it, number of sentences; the window may run on into the
    following paragraphs (paragraph breaks are kept as newlines). Returns the verbatim joined text."""
    p, s, n = (int(x) for x in loc.split(":"))
    out, first, i = [], True, p
    joiner = "" if lang in ("ja", "zh") else " "
    while n > 0 and i < len(paras):
        sen = sentences(paras[i], lang) if paras[i] else []
        sen = sen[s:] if first else sen
        first = False
        take = sen[:n]
        if take: out.append(joiner.join(take)); n -= len(take)
        i += 1
    return "\n".join(out)


def read_text(path: str) -> str:
    b = open(path, "rb").read()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", "replace")
