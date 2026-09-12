# -*- coding: utf-8 -*-
"""Block helpers shared by deck content files and the engine.

A card back is a list of (kind, value) tuples. Content files build them with
these one-letter helpers so a card reads like an outline, not like markup.
"""


def P(v):    return ("p", v)                      # plain paragraph
def L(*v):   return ("ul", list(v))               # bullet list
def C(v):    return ("code", v.strip("\n"))       # code block (never wraps)
def W(v):    return ("warn", v)                   # gotcha / pitfall box
def K(v):    return ("key", v)                    # the one insight worth memorising
def T(h, rows): return ("table", (h, rows))       # decision matrix
def CX(v):   return ("cx", v)                     # complexity footer
def MORE():  return ("more", None)                # everything after is app-only depth
def PAT(why, concept): return ("pat", (why, concept))   # ① which pattern, and why
def FQ(pairs):  return ("fq", pairs)                     # follow-up Q/A
def VAR(pairs): return ("var", pairs)                    # neighbouring problems
def IDEA(steps): return ("idea", steps)                  # ② the derivation
def DIA(text):   return ("dia", text.strip("\n"))        # ②b ASCII diagram (fallback)
def FIG(svg):    return ("fig", svg)                     # ②b SVG figure (preferred)
def KEYS(items): return ("keys", items)                  # ④ what to walk away with

# Front-of-card helpers for concept cards.
def LEAD(t): return f"<span class='lead'>{t}</span>"
def ASK(q="Which pattern, and what's the <b>one insight</b> that makes it work?"): return q
