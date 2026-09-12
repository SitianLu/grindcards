# -*- coding: utf-8 -*-
# lc -> [hint1, hint2, hint3], revealed one at a time on the card front.
# 1 = notice something (a constraint, a trap), no pattern named; 2 = name the pattern;
# 3 = the one key step.

HINTS = {
    1: [
        'You need a memory of "which numbers have I seen". What answers "has x appeared?" in O(1)?',
        'A hash map, value → index.',
        'The <b>order</b> of check and insert inside the loop decides whether the same index can get used twice.',
    ],
    49: [
        'What <b>computable feature</b> do words in the same group share? Compute it and group on it.',
        'Hash-map grouping; the key is each word\'s "canonical form".',
        'Which canonical form depends on the alphabet: a–z → a 26-slot count array; any characters → the sorted string.',
    ],
    11: [
        'Area = min(the two heights) × width. Moving inward, width can only shrink — so what has to happen to height?',
        'Two pointers from both ends; each step move the <b>shorter</b> side.',
        'The key is saying why the shorter side can be thrown away: paired with any other post it never does better.',
    ],
    3: [
        'You want the <b>longest</b> window — so when should the window shrink?',
        'Sliding window; the window keeps a record of "characters already inside".',
        'Storing "char → last position" lets the left end jump in one step, but you must check that position is still inside the window.',
    ],
    560: [
        'The array <b>contains negatives</b> — why does a sliding window break down here?',
        'Prefix sums + hash map: sum(i..j) = pre[j] − pre[i−1].',
        'The map must start as {0: 1}, standing for the empty prefix.',
    ],
    33: [
        'After the rotation the array is not sorted as a whole, but cut it in half anywhere — what is true of <b>at least one half</b>?',
        'Binary search: first decide which half is sorted, then check whether target lies inside that sorted range.',
        'The sortedness test needs the equals sign, or the two-element case takes the wrong branch.',
    ],
    227: [
        'When you read an operator, the number to its <b>left</b> has only just finished. What does that say about <i>when</i> to do the arithmetic?',
        'A stack of terms waiting to be summed: on * or / settle with the top right away; on + or − just push.',
        'What gets settled is always the <b>previous</b> operator; add a sentinel operator at the end so the last number gets settled too.',
    ],
    236: [
        'Don\'t think "find both nodes, then walk back up". Ask instead: what should each subtree <b>report</b> upward?',
        'The recursion returns "the p or q found in this subtree"; both left and right non-empty → the current node is the LCA.',
        'Return on a hit and stop descending — when p is an ancestor of q, returning p itself is already the right answer.',
    ],
    124: [
        'Almost the same as computing the diameter, but node values can be <b>negative</b> — that adds one decision.',
        'The recursion returns the best downward sum; a global tracks L + R + val.',
        'The key guard: max(0, child\'s return value). A negative subtree is skipped, and the path ends there.',
    ],
    207: [
        '"Can every course be finished?" — rephrase it: what is that asking about the graph?',
        'Topological sort (Kahn\'s): in-degree 0 goes into the queue; pop, and decrement each neighbor\'s in-degree.',
        'Cycle detection needs no extra bookkeeping: len(result) != n means there is a cycle.',
    ],
    139: [
        'If the first j characters can be split, and s[j:i] is a word, what about the first i?',
        '1D DP: dp[i] = can the first i characters be split completely; dp[0] = True.',
        'The dictionary has to become a set, or every <code>in</code> is a linear scan and the whole thing degrades.',
    ],
}
