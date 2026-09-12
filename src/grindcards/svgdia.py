# -*- coding: utf-8 -*-
"""卡片图解的 SVG 生成器。

为什么不用 ASCII 图：等宽字符画在手机上靠 fitDia 一路缩字号才塞得下，
缩到 8.2px 就糊了；而且中文占两格、箭头对不齐，改一个字整张图要重排。
SVG 是矢量的——viewBox 定死逻辑坐标，width:100% 交给卡片，多小的屏都清晰。

配色全部走 CSS 变量（--fig-*），所以深色模式自动跟随，不用出两套图。

用法：

    f = Fig()
    f.title('s = "ADOBECODEBANC"   t = "ABC"')
    r = f.row("ADOBECODEBANC")
    f.span(r, 0, 5, "合法, 长 6")
    f.gap()
    ...
    svg = f.done()

坐标系：x 向右、y 向下，单位就是 viewBox 单位（≈ 手机上的 CSS px）。
Fig 自己记录当前的 y 游标，大部分时候不用手写 y。
"""

W = 340                     # viewBox 宽度：卡片正文在手机上的可用宽度
PAD = 2                     # 左右留一点，描边才不会被裁掉

# 语义色，值定义在 app_template.html 的 :root 里（深色模式自动换）
INK = "var(--fig-ink)"      # 主线条、主文字
MUTE = "var(--fig-mute)"    # 次要标注
AC = "var(--fig-ac)"        # 强调：当前窗口、命中的那条边
HI = "var(--fig-hi)"        # 强调块的填充
FILL = "var(--fig-fill)"    # 普通格子的填充
BAD = "var(--fig-bad)"      # 反例、错误路径
GOOD = "var(--fig-good)"    # 答案


def _n(v):
    """坐标取一位小数，别让 SVG 里全是 17 位浮点。"""
    return f"{v:.1f}".rstrip("0").rstrip(".")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


