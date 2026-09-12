# -*- coding: utf-8 -*-
# 概念卡：("C", section, 标题, 正面 HTML, [背面 block])。标题跨语言必须一致。
from grindcards.helpers import *

CONCEPTS = [

("C", "ARRAYS & HASHING", "Hashmap as Memory",
 "<span class='lead'>哈希表把 O(n) 的查找压成 O(1)，代价是 O(n) 空间。</span>大多数数组题最后都归结成一个问题：<b>key 存什么</b>？——以及什么时候写、什么时候读？",
 [K("<b>用「答案的形状」当 key。</b>找配对 → key 是补数；找分组 → key 是规范形式；找子数组 → key 是前缀和。想清楚 key 就想清楚了整题。"),
  K("<b>先查后插</b>：查的那一刻 map 里只有左边的元素，所以匹配到的一定不是自己。Two Sum、Subarray Sum 都靠这一条免掉特判。"),
  T(["要找什么", "key 存什么", "题"],
     [["两数配对", "<code>target - x</code>", "Two Sum"],
     ["同构分组", "规范形式（排序串 / 计数元组）", "Group Anagrams"],
     ["连续子数组", "前缀和（或 % k）", "Subarray Sum Equals K"],
     ["最近一次出现", "元素 → 最后下标", "Longest Substring No Repeat"],
     ["频率", "元素 → 次数", "Top K Frequent"]]),
  W("<b>list 不可 hash</b>，当 key 必须转 <code>tuple</code>；set/dict 也不行，用 <code>frozenset</code>。"),
  CX("平均 O(1) 查改；最坏 O(n)（哈希冲突，面试里一般不追究）"),
  MORE(),
  P("<b>什么时候不该用哈希表</b>：数组已经有序（双指针更省空间）、值域很小（数组/计数桶更快）、要求 O(1) 空间（原地标记：把 <code>nums[abs(v)-1]</code> 置负当访问标记）。"),
  P("<code>Counter</code> 和 <code>defaultdict</code> 省掉大量样板：<code>Counter(nums)</code> 一行统计频率、<code>freq[missing]</code> 返回 0 不报 KeyError、<code>defaultdict(list)</code> 直接 append 不用先建空列表。")]),

("C", "TWO POINTERS", "Opposite Ends",
 "<span class='lead'>两个指针从数组两端往中间走，每步淘汰一端。</span>数据得满足什么条件这招才成立？<b>每一步怎么决定动哪个指针</b>？",
 [K("前提：数组<b>有序</b>，或者「移动某一端能单调地改善/恶化目标」。没有这个单调性，两端指针就是瞎猜。"),
  K("移动规则：<b>看当前状态离目标差在哪一边</b>，就动那一边。和太小 → 左指针右移（唯一能变大的操作）。"),
  C("""l, r = 0, len(a) - 1
while l < r:
    s = a[l] + a[r]
    if s == target: return [l, r]
    if s < target:  l += 1        # 只有左移能变大
    else:           r -= 1"""),
  W("<code>while l &lt; r</code> 还是 <code>l &lt;= r</code>？取两个不同元素用 <code>&lt;</code>；允许同一个元素（如二分查找式的收缩）才用 <code>&lt;=</code>。"),
  CX("O(n) time / O(1) space —— 比排序后二分的 O(n log n) 好"),
  MORE(),
  T(["题", "怎么用"],
     [["Two Sum II (有序)", "和小了左移，和大了右移"],
     ["3Sum", "固定一个数 + 剩下两端夹逼，先排序"],
     ["Container With Most Water", "动<b>矮</b>的那边（动高的只会更差）"],
     ["Trapping Rain Water", "动 max 较小的那边"],
     ["Valid Palindrome", "两端比较，跳过非字母"]]),
  P("<b>3Sum 去重</b>：外层 <code>if i &gt; 0 and a[i] == a[i-1]: continue</code>；内层找到答案后 <code>while l &lt; r and a[l] == a[l+1]: l += 1</code>。两处都要。")]),

("C", "SLIDING WINDOW", "The Shrink Rule",
 "<span class='lead'>窗口 [l, r] 在数组上滑动，右指针扩张，左指针收缩。</span><b>什么时候收缩 <code>left</code>？</b>一条规则把这一整类题分成两派。",
 [K("找<b>最长</b> → <b>不合法</b>时缩 left ｜ 找<b>最短</b> → <b>合法</b>时缩 left"),
  T(["目标", "何时缩 left", "窗口维护"],
     [["最长子串", "不合法时缩", "set / Counter"],
     ["最短子串", "合法时缩", "Counter + have/need"],
     ["固定窗口 k", "r-l+1 &gt; k 时缩", "sum / Counter"]]),
  C("""l = 0
for r in range(n):
    加入 a[r]
    while 需要收缩:
        移出 a[l]; l += 1
    更新答案            # 最长在 while 外, 最短在 while 内"""),
  W("<b>前提</b>：合法性随长度<b>单调</b>——加元素只会更不合法，删元素只会更合法。含负数的「和为 k 的最短子数组」不满足，必须改用前缀和 + 哈希。"),
  CX("O(n) —— 每个元素最多进出窗口各一次"),
  MORE(),
  P("<b>答案更新的位置决定了求什么</b>：求最长时在收缩<b>之后</b>更新（此刻窗口合法且尽可能大）；求最短时在收缩<b>循环内</b>更新（每次收缩前都是一个候选解）。写错位置答案会系统性偏大或偏小。"),
  K("话术：「右指针每步扩窗，违反约束时左指针收缩。每个元素最多进出窗口各一次，所以整体 O(n)，而不是暴力枚举的 O(n²)。」")]),

("C", "PREFIX SUM", "Subarray Sum with Hashmap",
 "<span class='lead'>求「和为 k 的子数组」，数组里可能有负数，滑动窗口失效。</span>前缀和存进哈希表。<b>到底查的是什么</b>？表里一开始必须放什么？",
 [K("<code>sum(i..j) = pre[j] - pre[i-1]</code>。要 <code>== k</code>，就查 <b><code>pre[j] - k</code> 之前出现过几次</b>。"),
  W("<b>map 必须以 <code>{0: 1}</code> 起手</b>——代表「空前缀」，否则从下标 0 开始的子数组全部漏掉。这是本类题第一大坑。"),
  C("""seen = {0: 1}            # 空前缀出现过一次!
pre = res = 0
for x in nums:
    pre += x
    res += seen.get(pre - k, 0)   # 先查
    seen[pre] = seen.get(pre, 0) + 1   # 后插"""),
  W("<b>先查后插</b>，和 Two Sum 同一个道理：查的那一刻 map 里只有左边的前缀，保证子数组非空。"),
  CX("O(n) time / O(n) space"),
  MORE(),
  T(["变体", "map 的 key 换成"],
     [["和为 k 的个数", "前缀和"],
     ["和能被 k 整除", "前缀和 <b>% k</b>"],
     ["0/1 数量相等", "把 0 记成 -1，找前缀和相同"],
     ["最长的那个", "存<b>最早</b>出现的下标，不要覆盖"]]),
  P("求<b>个数</b>用计数 map；求<b>最长</b>用「值 → 最早下标」的 map，且 <b>只在 key 不存在时才写入</b>，否则会把更早的下标覆盖掉。")]),

("C", "BINARY SEARCH", "The F→T Boundary",
 "<span class='lead'>二分不只用于有序查找。</span>所有二分本质上都在问<b>同一个问题</b>。是什么？你<b>唯一</b>要决定的又是什么？",
 [K("每个二分 = 找单调谓词 <code>p(i)</code> 的 <b>F→T 边界</b>。唯一要想的：p(i) 是什么。"),
  C("""lo, hi = 0, n              # hi = n, 不是 n-1
while lo < hi:
    mid = (lo + hi) // 2
    if p(mid): hi = mid        # 可能就是答案 -> 保留
    else:      lo = mid + 1    # 丢掉 mid 及左边
return lo                      # 第一个 True; 全 False 则 == n"""),
  T(["要找", "p(i)", "返回"],
     [["first &gt;= x", "a[i] &gt;= x", "lo"],
     ["first &gt; x", "a[i] &gt; x", "lo"],
     ["last &lt;= x", "a[i] &gt; x", "lo-1"],
     ["last &lt; x", "a[i] &gt;= x", "lo-1"]]),
  W("<b>永远别写 <code>lo = mid</code></b>（死循环）。用本模板就永远不需要 <code>(l+r+1)//2</code> 那个变体。<code>lo-1</code> 的分支要判 <code>lo == 0</code>。"),
  CX("O(log n)"),
  MORE(),
  P("<b>存在性判断必须两步</b>：<code>i = bisect_left(a, x)</code> 然后 <code>i &lt; len(a) and a[i] == x</code>。只判 <code>i &lt; len(a)</code> 是错的——那只说明有位置，不说明值相等。"),
  P("Python 自带：<code>bisect_left</code> = lower_bound，<code>bisect_right</code> = upper_bound，<code>bisect_right - bisect_left</code> = x 的出现次数。面试能用就用，但要能手写。")]),

("C", "STACK", "Parsing & Matching",
 "<span class='lead'>括号匹配、表达式求值、路径化简——都是「后进先出」。</span>这些题共同的形状是什么？输入是一个算式时，<b>栈里压的是什么</b>？",
 [K("规律：<b>遇到「开」就压栈，遇到「闭」就弹栈结算</b>。栈里存的是「还没结算完的上下文」。"),
  C("""# 括号: 压左括号的 index (为了知道位置)
# 表达式: 压数字, 遇到低优先级运算符才结算
# 路径: 压目录名, 遇到 '..' 就 pop

# Basic Calculator II 骨架
stack, num, op = [], 0, '+'
for i, ch in enumerate(s + '+'):        # 末尾哨兵强制结算
    if ch.isdigit(): num = num * 10 + int(ch)
    elif ch in '+-*/':
        if   op == '+': stack.append(num)       # / 向零取整
        elif op == '-': stack.append(-num)
        elif op == '*': stack.append(stack.pop() * num)
        else:           stack.append(int(stack.pop() / num))
        num, op = 0, ch
return sum(stack)"""),
  W("Python 的 <code>//</code> 对负数是<b>向下</b>取整（<code>-7//2 == -4</code>），题目通常要<b>向零</b>取整 → 写 <code>int(a/b)</code>。"),
  MORE(),
  P("<b>为什么用「上一个运算符」而不是当前的</b>：读到运算符时，它左边的数才刚读完。所以每次结算的是<b>上一轮</b>的 op，末尾补一个哨兵运算符把最后一个数结算掉。"),
  P("同款：Valid Parentheses、Simplify Path、Decode String、Remove All Adjacent Duplicates、Exclusive Time of Functions。")]),

("C", "TREES", "Design the DFS Return Value",
 "<span class='lead'>大多数二叉树题都是一次后序遍历。</span>全部难点只在一个决定上。<b>是哪个</b>？为什么那么多树题需要两个不同的量？",
 [K("唯一要设计的：<b>递归函数返回什么</b>。「返回值」= 子树向上汇报的信息，通常和最终答案<b>不是同一个东西</b>。"),
  P("经典分裂：<b>向上返回</b>「以我为端点的最优值」，<b>用全局变量</b>记录「经过我的最优值」。因为路径经过我拐弯后就不能再往上延伸了。"),
  C("""self.best = 0
def dfs(node):                    # 返回: 以 node 为端点向下的最大深度
    if not node: return 0
    L, R = dfs(node.left), dfs(node.right)
    self.best = max(self.best, L + R)   # 经过 node 的路径(拐弯)
    return 1 + max(L, R)                # 向上只能选一边
dfs(root); return self.best"""),
  W("<b>直径 = 边数</b>，深度 = 节点数。Diameter of Binary Tree 里 <code>L + R</code> 就是边数，不需要 +1。差一是这题最常见的错。"),
  CX("O(n) time / O(h) space（递归栈，h 为树高）"),
  MORE(),
  T(["题", "返回值", "全局答案"],
     [["Diameter", "向下最大深度", "max(L+R)"],
     ["Max Path Sum", "max(0, 向下最大和)", "max(L+R+val)"],
     ["Balanced Tree", "高度，不平衡返回 -1", "—（提前剪枝）"],
     ["LCA", "找到的节点或 None", "—（返回值即答案）"]]),
  P("<b>Max Path Sum 的 <code>max(0, ...)</code></b>：子树和为负就当作不选（返回 0），因为路径可以在这里断掉。漏了这一步全负数的树会算错。")]),

("C", "GRAPHS", "Topological Sort",
 "<span class='lead'>一堆任务有先后依赖，要排出一个合法的执行顺序。</span>Kahn 算法的四步循环是什么？不加任何额外记录，怎么<b>判环</b>？",
 [K("in_degree == 0 入队 → 取出 → 邻居 -1 → 变 0 入队。"),
  K("判环：<code>len(result) != len(all_nodes)</code> → 有环。剩下的节点互相锁死，入度永远降不到 0。"),
  C("""graph = defaultdict(set)                    # set 防重复边!
indeg = {n: 0 for n in all_nodes}           # 别漏孤立节点!
for pre, cur in edges:
    if cur not in graph[pre]:
        graph[pre].add(cur); indeg[cur] += 1
q = deque(n for n in all_nodes if indeg[n] == 0)
while q:
    node = q.popleft(); res.append(node)
    for nb in graph[node]:
        indeg[nb] -= 1
        if indeg[nb] == 0: q.append(nb)"""),
  W("坑1 邻接表用 <b>set</b>：重复边会把入度多加，节点永远出不来。坑2 <code>indeg</code> 要<b>初始化全部节点</b>，只从 edges 建会漏掉孤立点。"),
  CX("O(V + E) time / O(V + E) space"),
  MORE(),
  P("<b>DFS 版</b>：后序遍历 + 三色标记（白未访问 / 灰在栈上 / 黑已完成），<b>灰色遇到灰色 = 有环</b>，结果取逆序。Kahn 更直观且天生判环，面试推荐 Kahn。"),
  P("<b>要最短完成时间</b>（Parallel Courses）就按<b>层</b>做 BFS，层数即答案。要<b>字典序最小</b>的拓扑序，把 queue 换成 min-heap。")]),

("C", "DYNAMIC PROG.", "1D vs 2D State",
 "<span class='lead'>状态该开一维还是二维？</span>维数不是风格问题。<b>由什么决定</b>？",
 [K("<b>维度 = 独立变化的输入个数</b>。一个序列 → dp[i]；两个序列 → dp[i][j]；一个序列 + 一个预算/容量 → dp[i][w]。"),
  T(["类型", "状态含义", "典型题"],
     [["1D 线性", "以 i <b>结尾</b>/前 i 个的最优", "House Robber, Coin Change, LIS"],
     ["2D 双序列", "s1 前 i 个与 s2 前 j 个", "LCS, Edit Distance"],
     ["2D 网格", "走到 (i,j) 的最优", "Unique Paths, Min Path Sum"],
     ["背包", "前 i 个物品、容量 w", "0/1 Knapsack, Partition Equal Subset"]]),
  W("<b>「以 i 结尾」和「前 i 个」是不同的状态定义</b>。最大子数组和必须用「以 i 结尾」（否则转移断不掉），LIS 也是。House Robber 用「前 i 个」。选错定义转移就写不出来。"),
  MORE(),
  C("""# 双序列表开 (m+1) x (n+1), 第 0 行/列 = 空串 = base case 白送
for i in range(1, m+1):
    for j in range(1, n+1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
return dp[m][n]              # 最后合法下标是 [m][n], 不是 [m+1][n+1]"""),
  W("匹配时必须走<b>对角线</b> <code>dp[i-1][j-1]</code>：字符是一对一配对的，用 <code>dp[i-1][j]</code> 会让同一个字符被重复使用。"),
  P("空间优化：只依赖上一行 → 滚动两行，把<b>短</b>的串放列维度 → O(min(m,n))。注意 <code>cur[j-1]</code> 是本行，<code>prev[j]</code> 是上一行。")]),

]
