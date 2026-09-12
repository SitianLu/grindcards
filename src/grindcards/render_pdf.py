# -*- coding: utf-8 -*-
"""Cards -> printable PDF (US Letter, 3 strips per page, fold each strip in half).

Needs the optional `render` extra (playwright + chromium). The page is laid out in
HTML, then a headless browser shrinks each panel's font until nothing overflows.

The print face is deliberately smaller than the app face. A 4×3in panel cannot hold
pattern + reasoning + figure + full code + keys; measured on a 57-card deck, all four
sections overflowed 42 cards. Paper keeps what you actually recall when flipping —
pattern, code, keys — and leaves reasoning and figures to the scrolling app.
"""
from __future__ import annotations

import asyncio
import html
import os
from pathlib import Path

from .highlight import highlight
from .i18n import t

PER_PAGE = 3
PRINT_SKIP = {"dia", "fig", "idea"}
PRINT_CODE_MAX = 24            # lines a panel can hold; beyond that, truncate visibly

CSS = """
@page { size: 8.5in 11in; margin: 0.42in 0.25in 0.30in 0.25in; }
* { box-sizing: border-box; margin:0; padding:0; }
html,body { font-family:"Noto Sans CJK SC","Noto Sans","DejaVu Sans",sans-serif; color:#111; }
.page { width:8.0in; page-break-after:always; }
.page:last-child { page-break-after:auto; }
.phead { height:0.26in; display:flex; align-items:center; justify-content:space-between;
         font-size:6.2pt; color:#9aa0a6; letter-spacing:.04em; }
.phead b { color:#6b7280; font-weight:600; }
.strip { width:8.0in; height:3.0in; display:flex; border:0.6pt solid #c8ccd0;
         margin-bottom:0.085in; position:relative; overflow:hidden; }
.strip:after { content:""; position:absolute; left:4.0in; top:0; bottom:0;
               border-left:0.6pt dashed #c8ccd0; }
.panel { width:4.0in; height:100%; padding:0.15in 0.17in; overflow:hidden; position:relative; }
.front { display:flex; flex-direction:column; }
.fhead { display:flex; align-items:baseline; justify-content:space-between; }
.sect  { font-size:6.0pt; font-weight:700; letter-spacing:.10em; text-transform:uppercase; }
.num   { font-size:6.0pt; color:#b0b5bb; font-weight:600; letter-spacing:.05em; }
.ftitle{ font-size:11.5pt; font-weight:700; margin-top:0.045in; line-height:1.15; }
.frule { height:1.6pt; width:0.42in; margin:0.055in 0 0.075in 0; border-radius:2pt; }
.hookwrap { flex:1; display:flex; align-items:center; overflow:hidden; }
.hook  { font-size:10.2pt; line-height:1.42; color:#1f2328; }
.hook .sub { display:block; margin-top:0.05in; font-size:8.2pt; color:#7b8288; font-style:italic; }
.hook .lead { display:block; font-size:0.70em; color:#6b7280; font-weight:600; line-height:1.36;
              margin-bottom:0.062in; }
.hook code { font-family:"DejaVu Sans Mono",monospace; font-size:0.80em;
             background:#f1f3f5; padding:0 2px; border-radius:2px; }
.flip { position:absolute; right:0.13in; bottom:0.08in; font-size:5.6pt; color:#c3c8cd; letter-spacing:.06em; }
.back { display:flex; flex-direction:column; }
.bhead { display:flex; align-items:center; gap:4px; padding-bottom:0.035in;
         border-bottom:0.6pt solid #e5e7eb; margin-bottom:0.055in; flex:none; }
.dot   { width:5px; height:5px; border-radius:50%; flex:none; }
.btitle{ font-size:7.2pt; font-weight:700; color:#374151; letter-spacing:.02em;
         text-transform:uppercase; }
.bnum  { margin-left:auto; font-size:5.8pt; color:#c3c8cd; font-weight:600; }
.bbody { flex:1; overflow:hidden; font-size:6.6pt; line-height:1.38; }
.bbody > * + * { margin-top:0.045in; }
.bbody p { color:#22262b; }
.bbody code { font-family:"DejaVu Sans Mono",monospace; font-size:0.94em;
              background:#f1f3f5; padding:0 1.5px; border-radius:2px; }
.bbody ul { padding-left:0.155in; }
.bbody li { margin:0.012in 0; }
.bbody li::marker { color:#6b7280; }
pre { font-family:"DejaVu Sans Mono","Noto Sans Mono CJK SC",monospace;
      font-size:0.92em; line-height:1.30; background:#f6f7f9; border-left:1.6pt solid #d5d9dd;
      padding:0.035in 0.055in; white-space:pre; overflow:hidden; border-radius:0 2px 2px 0; }
.warn { border-left:1.6pt solid #e0a53a; background:#fdf8ec; padding:0.032in 0.055in;
        border-radius:0 2px 2px 0; color:#5c4a1f; }
.key  { border-left:1.6pt solid #4b9e6a; background:#eff8f2; padding:0.032in 0.055in;
        border-radius:0 2px 2px 0; color:#1e3f2c; }
.cx   { font-family:"DejaVu Sans Mono",monospace; font-size:0.87em; color:#7b8288;
        border-top:0.6pt dotted #d5d9dd; padding-top:0.03in; }
table { border-collapse:collapse; width:100%; font-size:0.90em; }
th { background:#f1f3f5; font-weight:700; color:#374151; }
th,td { border:0.5pt solid #dfe3e7; padding:0.018in 0.035in; text-align:left; vertical-align:top; }
.plab { font-weight:700; color:#111; letter-spacing:.01em; margin-bottom:0.02in; }
ul.keys { margin:0.03in 0 0 0; padding-left:0.14in; }
ul.keys li { margin:0.022in 0; }
.stmt  { display:block; }
.stmt code { background:none; padding:0; }
.ex    { display:block; margin-top:0.055in; padding-left:0.055in; border-left:1.2pt solid #e5e7eb;
         font-family:"DejaVu Sans Mono","Noto Sans Mono CJK SC",monospace;
         font-size:0.58em; line-height:1.42; color:#8b9198;
         white-space:pre-wrap; word-break:break-word; }
.prompt{ display:block; margin-top:0.06in; font-size:0.62em; color:#8b9198; letter-spacing:.03em; }
.hints { flex:none; border-top:0.6pt dotted #d5d9dd; margin-top:0.05in; padding-top:0.04in;
         font-size:5.4pt; line-height:1.32; color:#a8aeb5; }
.hints b { color:#8b9198; font-weight:600; }
.hints i { font-style:normal; color:#c3c8cd; font-weight:700; margin-right:2px; }
.bbody pre .k{color:#a626a4;font-style:normal}
.bbody pre .b{color:#0184bc;font-style:normal}
.bbody pre .s{color:#50a14f;font-style:normal}
.bbody pre .n{color:#b76b01;font-style:normal}
.bbody pre .f{color:#4078f2;font-style:normal}
.bbody pre .c{color:#9aa0a6;font-style:italic}
"""

