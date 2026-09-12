# -*- coding: utf-8 -*-
# lc -> dict(idea=[3–6 条], code="...", keys=[..., 最后一条是复杂度], test="表达式", want=值)
#
# idea 是推导过程：第一人称、现在时、像面试时边想边说，死胡同也保留。
# code 必须能跑：`grindcards verify` 会执行它并和 want 比对。每行 ≤ 64 列。

SOL = {
    1: dict(
        idea=[
            '笨办法：对每个 x，去右边把 <code>target − x</code> 找一遍。O(n²)。',
            '开销全在<b>找</b>上 ——而且我每次扫的那片右边，和上一轮几乎一模一样。'
            '同一批数被反复看，这就是要干掉的地方。',
            '那把方向反过来：走到 x 的时候不去右边找，而是问「<code>target − '
            'x</code> 我<b>之前</b>见过吗」。从「找」变成「查记忆」，一步 O(1)。',
            '顺带一个白捡的好处：查的那一刻 <code>seen</code> 里只有 x '
            '<b>左边</b>的数，所以自己配自己不可能发生，重复值也不用特判。',
        ],
        code="""
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}                          # 值 -> 下标
    for i, x in enumerate(nums):
        if target - x in seen:         # ① 先查：此时表里只有 x 左边的数
            return [seen[target - x], i]
        seen[x] = i                    # ② 后插
    return []
""",
        keys=[
            '<b>先查后插</b>。顺序反了，<code>[3,3], t=6</code> 会用同一个下标配自己。',
            '坑：我当初用双 map 特判 duplicate → <code>[3,2,4], t=6</code> 返回 '
            '<code>(0,0)</code>。先查后插一遍搞定，别打补丁。',
            'O(n) time / O(n) space',
        ],
        test='twoSum([3, 8, 11, 4], 12)',
        want=[1, 3],
    ),
    49: dict(
        idea=[
            '两两比较是 O(n²·k)，而且每一对都在做同一件事：判断两个词的字母是不是一样多。',
            '那就别比较了 ——给每个词算一个<b>规范形式</b>当 key，'
            '字母一样多的词自然算出同一个 key，同 key 自动同组。那 O(n²) '
            '的比较全省了。',
            '规范形式取什么？两个词是 anagram ⟺ 字符<b>多重集</b>相同。'
            '排序后的串可以，但那是 O(k log k)；题目限定小写字母，用长度 26 '
            '的计数数组只要 O(k)。',
            '计数数组是 list，不可 hash，当不了字典的 key —— 转成 tuple。',
        ],
        code="""
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        cnt = [0] * 26                 # ① 每个词都要新建一份
        for ch in s:
            cnt[ord(ch) - 97] += 1
        groups[tuple(cnt)].append(s)   # ② list 不可 hash，转 tuple
    return list(groups.values())
""",
        keys=[
            'key 是<b>字符多重集</b>，不是排序后的串；26 长计数数组 O(k)，'
            '面试时把这条 O(k) vs O(k log k) 的账说出来。',
            '坑：把 <code>cnt = [0]*26</code> 提到 for 外面，六个词共用一个数组，'
            '最后全挤进同一组。',
            '字符集不限定 a-z 时退回 <code>"".join(sorted(s))</code>，逻辑一字不变。',
            'O(n·k) time / O(n·k) space（n 个词，每词长 k）',
        ],
        test="sorted(map(sorted, groupAnagrams(['care','race','acre','bat','tab','cat'])))",
        want=[['acre', 'care', 'race'], ['bat', 'tab'], ['cat']],
    ),
    11: dict(
        idea=[
            '面积 = <code>min(两根柱子) × 距离</code>。枚举所有对是 O(n²)。',
            '从<b>最宽</b>的那一对开始想 ——左右两端。此后不管怎么动，'
            '宽度<b>只会变小</b>，那想让面积变大就只剩一个指望：高度。',
            '而高度由<b>矮的那根</b>封顶。所以如果我留着矮边不动、只挪高边：'
            '高度顶天还是矮边那么高，宽度却更小 ——<b>一定更差</b>。'
            '所以每一步只能挪矮的那一端。',
            '换个说法就是：矮边和它这一侧剩下的<b>任何</b>一根柱子搭配，高度都 ≤ '
            '它自己、宽度都比现在小 ——矮边参与的所有剩余组合可以<b>整批淘汰</b>。'
            '这才是双指针能做到线性的原因。',
        ],
        code="""
def maxArea(height: list[int]) -> int:
    l, r = 0, len(height) - 1        # 从最宽的一对起手
    best = 0
    while l < r:
        best = max(best, min(height[l], height[r]) * (r - l))
        if height[l] < height[r]:    # 移动矮的一边: 只有换掉短板才可能变大
            l += 1
        else:
            r -= 1
    return best
""",
        keys=[
            '<b>移动矮的那一边</b>。这是整题唯一的决策，'
            '说得出「为什么丢掉矮边是安全的」才算答上。',
            '坑：我写过 <code>if height[l] &lt; height[r]: l += 1</code> 之后忘了 '
            '<code>else</code> 分支，两边高度相等时不动 → 死循环。'
            '相等时随便挪一边都行，但<b>必须挪</b>。',
            '别和 <b>LC 42 Trapping Rain Water</b> 搞混：那题算总积水、'
            '要维护左右最大值；这题只取两根柱子。',
            'O(n) time / O(1) space',
        ],
        test='(maxArea([3,9,4,7,2,8]), maxArea([1,1]))',
        want=(32, 1),
    ),
    3: dict(
        idea=[
            '「最长的合法子串」这种问法，第一反应就是滑窗：右端一直往前吞，'
            '一旦出现重复就收左端，收到重新合法为止。',
            '可「收左端」怎么收？一格一格挪，最坏又是 O(n²) ——'
            '而且每挪一格还得重新判一次「还有没有重复」。',
            '想想我究竟为什么要收：因为 <code>s[r]</code> '
            '和窗口里<b>某一个位置</b>撞了。'
            '那我把左端直接<b>跳到那个位置的右边一格</b>，冲突立刻消失 ——一步到位。'
            '位置从哪来？记一张「字符 → 上次出现的下标」。',
            '手推 <code>"abba"</code> 会踩到唯一的坑：走到最后那个 a 时，表里的 '
            '<code>last[a] = 0</code> 已经<b>在窗口外面</b>了。照跳会把左端从 2 拉回 '
            '1，窗口就不是窗口了 ——所以守卫是 <code>last[ch] &gt;= l</code> 才跳。',
        ],
        code="""
def lengthOfLongestSubstring(s: str) -> int:
    last = {}                            # 字符 -> 最后出现的下标
    l = res = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:  # ① >= l 才算"窗口内"的重复
            l = last[ch] + 1              # ② 直接跳, 不用一格格缩
        last[ch] = r
        res = max(res, r - l + 1)
    return res
""",
        keys=[
            '<b><code>last[ch] &gt;= l</code> 不能省</b>。<code>"abba"</code>：'
            '走到最后的 a 时 <code>last[a]=0</code> 已在窗口外，直接跳会让 '
            '<code>l</code> 从 2 退回 1，答案变成 3（错，应是 2）。',
            '坑：我第一版用 <code>set</code> + <code>while ch in seen: '
            'seen.remove(s[l]); l += 1</code> ——也对，但要记得<b>先缩再加</b>；'
            '顺序反了会把刚进来的字符自己删掉。',
            '是<b>子串</b>不是子序列，所以窗口必须连续；'
            '答案在每次右端推进后更新即可（窗口恒合法）。',
            'O(n) time / O(min(n, 字符集大小)) space',
        ],
        test="(lengthOfLongestSubstring('dvdfab'), lengthOfLongestSubstring('abba'), lengthOfLongestSubstring(''))",
        want=(5, 2, 0),
    ),
    560: dict(
        idea=[
            '「和为 k 的子数组有几个」，第一反应是滑窗。但 <code>nums</code> '
            '<b>有负数</b> ——右端往前吞一格，和可能反而变小，'
            '「太大就收缩」这条规则直接失效。滑窗出局。',
            '退回暴力：枚举所有 <code>(i, j)</code> 算区间和，O(n²)。慢在哪很清楚 ——'
            '每换一个 j 都把前面重新加一遍。',
            '前缀和能把区间和变成<b>两个数的差</b>：<code>sum(i..j) = pre[j] − '
            'pre[i−1]</code>。于是问题改写成「走到 j 时，前面出现过多少个值为 '
            '<code>pre[j] − k</code> 的前缀和」——又是把「往回找」变成「查记忆」。',
            '表里存的是<b>次数</b>不是下标，因为问的是「有多少个」：'
            '同一个前缀和出现过 3 次，就贡献 3 个区间。',
            '起手必须 <code>{0: 1}</code>。那个 0 代表<b>空前缀</b> ——没有它，'
            '「从下标 0 开始」的子数组一个都匹配不上。',
        ],
        code="""
def subarraySum(nums: list[int], k: int) -> int:
    seen = {0: 1}                        # ① 空前缀! 少了它会漏掉从头开始的子数组
    pre = res = 0
    for x in nums:
        pre += x
        res += seen.get(pre - k, 0)       # ② 先查: 表里只有左边的前缀
        seen[pre] = seen.get(pre, 0) + 1  # ③ 后插
    return res
""",
        keys=[
            '<b><code>seen = {0: 1}</code> 起手</b>。<code>nums=[3], k=3</code> '
            '少了它直接返回 0 ——本题第一大坑。',
            '存的是<b>次数</b>不是下标：问的是「有多少个」，同一个前缀和出现 3 '
            '次就贡献 3 个区间。',
            '坑：我试过滑窗 ——<code>[1,-1,0], k=0</code> 立刻挂。'
            '<b>有负数就别想滑窗</b>，这是判断用哪个 pattern 的分水岭。',
            'O(n) time / O(n) space',
        ],
        test='(subarraySum([2,1,-1,3,1], 3), subarraySum([1,1,1], 2), subarraySum([1,-1,0], 0))',
        want=(4, 2, 3),
    ),
    33: dict(
        idea=[
            '要 O(log n)，基本就是逼你二分。可数组不是有序的 ——二分的前提没了，'
            '得先看清楚还剩下什么。',
            '画一下：旋转过的有序数组是<b>两段各自递增，中间只有一个断崖</b>。'
            '「只有一个」是接下来全部的依仗。',
            '既然只有一个断崖，那从中间切一刀，它只能掉进<b>其中一半</b> ——'
            '另一半必然是完整有序的。二分要的从来不是整体有序，'
            '是「能判断该往哪半走」。',
            '有序那半好办，比一下两个端点就知道 target 在不在里面。乱序那半不用判：'
            '两半二选一，不在这半就只能在那半。',
            '手推一下 <code>[3,1]</code> 会踩到：只剩两个元素时 <code>mid == '
            'left</code>，左半就一个元素，那也算有序。所以判断得写成 '
            '<code>nums[left] &lt;= nums[mid]</code>。',
        ],
        code="""
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        # 先判断哪一半是完整有序的。
        # 必须用 <=：窗口只剩两个元素时 left == mid，
        # 此时左半只有一个元素，也算有序。
        if nums[left] <= nums[mid]:
            # 左半 [left, mid] 有序，可以直接用端点做区间判断
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # 断崖在左半，那么右半 [mid, right] 一定有序
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
""",
        keys=[
            '<b>只有一个断崖 ⟹ 切开后至少一半是完整有序的。'
            '</b>在有序那半用端点做区间判断，不在就去另一半 ——'
            '乱序那半永远不用直接判断。',
            '坑：写成 <code>nums[left] &lt; nums[mid]</code>。窗口剩两个元素时 '
            '<code>left == mid</code>，左半被误判成乱序，<code>[3,1]</code> 找 1 '
            '就会走错分支。<b>必须是 <code>&lt;=</code></b>。',
            '坑：拿 <code>nums[0]</code> 当左端点比较。第一轮碰巧对，'
            '之后窗口移走就全错了 ——要用<b>当前窗口</b>的 <code>nums[left]</code>。',
            '坑：区间判断的等号漏了。<code>nums[left] &lt;= target</code> 写成 '
            '<code>&lt;</code> 的话，<code>[6,8,9,1,3,4]</code> 找 6 直接找不到。',
            'O(log n) time / O(1) space（有重复元素时退化到 O(n)，见 LC 81）',
        ],
        test='[search([6,8,9,1,3,4], 3), search([6,8,9,1,3,4], 7), search([1], 0), search([3,1], 1), search([5,1,3], 3)]',
        want=[4, -1, -1, 1, 2],
    ),
    227: dict(
        idea=[
            '有括号的话就得老老实实建语法树了。可这题<b>没有括号</b>，'
            '只剩加减和乘除两级优先级 ——这个限制值得先盯一会儿。',
            '只有两级会怎么样？语法树的形状就被<b>钉死</b>了：根一定是加法，'
            '儿子一定是一串乘除，没有任何需要「决定」的地方。既然如此，要树干嘛，'
            '一个列表就够。',
            '于是把式子重读一遍：<code>3+2*2-6/4</code> 其实是 <code>3 + (2*2) + '
            '(−(6/4))</code>，就是<b>若干项相加</b>。乘除在项内部消化掉，'
            '加减留到最后一口气加完 ——列表 + 求和，那就是个栈。',
            '动手写才发现一个时序问题：扫到一个数字，它该自己单独成项，'
            '还是该和上一项乘起来？取决于它<b>前面</b>那个算符。所以算符得先攒着，'
            '等下一个数字出现才生效。',
            '最后一个坑是语言的：<code>//</code> 向下取整，题目要<b>向零截断</b>。'
            '<code>-6 // 4</code> 得到 −2，要的是 −1 ——用 <code>int(a / b)</code>。',
        ],
        code="""
def calculate(s: str) -> int:
    stack = []
    num = 0
    prev_op = '+'          # 「上一个算符」，起手当成 + ，第一个数就会被压栈

    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)     # 多位数一位位拼

        # 遇到算符、或者走到最后一个字符，就该结算前面那个数了
        is_last = (i == len(s) - 1)
        if (ch in '+-*/') or is_last:
            if prev_op == '+':
                stack.append(num)        # 一个新的项
            elif prev_op == '-':
                stack.append(-num)       # 减法 = 加一个负项
            elif prev_op == '*':
                stack.append(stack.pop() * num)
            else:
                # 向零截断，不是向下取整：int(-6/4) = -1，而 -6//4 = -2
                stack.append(int(stack.pop() / num))
            prev_op = ch
            num = 0
        # 空格：既不是数字也不是算符，直接跳过，num 和 prev_op 都不动

    return sum(stack)
""",
        keys=[
            '<b>数字用的是它前面那个算符</b>，所以算符要延迟一步生效。'
            '拿当前算符去算，最后一个数会被整个丢掉 ——<code>"42"</code> 直接返回 0。',
            '坑：用 <code>//</code>。<code>"1-7/2"</code> 得到 −3（应为 −2）：'
            '减法被压成负数之后，向下取整和向零截断就分道扬镳了。<b>用 <code>int(a / '
            'b)</code></b>。',
            '坑：忘了「最后一个字符」也要触发结算。循环只在遇到算符时结算的话，'
            '式子末尾那个数永远留在 <code>num</code> 里没进栈。',
            '空格只跳过、不重置状态：<code>" 3 + 50 / 2 "</code> 里 <code>50</code> '
            '中间没空格，但两侧有，别把 <code>num</code> 清掉。',
            'O(n) time / O(n) space（栈里最多存 n/2 个项）',
        ],
        test="[calculate('3+2*2-6/4'), calculate(' 9 / 2 '), calculate('3+5 / 2'), calculate('14-3/2'), calculate('1-7/2'), calculate('42')]",
        want=[6, 4, 5, 13, -2, 42],
    ),
    236: dict(
        idea=[
            '直觉是先分别找到 p 和 q，各记一条从根出发的路径，再从头比到分岔点。'
            '能做，但要存两条路径、还要处理长度不等 ——白板上写不完。',
            '换个方向：与其自顶向下地找，不如让递归<b>自底向上地报</b>。'
            '每棵子树只回答一句话：「我这里面，能交上去的最好答案是谁？」',
            '撞见 p 或 q 就<b>立刻返回它、不再往下挖</b>。这一步顺手把「p 恰好是 q '
            '的祖先」那个恶心情况也解决了 ——答案自然落在 p 上，不需要任何特判。',
            '于是只剩两种情况：左右都返回非空 → 两个目标分居两侧 → <b>我就是 '
            'LCA</b>；只有一侧非空 → 把它原样上传（它要么是找到的目标，'
            '要么是已经定下的 LCA）。',
        ],
        code="""
def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    if root is None or root is p or root is q:
        return root                # ① 撞见目标就上交，不必再往下挖
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:             # ② 两边各找到一个 -> 分叉点就是我
        return root
    return left or right           # ③ 只有一边有 -> 原样上传
""",
        keys=[
            '返回值的含义定死了整题：<b>「这棵子树里找到的 p/q，或已经确定的 LCA」</b>。',
            '坑：我加了「先确认两个都存在」的预检查，代码翻倍还是错的。题目保证 p、q '
            '都在树里，<b>命中即返回</b>就够；'
            '不保证时才需要额外返回一个「找到几个」的计数。',
            '比较用 <code>is</code>（节点身份）而不是 <code>.val</code>；LC 235 的 '
            'BST 版可以直接靠值二分，别混。',
            'O(n) time / O(h) space（h 为树高，最坏 O(n)）',
        ],
        test='(lambda t: lowestCommonAncestor(t, t.left.left, t.left.right.right).val)(build_tree([8,3,10,1,6,None,14,None,None,4,7]))',
        want=3,
    ),
    124: dict(
        idea=[
            '路径有指数多条，一条条数不可能。这种时候我想的是：'
            '能不能给它们<b>分个类</b>，让每一类一次算完。',
            '按什么分？在纸上画一条路径出来看看 ——它在树上长得像个「∧」：'
            '从某个点往下走两条腿，而<b>那个顶点是唯一的</b>。按顶点分类，'
            '指数条路径就归成了 n 类。',
            '于是每个节点只回答一句话：「路径要是在我这儿拐弯，最大是多少？」= 左腿 '
            '+ 我 + 右腿。递归求两条腿，看着就收工了。',
            '可试着把这个值往上传就发现传不动：带着两条腿再接父节点，'
            '这个点上就有三条边了 ——那是个岔路口，不是一条路径。',
            '所以一个函数得吐两样东西：<b>记进答案</b>的是「在我这拐弯」，'
            '<b>返回给父亲</b>的是「一条还能往上长的链」= 我 + max(一条腿)。'
            '全题就卡在这个区别上。',
        ],
        code='''
def maxPathSum(root: 'TreeNode') -> int:
    # 路径至少含一个节点；全负的树答案是负数，所以不能起手 0
    best = float('-inf')

    def max_arm(node) -> int:
        """返回：从 node 一路向下、只走一条链的最大和。"""
        nonlocal best
        if not node:
            return 0

        # 腿的贡献是负的就不要这条腿（等价于路径到 node 为止）
        left_arm = max(0, max_arm(node.left))
        right_arm = max(0, max_arm(node.right))

        # 在 node 拐弯的路径：左腿 + 自己 + 右腿。
        # 它只能进全局答案，不能上报——带两条腿再接父节点，
        # node 就有三条边了，那不是一条路径。
        bend_here = node.val + left_arm + right_arm
        best = max(best, bend_here)

        # 上报给父节点：只能带一条腿
        return node.val + max(left_arm, right_arm)

    max_arm(root)
    return best
''',
        keys=[
            '<b>上报一条腿，记录两条腿。</b>这是全题的分界线：'
            '上报的必须是能被父节点接着延伸的直链，拐弯的那条只能进全局。',
            '坑：<code>best = 0</code> 起手。<code>[-3]</code> 返回 0（应为 −3）、'
            '<code>[-2,-1]</code> 返回 0（应为 −1）。<b>必须 <code>-inf</code></b>。',
            '坑：把 <code>node.val</code> 也套进 <code>max(0, ...)</code>。'
            '节点自己是必选的，砍掉它路径就断了 ——只砍<b>子树</b>的贡献。',
            '坑：以为答案一定过根。<code>[2,-4,6,null,null,3,9]</code> 的答案 18 '
            '整条都不含根节点。',
            'O(n) time / O(h) space',
        ],
        test='(maxPathSum(build_tree([2,-4,6,None,None,3,9])), maxPathSum(build_tree([1,2,3])), maxPathSum(build_tree([-3])), maxPathSum(build_tree([2,-1])))',
        want=(18, 6, -3, 2),
    ),
    207: dict(
        idea=[
            '「能不能修完所有课」怎么翻译成图的话？一门课永远开不了工只有一个原因：'
            '它的先修链<b>绕回了自己</b>。所以问的其实是：依赖图里<b>有没有环</b>。',
            '判环的常规手段就是拓扑排序 —— 能把所有节点排成一条线就无环，排不出来就有环。',
            'Kahn 的做法很像现实：<b>入度 0 = 先修课全修完了</b>，现在就能上；'
            '上完它，把它指向的课各减一个入度，谁减到 0 谁进队。',
            '边的方向最容易搞反。<code>[a, b]</code> 是「修 a 之前先修 b」，'
            '所以箭头是 <b>b → a</b>，指向<b>后</b>修的那门。反了的话 '
            '<code>[[1,0]]</code> 和 <code>[[0,1]]</code> 的答案互换。',
            '结尾比出队总数和 <code>numCourses</code>：环里的节点入度永远降不到 0，'
            '一个都进不了队，差额就是被锁死的那批。',
        ],
        code="""
from collections import defaultdict, deque

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    graph = defaultdict(list)
    indeg = [0] * numCourses
    for course, pre in prerequisites:  # [a,b] = 先修 b 才能修 a
        graph[pre].append(course)      # ① 边的方向是 pre -> course
        indeg[course] += 1
    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    done = 0
    while q:
        cur = q.popleft()
        done += 1
        for nxt in graph[cur]:
            indeg[nxt] -= 1            # ② 它的一门先修课修完了
            if indeg[nxt] == 0:        # ③ 全部先修课到齐才进队
                q.append(nxt)
    return done == numCourses          # ④ 排不完 = 剩下的被环锁死
""",
        keys=[
            '<b>能修完 ⟺ 无环</b>，判环的手段就是拓扑排序：<code>done != '
            'numCourses</code> 即有环。',
            '坑：把边建成 <code>course → pre</code>，<code>[[1,0]]</code> 和 '
            '<code>[[0,1]]</code> 的答案互换。记法：<b>箭头指向「后修的那门」</b>。',
            '坑：<code>q.append(nxt)</code> 写在 <code>if indeg[nxt] == 0</code> '
            '外面 ——一门课有两个先修时会被排两次，<code>done</code> 虚高，有环也返回 '
            'True。',
            '要输出<b>顺序</b>就是 LC 210，把 <code>done</code> 换成 '
            '<code>res</code> 列表即可，长度不足时返回 <code>[]</code>。',
            'O(V + E) time / O(V + E) space',
        ],
        test='(canFinish(3, [[1,0],[2,1]]), canFinish(3, [[1,0],[2,1],[0,2]]), canFinish(4, [[1,0],[2,0],[3,1],[3,2]]), canFinish(3, []))',
        want=(True, False, True, True),
    ),
    139: dict(
        idea=[
            '先写递归：s 能不能拆 = <b>存在</b>某个切点 j，前半段能拆、后半段是个单词。',
            '会超时，但超时的原因很具体：不同的切法会<b>反复问到同一批前缀</b>，'
            '同一个子问题算了指数次。那就把答案记下来 ——记忆化，或者干脆摊平成 DP。',
            '状态定成 <code>dp[i]</code> = 前 i 个字符能不能被完整拆开；'
            '转移就是枚举<b>最后一个单词</b>的起点 j：<code>dp[j] and s[j:i] in '
            'words</code>。',
            '<code>dp[0] = True</code> 是整张表的<b>火种</b> ——空串可拆。'
            '少了它全表都是 False，<code>s="leet", dict=["leet"]</code> 都返回 '
            'false。',
            '顺便否掉一个很自然的想法：贪心「每次匹配最长的单词」。<code>s="cars", '
            'dict=["car","ca","rs"]</code> 先吃掉 car 就卡死了 ——正解是 ca + rs。',
        ],
        code="""
def wordBreak(s: str, wordDict: list[str]) -> bool:
    words = set(wordDict)              # ① 必须转 set: in 要 O(1)
    dp = [False] * (len(s) + 1)
    dp[0] = True                       # ② 空串可拆, 整张表的火种
    for i in range(1, len(s) + 1):
        for j in range(i):             # j = 最后一个单词的起点
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break                  # ③ 只问存在性, 找到一种拆法就够
    return dp[len(s)]
""",
        keys=[
            '<b><code>dp[0] = True</code></b>。少了它整张表全 False，<code>s="leet", '
            'dict=["leet"]</code> 都会返回 false。',
            '坑：我先写了贪心「每次匹配最长的单词」——<code>s="cars", '
            'dict=["car","ca","rs"]</code> 先吃掉 <code>car</code> 就卡死了，正解是 '
            '<code>ca + rs</code>。<b>必须枚举所有切点</b>。',
            '坑：<code>wordDict</code> 不转 <code>set</code>，<code>in</code> 退化成 '
            'O(len(dict)) 线性扫，整体多一个量级 ——面试官最爱抓这一条。',
            'O(n²·k) time / O(n) space（k = 切片长度；把 j 限制在 <code>i − '
            '最长单词长</code> 以内可再快一截）',
        ],
        test="(wordBreak('cars', ['car','ca','rs']), wordBreak('grindcards', ['grind','cards','card']), wordBreak('catsandog', ['cats','dog','sand','and','cat']), wordBreak('grindcard', ['grind','cards']))",
        want=(True, True, False, False),
    ),
}
