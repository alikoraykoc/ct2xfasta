from typing import List, Tuple

# Canonical + wobble
CANONICAL_RNA = {
    ("A", "U"),
    ("U", "A"),
    ("G", "C"),
    ("C", "G"),
    ("G", "U"),
    ("U", "G"),
}


def basic_consistency(seq: str, dot: str) -> List[str]:
    errs = []
    if len(seq) != len(dot):
        errs.append(f"Length mismatch: sequence={len(seq)} structure={len(dot)}")
    # parentheses balance
    bal = 0
    for i, ch in enumerate(dot, start=1):
        if ch == "(":
            bal += 1
        elif ch == ")":
            bal -= 1
        if bal < 0:
            errs.append(f"Structure closes before opening at position {i}")
            break
    if bal != 0:
        errs.append("Unbalanced parentheses in structure")
    return errs


def noncanonical_pairs(seq: str, dot: str) -> List[Tuple[int, str, int, str]]:
    """
    Return list of non-canonical base pairs (1-based positions and bases).
    """
    stack = []
    res = []
    for i, ch in enumerate(dot, start=1):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if not stack:
                continue
            j = stack.pop()
            b1 = seq[j - 1].upper()
            b2 = seq[i - 1].upper()
            if (b1, b2) not in CANONICAL_RNA:
                res.append((j, b1, i, b2))
    return res
