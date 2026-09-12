# -*- coding: utf-8 -*-
# 思路配图，lc -> "<svg …>"。用 grindcards.svgdia 画：颜色走 CSS 变量，自动适配深色模式。
from grindcards.svgdia import Fig, INK, MUTE, AC, HI, FILL, BAD, GOOD, PAD

FIG = {}

# ── 1 两数之和：从「往后找」变成「查记忆」 ───────────────────────
f = Fig()
f.title("nums = [3, 8, 11, 4]     target = 12")
f.gap(22)
r = f.row(["3", "8", "11", "4"], cw=48, idx=True, hl={3})
f.ptr(r, 3, "走到这里", color=AC)
f.gap(14)
f.caption("我不去右边找 8，而是问：12 − 4 = 8 之前见过吗？", fill=AC,
          weight="600")
f.gap(10)
f.row(["3 → 0", "8 → 1", "11 → 2"], cw=60, x0=20)
f.text(216, f.y - 6, "seen（只有我左边的数）", size=9.5, fill=MUTE,
       anchor="start")
f.gap(10)
f.caption("命中 → 返回 [1, 3]。查找从 O(n) 变成 O(1)。", fill=GOOD,
          weight="600")
f.gap(14)
f.caption("先查后插，所以查的那一刻表里只有左边的数 ——", fill=INK)
f.caption("自己配自己不可能发生，[6,6] 找 12 也不用特判。", fill=INK)
FIG[1] = f.done()

# ── 49 字母异位词分组：算 key，不做比较 ──────────────────────────
f = Fig()
f.title('["care", "race", "cat"]')
f.gap(12)
f.caption("两两比较：每一对都在重复判断「字母是不是一样多」", fill=BAD,
          weight="600")
f.gap(10)
f.caption("换成给每个词算一个规范形式当 key：", fill=INK, weight="600")
f.gap(8)
for w, key, col in (("care", "(1,0,1,0,1,…,1,…)", AC),
                    ("race", "(1,0,1,0,1,…,1,…)", AC),
                    ("cat", "(1,0,1,0,0,…,1,…)", GOOD)):
    f.row(list(w), cw=26, x0=16, strokes=[col] * len(w))
    f.text(130, f.y - 6, key, size=9, fill=col, anchor="start", mono=True)
    f.gap(8)
f.gap(6)
f.caption("前两个 key 一样 → 自动同组，一次比较都没做。", fill=GOOD,
          weight="600")
f.gap(12)
f.caption("key 用长度 26 的计数数组：O(k)，比 sorted(s) 的 O(k log k) 快。",
          fill=INK, weight="600")
f.gap(6)
f.caption("list 不可 hash，得转成 tuple 才能当字典的 key。")
FIG[49] = f.done()

# ── 11 盛水容器：为什么丢掉矮边是安全的 ──────────────────────────
f = Fig()
f.title("height = [3, 9, 4, 7, 2, 8]")
f.gap(10)
f.bars([3, 9, 4, 7, 2, 8], hl={0, 5}, h=50,
       labels=["l", "", "", "", "", "r"])
f.gap(12)
f.caption("从最宽的一对起步。此后宽度只会变小 ——", fill=INK, weight="600")
f.caption("想让面积变大，唯一的指望是高度。", fill=INK, weight="600")
f.gap(12)
f.caption("而高度由矮的那根（l = 3）封顶。", fill=AC)
f.gap(12)
f.caption("要是留着矮边、只挪高边：", fill=BAD, weight="600")
f.gap(6)
f.bars([3, 9, 4, 7, 2], hl={0, 4}, h=40, color=BAD,
       labels=["l", "", "", "", "r−1"])
f.gap(10)
f.caption("高度顶天还是 3，宽度却更小 —— 必然更差。", fill=BAD)
f.gap(10)
f.caption("矮边和它那侧任何一根搭配都不会更好，所以它参与的",
          fill=GOOD, weight="600")
f.caption("全部剩余组合可以整批淘汰 —— 这才是双指针线性的原因。",
          fill=GOOD)
FIG[11] = f.done()

# ── 3 无重复最长子串：左端一步跳到位 ────────────────────────────
f = Fig()
f.title('s = "abba"     窗口里不许有重复')
f.gap(22)
r = f.row("abba", cw=44, idx=True, hl={2})
f.ptr(r, 2, "r 走到 b，和下标 1 撞了", color=AC)
f.gap(14)
f.caption("一格格缩左端太慢 —— 而且我明明知道它撞在哪：", fill=INK,
          weight="600")
f.caption("last[b] = 1，那左端直接跳到 2，一步到位。", fill=GOOD)
f.gap(26)
r2 = f.row("abba", cw=44, idx=True, hl={3})
f.ptr(r2, 3, "r 走到最后的 a", color=BAD)
f.gap(14)
f.caption("表里 last[a] = 0，可窗口现在是 [2, 3] —— 0 早就在窗外了。",
          fill=BAD, weight="600")
