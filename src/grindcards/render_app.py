# -*- coding: utf-8 -*-
"""Cards (all languages) -> one self-contained offline web app + PWA sidecars."""
from __future__ import annotations

import base64
import datetime
import html
import io
import json
import os
import unicodedata
from pathlib import Path

from .highlight import CSS_DARK, CSS_LIGHT, highlight
from .i18n import HTML_LANG, LANG_NAMES, STRINGS, t

TEMPLATE = Path(__file__).parent / "templates" / "app.html"


def _blocks_html(blocks, lang, concept_index, deck_lc, variants, is_problem):
    L = lambda k: t(lang, k)
    o = []
    for kind, v in blocks:
        if kind == "more":
            o.append(f"<div class='more'><span>{L('back.more')}</span></div>")
        elif kind == "p":
            o.append(f"<p>{v}</p>")
        elif kind == "ul":
            o.append("<ul>" + "".join(f"<li>{i}</li>" for i in v) + "</ul>")
        elif kind == "code":
            if is_problem:
                # The expand button lives in the label row so it stays glued to the top
                # edge of the code block instead of scrolling away with it.
                o.append(f"<div class='dlab codelab'>{L('back.code')}"
                         f"<button class='zoom ctl' type='button' "
                         f"aria-label='{html.escape(L('back.code.expand_aria'))}'>"
                         f"{L('back.code.expand')}</button></div>")
            parts, wide, wide_wrap = [], 0, 0
            for ln in v.split("\n"):
                n = len(ln) - len(ln.lstrip(" "))
                rest = ln[n:]
                txt = highlight(rest) or " "
                parts.append(f"<span class='cl' style='--i:{n + 2}ch'>{txt}</span>")
                # CJK glyphs take two monospace columns; len() under-counts them and the
                # app would then pick a font size that still wraps. Measure properly.
                w = sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in rest)
                wide = max(wide, n + w)
                wide_wrap = max(wide_wrap, min(n, 9) + w)
            # Widest line is computed at build time so the app can size the font in one
            # step instead of the measure-shrink-measure loop that used to dominate flips.
            o.append(f"<pre data-w='{wide}' data-ww='{wide_wrap}'>" + "".join(parts) + "</pre>")
        elif kind == "warn":
            o.append(f"<div class='warn'>{v}</div>")
        elif kind == "key":
            o.append(f"<div class='key'>{v}</div>")
        elif kind == "cx":
            o.append(f"<div class='cx'>{v}</div>")
        elif kind == "pat":
            why, cname = v
            idx, col = concept_index[cname]
            o.append(f"<div class='dlab'>{L('back.pattern')}</div>"
                     f"<button class='jump ctl' data-i='{idx}' style='--jc:{col}'>"
                     f"{html.escape(cname)}<i>›</i></button>"
                     f"<p class='dwhy'>{why}</p>")
        elif kind == "idea":
            li = "".join(f"<li>{i}</li>" for i in v)
            o.append(f"<div class='dlab'>{L('back.idea')}</div><ol class='idea'>{li}</ol>")
        elif kind == "fig":
            # Inline SVG with its own viewBox; CSS owns the width. No font-fitting loop —
            # vector art does not lose detail when scaled.
            o.append("<div class='figwrap'>" + v + "</div>")
        elif kind == "dia":
            o.append("<div class='diawrap'><pre class='dia'>" + html.escape(v) + "</pre></div>")
        elif kind == "keys":
            *rest, cx = v                      # last item is always the complexity line
            li = "".join(f"<li>{i}</li>" for i in rest)
            o.append(f"<div class='dlab'>{L('back.keys')}</div><ul class='keys'>{li}</ul>"
                     f"<div class='cx'>{cx}</div>")
        elif kind == "fq":
            qa = "".join(f"<div class='qa'><div class='qaq'>{q}</div>"
                         f"<div class='qaa'>{a}</div></div>" for q, a in v)
            o.append(f"<div class='dsec'><div class='dlab'>{L('back.fq')}</div>{qa}</div>")
        elif kind == "var":
            rows = []
            for lc, title, diff in v:
                if lc in deck_lc:
                    name = (f"<button class='vn vgo ctl' data-i='{deck_lc[lc]}'>"
                            f"{title}<i>›</i></button>")
                elif lc:
                    name = (f"<a class='vn vgo ctl' target='_blank' rel='noopener' "
                            f"href='https://leetcode.com/problems/{variants[lc][1]}/'>"
                            f"{title}<i>↗</i></a>")
                else:
                    name = f"<span class='vn'>{title}</span>"
                rows.append(f"<div class='vr'>{name}<div class='vd'>{diff}</div></div>")
            o.append(f"<div class='dsec'><div class='dlab'>{L('back.var')}</div>"
                     + "".join(rows) + "</div>")
        elif kind == "table":
            head, rows = v
            th = "".join(f"<th>{h}</th>" for h in head)
            tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
            o.append(f"<table><tr>{th}</tr>{tr}</table>")
        else:
            raise ValueError(f"unknown block kind {kind!r}")
    return "".join(o)


