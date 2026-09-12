# -*- coding: utf-8 -*-
# lc -> dict(idea=[3–6 bullets], code="...", keys=[..., complexity], test="expr", want=value)
#
# `idea` is the derivation: first person, present tense, thinking aloud at the whiteboard,
# dead-ends included. `code` must run: `grindcards verify` executes it against `test`
# and compares with `want`. Every code line ≤ 64 characters.

SOL = {
    1: dict(
        idea=[
            'Dumb way first: for each x, scan everything to its right for '
            '<code>target − x</code>. O(n²).',
            'All the cost is in the <b>searching</b> — and the slice I scan each round is '
            'nearly the same slice as last round.',
            'Flip it around: when I reach x, don\'t look ahead — ask "have I '
            '<b>already</b> seen <code>target − x</code>?"',
            'That turns a search into a memory lookup, O(1) a step. One pass and I\'m done.',
            'Bonus: at check time <code>seen</code> only holds what\'s <b>left</b> of x, '
            'so nothing pairs with itself. No special case.',
        ],
        code="""
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}                          # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:         # ① check: left side only
            return [seen[target - x], i]
        seen[x] = i                    # ② insert after
    return []
""",
        keys=[
            '<b>Check, then insert</b>. Reverse the order and <code>[3,3], t=6</code> '
            'pairs an index with itself.',
            'Mistake I made: two maps plus a duplicate special-case → <code>[3,2,4], t=6</code> '
            'returned <code>(0,0)</code>. Check-then-insert handles it in one pass; don\'t patch.',
            'O(n) time · O(n) space',
        ],
        test='twoSum([3, 8, 11, 4], 12)',
        want=[1, 3],
    ),
    49: dict(
        idea=[
            'Comparing every pair is O(n²·k), and every comparison asks the same thing: '
            'same letter counts or not?',
            'So stop comparing. Give each word a <b>canonical form</b> as its key: same '
            'letters, same key, same group.',
            'Which form? Anagram ⟺ same <b>multiset</b> of characters. '
            'The sorted string works, but that\'s O(k log k).',
            'The problem says lowercase only, so a 26-slot count array gives the same key in O(k).',
            'A count array is a list, and lists aren\'t hashable, so it can\'t be a dict key — '
            'turn it into a tuple.',
        ],
        code="""
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        cnt = [0] * 26                 # ① fresh array per word
        for ch in s:
            cnt[ord(ch) - 97] += 1
        groups[tuple(cnt)].append(s)   # ② unhashable → tuple
    return list(groups.values())
""",
        keys=[
            'The key is the <b>character multiset</b>, not the sorted string; a 26-slot '
            'count array is O(k). Say the O(k) vs O(k log k) trade-off out loud.',
            'Mistake: hoisting <code>cnt = [0]*26</code> above the for loop — six words '
            'share one array and all land in the same group.',
            'If the alphabet isn\'t limited to a–z, fall back to '
            '<code>"".join(sorted(s))</code>; the logic doesn\'t change.',
            'O(n·k) time · O(n·k) space (n words of length k)',
        ],
        test="sorted(map(sorted, groupAnagrams(['care','race','acre','bat','tab','cat'])))",
        want=[['acre', 'care', 'race'], ['bat', 'tab'], ['cat']],
    ),
    11: dict(
        idea=[
            'Area = <code>min(two posts) × distance</code>. Trying every pair is O(n²).',
            'Start from the <b>widest</b> pair: the two ends. From here width <b>only '
            'shrinks</b>, so the only hope is height.',
            'And height is capped by the <b>shorter</b> post. Move the tall one instead: '
            'same cap, less width — <b>always worse</b>.',
            'So each step I can only move the shorter end.',
            'Put differently: the short post with <b>any</b> post left on the far side is '
            'no taller and narrower than right now.',
            'So every remaining pair it\'s in is <b>gone in one batch</b>. That\'s the '
            'reason two pointers comes out linear.',
        ],
        code="""
def maxArea(height: list[int]) -> int:
    l, r = 0, len(height) - 1        # start at the widest pair
    best = 0
    while l < r:
        best = max(best, min(height[l], height[r]) * (r - l))
        if height[l] < height[r]:    # move the short side only
            l += 1
        else:
            r -= 1
    return best
""",
        keys=[
            '<b>Move the shorter side</b>. It\'s the only decision in the problem, and you\'ve '
            'answered it only once you can say why dropping the short side is safe.',
            'Mistake: I wrote <code>if height[l] &lt; height[r]: l += 1</code> and forgot the '
            '<code>else</code> — equal heights, nobody moves, infinite loop. On a tie either '
            'side is fine, but <b>something must move</b>.',
            'Don\'t mix it up with <b>LC 42 Trapping Rain Water</b>: that one sums all the '
            'trapped water and needs left/right maxima; here only two posts count.',
            'O(n) time · O(1) space',
        ],
        test='(maxArea([3,9,4,7,2,8]), maxArea([1,1]))',
        want=(32, 1),
    ),
    3: dict(
        idea=[
            '"Longest valid substring" says window: the right end keeps eating, '
            'and on a repeat I pull the left end in.',
            'Pull it in how? One cell at a time is O(n²) again in the worst case, '
            'and every step re-checks for repeats.',
            'Why am I shrinking at all? Because <code>s[r]</code> collided with <b>one '
            'specific position</b> in the window.',
            'So jump the left end <b>right past that spot</b> — conflict gone in one '
            'move. Where? A map of char → last index.',
            'Hand-run <code>"abba"</code> and the one trap shows up: at the final a, '
            '<code>last[a] = 0</code> is already <b>outside the window</b>.',
            'Jump blindly and l goes from 2 back to 1 — that\'s not a window anymore. So '
            'jump only if <code>last[ch] &gt;= l</code>.',
        ],
        code="""
def lengthOfLongestSubstring(s: str) -> int:
    last = {}                            # char -> last index
    l = res = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:  # ① repeat in window
            l = last[ch] + 1              # ② jump, don't crawl
        last[ch] = r
        res = max(res, r - l + 1)
    return res
""",
        keys=[
            '<b><code>last[ch] &gt;= l</code> is not optional</b>. <code>"abba"</code>: at the '
            'last a, <code>last[a]=0</code> is outside the window; a blind jump sends '
            '<code>l</code> from 2 back to 1 and the answer becomes 3 (should be 2).',
            'Mistake: my first version used a <code>set</code> + <code>while ch in seen: '
            'seen.remove(s[l]); l += 1</code> — also correct, but <b>shrink before add</b>; '
            'reversed, it deletes the character that just came in.',
            '<b>Substring</b>, not subsequence, so the window has to be contiguous; update the '
            'answer after every right-end step (the window is always valid).',
            'O(n) time · O(min(n, alphabet size)) space',
        ],
        test="(lengthOfLongestSubstring('dvdfab'), lengthOfLongestSubstring('abba'), lengthOfLongestSubstring(''))",
        want=(5, 2, 0),
    ),
    560: dict(
        idea=[
            'Count subarrays summing to k — I reach for a window. But <code>nums</code> '
            '<b>has negatives</b>: add a cell, the sum can drop.',
            '"Too big → shrink" means nothing. Brute force: every '
            '<code>(i, j)</code> is O(n²), and each new j re-adds everything.',
            'Prefix sums turn a range sum into <b>a difference of two numbers</b>: '
            '<code>sum(i..j) = pre[j] − pre[i−1]</code>.',
            'So at j I ask "how many earlier prefix sums equal <code>pre[j] − '
            'k</code>?" — search backwards becomes look it up, again.',
            'The map stores <b>counts</b>, not indices — the question is "how many": '
            'a prefix sum seen 3 times gives 3 ranges.',
            'Start with <code>{0: 1}</code>. That 0 is the <b>empty prefix</b> — without it '
            'no subarray starting at index 0 ever matches.',
        ],
        code="""
def subarraySum(nums: list[int], k: int) -> int:
    seen = {0: 1}                        # ① the empty prefix!
    pre = res = 0
    for x in nums:
        pre += x
        res += seen.get(pre - k, 0)       # ② check: left only
        seen[pre] = seen.get(pre, 0) + 1  # ③ then insert
    return res
""",
        keys=[
            '<b>Start with <code>seen = {0: 1}</code></b>. <code>nums=[3], k=3</code> returns 0 '
            'without it — the number-one trap in this problem.',
            'Store <b>counts</b>, not indices: the question is "how many", and a prefix sum '
            'seen 3 times contributes 3 ranges.',
            'Mistake: I tried a sliding window — <code>[1,-1,0], k=0</code> broke it at once. '
            '<b>Negatives → forget the window</b>; that\'s the line between the two patterns.',
            'O(n) time · O(n) space',
        ],
        test='(subarraySum([2,1,-1,3,1], 3), subarraySum([1,1,1], 2), subarraySum([1,-1,0], 0))',
        want=(4, 2, 3),
    ),
    33: dict(
        idea=[
            'O(log n) required — that\'s code for binary search. But the array isn\'t sorted, '
            'so what\'s left to lean on?',
            'Draw it: a rotated sorted array is <b>two rising runs with one cliff</b> '
            'between them. "Only one" is the lever.',
            'One cliff, so a cut through the middle drops it into <b>one half only</b> — '
            'the other half is intact and sorted.',
            'Binary search never needed everything sorted, just a rule for which half to keep.',
            'Sorted half: check target against its endpoints. The messy half needs no '
            'test — not here means over there.',
            'Hand-run <code>[3,1]</code>: two elements, <code>mid == left</code>, and a '
            'one-element half still counts as sorted — so <code>&lt;=</code>.',
        ],
        code="""
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        # First decide which half is fully sorted.
        # Must be <=: with two elements left, left == mid,
        # and a one-element left half still counts as sorted.
        if nums[left] <= nums[mid]:
            # left half [left, mid] sorted: endpoints decide
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # cliff is on the left, so [mid, right] is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
""",
        keys=[
            '<b>One cliff ⟹ after any cut, at least one half is fully sorted.</b> Test the '
            'sorted half by its endpoints; not there → go to the other. The messy half is '
            'never tested directly.',
            'Mistake: <code>nums[left] &lt; nums[mid]</code>. With two elements '
            '<code>left == mid</code>, the left half reads as unsorted, and <code>[3,1]</code> '
            'looking for 1 takes the wrong branch. <b>Must be <code>&lt;=</code></b>.',
            'Mistake: comparing against <code>nums[0]</code> as the left endpoint. Right on '
            'the first round by luck, wrong once the window moves — use the <b>current '
            'window\'s</b> <code>nums[left]</code>.',
            'Mistake: dropping the equals in the range test. <code>nums[left] &lt;= '
            'target</code> written as <code>&lt;</code>, and <code>[6,8,9,1,3,4]</code> '
            'can\'t find 6.',
            'O(log n) time · O(1) space (degrades to O(n) with duplicates, see LC 81)',
        ],
        test='[search([6,8,9,1,3,4], 3), search([6,8,9,1,3,4], 7), search([1], 0), search([3,1], 1), search([5,1,3], 3)]',
        want=[4, -1, -1, 1, 2],
    ),
    227: dict(
        idea=[
            'Parentheses would force a real parse tree. But this one has <b>no '
            'parentheses</b> — worth staring at that.',
            'Two precedence levels pin the tree\'s shape: root is a sum, each child a run '
            'of × ÷. Nothing to decide.',
            'So no tree. Reread it: <code>3+2*2-6/4</code> is <code>3 + (2*2) + '
            '(−(6/4))</code> — a <b>sum of terms</b>.',
            '× ÷ get eaten inside a term; + − wait for one final sum. A list I push onto '
            'and sum — that\'s a stack.',
            'Writing it, a timing snag: is this number its own term, or times the last '
            'one? That hangs on the op <b>before</b> it.',
            'So an operator waits for the next number before it acts. Last trap: '
            '<code>//</code> floors; I need <code>int(a / b)</code>.',
        ],
        code="""
def calculate(s: str) -> int:
    stack = []
    num = 0
    prev_op = '+'          # last op seen; + pushes 1st number

    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)     # multi-digit numbers

        # operator or last char: settle the number before it
        is_last = (i == len(s) - 1)
        if (ch in '+-*/') or is_last:
            if prev_op == '+':
                stack.append(num)        # a new term
            elif prev_op == '-':
                stack.append(-num)       # minus = negative term
            elif prev_op == '*':
                stack.append(stack.pop() * num)
            else:
                # toward zero: int(-6/4) = -1, but -6//4 = -2
                stack.append(int(stack.pop() / num))
            prev_op = ch
            num = 0
        # space: neither digit nor op -> skip, touch nothing

    return sum(stack)
""",
        keys=[
            '<b>A number uses the operator before it</b>, so the operator acts one step '
            'late. Use the current operator and the last number is dropped whole — '
            '<code>"42"</code> returns 0.',
            'Mistake: <code>//</code>. <code>"1-7/2"</code> gives −3 (should be −2): once '
            'subtraction is pushed as a negative, floor and truncate-toward-zero part '
            'ways. <b>Use <code>int(a / b)</code></b>.',
            'Mistake: forgetting that the <b>last character</b> also triggers a settle. '
            'Settle only on operators and the final number sits in <code>num</code> and '
            'never reaches the stack.',
            'Spaces are skipped, not a reset: in <code>" 3 + 50 / 2 "</code> the '
            '<code>50</code> has spaces on both sides but none inside — don\'t clear '
            '<code>num</code>.',
            'O(n) time · O(n) space (the stack holds at most n/2 terms)',
        ],
        test="[calculate('3+2*2-6/4'), calculate(' 9 / 2 '), calculate('3+5 / 2'), calculate('14-3/2'), calculate('1-7/2'), calculate('42')]",
        want=[6, 4, 5, 13, -2, 42],
    ),
    236: dict(
        idea=[
            'Instinct: find p and q separately, record a root-to-node path for each, '
            'compare from the top until they split.',
            'That works, but it\'s two stored paths plus unequal lengths — it won\'t fit '
            'on a whiteboard.',
            'Flip it: instead of searching top-down, let the recursion <b>report '
            'bottom-up</b>. Each subtree answers one question.',
            '"Of what\'s inside me, what\'s the best I can hand up?" Hit p or q → '
            '<b>return it at once, stop digging</b>.',
            'That move also kills the nasty "p is q\'s ancestor" case — the answer '
            'lands on p by itself, no special case.',
            'Two cases left: both sides non-empty → targets on opposite sides → <b>I\'m '
            'the LCA</b>; one side → pass it up as is.',
        ],
        code="""
def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    if root is None or root is p or root is q:
        return root                # ① found one -> hand it up
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:             # ② one on each side -> me
        return root
    return left or right           # ③ one side -> pass up as is
""",
        keys=[
            'The return value\'s meaning locks the whole problem: <b>"the p/q found in this '
            'subtree, or the LCA once it\'s settled"</b>.',
            'Mistake: I added a pre-check "confirm both exist first" — twice the code and '
            'still wrong. The problem guarantees p and q are in the tree; <b>return on '
            'hit</b> is enough. Only without that guarantee do you need an extra "how many '
            'found" count.',
            'Compare with <code>is</code> (node identity), not <code>.val</code>; the BST '
            'version LC 235 can steer by value — don\'t mix them up.',
            'O(n) time · O(h) space (h = tree height, O(n) worst case)',
        ],
        test='(lambda t: lowestCommonAncestor(t, t.left.left, t.left.right.right).val)(build_tree([8,3,10,1,6,None,14,None,None,4,7]))',
        want=3,
    ),
    124: dict(
        idea=[
            'Exponentially many paths — no counting them one by one. Can I <b>sort them '
            'into classes</b> and do a class at a time?',
            'Draw one: a path on a tree is a "∧" — two legs off one top, and <b>the top '
            'is unique</b>. Class by top: n classes.',
            'Each node answers "if the path bends at me, how big?" = left leg + me + '
            'right leg. Recurse for the legs. Done?',
            'Try passing that up and it won\'t go: two legs plus the parent is <b>three '
            'edges</b> on this node. A fork, not a path.',
            'One function, two outputs: I <b>record</b> "bends at me"; I <b>return</b> a '
            'chain that can still grow: me + max(leg).',
            'The whole problem is that one distinction.',
        ],
        code='''
def maxPathSum(root: 'TreeNode') -> int:
    # all-negative tree -> negative answer, so no starting at 0
    best = float('-inf')

    def max_arm(node) -> int:
        """Max sum of one downward chain starting at node."""
        nonlocal best
        if not node:
            return 0

        # a negative leg is dropped (the path just ends at node)
        left_arm = max(0, max_arm(node.left))
        right_arm = max(0, max_arm(node.right))

        # path bending at node: left leg + node + right leg.
        # it only goes into the global answer, never upward --
        # two legs plus the parent puts three edges on node,
        # and that is not a path.
        bend_here = node.val + left_arm + right_arm
        best = max(best, bend_here)

        # report to the parent: one leg only
        return node.val + max(left_arm, right_arm)

    max_arm(root)
    return best
''',
        keys=[
            '<b>Return one leg, record two.</b> That\'s the line through the whole problem: '
            'what goes up must be a straight chain the parent can extend; the bent one '
            'only goes into the global.',
            'Mistake: <code>best = 0</code>. <code>[-3]</code> returns 0 (should be −3), '
            '<code>[-2,-1]</code> returns 0 (should be −1). <b>Must be '
            '<code>-inf</code></b>.',
            'Mistake: wrapping <code>node.val</code> in the <code>max(0, ...)</code> too. '
            'The node itself is mandatory — cut it and the path breaks. Clamp only the '
            '<b>subtree</b> contributions.',
            'Mistake: assuming the answer goes through the root. In '
            '<code>[2,-4,6,null,null,3,9]</code> the answer 18 never touches the root.',
            'O(n) time · O(h) space',
        ],
        test='(maxPathSum(build_tree([2,-4,6,None,None,3,9])), maxPathSum(build_tree([1,2,3])), maxPathSum(build_tree([-3])), maxPathSum(build_tree([2,-1])))',
        want=(18, 6, -3, 2),
    ),
    207: dict(
        idea=[
            'In graph terms: a course is stuck for good only when its prerequisite chain '
            '<b>loops back to itself</b>.',
            'So the real question is whether the dependency graph <b>has a cycle</b>. '
            'Topological sort: full line-up = no cycle.',
            'Kahn\'s version reads like real life: <b>in-degree 0 = every prerequisite '
            'done</b>, so I can take it right now.',
            'Finish it, and each course it points to loses one in-degree; whoever drops '
            'to 0 joins the queue.',
            'Edge direction is easy to flip. <code>[a, b]</code> is "b before a", so the '
            'arrow is <b>b → a</b>, toward the <b>later</b> course.',
            'At the end compare pops with <code>numCourses</code>: nodes on a cycle never '
            'hit 0, never queue. The gap is the locked set.',
        ],
        code="""
from collections import defaultdict, deque

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    graph = defaultdict(list)
    indeg = [0] * numCourses
    for course, pre in prerequisites:  # [a,b] = b before a
        graph[pre].append(course)      # ① edge is pre -> course
        indeg[course] += 1
    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    done = 0
    while q:
        cur = q.popleft()
        done += 1
        for nxt in graph[cur]:
            indeg[nxt] -= 1            # ② one prereq finished
            if indeg[nxt] == 0:        # ③ all prereqs done
                q.append(nxt)
    return done == numCourses          # ④ rest are cycle-locked
""",
        keys=[
            '<b>Finishable ⟺ acyclic</b>, and topological sort is the cycle test: '
            '<code>done != numCourses</code> means a cycle.',
            'Mistake: building the edge as <code>course → pre</code>; <code>[[1,0]]</code> '
            'and <code>[[0,1]]</code> swap answers. Mnemonic: <b>the arrow points at the '
            'course taken later</b>.',
            'Mistake: <code>q.append(nxt)</code> outside the <code>if indeg[nxt] == '
            '0</code> — a course with two prerequisites gets queued twice, '
            '<code>done</code> inflates, and a cyclic graph returns True.',
            'To output the <b>order</b> it\'s LC 210: swap <code>done</code> for a '
            '<code>res</code> list, and return <code>[]</code> when it comes up short.',
            'O(V + E) time · O(V + E) space',
        ],
        test='(canFinish(3, [[1,0],[2,1]]), canFinish(3, [[1,0],[2,1],[0,2]]), canFinish(4, [[1,0],[2,0],[3,1],[3,2]]), canFinish(3, []))',
        want=(True, False, True, True),
    ),
    139: dict(
        idea=[
            'Recursion first: s splits ⟺ there <b>exists</b> a cut j where the front '
            'splits and the back is a word.',
            'It times out for a concrete reason: cuts <b>re-ask the same prefixes</b>, '
            'so one subproblem is solved over and over.',
            'So write the answers down — memoize, or flatten it into a DP.',
            'State: <code>dp[i]</code> = can the first i characters be split. Transition: '
            'try every start j of the <b>last word</b>.',
            '<code>dp[0] = True</code> is the <b>spark</b>: the empty string splits. '
            'Without it the table stays all False.',
            'One tempting idea to kill: greedy "match the longest word". '
            '<code>"cars"</code> with <code>["car","ca","rs"]</code> eats car and jams.',
        ],
        code="""
def wordBreak(s: str, wordDict: list[str]) -> bool:
    words = set(wordDict)              # ① set: in must be O(1)
    dp = [False] * (len(s) + 1)
    dp[0] = True                       # ② the spark: '' splits
    for i in range(1, len(s) + 1):
        for j in range(i):             # j = last word's start
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break                  # ③ one split is enough
    return dp[len(s)]
""",
        keys=[
            '<b><code>dp[0] = True</code></b>. Without it the whole table stays False and '
            'even <code>s="leet", dict=["leet"]</code> returns false.',
            'Mistake: I wrote greedy "match the longest word" first — <code>s="cars", '
            'dict=["car","ca","rs"]</code> eats <code>car</code> and jams; the answer is '
            '<code>ca + rs</code>. <b>Every cut has to be tried</b>.',
            'Mistake: not turning <code>wordDict</code> into a <code>set</code>; '
            '<code>in</code> degrades to an O(len(dict)) scan and the whole thing gains an '
            'order of magnitude — interviewers love catching this one.',
            'O(n²·k) time · O(n) space (k = slice length; bounding j to within '
            '<code>i − longest word</code> shaves a bit more)',
        ],
        test="(wordBreak('cars', ['car','ca','rs']), wordBreak('grindcards', ['grind','cards','card']), wordBreak('catsandog', ['cats','dog','sand','and','cat']), wordBreak('grindcard', ['grind','cards']))",
        want=(True, True, False, False),
    ),
}