f.gap(4)
f.caption("照跳会把左端从 2 拉回 1，窗口就不是窗口了。", fill=BAD)
f.gap(10)
f.caption("所以守卫是 last[ch] >= l 才跳。这是本题唯一的坑。", fill=INK,
          weight="600")
FIG[3] = f.done()

# ── 560 和为 K 的子数组：区间和变成两个数的差 ────────────────────
f = Fig()
f.title("nums = [1, 2, 3, -3, 3]    k = 3")
f.gap(10)
f.caption("前缀和（pre[-1] = 0 是空前缀）：", fill=INK, weight="600")
f.gap(6)
r = f.row(["0", "1", "3", "6", "3", "6"], cw=48,
          idx=["空", "0", "1", "2", "3", "4"], hl={2, 5})
f.gap(8)
f.caption("走到 j=4 时 pre = 6，要找的是值为 6 − 3 = 3 的前缀和。",
          fill=AC, weight="600")
f.gap(6)
f.caption("表里 3 出现过 2 次（下标 1 和 3）→ 这一步贡献 2 个区间。",
          fill=GOOD)
f.gap(12)
f.caption("所以存的是次数，不是下标 —— 问的是「有多少个」。", fill=INK,
          weight="600")
f.gap(12)
f.caption("有负数就别想滑窗：[1,-1,0], k=0 立刻挂 ——", fill=BAD)
f.caption("右端吞一格，和可能变小，「太大就收缩」根本不成立。", fill=BAD)
FIG[560] = f.done()

# ── 33 旋转有序数组：切开后必有一半是完整有序的 ───────────────────
f = Fig()
f.title("nums = [6,8,9,1,3,4]     断崖只有一个：9 | 1")
f.gap(20)
r = f.row(["6", "8", "9", "1", "3", "4"], cw=40, idx=True)
f.line(f.edge(r, 3), r[1] - 6, f.edge(r, 3), r[1] + r[5] + 4, stroke=BAD,
       sw=1.6, dash="3 2")
f.text(f.edge(r, 3), r[1] - 10, "断崖", size=9, fill=BAD)
f.gap(16)
f.caption("从 mid = 2 切一刀：", fill=INK, weight="600")
f.gap(6)
r2 = f.row(["6", "8", "9", "1", "3", "4"], cw=40,
           hl={0, 1, 2})
f.span(r2, 0, 2, "完整有序 → 比端点就能判", color=GOOD, drop=8)
f.span(r2, 3, 5, "含断崖 → 判不了", color=BAD, drop=8)
f.gap(14)
f.caption("断崖只有一个，所以它最多毁掉一半。另一半必然有序 ——", indent=2)
f.caption("二分要的从来不是整体有序，是「能判断该往哪半走」。", indent=2)
FIG[33] = f.done()

# ── 227 基本计算器 II：栈里存的是「项」 ─────────────────────────
f = Fig()
f.title('"3+2*2-6/4"    栈里存的是已经算完的项')
f.gap(10)
STEPS = [
    ("读到 3，前一个符号 +", ["3"], "压栈"),
    ("读到 2，前一个符号 +", ["3", "2"], "压栈"),
    ("读到 2，前一个符号 *", ["3", "4"], "弹 2，压 2*2"),
    ("读到 6，前一个符号 −", ["3", "4", "-6"], "压 −6"),
    ("读到 4，前一个符号 /", ["3", "4", "-1"], "弹 −6，压 int(−6/4)"),
]
for i, (head, st, note) in enumerate(STEPS):
    f.caption(head, fill=INK, weight="600" if i in (2, 4) else None)
    f.gap(4)
    f.row(st, cw=30, h=19, x0=14, mono=True,
          hl={len(st) - 1} if i in (2, 4) else set())
    f.text(14 + len(st) * 31 + 8, f.y - 5, note, size=9,
           fill=AC if i in (2, 4) else MUTE, anchor="start")
    f.gap(9)
f.gap(2)
f.caption("最后把栈里一加：3 + 4 − 1 = 6", fill=GOOD, weight="600")
f.gap(4)
f.caption("注意 int(−6/4) = −1，而 −6 // 4 = −2。", fill=BAD)
FIG[227] = f.done()

# ── 236 最近公共祖先：让递归自底向上报 ──────────────────────────
f = Fig()
f.title("找 p=1 和 q=7 的 LCA")
f.gap(6)
T = ("8", ("3", ("1", None, None), ("6", ("4", None, None),
                                     ("7", None, None))),
     ("10", None, ("14", None, None)))
f.tree(T, hl={"1", "7", "3"}, hledge={("3", "1"), ("3", "6"), ("6", "7")},
       vgap=30)
