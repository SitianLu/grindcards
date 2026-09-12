# -*- coding: utf-8 -*-
# Concept cards: ("C", section, title, front_html, [back blocks]). Titles are shared
# across languages; the app keys progress on them.
from grindcards.helpers import *

CONCEPTS = [

("C", "ARRAYS & HASHING", "Hashmap as Memory",
 LEAD("A hash map turns an O(n) lookup into O(1), paid for with O(n) space.") +
 "Most array problems boil down to one decision: <b>what goes in the key</b> — and when do I write it, when do I read it?",
 [K("<b>Key on the shape of the answer.</b> Looking for a pair → key is the complement; grouping → key is a canonical form; subarrays → key is the prefix sum. Once the key is right, the problem is done."),
  K("<b>Check before insert.</b> At the moment I look up, the map only holds elements to my left, so whatever I hit can't be me. Two Sum and Subarray Sum both skip a special case because of this."),
  T(["Looking for", "What the key holds", "Problem"],
     [["a pair that sums", "<code>target - x</code>", "Two Sum"],
     ["groups of equivalents", "canonical form (sorted string / count tuple)", "Group Anagrams"],
     ["a contiguous subarray", "prefix sum (or % k)", "Subarray Sum Equals K"],
     ["last time I saw it", "element → last index", "Longest Substring No Repeat"],
     ["frequency", "element → count", "Top K Frequent"]]),
  W("<b>A list isn't hashable</b> — convert it to a <code>tuple</code> before using it as a key; set/dict aren't either, use <code>frozenset</code>."),
  CX("O(1) average lookup and update; O(n) worst case (hash collisions — interviewers rarely push on it)"),
  MORE(),
  P("<b>When not to reach for a hash map</b>: the array is already sorted (two pointers use less space), the value range is tiny (an array or counting buckets is faster), or O(1) space is required (mark in place: negate <code>nums[abs(v)-1]</code> as a visited flag)."),
  P("<code>Counter</code> and <code>defaultdict</code> kill a lot of boilerplate: <code>Counter(nums)</code> counts in one line, <code>freq[missing]</code> returns 0 instead of raising KeyError, and <code>defaultdict(list)</code> lets you append without creating the empty list first.")]),

("C", "TWO POINTERS", "Opposite Ends",
 LEAD("Two pointers start at both ends of the array and walk inward, discarding one end per step.") +
 "What must be true about the data for this to be safe? And <b>how do I decide which pointer moves</b> at each step?",
 [K("Precondition: the array is <b>sorted</b>, or moving one end changes the target <b>monotonically</b> for better or worse. Without that monotonicity, opposite-end pointers are just guessing."),
  K("Move rule: <b>look at which side of the target the current state falls on</b>, and move that side. Sum too small → move left pointer right (the only move that can make it bigger)."),
  C("""l, r = 0, len(a) - 1
while l < r:
    s = a[l] + a[r]
    if s == target: return [l, r]
    if s < target:  l += 1        # only l can grow the sum
    else:           r -= 1"""),
  W("<code>while l &lt; r</code> or <code>l &lt;= r</code>? Picking two distinct elements → <code>&lt;</code>. Only use <code>&lt;=</code> when the same element may serve twice (binary-search-style narrowing)."),
  CX("O(n) time / O(1) space — beats sort-then-binary-search at O(n log n)"),
  MORE(),
  T(["Problem", "How it's used"],
     [["Two Sum II (sorted)", "sum too small → move l; too big → move r"],
     ["3Sum", "fix one number, squeeze the other two from both ends; sort first"],
     ["Container With Most Water", "move the <b>shorter</b> side (moving the taller one can only lose)"],
     ["Trapping Rain Water", "move the side whose running max is smaller"],
     ["Valid Palindrome", "compare from both ends, skip non-letters"]]),
  P("<b>3Sum dedup</b>: outer loop <code>if i &gt; 0 and a[i] == a[i-1]: continue</code>; inner loop, after recording an answer, <code>while l &lt; r and a[l] == a[l+1]: l += 1</code>. You need both.")]),

("C", "SLIDING WINDOW", "The Shrink Rule",
 LEAD("A window [l, r] slides over the array: the right pointer expands, the left pointer shrinks.") +
 "<b>When do you shrink <code>left</code>?</b> One rule splits this whole family of problems into two camps.",
 [K("Want the <b>longest</b> → shrink left while <b>invalid</b> ｜ want the <b>shortest</b> → shrink left while <b>valid</b>"),
  T(["Goal", "When to shrink left", "Window bookkeeping"],
     [["longest substring", "while invalid", "set / Counter"],
     ["shortest substring", "while valid", "Counter + have/need"],
     ["fixed window k", "while r-l+1 &gt; k", "sum / Counter"]]),
  C("""l = 0
for r in range(n):
    add a[r]
    while window needs shrinking:
        remove a[l]; l += 1
    update answer       # longest: after while; shortest: inside"""),
  W("<b>Precondition</b>: validity is <b>monotonic</b> in length — adding an element can only make it less valid, removing one only more valid. 'Shortest subarray with sum k' over negatives breaks this; switch to prefix sum + hash map."),
  CX("O(n) — every element enters and leaves the window at most once"),
  MORE(),
  P("<b>Where you update the answer decides what you're computing</b>: for longest, update <b>after</b> the shrink loop (the window is valid and as wide as it gets); for shortest, update <b>inside</b> the shrink loop (every state right before a shrink is a candidate). Put it in the wrong place and the answer is systematically too big or too small."),
  K("Say it out loud: 'The right pointer expands the window every step; when the constraint breaks, the left pointer shrinks. Each element enters and leaves at most once, so the whole thing is O(n) instead of the brute-force O(n²).'")]),

("C", "PREFIX SUM", "Subarray Sum with Hashmap",
 LEAD("Count subarrays summing to k when the array may hold negatives, so sliding window is out.") +
 "Prefix sums go into a hash map. <b>What exactly do you look up</b> — and what must the map hold before you start?",
 [K("<code>sum(i..j) = pre[j] - pre[i-1]</code>. For that to <code>== k</code>, look up <b>how many times <code>pre[j] - k</code> has appeared before</b>."),
  W("<b>The map must start as <code>{0: 1}</code></b> — the 'empty prefix'. Skip it and every subarray that starts at index 0 goes missing. This is the number-one bug in this family."),
  C("""seen = {0: 1}            # the empty prefix has been seen once!
pre = res = 0
for x in nums:
    pre += x
    res += seen.get(pre - k, 0)   # look up first
    seen[pre] = seen.get(pre, 0) + 1   # then insert"""),
  W("<b>Look up, then insert</b> — same reason as Two Sum: at lookup time the map only holds prefixes to my left, which guarantees the subarray is non-empty."),
  CX("O(n) time / O(n) space"),
  MORE(),
  T(["Variant", "Swap the map key for"],
     [["count of sum == k", "prefix sum"],
     ["sum divisible by k", "prefix sum <b>% k</b>"],
     ["equal count of 0s and 1s", "treat 0 as -1, look for a repeated prefix sum"],
     ["the longest one", "store the <b>earliest</b> index, never overwrite"]]),
  P("Counting → a count map. Longest → a 'value → earliest index' map, and <b>only write when the key is absent</b>; otherwise you clobber the earlier index and the answer shrinks.")]),

("C", "BINARY SEARCH", "The F→T Boundary",
 LEAD("Binary search isn't only for finding a value in a sorted array.") +
 "Every binary search is really asking <b>the same question</b>. What is it — and what's the <b>only</b> thing you have to decide?",
 [K("Every binary search = find the <b>F→T boundary</b> of a monotonic predicate <code>p(i)</code>. The only thing to think about: what is p(i)?"),
  C("""lo, hi = 0, n              # hi = n, not n-1
while lo < hi:
    mid = (lo + hi) // 2
    if p(mid): hi = mid        # may be the answer -> keep it
    else:      lo = mid + 1    # drop mid and all to its left
return lo                      # first True; all False gives n"""),
  T(["Want", "p(i)", "Return"],
     [["first &gt;= x", "a[i] &gt;= x", "lo"],
     ["first &gt; x", "a[i] &gt; x", "lo"],
     ["last &lt;= x", "a[i] &gt; x", "lo-1"],
     ["last &lt; x", "a[i] &gt;= x", "lo-1"]]),
  W("<b>Never write <code>lo = mid</code></b> (infinite loop). With this template you never need the <code>(l+r+1)//2</code> variant. Any branch that returns <code>lo-1</code> must guard <code>lo == 0</code>."),
  CX("O(log n)"),
  MORE(),
  P("<b>An existence check takes two steps</b>: <code>i = bisect_left(a, x)</code>, then <code>i &lt; len(a) and a[i] == x</code>. Checking only <code>i &lt; len(a)</code> is wrong — it says there's a slot, not that the value matches."),
  P("Python ships it: <code>bisect_left</code> = lower_bound, <code>bisect_right</code> = upper_bound, <code>bisect_right - bisect_left</code> = how many times x occurs. Use it in an interview when allowed, but be able to write it by hand.")]),

("C", "STACK", "Parsing & Matching",
 LEAD("Bracket matching, expression evaluation, path simplification — all last-in, first-out.") +
 "What shape do these problems share? When the input is an arithmetic expression, <b>what goes on the stack</b>?",
 [K("The rule: <b>on an 'open', push; on a 'close', pop and settle</b>. The stack holds 'context that hasn't been settled yet'."),
  C("""# brackets: push the index of '(' (to know where it was)
# expressions: push numbers, settle on lower-precedence op
# paths: push dir names, pop on '..'

# Basic Calculator II skeleton
stack, num, op = [], 0, '+'
for i, ch in enumerate(s + '+'):   # sentinel flushes last num
    if ch.isdigit(): num = num * 10 + int(ch)
    elif ch in '+-*/':
        if   op == '+': stack.append(num)   # / truncates to 0
        elif op == '-': stack.append(-num)
        elif op == '*': stack.append(stack.pop() * num)
        else:           stack.append(int(stack.pop() / num))
        num, op = 0, ch
return sum(stack)"""),
  W("Python's <code>//</code> rounds <b>down</b> for negatives (<code>-7//2 == -4</code>); the problem usually wants truncation <b>toward zero</b> → write <code>int(a/b)</code>."),
  MORE(),
  P("<b>Why act on the previous operator, not the current one</b>: when I read an operator, the number to its left has only just finished. So each settle applies the <b>previous</b> op, and a sentinel operator at the end forces the last number through."),
  P("Same shape: Valid Parentheses, Simplify Path, Decode String, Remove All Adjacent Duplicates, Exclusive Time of Functions.")]),

("C", "TREES", "Design the DFS Return Value",
 LEAD("Most binary tree problems are one post-order traversal.") +
 "All the difficulty sits in a single decision. <b>Which one</b>? And why do so many tree problems need two different quantities?",
 [K("The only thing to design: <b>what the recursive function returns</b>. The return value is what a subtree reports upward, and it's usually <b>not the same thing</b> as the final answer."),
  P("The classic split: <b>return upward</b> 'the best value with me as an endpoint'; <b>record in a global</b> 'the best value passing through me'. Once a path bends at me it can't keep going up."),
  C("""self.best = 0
def dfs(node):                # returns max depth below node
    if not node: return 0
    L, R = dfs(node.left), dfs(node.right)
    self.best = max(self.best, L + R)   # path bends at node
    return 1 + max(L, R)                # upward: one side only
dfs(root); return self.best"""),
  W("<b>Diameter counts edges</b>; depth counts nodes. In Diameter of Binary Tree, <code>L + R</code> is already the edge count — no +1. Off-by-one here is the most common mistake on this problem."),
  CX("O(n) time / O(h) space (recursion stack, h = tree height)"),
  MORE(),
  T(["Problem", "Return value", "Global answer"],
     [["Diameter", "max depth going down", "max(L+R)"],
     ["Max Path Sum", "max(0, best downward sum)", "max(L+R+val)"],
     ["Balanced Tree", "height, or -1 if unbalanced", "— (prunes early)"],
     ["LCA", "the node found, or None", "— (return value is the answer)"]]),
  P("<b>The <code>max(0, ...)</code> in Max Path Sum</b>: a negative subtree sum counts as 'don't take it' (return 0), because the path is allowed to stop here. Drop that step and an all-negative tree comes out wrong.")]),

("C", "GRAPHS", "Topological Sort",
 LEAD("A pile of tasks with prerequisites; produce a valid execution order.") +
 "What are the four steps of Kahn's loop? And with no extra bookkeeping, how do you <b>detect a cycle</b>?",
 [K("in_degree == 0 → enqueue → pop → neighbors -1 → hits 0 → enqueue."),
  K("Cycle check: <code>len(result) != len(all_nodes)</code> → there's a cycle. The leftover nodes lock each other up; their in-degree never reaches 0."),
  C("""graph = defaultdict(set)                    # set: no dup edges!
indeg = {n: 0 for n in all_nodes}       # isolated nodes too!
for pre, cur in edges:
    if cur not in graph[pre]:
        graph[pre].add(cur); indeg[cur] += 1
q = deque(n for n in all_nodes if indeg[n] == 0)
while q:
    node = q.popleft(); res.append(node)
    for nb in graph[node]:
        indeg[nb] -= 1
        if indeg[nb] == 0: q.append(nb)"""),
  W("Bug 1: adjacency as a <b>set</b>. A duplicate edge bumps the in-degree twice and the node never comes out. Bug 2: <code>indeg</code> must be <b>initialized for every node</b>; building it from edges alone drops isolated nodes."),
  CX("O(V + E) time / O(V + E) space"),
  MORE(),
  P("<b>DFS version</b>: post-order + three colors (white unvisited / gray on the stack / black done); <b>gray meets gray = cycle</b>; reverse the finish order. Kahn is more intuitive and detects cycles for free — recommend Kahn in interviews."),
  P("<b>Minimum time to finish</b> (Parallel Courses) → BFS by <b>level</b>, the level count is the answer. <b>Lexicographically smallest</b> topological order → swap the queue for a min-heap.")]),

("C", "DYNAMIC PROG.", "1D vs 2D State",
 LEAD("Should the state be one-dimensional or two?") +
 "Dimensionality isn't a style choice. <b>What decides it</b>?",
 [K("<b>Dimensions = number of independently varying inputs</b>. One sequence → dp[i]; two sequences → dp[i][j]; one sequence + a budget/capacity → dp[i][w]."),
  T(["Type", "State meaning", "Typical problems"],
     [["1D linear", "best <b>ending at</b> i / among the first i", "House Robber, Coin Change, LIS"],
     ["2D two sequences", "first i of s1 vs first j of s2", "LCS, Edit Distance"],
     ["2D grid", "best way to reach (i,j)", "Unique Paths, Min Path Sum"],
     ["knapsack", "first i items, capacity w", "0/1 Knapsack, Partition Equal Subset"]]),
  W("<b>'Ending at i' and 'among the first i' are different state definitions</b>. Max Subarray needs 'ending at i' (otherwise the transition can't cut the run); so does LIS. House Robber uses 'first i'. Pick the wrong one and the transition won't write itself."),
  MORE(),
  C("""# table is (m+1) x (n+1); row/col 0 = empty string = free base
for i in range(1, m+1):
    for j in range(1, n+1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
return dp[m][n]         # last index is [m][n], not [m+1][n+1]"""),
  W("On a match you must step <b>diagonally</b> to <code>dp[i-1][j-1]</code>: characters pair one-to-one, and <code>dp[i-1][j]</code> would let the same character be used twice."),
  P("Space optimization: only the previous row is needed → roll two rows, and put the <b>shorter</b> string on the column axis → O(min(m,n)). Remember <code>cur[j-1]</code> is this row and <code>prev[j]</code> is the previous row.")]),

]
