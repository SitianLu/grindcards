# -*- coding: utf-8 -*-
"""Load a deck directory into plain Python objects.

A deck is a directory:

    mydeck/
      deck.toml          name, languages, default language
      sections.py        SECTIONS = {"SLIDING WINDOW": "#047857", ...}   (order matters)
      problems.py        PROBLEMS = [dict(lc=76, title="Minimum Window Substring",
                                          section="SLIDING WINDOW",
                                          slug="minimum-window-substring", meta=True), ...]
      variants.py        VARIANTS = {lc: (official title, slug)}   (optional)
      <lang>/            one folder per language, same files in each:
        concepts.py      CONCEPTS = [("C", section, title, hook_html, [blocks]), ...]
        statements.py    STMT = {lc: (statement_html, example_line)}
        hints.py         HINTS = {lc: [hint1, hint2, hint3]}
        deep.py          DEEP = {lc: dict(pat=(why, concept_title), fq=[(q,a)], var=[(name, diff)])}
        solutions.py     SOL = {lc: dict(idea=[...], code="...", keys=[...], test="...", want=...)}
        figures.py       FIG = {lc: "<svg ...>"}   (optional)

Everything language-neutral (which problems, their sections, colours, slugs, official
titles) lives at the top level once. Everything a reader reads lives under a language
folder. That split is what makes "add a language" a content task and not an engine task.
"""
from __future__ import annotations

import importlib.util
import sys

try:
    import tomllib
except ImportError:                      # Python 3.10
    import tomli as tomllib
from dataclasses import dataclass, field
from pathlib import Path


class DeckError(Exception):
    pass


def _load_module(path: Path, name: str):
    if not path.exists():
        raise DeckError(f"missing {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    # Let sibling files import each other (e.g. solutions.py pulling a shared
    # example from statements.py) without any sys.path gymnastics on their side.
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(mod)
    except SyntaxError as ex:
        raise DeckError(f"{path}:{ex.lineno}: {ex.msg}") from ex
    except Exception as ex:                  # content files are code; surface their errors plainly
        raise DeckError(f"{path}: {type(ex).__name__}: {ex}") from ex
    finally:
        sys.path.pop(0)
    return mod


@dataclass
class LangContent:
    lang: str
    concepts: list                     # 5-tuples
    stmt: dict                         # lc -> (statement, example)
    hints: dict                        # lc -> [hints]
    deep: dict                         # lc -> dict(pat, fq, var)
    sol: dict                          # lc -> dict(idea, code, keys, test, want, fig?)


@dataclass
class Deck:
    root: Path
    name: str
    langs: list[str]
    default_lang: str
    sections: dict                     # name -> colour
    problems: list                     # dicts
    variants: dict                     # lc -> (title, slug)
    content: dict = field(default_factory=dict)   # lang -> LangContent

    @property
    def order(self):
        return list(self.sections)

    def problem_title(self, p) -> str:
        return f"LC {p['lc']} · {p['title']}"


def load_deck(root: str | Path) -> Deck:
    root = Path(root).resolve()
    cfg_path = root / "deck.toml"
    if not cfg_path.exists():
        raise DeckError(f"{root} is not a deck: no deck.toml (run `grindcards init` first)")
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    d = cfg.get("deck", cfg)
    langs = list(d.get("languages", ["en"]))
    default = d.get("default_language", langs[0])
    if default not in langs:
        raise DeckError(f"default_language {default!r} is not in languages {langs}")

    tag = root.name.replace("-", "_")
    sections = _load_module(root / "sections.py", f"gc_{tag}_sections").SECTIONS
    problems = list(_load_module(root / "problems.py", f"gc_{tag}_problems").PROBLEMS)
    vpath = root / "variants.py"
    variants = dict(_load_module(vpath, f"gc_{tag}_variants").VARIANTS) if vpath.exists() else {}

    deck = Deck(root=root, name=d.get("name", root.name), langs=langs, default_lang=default,
                sections=sections, problems=problems, variants=variants)

    for p in problems:
        for k in ("lc", "title", "section", "slug"):
            if k not in p:
                raise DeckError(f"problems.py: entry {p} is missing {k!r}")
        if p["section"] not in sections:
            raise DeckError(f"problems.py: LC {p['lc']} uses unknown section {p['section']!r}")

    for lang in langs:
        ld = root / lang
        if not ld.is_dir():
            raise DeckError(f"language folder missing: {ld}")
        m = lambda f: _load_module(ld / f, f"gc_{tag}_{lang}_{f[:-3]}")
        sol = {k: dict(v) for k, v in m("solutions.py").SOL.items()}
        fpath = ld / "figures.py"
        if fpath.exists():
            for lc, svg in m("figures.py").FIG.items():
                if lc not in sol:
                    raise DeckError(f"{lang}/figures.py draws LC {lc}, which has no solution")
                sol[lc]["fig"] = svg
        deck.content[lang] = LangContent(
            lang=lang,
            concepts=list(m("concepts.py").CONCEPTS),
            stmt=dict(m("statements.py").STMT),
            hints=dict(m("hints.py").HINTS),
            deep=dict(m("deep.py").DEEP),
            sol=sol,
        )
    return deck
