# -*- coding: utf-8 -*-
"""把 solutions.py 里的代码改写成「上卡片的样子」。

作者写的是带类型标注的完整实现（跑测试方便、也贴近 LeetCode 给的签名），
但一张 393px 宽的卡片上，`def twoSum(nums: list[int], target: int) -> list[int]:`
会折成三行，注释也被挤到下一行去，读起来比没有还糟。

卡片上要的是「面试时在白板上写的那版」——所以构建时把标注去掉。
去完之后 verify_sol.py 会再跑一遍**去标注后的代码**，保证卡上印的那份本身是对的，
而不是「作者手里那份是对的」。
"""
import re

_DEF = re.compile(r"^(\s*)def\s+(\w+)\s*\((.*)$")


def _split_params(src, i):
    """从 '(' 之后开始扫，返回 (参数原文, 右括号之后的剩余部分)。按括号深度配对。"""
    depth, out = 1, []
    while i < len(src):
        c = src[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                return "".join(out), src[i + 1:]
        out.append(c)
        i += 1
    return "".join(out), ""            # 签名跨行了，交给调用方原样返回


def _strip_params(params):
    """去掉每个参数的 `: 类型`，保留默认值。逗号只在深度 0 处才算分隔。"""
    parts, depth, cur = [], 0, []
    for c in params:
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        if c == "," and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(c)
    parts.append("".join(cur))

    out = []
    for p in parts:
        if not p.strip():
            continue
        name, sep, rest = p.partition(":")
        if not sep:
            out.append(p.strip())
            continue
        # `x: int = 3` -> `x=3`；`x: int` -> `x`
        d = 0
        for j, c in enumerate(rest):
            if c in "([{": d += 1
            elif c in ")]}": d -= 1
            elif c == "=" and d == 0:
                out.append(name.strip() + "=" + rest[j + 1:].strip())
                break
        else:
            out.append(name.strip())
    return ", ".join(out)


def strip_hints(code):
    lines = []
    for line in code.split("\n"):
        m = _DEF.match(line)
        if not m:
            lines.append(line); continue
        indent, name, rest = m.groups()
        params, after = _split_params(rest, 0)
        if not after:                   # 括号没在本行闭合，别动
            lines.append(line); continue
        after = re.sub(r"^\s*->[^:]*:", ":", after, count=1)   # 去返回值标注
        lines.append(f"{indent}def {name}({_strip_params(params)}){after}")
    return "\n".join(lines)


if __name__ == "__main__":
    import solutions
    worst = sorted(((max(len(l) for l in strip_hints(v["code"]).split("\n")), lc)
                    for lc, v in solutions.SOL.items()), reverse=True)
    print("去标注后最长的行:")
    for w, lc in worst[:10]:
        print(f"  LC {lc:>5}  {w} 列")