class Fig:
    def __init__(self, w=W, top=4):
        self.w = w
        self.y = top          # 当前排版游标
        self.parts = []
        self.ymin = top         # 画过的内容的实际上下边界（含标签）
        self.ymax = top
        self._markers = {}      # 颜色 -> marker id（按出现顺序，保证可复现）

    def _ext(self, top, bot=None):
        """登记一段被占用的纵向空间。

        排版塌掉过一次：span 的标签写在方括号下面，但游标只推到方括号，
        下一行的 ptr 标签就压在它身上了。与其每处手算，不如每个图元
        把自己真正占的高度报上来，gap() 一律从 ymax 起跳。
        """
        bot = top if bot is None else bot
        self.ymin = min(self.ymin, top)
        self.ymax = max(self.ymax, bot)

    # ── 基础图元 ────────────────────────────────────────────────
    def raw(self, s):
        self.parts.append(s)

    def text(self, x, y, s, *, size=10.5, fill=INK, anchor="middle",
             mono=False, weight=None, dy=None, opacity=None):
        a = [f'x="{_n(x)}"', f'y="{_n(y)}"', f'font-size="{_n(size)}"',
             f'fill="{fill}"', f'text-anchor="{anchor}"']
        if mono:
            a.append('class="m"')
        if weight:
            a.append(f'font-weight="{weight}"')
        if dy is not None:
            a.append(f'dy="{_n(dy)}"')
        if opacity is not None:
            a.append(f'opacity="{opacity}"')
        self._ext(y - size * 0.86, y + size * 0.30)
        self.raw(f'<text {" ".join(a)}>{esc(s)}</text>')

    def rect(self, x, y, w, h, *, fill="none", stroke=INK, rx=3, sw=1,
             dash=None):
        a = [f'x="{_n(x)}"', f'y="{_n(y)}"', f'width="{_n(w)}"',
             f'height="{_n(h)}"', f'rx="{rx}"', f'fill="{fill}"',
             f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        self._ext(y, y + h)
        self.raw(f'<rect {" ".join(a)}/>')

    def circle(self, cx, cy, r, *, fill="none", stroke=INK, sw=1):
        self._ext(cy - r, cy + r)
        self.raw(f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(r)}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, x1, y1, x2, y2, *, stroke=INK, sw=1, dash=None, arrow=False):
        a = [f'x1="{_n(x1)}"', f'y1="{_n(y1)}"', f'x2="{_n(x2)}"',
             f'y2="{_n(y2)}"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        if arrow:
            a.append(f'marker-end="url(#{self._need_arrow(stroke)})"')
        self._ext(min(y1, y2), max(y1, y2))
        self.raw(f'<line {" ".join(a)}/>')

    def path(self, d, *, stroke=INK, sw=1, fill="none", dash=None, arrow=False,
             ext=None):
        a = [f'd="{d}"', f'fill="{fill}"', f'stroke="{stroke}"',
             f'stroke-width="{sw}"']
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        if arrow:
            a.append(f'marker-end="url(#{self._need_arrow(stroke)})"')
        if ext:
            self._ext(*ext)
        self.raw(f'<path {" ".join(a)}/>')

    def _need_arrow(self, color):
        """每种颜色一个 marker。

        本来想用 marker 的 fill="context-stroke" 一个通吃，但那是 SVG 2 的
        特性，iOS Safari 16.4 之前不认——箭头会变成黑色实心，深色模式下
        直接看不见。按颜色各出一个 marker，兼容到底。
        """
        # 不能用 hash(color) 编号：Python 3 的字符串 hash 每次进程都不一样，
        # 生成出来的 id 会随机变，整个 index.html 的 diff 天天在动。按出现
        # 顺序编号，同样的输入永远得到同样的字节。
        if color not in self._markers:
            self._markers[color] = f"a{len(self._markers)}"
        return self._markers[color]

    # ── 排版 ────────────────────────────────────────────────────
    def gap(self, h=9):
        self.y = max(self.y, self.ymax) + h

    def title(self, s, *, size=10.5, mono=True, fill=MUTE):
        """整张图最上面那行说明。"""
        self.y += size
        self.text(PAD, self.y, s, size=size, fill=fill, anchor="start",
                  mono=mono)
        self.y += 5

    def caption(self, s, *, size=10, fill=MUTE, mono=False, indent=0,
                weight=None):
        """一行小字注解，跟在图下面。"""
        self.y += size
        self.text(PAD + indent, self.y, s, size=size, fill=fill,
                  anchor="start", mono=mono, weight=weight)
        self.y += 3

    # ── 数组 / 字符串 ───────────────────────────────────────────
    def row(self, vals, *, cw=None, h=21, idx=None, x0=None, gap=1,
            hl=(), hlfill=None, mono=True, size=10.5, fills=None,
            strokes=None):
        """一排格子。返回 (x0, y, cw, gap, n)，后面的 span/ptr 拿它定位。

        vals 可以是字符串（每个字符一格）或列表。
        hl   要高亮的下标集合。
        idx  True 在下方标 0..n-1；也可以传一个列表当自定义标签。
        """
        items = list(vals)
        n = len(items)
        if cw is None:
            longest = max((len(str(v)) for v in items), default=1)
            cw = max(19, min(30, 8 * longest + 11))
        total = n * cw + (n - 1) * gap
        if x0 is None:
            x0 = (self.w - total) / 2
        y = self.y
        for i, v in enumerate(items):
            x = x0 + i * (cw + gap)
            on = i in hl
            fc = fills[i] if fills else None
            sc = strokes[i] if strokes else None
            self.rect(x, y, cw, h,
                      fill=fc or ((hlfill or HI) if on else FILL),
                      stroke=sc or (AC if on else INK), sw=1.2 if on else 1)
            self.text(x + cw / 2, y + h / 2 + 3.6, v, size=size,
                      fill=sc or (AC if on else INK), mono=mono,
                      weight="700" if (on or sc) else None)
        self.y = y + h
        if idx:
            labels = range(n) if idx is True else idx
            self.y += 9
            for i, lab in enumerate(labels):
                self.text(x0 + i * (cw + gap) + cw / 2, self.y, lab,
                          size=8.5, fill=MUTE, mono=True)
            self.y += 2
        # 第 7 项 = 这一排真正的底边（含下标标签）。span / ptr 拿它定位，
        # 不然带 idx 的行上，区间标签会压在 0 1 2 3 那一行上。
        return (x0, y, cw, gap, n, h, self.y)

    @staticmethod
    def cx(r, i):
        """第 i 格的中心 x。"""
        return r[0] + i * (r[2] + r[3]) + r[2] / 2

    @staticmethod
    def edge(r, i, right=False):
        """第 i 格的左边缘（right=True 取右边缘）。"""
        return r[0] + i * (r[2] + r[3]) + (r[2] if right else 0)

    @staticmethod
    def _bot(r):
        return r[6] if len(r) > 6 else r[1] + r[5]

    def span(self, r, i, j, label="", *, color=AC, below=True, drop=0):
        """在第 i..j 格下方画一条方括号，标一段区间。"""
        x1, x2 = self.edge(r, i), self.edge(r, j, right=True)
        y = (self._bot(r) + 5 + drop) if below else (r[1] - 5 - drop)
        d = 4 if below else -4
        self.path(f"M{_n(x1)} {_n(y + d)} L{_n(x1)} {_n(y)} "
                  f"L{_n(x2)} {_n(y)} L{_n(x2)} {_n(y + d)}",
                  stroke=color, sw=1.2)
        if label:
            ly = y + d + 10 if below else y + d - 4
            self.text((x1 + x2) / 2, ly, label, size=9.5, fill=color)
            self.y = max(self.y, ly + 3)
        else:
            self.y = max(self.y, y + d + 2)

    def ptr(self, r, i, label, *, color=AC, above=True, drop=0):
        """指向第 i 格的小三角 + 标签。"""
        x = self.cx(r, i)
        if above:
            top = r[1] - 4 - drop
            self.path(f"M{_n(x)} {_n(top)} l-3.5 -5 l7 0 Z", fill=color,
                      stroke="none")
            self.text(x, top - 7, label, size=9.5, fill=color)
        else:
            bot = self._bot(r) + 4 + drop
            self.path(f"M{_n(x)} {_n(bot)} l-3.5 5 l7 0 Z", fill=color,
                      stroke="none")
            self.text(x, bot + 14, label, size=9.5, fill=color)
            self.y = max(self.y, bot + 17)

    # ── 二叉树 ──────────────────────────────────────────────────
    def tree(self, spec, *, r=12, vgap=34, hl=(), hledge=(), x0=None,
             span=None, size=10.5, color=None, hifill=None):
        """spec 是嵌套元组 (val, left, right)，None 表示空。

        按<b>中序</b>位置排 x、按深度排 y —— 这样任何形状的树都不会重叠。
        hl      要强调的节点值集合
        hledge  要强调的边，写成 (父值, 子值)
        返回 {值: (x, y)}，方便调用方再画标注。
        """
        # 先给每个节点编中序号
        order = []

        def walk(node, depth):
            if node is None:
                return
            val, left, right = node
            walk(left, depth + 1)
            order.append((val, depth))
            walk(right, depth + 1)

        hifill = hifill or (HI if (color in (None, AC)) else FILL)
        color = color or AC
        walk(spec, 0)
        n = len(order)
        avail = (span or (self.w - 2 * PAD - 2 * r))
        step = avail / max(1, n - 1) if n > 1 else 0
        left0 = (x0 if x0 is not None else (self.w - step * (n - 1)) / 2)
        pos = {}
        for i, (val, depth) in enumerate(order):
            pos[val] = (left0 + i * step, self.y + r + depth * vgap)

        # 边先画，节点后画（节点要盖住边的端点）
        def edges(node):
            if node is None:
                return
            val, left, right = node
            for child in (left, right):
                if child is not None:
                    a, b = pos[val], pos[child[0]]
                    on = (val, child[0]) in hledge
                    self.line(a[0], a[1], b[0], b[1],
                              stroke=color if on else INK, sw=2 if on else 1)
                    edges(child)

        edges(spec)
        for val, (x, y) in pos.items():
            on = val in hl
            self.circle(x, y, r, fill=hifill if on else FILL,
                        stroke=color if on else INK, sw=1.8 if on else 1)
            self.text(x, y + 3.6, val, size=size, fill=color if on else INK,
                      weight="700" if on else None)
        self.y = max(y for _, y in pos.values()) + r
        return pos

    # ── 链表 ────────────────────────────────────────────────────
    def chain(self, vals, *, bw=None, h=22, gap=18, x0=None, hl=(),
              labels=None, size=10.5):
        """一排方块 + 中间的 next 箭头。返回 {下标: (中心x, 顶y, 宽)}。"""
        items = list(vals)
        n = len(items)
        if bw is None:
            bw = max(24, min(40, (self.w - 2 * PAD - (n - 1) * gap) / n))
        total = n * bw + (n - 1) * gap
        if x0 is None:
            x0 = (self.w - total) / 2
        y = self.y
        pos = {}
        for i, v in enumerate(items):
            x = x0 + i * (bw + gap)
            on = i in hl
            self.rect(x, y, bw, h, fill=HI if on else FILL,
                      stroke=AC if on else INK, sw=1.4 if on else 1)
            self.text(x + bw / 2, y + h / 2 + 3.6, v, size=size,
                      fill=AC if on else INK, weight="700" if on else None)
            pos[i] = (x + bw / 2, y, bw)
            if i:
                px = x0 + (i - 1) * (bw + gap) + bw
                self.line(px + 2, y + h / 2, x - 3, y + h / 2, arrow=True,
                          stroke=MUTE)
        self.y = y + h
        if labels:
            self.y += 9
            for i, lab in enumerate(labels):
                if lab:
                    self.text(pos[i][0], self.y, lab, size=8.5, fill=MUTE)
            self.y += 2
        return pos

    def hop(self, pos, i, j, *, label="", color=AC, up=True, lift=16,
            dash=None):
        """从第 i 块到第 j 块画一条弧线（random 指针、回边都用它）。"""
        (x1, y1, _), (x2, y2, _) = pos[i], pos[j]
        if up:
            ya = y1 - 1
            c = min(y1, y2) - lift
        else:
            ya = y1 + 22 + 1
            c = max(y1, y2) + 22 + lift
        self.path(f"M{_n(x1)} {_n(ya)} Q{_n((x1 + x2) / 2)} {_n(c)} "
                  f"{_n(x2)} {_n(ya)}", stroke=color, sw=1.2, arrow=True,
                  dash=dash)
        if label:
            self.text((x1 + x2) / 2, c + (-3 if up else 10), label, size=9,
                      fill=color)
        if up:
            self.y = max(self.y, y1 + 22)

    # ── 栈 ──────────────────────────────────────────────────────
    def stack(self, items, *, x, y=None, bw=44, h=18, label="", top_label=""):
        """从下往上堆的格子。items[0] 是栈底。"""
        y = self.y if y is None else y
        n = max(1, len(items))
        base = y + n * h
        for i, v in enumerate(items):
            yy = base - (i + 1) * h
            self.rect(x, yy, bw, h, fill=FILL, stroke=INK)
            self.text(x + bw / 2, yy + h / 2 + 3.4, v, size=9.5, mono=True)
        if not items:
            self.rect(x, base - h, bw, h, fill="none", stroke=MUTE, dash="3 3")
            self.text(x + bw / 2, base - h / 2 + 3.4, "空", size=9, fill=MUTE)
        if label:
            self.text(x + bw / 2, base + 11, label, size=9, fill=MUTE)
        if top_label:
            self.text(x + bw / 2, base - n * h - 5, top_label, size=9, fill=AC)
        self.y = max(self.y, base + (13 if label else 2))
        return base

    # ── 柱状图（找峰、单调栈这类「高低」题）────────────────────
    def bars(self, vals, *, h=54, bw=None, gap=3, hl=(), labels=None,
             color=None, size=9.5):
        """按值高矮画一排柱子。返回 (x0, ybase, bw, gap, n)。"""
        vals = list(vals)
        n = len(vals)
        lo, hi = min(vals), max(vals)
        rng = (hi - lo) or 1
        if bw is None:
            bw = (self.w - 2 * PAD - (n - 1) * gap) / n
        x0 = (self.w - (n * bw + (n - 1) * gap)) / 2
        base = self.y + 11 + h      # +11 = 给最高那根柱子的数值标签留一行
        for i, v in enumerate(vals):
            bh = 8 + (v - lo) / rng * (h - 8)
            x = x0 + i * (bw + gap)
            on = i in hl
            self.rect(x, base - bh, bw, bh, rx=2,
                      fill=HI if on else FILL,
                      stroke=(color or AC) if on else INK, sw=1.3 if on else 1)
            self.text(x + bw / 2, base - bh - 4, v, size=size,
                      fill=(color or AC) if on else MUTE, mono=True)
        self.y = base
        if labels:
            self.y += 9
            for i, lab in enumerate(labels):
                if lab != "":
                    self.text(x0 + i * (bw + gap) + bw / 2, self.y, lab,
                              size=8.5, fill=MUTE, mono=True)
            self.y += 2
        return (x0, base, bw, gap, n)

    # ── 自由摆位的图（约束图、账号-邮箱这类）────────────────────
    def graph(self, nodes, edges, *, r=12, size=10.5, hl=(), directed=True,
              hledge=(), color=None):
        """nodes: {名字: (x, y)}，y 相对当前游标。edges: [(a, b, 可选标签)]。"""
        color = color or AC
        pos = {k: (x, self.y + y) for k, (x, y) in nodes.items()}
        for e in edges:
            a, b = e[0], e[1]
            lab = e[2] if len(e) > 2 else ""
            (x1, y1), (x2, y2) = pos[a], pos[b]
            dx, dy = x2 - x1, y2 - y1
            d = (dx * dx + dy * dy) ** 0.5 or 1
            ux, uy = dx / d, dy / d          # 端点缩到圆周上，箭头才不会插进节点里
            on = (a, b) in hledge
            self.line(x1 + ux * r, y1 + uy * r, x2 - ux * (r + 3),
                      y2 - uy * (r + 3), arrow=directed,
                      stroke=color if on else INK, sw=1.6 if on else 1)
            if lab:
                self.text((x1 + x2) / 2, (y1 + y2) / 2 - 4, lab, size=8.5,
                          fill=MUTE)
        for k, (x, y) in pos.items():
            on = k in hl
            self.circle(x, y, r, fill=HI if on else FILL,
                        stroke=color if on else INK, sw=1.6 if on else 1)
            self.text(x, y + 3.6, k, size=size, fill=color if on else INK,
                      weight="700" if on else None)
        return pos

    # ── 网格（岛屿、矩阵 BFS 这类）──────────────────────────────
    def grid(self, rows, *, cell=26, x0=None, fills=None, strokes=None,
             size=10.5, coords=False):
        """rows 是一个二维列表（字符串也行，一个字符一格）。

        fills / strokes 同形状，None 表示用默认色。返回 (x0, y0, cell)。
        """
        rows = [list(r) for r in rows]
        h, w = len(rows), max(len(r) for r in rows)
        if x0 is None:
            x0 = (self.w - w * cell) / 2
        y0 = self.y
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                fc = fills[i][j] if fills else None
                sc = strokes[i][j] if strokes else None
                self.rect(x0 + j * cell, y0 + i * cell, cell, cell, rx=2,
                          fill=fc or FILL, stroke=sc or INK, sw=1)
                self.text(x0 + j * cell + cell / 2,
                          y0 + i * cell + cell / 2 + 3.6, v, size=size,
                          fill=sc or INK, mono=True,
                          weight="700" if sc else None)
        self.y = y0 + h * cell
        if coords:
            self.y += 9
            for j in range(w):
                self.text(x0 + j * cell + cell / 2, self.y, j, size=8,
                          fill=MUTE, mono=True)
            self.y += 2
        return (x0, y0, cell)

    # ── 区间条（会议室、合并区间、区间交集）──────────────────────
    def bands(self, items, *, lo=None, hi=None, bh=13, vgap=5, ticks=None,
              label_w=0):
        """items: [(起, 止, 标签, 颜色)]，每条占一行，共用一根数轴。

        标签写在条子右边；颜色省略则用 AC。
        """
        vals = [v for it in items for v in it[:2]]
        lo = min(vals) if lo is None else lo
        hi = max(vals) if hi is None else hi
        span = (hi - lo) or 1
        left, right = PAD + 4, self.w - PAD - 4 - label_w
        sx = lambda v: left + (v - lo) / span * (right - left)
        y = self.y
        for k, it in enumerate(items):
            a, b, lab = it[0], it[1], (it[2] if len(it) > 2 else "")
            col = it[3] if len(it) > 3 else AC
            yy = y + k * (bh + vgap)
            self.rect(sx(a), yy, max(3, sx(b) - sx(a)), bh, rx=2,
                      fill=HI if col in (AC, None) else FILL, stroke=col,
                      sw=1.3)
            if lab:
                self.text(sx(b) + 5, yy + bh / 2 + 3.4, lab, size=9,
                          fill=col, anchor="start")
        self.y = y + len(items) * (bh + vgap) - vgap
        if ticks:
            self.y += 10
            self.line(left, self.y - 5, right, self.y - 5, stroke=MUTE)
            for t in ticks:
                self.line(sx(t), self.y - 8, sx(t), self.y - 2, stroke=MUTE)
                self.text(sx(t), self.y + 5, t, size=8.5, fill=MUTE, mono=True)
            self.y += 8
        return sx

    # ── 输出 ────────────────────────────────────────────────────
    def done(self, *, pad=4):
        top = min(self.ymin, 0)
        h = max(self.y, self.ymax) - top + 2 * pad
        shift = pad - top
        defs = ""
        if self._markers:
            ms = "".join(
                f'<marker id="{mid}" viewBox="0 0 8 8" refX="7" refY="4" '
                f'markerWidth="5" markerHeight="5" orient="auto">'
                f'<path d="M0 0.5 L8 4 L0 7.5 z" fill="{color}"/></marker>'
                for color, mid in self._markers.items())
            defs = f"<defs>{ms}</defs>"
        body = "".join(self.parts)
        if abs(shift) > 0.05:
            body = f'<g transform="translate(0 {_n(shift)})">{body}</g>'
        return (f'<svg class="fig" viewBox="0 0 {self.w} {_n(h)}" '
                f'role="img" xmlns="http://www.w3.org/2000/svg">'
                + defs + body + "</svg>")
