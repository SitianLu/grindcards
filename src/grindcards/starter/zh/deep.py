# -*- coding: utf-8 -*-
# lc -> dict(pat=(为什么是这个 pattern, 概念卡标题), fq=[(追问, 回答)], var=[(题名含 LC 号, 区别)])

DEEP = {
    1: dict(
        pat=('配对问题 = 用哈希表把「见过的值」变成 O(1) 可查的记忆，'
             '暴力两重循环退化成一次遍历。',
             'Hashmap as Memory'),
        fq=[
            ('有多组答案怎么办？',
             '题目保证唯一。要返回全部就排序 + 双指针 + 跳过重复值（3Sum 的做法）。'),
            ('数组已经有序呢？',
             '双指针从两端夹逼，<b>O(1) 空间</b>，不需要哈希表。'
             '面试官经常用这句把你逼到双指针。'),
            ('能不能不用额外空间？',
             '不排序就不行——不排序时你必须记住见过什么，那就是 O(n) 空间。'),
        ],
        var=[
            ('LC 167 Two Sum II', '输入<b>有序</b> → 双指针，O(1) 空间'),
            ('LC 15 3Sum', '固定一个数 + 双指针，去重要做两处'),
            ('LC 653 Two Sum IV', '输入是 BST → 中序展开成有序数组再双指针'),
            ('Variant: existence only, no indices', '同样是 map，只是不记下标'),
        ],
    ),
    49: dict(
        pat=('分组问题 = 给每个元素算一个<b>规范形式</b>当哈希 key，同 key 自动归为一组。',
             'Hashmap as Memory'),
        fq=[
            ('字符集不限于小写字母呢？',
             '计数数组用不了，改 <code>frozenset(Counter(s).items())</code> '
             '或排序串当 key。'),
            ('为什么计数比排序快？',
             '排序 O(k log k)，计数 O(k)。词长时差距明显，说出来是加分项。'),
            ('能不能不用哈希表？',
             '可以整体排序（按规范形式排），O(nk log n)，但没有理由这么做。'),
        ],
        var=[
            ('LC 242 Valid Anagram', '只判两个词，直接比 Counter'),
            ('LC 438 Find All Anagrams', '定长滑动窗口 + Counter 比较'),
            ('LC 953 Verifying Alien Dictionary', '规范形式换成「按自定义字母序映射后的串」'),
        ],
    ),
    11: dict(
        pat=('贪心 + 双指针：每步移动<b>限制因素</b>那一端，正确性靠交换论证保证。',
             'Opposite Ends'),
        fq=[
            ('为什么可以丢掉矮的那一边？',
             '矮边和任何其他柱子的组合，高度不超过它自己、宽度还更小，不可能更优。'
             '<b>这是必须说清的证明</b>。'),
            ('两边一样高呢？',
             '移哪边都行，丢掉的那条不可能是唯一最优。'),
            ('和接雨水什么区别？',
             '这题只要两根柱子围成的面积；接雨水要算逐格积水，需要左右最大值。'),
        ],
        var=[
            ('LC 42 Trapping Rain Water', '双指针但要维护左右最大值'),
            ('LC 84 Largest Rectangle in Histogram', '单调栈，找左右第一个更矮'),
            ('LC 1793 Maximum Score of a Good Subarray', '同样从中间向两边扩，移矮的一边'),
        ],
    ),
    3: dict(
        pat=('<b>最长</b>类滑窗：不合法时收缩左边界，窗口内维护「无重复」这个约束。',
             'The Shrink Rule'),
        fq=[
            ('字符集多大？',
             '决定空间是 O(128) 还是 O(n)，也决定能不能用定长数组代替哈希表。'),
            ('map 版为什么要判 <code>last[ch] &gt;= l</code>？',
             'map 里可能存着<b>窗口外</b>的旧位置，直接跳会把 l 往回拉。'),
            ('要返回子串本身呢？',
             '记录最优时的 (l, r)，最后切片。'),
        ],
        var=[
            ('LC 159 / 340 At Most K Distinct Characters', '约束从「无重复」变成「种类 ≤ k」'),
            ('LC 424 Char Replacement', '约束变成「非主元素 ≤ k」'),
            ('LC 1004 Max Consecutive Ones III', '同上，0 的个数 ≤ k'),
        ],
    ),
    560: dict(
        pat=('含负数 → 滑窗失效 → 前缀和 + 哈希表，把「区间和为 k」变成「查 pre−k '
             '出现过几次」。',
             'Subarray Sum with Hashmap'),
        fq=[
            ('为什么滑动窗口不行？',
             '有负数时窗口和<b>不单调</b>，扩窗不一定让和变大，收缩条件失去意义。'),
            ('map 为什么要 {0: 1}？',
             '代表空前缀，否则从下标 0 开始的子数组全部漏掉。'),
            ('求最长而不是个数呢？',
             'map 存「前缀和 → <b>最早</b>下标」，且只在 key 不存在时写入。'),
        ],
        var=[
            ('LC 523 Continuous Subarray Sum', 'key 换成前缀和 % k'),
            ('LC 525 Contiguous Array', '0 记成 -1，找前缀和相同的最远两点'),
            ('LC 974 Subarray Sums Divisible by K', '同样取模，注意负数取模'),
        ],
    ),
    33: dict(
        pat=('旋转数组：任意切开后<b>至少一半有序</b>，先判哪半有序，再判 target '
             '在不在其中。',
             'The F→T Boundary'),
        fq=[
            ('有重复元素呢？',
             '<code>nums[lo] == nums[mid]</code> 时无法判断哪半有序，只能 lo += 1 '
             '线性收缩，<b>最坏退化 O(n)</b>。'),
            ('为什么判断有序要带等号？',
             '区间只剩两个元素时 lo == mid，少了等号会走错分支。'),
            ('能不能先找旋转点再二分？',
             '可以，两次二分，思路更直观但代码更长。'),
        ],
        var=[
            ('LC 81 Search in Rotated II', '含重复，最坏 O(n)'),
            ('LC 153 Find Minimum in Rotated', '找旋转点本身'),
            ('LC 852 / 1095 Mountain Array', '同样是「哪半单调」的判断'),
        ],
    ),
    227: dict(
        pat=('表达式求值 = 栈延迟结算：读到运算符时结算的是<b>上一个</b>运算符。',
             'Parsing & Matching'),
        fq=[
            ('带括号怎么办？',
             '遇 ( 把当前结果和符号压栈、清零重来，遇 ) 弹出合并；'
             '或递归处理子表达式（LC 224）。'),
            ('Python 整除的坑？',
             '<code>//</code> 对负数向下取整（-7//2 = -4），题目要向零取整 → 写 '
             '<code>int(a/b)</code>。'),
            ('能不能 O(1) 空间？',
             '能：只有 + − × ÷ 时用两个变量（当前项、总和）代替栈。'),
        ],
        var=[
            ('LC 224 Basic Calculator', '带括号，无乘除'),
            ('LC 772 Basic Calculator III', '括号 + 乘除，递归 + 栈'),
            ('LC 150 Evaluate RPN', '已经是后缀表达式，栈更直接'),
        ],
    ),
    236: dict(
        pat=('树形递归的返回值设计：返回「这棵子树里找到的目标」，左右都非空即为分叉点。',
             'Design the DFS Return Value'),
        fq=[
            ('p 是 q 的祖先怎么办？',
             '命中即返回 p 本身，正好是答案——所以<b>不要继续往下找</b>。'),
            ('BST 版能更快吗？',
             '能，比大小走：都小往左、都大往右、一大一小就是 LCA，O(h) 且不用递归。'),
            ('有 parent 指针呢？',
             '变成「两条链表求交点」：把 p 的祖先存 set，再从 q 往上找第一个命中的。'),
        ],
        var=[
            ('LC 235 LCA of BST', '利用有序性，O(h)'),
            ('LC 1650 LCA III (with parent pointer)', '链表求交点'),
            ('LC 1123 LCA of Deepest Leaves', '返回 (深度, 节点) 二元组'),
        ],
    ),
    124: dict(
        pat=('和求直径同一个骨架，多一个 <code>max(0, ...)</code>：'
             '路径可以在负数子树处断掉。',
             'Design the DFS Return Value'),
        fq=[
            ('为什么要 max(0, ...)？',
             '子树和为负就不选它，路径在这里断掉。漏了它全负数的树会算错。'),
            ('best 初始化成什么？',
             '<code>-inf</code>。初始化成 0 会让全负数的树错误返回 0。'),
            ('路径必须经过根吗？',
             '不必。所以答案在全局变量里，不是返回值。'),
        ],
        var=[
            ('LC 543 Diameter', '算边数，不看节点值'),
            ('LC 687 Longest Univalue Path', '加「值相等」约束'),
            ('LC 1372 Longest ZigZag Path', '返回值要区分左右两个方向'),
        ],
    ),
    207: dict(
        pat=('依赖排序 = 拓扑排序；「能否全部完成」等价于「有没有环」。',
             'Topological Sort'),
        fq=[
            ('怎么判环？',
             '<code>len(result) != n</code>。剩下的节点互相锁死，入度降不到 0——'
             '不需要额外记录。'),
            ('边的方向别搞反',
             '<code>[course, pre]</code> 意思是先修 pre，所以边是 <b>pre → course</b>。'),
            ('要返回具体顺序呢？',
             '把计数换成结果列表；有环时返回空数组（LC 210）。'),
        ],
        var=[
            ('LC 210 Course Schedule II', '返回一个合法顺序'),
            ('LC 269 Alien Dictionary', '边要从相邻单词推出来'),
            ('LC 1136 Parallel Courses', '求最短学期数 → 按<b>层</b>做 BFS'),
        ],
    ),
    139: dict(
        pat=('1D 线性 DP：<code>dp[i]</code> = 前 i 个字符能否拆分，'
             '转移枚举最后一个单词的起点。',
             '1D vs 2D State'),
        fq=[
            ('为什么 dp[0] = True？',
             '空串可拆，是所有转移的基准点。'),
            ('字典要转 set 吗？',
             '<b>必须</b>。否则 <code>in</code> 是线性查找，整体退化。'
             '这是最容易被忽略的性能点。'),
            ('能不能剪枝？',
             '内层 j 从 <code>i − maxWordLen</code> 开始——'
             '比最长单词还长的切片不可能在字典里。'),
        ],
        var=[
            ('LC 140 Word Break II', '返回所有方案 → 回溯 + 记忆化，最坏指数级'),
            ('LC 472 Concatenated Words', '对每个词跑一次 Word Break'),
            ('LC 91 Decode Ways', '同样 1D，转移只看最后 1~2 个字符'),
        ],
    ),
}
