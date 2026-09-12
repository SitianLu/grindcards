# -*- coding: utf-8 -*-
# lc -> dict(pat=(why this pattern, concept card title),
#            fq=[(follow-up question, answer)],
#            var=[(problem name incl. 'LC n', how it differs)])

DEEP = {
    1: dict(
        pat=('A pairing problem = a hash map turns "values I have seen" into an O(1) memory, '
             'so the brute-force double loop collapses into one pass.',
             'Hashmap as Memory'),
        fq=[
            ('What if there are several answers?',
             'The problem guarantees one. To return all of them: sort + two pointers + skip '
             'duplicates — the 3Sum approach.'),
            ('What if the array is already sorted?',
             'Two pointers squeezing in from both ends, <b>O(1) space</b>, no hash map. '
             'Interviewers use this line to push you toward two pointers.'),
            ('Can you do it without extra space?',
             'Not without sorting — unsorted, you have to remember what you have seen, '
             'and that is O(n) space.'),
        ],
        var=[
            ('LC 167 Two Sum II', 'input is <b>sorted</b> → two pointers, O(1) space'),
            ('LC 15 3Sum', 'fix one number + two pointers; dedupe in two places'),
            ('LC 653 Two Sum IV', 'input is a BST → inorder flatten to a sorted array, then two pointers'),
            ('Variant: existence only, no indices', 'same map, just don\'t store the index'),
        ],
    ),
    49: dict(
        pat=('A grouping problem = compute a <b>canonical form</b> for each element and use it as the '
             'hash key; equal keys fall into the same group on their own.',
             'Hashmap as Memory'),
        fq=[
            ('What if the alphabet is not just lowercase letters?',
             'The count array is out; use <code>frozenset(Counter(s).items())</code> '
             'or the sorted string as the key.'),
            ('Why is counting faster than sorting?',
             'Sorting is O(k log k), counting is O(k). The gap shows on long words; '
             'saying it out loud earns points.'),
            ('Can you do it without a hash map?',
             'You could sort the whole array by canonical form, O(nk log n), but there is no reason to.'),
        ],
        var=[
            ('LC 242 Valid Anagram', 'only two words → compare their Counters directly'),
            ('LC 438 Find All Anagrams', 'fixed-size sliding window + Counter comparison'),
            ('LC 953 Verifying Alien Dictionary', 'the canonical form becomes "the string mapped through a custom letter order"'),
        ],
    ),
    11: dict(
        pat=('Greedy + two pointers: each step move the end that is the <b>limiting factor</b>; '
             'correctness rests on an exchange argument.',
             'Opposite Ends'),
        fq=[
            ('Why is it safe to throw away the shorter side?',
             'Paired with any other post, the shorter side gets height no better than itself and '
             'less width — it cannot win. <b>This is the proof you have to say out loud</b>.'),
            ('What if both sides are the same height?',
             'Move either one; the post you drop cannot be the unique optimum.'),
            ('How is this different from Trapping Rain Water?',
             'Here only the area between two posts matters; rain water sums water cell by cell '
             'and needs the running left and right maxima.'),
        ],
        var=[
            ('LC 42 Trapping Rain Water', 'two pointers, but you carry the left and right maxima'),
            ('LC 84 Largest Rectangle in Histogram', 'monotonic stack: first shorter bar on each side'),
            ('LC 1793 Maximum Score of a Good Subarray', 'same idea expanding outward from the middle; move the shorter side'),
        ],
    ),
    3: dict(
        pat=('A <b>longest</b>-type sliding window: shrink the left edge when the window goes invalid; '
             'the constraint kept inside is "no repeats".',
             'The Shrink Rule'),
        fq=[
            ('How big is the character set?',
             'It decides whether space is O(128) or O(n), and whether a fixed-size array can '
             'replace the hash map.'),
            ('Why does the map version check <code>last[ch] &gt;= l</code>?',
             'The map may hold a stale position from <b>outside the window</b>; jumping to it '
             'would drag l backwards.'),
            ('What if they want the substring itself?',
             'Record (l, r) whenever the best improves, and slice at the end.'),
        ],
        var=[
            ('LC 159 / 340 At Most K Distinct Characters', 'the constraint changes from "no repeats" to "at most k distinct"'),
            ('LC 424 Char Replacement', 'the constraint becomes "non-majority characters ≤ k"'),
            ('LC 1004 Max Consecutive Ones III', 'same, with the count of zeros ≤ k'),
        ],
    ),
    560: dict(
        pat=('Negatives → sliding window breaks → prefix sums + hash map, turning "a range summing '
             'to k" into "how many times has pre−k appeared".',
             'Subarray Sum with Hashmap'),
        fq=[
            ('Why does a sliding window not work?',
             'With negatives the window sum is <b>not monotonic</b>: extending does not have to '
             'grow it, so "too big → shrink" means nothing.'),
            ('Why does the map start with {0: 1}?',
             'It stands for the empty prefix; without it every subarray starting at index 0 is missed.'),
            ('What if they ask for the longest instead of the count?',
             'Map prefix sum → <b>earliest</b> index, and only write when the key is new.'),
        ],
        var=[
            ('LC 523 Continuous Subarray Sum', 'the key becomes prefix sum % k'),
            ('LC 525 Contiguous Array', 'treat 0 as −1, find the two farthest points with equal prefix sums'),
            ('LC 974 Subarray Sums Divisible by K', 'same modulo trick; watch out for negative modulo'),
        ],
    ),
    33: dict(
        pat=('Rotated array: cut it anywhere and <b>at least one half is sorted</b> — decide which '
             'half first, then whether target is inside it.',
             'The F→T Boundary'),
        fq=[
            ('What if there are duplicates?',
             'When <code>nums[lo] == nums[mid]</code> you cannot tell which half is sorted; all you '
             'can do is lo += 1, so the <b>worst case degrades to O(n)</b>.'),
            ('Why does the sortedness test need the equals sign?',
             'With two elements left, lo == mid; drop the equals and you take the wrong branch.'),
            ('Could you find the pivot first and then binary search?',
             'Yes — two binary searches. More intuitive, longer code.'),
        ],
        var=[
            ('LC 81 Search in Rotated II', 'with duplicates; worst case O(n)'),
            ('LC 153 Find Minimum in Rotated', 'find the pivot itself'),
            ('LC 852 / 1095 Mountain Array', 'the same "which half is monotonic" test'),
        ],
    ),
    227: dict(
        pat=('Expression evaluation = a stack with delayed settlement: when you read an '
             'operator, what actually gets computed is the <b>previous</b> one.',
             'Parsing & Matching'),
        fq=[
            ('What about parentheses?',
             'On ( push the running result and the sign, reset and start over; on ) pop and '
             'merge. Or recurse on the sub-expression (LC 224).'),
            ('The Python integer-division trap?',
             '<code>//</code> rounds toward −∞ on negatives (-7//2 = -4); the problem wants '
             'truncation toward zero → write <code>int(a/b)</code>.'),
            ('Can you do it in O(1) space?',
             'Yes: with only + − × ÷, two variables (current term, running total) replace '
             'the stack.'),
        ],
        var=[
            ('LC 224 Basic Calculator', 'parentheses, no × ÷'),
            ('LC 772 Basic Calculator III', 'parentheses + × ÷, recursion + stack'),
            ('LC 150 Evaluate RPN', 'already postfix; the stack is even more direct'),
        ],
    ),
    236: dict(
        pat=('Designing the return value of a tree recursion: return "the target found in '
             'this subtree"; the node where both sides come back non-empty is the fork.',
             'Design the DFS Return Value'),
        fq=[
            ('What if p is an ancestor of q?',
             'Return p itself on the hit — that is exactly the answer, which is why you '
             '<b>don\'t keep descending</b>.'),
            ('Is the BST version faster?',
             'Yes, steer by comparison: both smaller → go left, both larger → go right, one '
             'on each side → this is the LCA. O(h), and no recursion needed.'),
            ('What if the nodes have parent pointers?',
             'It becomes "intersection of two linked lists": put p\'s ancestors in a set, '
             'then walk up from q to the first hit.'),
        ],
        var=[
            ('LC 235 LCA of BST', 'use the ordering, O(h)'),
            ('LC 1650 LCA III (with parent pointer)', 'linked-list intersection'),
            ('LC 1123 LCA of Deepest Leaves', 'return a (depth, node) pair'),
        ],
    ),
    124: dict(
        pat=('Same skeleton as the diameter, plus one <code>max(0, ...)</code>: the path '
             'is allowed to stop short of a negative subtree.',
             'Design the DFS Return Value'),
        fq=[
            ('Why max(0, ...)?',
             'A subtree with a negative sum is left out, and the path ends there. Skip it '
             'and an all-negative tree comes out wrong.'),
            ('What do you initialize best to?',
             '<code>-inf</code>. Starting at 0 makes an all-negative tree return 0.'),
            ('Does the path have to go through the root?',
             'No. That is why the answer lives in a global, not in the return value.'),
        ],
        var=[
            ('LC 543 Diameter', 'counts edges, ignores node values'),
            ('LC 687 Longest Univalue Path', 'adds an "equal values" constraint'),
            ('LC 1372 Longest ZigZag Path', 'the return value has to tell left from right'),
        ],
    ),
    207: dict(
        pat=('Ordering by dependencies = topological sort; "can everything be finished" is '
             'the same question as "is there a cycle".',
             'Topological Sort'),
        fq=[
            ('How do you detect the cycle?',
             '<code>len(result) != n</code>. The leftover nodes lock each other, so their '
             'in-degrees never reach 0 — no extra bookkeeping needed.'),
            ('Don\'t flip the edge direction',
             '<code>[course, pre]</code> means take pre first, so the edge is '
             '<b>pre → course</b>.'),
            ('What if they want the actual order?',
             'Swap the counter for a result list; on a cycle return an empty array (LC 210).'),
        ],
        var=[
            ('LC 210 Course Schedule II', 'return one valid order'),
            ('LC 269 Alien Dictionary', 'the edges have to be derived from adjacent words'),
            ('LC 1136 Parallel Courses', 'minimum number of semesters → BFS by <b>level</b>'),
        ],
    ),
    139: dict(
        pat=('1D linear DP: <code>dp[i]</code> = can the first i characters be split; the '
             'transition enumerates where the last word starts.',
             '1D vs 2D State'),
        fq=[
            ('Why dp[0] = True?',
             'The empty string splits trivially; it is the base every transition builds on.'),
            ('Does the dictionary need to be a set?',
             '<b>Yes.</b> Otherwise <code>in</code> is a linear scan and the whole thing '
             'degrades. It is the most-overlooked performance point here.'),
            ('Any pruning?',
             'Start the inner j at <code>i − maxWordLen</code> — a slice longer than the '
             'longest word can\'t be in the dictionary.'),
        ],
        var=[
            ('LC 140 Word Break II', 'return every split → backtracking + memo, exponential worst case'),
            ('LC 472 Concatenated Words', 'run Word Break once per word'),
            ('LC 91 Decode Ways', 'also 1D; the transition only looks at the last 1–2 characters'),
        ],
    ),
}