def _lang_payload(cards, variants, sections, lang):
    concept_index = {tt: (i, sections[s]) for i, (k, s, tt, *_) in enumerate(cards) if k == "C"}
    deck_lc = {x["lc"]: i for i, (k, *_r, x) in enumerate(cards) if k == "P"}
    data = [dict(n=i + 1, k=k, s=s, c=sections[s], t=tt, h=h,
                 b=_blocks_html(b, lang, concept_index, deck_lc, variants, k == "P"), **x)
            for i, (k, s, tt, h, b, x) in enumerate(cards)]
    # Variant catalogue for the menu: grouped by section, each row remembers which
    # deck cards it is a variant of (one problem often hangs under two or three).
    vcat = {}
    for k, sec, tt, h, blocks, x in cards:
        for kind, val in blocks:
            if kind != "var":
                continue
            for lc, title, diff in val:
                if not lc or lc in deck_lc:
                    continue
                e = vcat.setdefault(lc, {"lc": lc, "t": title, "g": variants[lc][1],
                                         "s": sec, "c": sections[sec], "from": []})
                e["from"].append({"t": tt, "d": diff})
    order = list(sections)
    vlist = sorted(vcat.values(), key=lambda e: (order.index(e["s"]), e["lc"]))
    return data, vlist


def _icon_img(z=180, pad=0):
    """Two stacked cards. pad>0 insets the whole drawing for Android's maskable crop."""
    from PIL import Image, ImageDraw
    k = (z - 2 * pad) / 180.0
    im = Image.new("RGBA", (z, z), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def r(box, rad, fill):
        d.rounded_rectangle([pad + v * k for v in box], rad * k, fill=fill)
    r([0, 0, 179, 179], 40, (29, 32, 38, 255))
    r([34, 30, 146, 124], 13, (70, 78, 92, 255))
    r([26, 46, 138, 148], 13, (246, 247, 249, 255))
    for i, (y, w, col) in enumerate([(70, 74, (36, 40, 48)), (92, 88, (150, 158, 168)),
                                     (110, 60, (150, 158, 168))]):
        r([42, y, 42 + w, y + (9 if i == 0 else 7)], 4, col)
    r([42, 58, 74, 64], 3, (15, 118, 110))
    return im


def _icon_data_uri():
    try:
        buf = io.BytesIO()
        _icon_img(180).save(buf, "PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        return ""


# Network-first: a fresh deploy shows up after one reload (cache-first would pin the old
# deck to the screen). Offline falls back to the cache, so the app still works on a plane.
SW = """const C = 'gc-%s';
const SHELL = ['./', './index.html', './manifest.webmanifest',
               './icon-192.png', './icon-512.png', './icon-maskable-512.png'];
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(C).then(c => c.addAll(SHELL)).catch(() => {}));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(r => {
      const copy = r.clone();
      caches.open(C).then(c => c.put(e.request, copy)).catch(() => {});
      return r;
    }).catch(() => caches.match(e.request).then(m => m || caches.match('./index.html')))
  );
});
"""


def _sidecars(outdir: Path, version: str, name: str, desc: str, lang: str):
    outdir.mkdir(parents=True, exist_ok=True)
    written = ["manifest.webmanifest", "sw.js"]
    try:
        _icon_img(192).save(outdir / "icon-192.png")
        _icon_img(512).save(outdir / "icon-512.png")
        _icon_img(512, pad=52).save(outdir / "icon-maskable-512.png")
        written += ["icon-192.png", "icon-512.png", "icon-maskable-512.png"]
    except ImportError:
        pass                                   # Pillow is optional; the app still runs
    manifest = {
        "name": name, "short_name": name, "description": desc,
        # No start_url on purpose: iOS would use it to replace the URL you were on when
        # you tapped "Add to Home Screen", dropping the #k=<sync key> fragment.
        "scope": "./", "display": "standalone", "orientation": "any",
        "lang": HTML_LANG.get(lang, lang),
        "background_color": "#eef0f3", "theme_color": "#f6f7f9",
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png",
                   "purpose": "maskable"}],
    }
    (outdir / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                                                 encoding="utf-8")
    (outdir / "sw.js").write_text(SW % version, encoding="utf-8")
    return written


def render_app(deck, built: dict, out: Path):
    """built: {lang: (cards, listed_variants)} from assemble()."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    decks, variants = {}, {}
    for lang, (cards, listed) in built.items():
        decks[lang], variants[lang] = _lang_payload(cards, listed, deck.sections, lang)

    n = len(next(iter(decks.values())))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ui = {lang: {k[3:]: v for k, v in STRINGS[lang].items() if k.startswith("ui.")}
          for lang in built}
    js = lambda obj: json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    doc = TEMPLATE.read_text(encoding="utf-8")
    for key, val in {
        "__DECKS__":     js(decks),
        "__VARIANTS__":  js(variants),
        "__SECTIONS__":  js(deck.sections),
        "__I18N__":      js(ui),
        "__LANGS__":     js([[l, LANG_NAMES.get(l, l)] for l in deck.langs]),
        "__LANG__":      json.dumps(deck.default_lang),
        "__APPNAME__":   html.escape(deck.name),
        "__ICON__":      _icon_data_uri(),
        "__BUILD__":     js({l: t(l, "build.stamp", n=n, stamp=stamp) for l in built}),
        "/*__HL_LIGHT__*/": CSS_LIGHT,
        "/*__HL_DARK__*/":  CSS_DARK,
    }.items():
        assert key in doc, f"template is missing placeholder {key}"
        doc = doc.replace(key, val)
    if not _icon_data_uri():
        # No Pillow: drop the icon links rather than point them at an empty href
        # (browsers would fetch the page itself as the icon).
        doc = "\n".join(l for l in doc.split("\n") if 'href=""' not in l)
    out.write_text(doc, encoding="utf-8")
    extra = _sidecars(out.parent, stamp.replace(" ", "-").replace(":", ""),
                      deck.name, t(deck.default_lang, "manifest.desc"), deck.default_lang)
    return {"cards": n, "bytes": os.path.getsize(out), "sidecars": extra, "langs": list(built)}