FIT_JS = """
() => {
  const over = (el) => {
    if (el.scrollHeight > el.clientHeight) return true;
    for (const p of el.querySelectorAll('pre'))
      if (p.scrollWidth > p.clientWidth) return true;
    return false;
  };
  const fit = (el, start, min, step) => {
    let fs = start, guard = 0;
    el.style.fontSize = fs + 'pt';
    while (over(el) && fs > min && guard++ < 200) { fs -= step; el.style.fontSize = fs + 'pt'; }
    return fs;
  };
  document.querySelectorAll('.bbody').forEach(el => fit(el, 8.0, 4.30, 0.08));
  document.querySelectorAll('.hookwrap').forEach(w => {
    const h = w.querySelector('.hook');
    let fs = 14.0, guard = 0;
    h.style.fontSize = fs + 'pt';
    while (h.scrollHeight > w.clientHeight && fs > 6.5 && guard++ < 200) {
      fs -= 0.2; h.style.fontSize = fs + 'pt';
    }
  });
}
"""

OVERFLOW_JS = """(TITLES) => {
  const r = [];
  document.querySelectorAll('.bbody').forEach((el, i) => {
    if (el.scrollHeight > el.clientHeight + 1) r.push([TITLES[i], el.scrollHeight - el.clientHeight]);
  });
  return r;
}"""


