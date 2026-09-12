# -*- coding: utf-8 -*-
# lc -> (statement_html, example_line). The statement is what the interviewer would say:
# what you are given → what to return → which edges are explicit. Never hint at the
# solution. One example line, input → output.

STMT = {
    1: (
        'Given an integer array <code>nums</code> and a <code>target</code>, '
        'return the <b>indices of the two numbers</b> that add up to target. '
        'Every input has <b>exactly one</b> answer, you may not use the same element '
        'twice, and the two indices can come back in any order.',
        'nums = [3,8,11,4], target = 12  →  [1,3]',
    ),
    49: (
        'Given an array of strings <code>strs</code>, group together the strings that '
        'are <b>rearrangements of the same letters</b> and return all the groups. '
        'The order of the groups, and the order inside a group, does not matter. '
        'Strings contain only lowercase letters; the empty string may appear.',
        'strs = ["care","race","acre","bat","tab","cat"]  →  [["care","race","acre"],["bat","tab"],["cat"]]',
    ),
    11: (
        'Given an array <code>height</code>, where <code>height[i]</code> is the height '
        'of the i-th vertical post. Pick any two posts; together with the x-axis they '
        'form a container. Return the <b>most water</b> it can hold. The container '
        'cannot tilt, so water = distance between the posts × the shorter post\'s height.',
        'height = [3,9,4,7,2,8]  →  32 (indices 1 and 5: min(9,8) × 4)',
    ),
    3: (
        'Given a string <code>s</code>, return the length of the longest '
        '<b>substring</b> with <b>no repeated characters</b>. Substring means '
        'contiguous, not a subsequence. s may contain letters, digits, symbols '
        'and spaces.',
        's = "dvdfab"  →  5 ("vdfab")',
    ),
    560: (
        'Given an integer array <code>nums</code> and an integer <code>k</code>, '
        'return the <b>number</b> of contiguous subarrays whose sum is <b>exactly '
        'k</b> (the count, not a length). <b>The array may contain negatives and '
        'zeros.</b>',
        'nums = [2,1,-1,3,1], k = 3  →  4 ([2,1] [1,-1,3] [3] [-1,3,1])',
    ),
    33: (
        'An ascending array was <b>rotated</b> at some unknown index (for example '
        '[0,1,2,4,5,6,7] becomes [4,5,6,7,0,1,2]); all elements are <b>distinct</b>. '
        'Given the rotated array <code>nums</code> and a <code>target</code>, return '
        'the index of target, or −1 if it is not present. Must run in O(log n).',
        'nums = [6,8,9,1,3,4], target = 3  →  4　｜　target = 7 → -1',
    ),
    227: (
        'Given a string expression <code>s</code>, evaluate it and return the value. '
        'The expression contains only <b>non-negative integers</b>, the operators '
        '<code>+ - * /</code>, and spaces; there are <b>no parentheses</b>. Integer '
        'division <b>truncates toward zero</b>. The expression is guaranteed valid, and '
        'every intermediate result fits in an int.',
        's = "3+2*2-6/4"  →  6　｜　" 9 / 2 " → 4',
    ),
    236: (
        'Given an <b>ordinary</b> binary tree (not a BST) and two of its nodes '
        '<code>p</code> and <code>q</code>, return their <b>lowest common ancestor</b>. '
        'A node <b>counts as its own ancestor</b>. Both p and q are guaranteed to be '
        'in the tree, and all node values are distinct.',
        'root = [8,3,10,1,6,null,14,null,null,4,7], p = 1, q = 7  →  3',
    ),
    124: (
        'Given a binary tree. A path is any sequence of nodes in which each pair of '
        '<b>adjacent nodes is connected</b> by an edge; it <b>need not pass through '
        'the root</b>, and no node appears more than once. Return the <b>maximum sum '
        'of node values</b> over all paths. A path has at least one node, and '
        '<b>node values may be negative</b>.',
        'root = [2,-4,6,null,null,3,9]  →  18 (3→6→9)',
    ),
    207: (
        'There are <code>numCourses</code> courses, and <code>prerequisites[i] = '
        '[a, b]</code> means <b>you must take b before a</b>. Decide whether it is '
        'possible to finish every course. The prerequisites may form a cycle, and '
        'some courses may have no dependencies at all.',
        'numCourses = 3, prerequisites = [[1,0],[2,1]]  →  true　｜　add [0,2] → false',
    ),
    139: (
        'Given a string <code>s</code> and a dictionary of words <code>wordDict</code>, '
        'decide whether s can be split into <b>a sequence</b> of dictionary words '
        '<b>concatenated end to end</b>. A dictionary word <b>may be reused</b> any '
        'number of times, and some words may go unused.',
        's = "cars", wordDict = ["car","ca","rs"]  →  true',
    ),
}
