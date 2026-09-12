# -*- coding: utf-8 -*-
"""Minimal Python syntax highlighter -> HTML spans.

Deliberately small and dependency-free: the card code is short, Python-ish, and
often carries Chinese comments. Anything it can't classify stays plain text, so
a mis-tokenised line degrades to unstyled — never to broken markup.

Emitted classes:  k=keyword  b=builtin  s=string  n=number  c=comment  f=call
"""
import html
import re

KEYWORDS = {
    "and", "as", "assert", "async", "await", "break", "class", "continue", "def",
    "del", "elif", "else", "except", "finally", "for", "from", "global", "if",
    "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise",
    "return", "try", "while", "with", "yield", "True", "False", "None", "self",
}
BUILTINS = {
    "abs", "all", "any", "bool", "dict", "enumerate", "float", "int", "len",
    "list", "map", "max", "min", "print", "range", "reversed", "set", "sorted",
    "str", "sum", "tuple", "zip", "isinstance", "type", "inf", "defaultdict",
    "Counter", "deque", "heapq", "bisect", "random", "itertools", "OrderedDict",
    "frozenset", "ord", "chr", "divmod", "append", "pop", "popleft", "add",
    "items", "keys", "values", "get", "sort", "join", "split", "extend",
}

TOKEN = re.compile(r"""
    (?P<comment>\#[^\n]*)
  | (?P<string>'''.*?'''|\"\"\".*?\"\"\"|'[^'\n]*'|"[^"\n]*")
  | (?P<number>\b\d+(?:\.\d+)?\b)
  | (?P<word>[A-Za-z_][A-Za-z_0-9]*)
""", re.X | re.S)


def highlight(line: str) -> str:
    """One source line -> HTML. Non-ASCII (Chinese) passes through untouched."""
    out, pos = [], 0
    for m in TOKEN.finditer(line):
        out.append(html.escape(line[pos:m.start()]))
        kind = m.lastgroup
        text = html.escape(m.group())
        if kind == "comment":
            out.append(f'<i class="c">{text}</i>')
        elif kind == "string":
            out.append(f'<i class="s">{text}</i>')
        elif kind == "number":
            out.append(f'<i class="n">{text}</i>')
        else:  # word
            raw = m.group()
            after = line[m.end():m.end() + 1]
            if raw in KEYWORDS:
                out.append(f'<i class="k">{text}</i>')
            elif raw in BUILTINS:
                out.append(f'<i class="b">{text}</i>')
            elif after == "(":
                out.append(f'<i class="f">{text}</i>')
            else:
                out.append(text)
        pos = m.end()
    out.append(html.escape(line[pos:]))
    return "".join(out)


CSS_LIGHT = """
pre .k{color:#a626a4;font-style:normal}
pre .b{color:#0184bc;font-style:normal}
pre .s{color:#50a14f;font-style:normal}
pre .n{color:#b76b01;font-style:normal}
pre .f{color:#4078f2;font-style:normal}
pre .c{color:#9aa0a6;font-style:italic}
"""
CSS_DARK = """
pre .k{color:#c678dd}
pre .b{color:#56b6c2}
pre .s{color:#98c379}
pre .n{color:#d19a66}
pre .f{color:#61afef}
pre .c{color:#6b7480;font-style:italic}
"""