f.gap(12)
f.caption("每棵子树只回答一句：「我这里面能交上去的最好答案是谁？」",
          fill=INK, weight="600")
f.gap(8)
f.caption("1 撞见目标 → 返回自己", fill=AC, indent=4)
f.caption("6 只有右边非空 → 把 7 原样上传", fill=AC, indent=4)
f.caption("3 左右都非空 → 目标分居两侧 → 我就是 LCA", fill=GOOD,
          indent=4, weight="600")
f.caption("8 只有左边非空 → 把 3 原样上传", fill=MUTE, indent=4)
f.gap(12)
f.caption("撞见就返回，顺手解决了「p 是 q 的祖先」——", fill=INK)
f.caption("那时答案自然落在 p 上，不用任何特判。", fill=INK)
FIG[236] = f.done()

# ── 124 树中最大路径和：上报一条腿，记录两条腿 ──────────────────
T124 = ("1", ("2", ("4", None, None), ("5", None, None)), ("3", None, None))
f = Fig()
f.gap(6)
f.tree(T124, hl={"2", "4", "5"}, hledge={("2", "4"), ("2", "5")})
f.gap(12)
f.caption("路径 4–2–5 在 2 这里拐弯：4 + 2 + 5 = 11", fill=AC, weight="600")
f.caption("← 这个值只能记进答案", fill=AC, indent=10)
f.gap(3)
f.caption("上报给父节点 1 的是 2 + max(4, 5) = 7", fill=INK, weight="600")
f.caption("← 只带一条腿", fill=INK, indent=10)
f.gap(16)
f.caption("要是 2 把两条腿都上报（11）会怎样：", fill=BAD, weight="600")
f.gap(8)
f.tree(T124, r=11, vgap=28, hl={"2"}, color=BAD,
       hledge={("2", "4"), ("2", "5"), ("1", "2")})
f.gap(10)
f.caption("节点 2 上就有了三条边 —— 那是岔路口，不是一条路径。", fill=BAD)
FIG[124] = f.done()

# ── 207 课程表：能修完 ⟺ 无环 ───────────────────────────────────
f = Fig()
f.title("prerequisites = [[1,0], [2,1]]   箭头指向后修的那门")
f.gap(14)
f.graph({"0": (74, 12), "1": (170, 12), "2": (266, 12)},
        [("0", "1"), ("1", "2")], hl={"0"})
f.gap(14)
f.caption("入度 0 = 先修课全修完了 → 现在就能上。", fill=GOOD,
          weight="600")
f.caption("上完就把它指向的课各减一个入度，谁减到 0 谁进队。", fill=GOOD)
f.gap(16)
f.caption("有环会怎样：[[1,0], [0,1]]", fill=BAD, weight="600")
f.gap(14)
f.graph({"0": (122, 12), "1": (218, 12)},
        [("0", "1"), ("1", "0")], color=BAD, hledge={("0", "1"), ("1", "0")})
f.gap(14)
f.caption("两个入度都是 1，永远降不到 0 —— 一个都进不了队。", fill=BAD)
f.gap(6)
f.caption("所以结尾比的是「出队总数 == numCourses」。", fill=INK,
          weight="600")
FIG[207] = f.done()

# ── 139 单词拆分：贪心的死胡同 + dp[0] 是火种 ─────────────────────
f = Fig()
f.title('s = "cars"    dict = ["car", "ca", "rs"]')
f.gap(12)
f.caption("贪心「每次匹配最长的单词」：", fill=BAD, weight="600")
f.gap(8)
r = f.row("cars", cw=44, idx=True, strokes=[BAD, BAD, BAD, INK])
f.gap(6)
f.span(r, 0, 2, "先吃掉 car …剩一个 s，卡死", color=BAD, drop=2)
f.gap(20)
f.caption("正解是 ca + rs —— 所以不能贪，得允许回头。", fill=GOOD,
          weight="600")
f.gap(14)
f.caption("dp[i] = 前 i 个字符能不能被完整拆开：", fill=INK, weight="600")
f.gap(8)
f.row(["T", "F", "T", "F", "T"], cw=48,
      idx=["dp0", "dp1", "dp2", "dp3", "dp4"], hl={0, 2, 4})
f.gap(10)
f.caption("dp[2] ← dp[0] 且 \"ca\" 在词典里", fill=AC, indent=4)
f.caption("dp[4] ← dp[2] 且 \"rs\" 在词典里", fill=AC, indent=4)
f.gap(12)
f.caption("dp[0] = True 是整张表的火种 —— 空串可拆。", fill=GOOD,
          weight="600")
f.caption("少了它全表都是 False，连 s=\"car\" 都返回 false。", fill=GOOD)
FIG[139] = f.done()