def _blocks(blocks, lang):
    out = []
    for kind, v in blocks:
        if kind == "more":
            break                                     # everything past here is app-only
        if kind in PRINT_SKIP:
            continue
        if kind == "p":
            out.append(f"<p>{v}</p>")
        elif kind == "ul":
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in v) + "</ul>")
        elif kind == "code":
            lines = v.split("\n")
            if len(lines) > PRINT_CODE_MAX:
                lines = lines[:PRINT_CODE_MAX] + [t(lang, "pdf.truncated")]
            out.append("<pre>" + "\n".join(highlight(ln) for ln in lines) + "</pre>")
        elif kind == "warn":
            out.append(f"<div class='warn'>{v}</div>")
        elif kind == "key":
            out.append(f"<div class='key'>{v}</div>")
        elif kind == "cx":
            out.append(f"<div class='cx'>{v}</div>")
        elif kind == "pat":
            _why, cname = v                           # on paper only the name: "oh, sliding window"
            out.append(f"<div class='plab'>{html.escape(cname)}</div>")
        elif kind == "keys":
            *rest, cx = v                             # two keys + complexity fit; more won't be read at 4pt
            out.append("<ul class='keys'>" + "".join(f"<li>{i}</li>" for i in rest[:2]) + "</ul>"
                       f"<div class='cx'>{cx}</div>")
        elif kind == "table":
            head, rows = v
            th = "".join(f"<th>{h}</th>" for h in head)
            tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f"<table><tr>{th}</tr>{tr}</table>")
        elif kind in ("fq", "var", "idea", "dia", "fig"):
            pass
        else:
            raise ValueError(f"unknown block kind {kind!r}")
    return "".join(out)


def build_html(deck, cards, lang):
    total = len(cards)
    npages = (total + PER_PAGE - 1) // PER_PAGE
    pages = []
    for pi in range(0, total, PER_PAGE):
        strips = []
        for j, (kind, sect, title, hook, blocks, extra) in enumerate(cards[pi:pi + PER_PAGE]):
            n = pi + j + 1
            color = deck.sections[sect]
            prob = kind == "P"
            fcolor = "#8b9198" if prob else color         # the front must not leak the pattern
            flabel = "Problem" if prob else sect
            hints = extra.get("hints") or []
            hint_html = (f"<div class='hints'><b>{t(lang, 'pdf.hints')}</b>　" + "　".join(
                f"<i>{i + 1}</i>{h}" for i, h in enumerate(hints)) + "</div>") if hints else ""
            strips.append(f"""
<div class="strip">
  <div class="panel front">
    <div class="fhead"><span class="sect" style="color:{fcolor}">{flabel}</span>
      <span class="num">{n:02d} / {total}</span></div>
    <div class="ftitle">{title}</div>
    <div class="frule" style="background:{fcolor}"></div>
    <div class="hookwrap"><div class="hook">{hook}</div></div>
    {hint_html}
    <div class="flip">{t(lang, 'pdf.fold')}</div>
  </div>
  <div class="panel back">
    <div class="bhead"><span class="dot" style="background:{color}"></span>
      <span class="btitle" style="color:{color}">{sect if prob else title}</span><span class="bnum">{n:02d}</span></div>
    <div class="bbody">{_blocks(blocks, lang)}</div>
  </div>
</div>""")
        pages.append(f"<div class='page'><div class='phead'><span>{t(lang, 'pdf.cut')}</span>"
                     f"<span><b>{html.escape(deck.name)}</b> &nbsp; {pi // PER_PAGE + 1} / {npages}</span></div>"
                     + "".join(strips) + "</div>")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            + "".join(pages) + "</body></html>")


async def _render(doc, titles, out: Path):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.set_content(doc, wait_until="load")
        # Measure only after web fonts are applied; `load` does not guarantee that, and
        # measuring too early made the same card overflow in one run and not the next.
        await pg.evaluate("() => document.fonts.ready")
        await pg.wait_for_timeout(250)
        await pg.evaluate(FIT_JS)
        bad = await pg.evaluate(OVERFLOW_JS, titles)
        await pg.pdf(path=str(out), width="8.5in", height="11in", print_background=True,
                     margin={"top": "0.42in", "bottom": "0.30in", "left": "0.25in", "right": "0.25in"})
        await b.close()
    return bad


def render_pdf(deck, cards, lang, out: Path, keep_html: bool = False):
    """Returns {"pages", "overflow": [(title, px), ...], "bytes"}."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = build_html(deck, cards, lang)
    if keep_html:
        out.with_suffix(".html").write_text(doc, encoding="utf-8")
    try:
        import playwright  # noqa: F401
    except ImportError as ex:
        raise RuntimeError("PDF rendering needs the `render` extra: "
                           "pip install 'grindcards[render]' && playwright install chromium") from ex
    bad = asyncio.run(_render(doc, [c[2] for c in cards], out))
    return {"pages": (len(cards) + PER_PAGE - 1) // PER_PAGE, "overflow": bad,
            "bytes": os.path.getsize(out)}
