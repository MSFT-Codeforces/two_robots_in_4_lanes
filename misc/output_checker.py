
import os
import re
from typing import List, Tuple


_INT_RE = re.compile(r"-?\d+\Z")


def _normalize_newlines(text: str) -> str:
    # Accept Windows and old-Mac newlines by normalizing to '\n'
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _tokenize(s: str) -> List[str]:
    return s.split()


def _parse_input(input_text: str) -> Tuple[int, List[int], List[bool]]:
    """
    Returns:
      t: number of test cases
      ns: list of n per test case
      impossible: list of booleans; True iff some tier has >=3 '#', making the case impossible
    """
    input_text = _normalize_newlines(input_text)
    toks = _tokenize(input_text)
    if not toks:
        raise ValueError("empty input")

    idx = 0

    def need_token() -> str:
        nonlocal idx
        if idx >= len(toks):
            raise ValueError("unexpected end of input")
        tok = toks[idx]
        idx += 1
        return tok

    try:
        t = int(need_token())
    except Exception:
        raise ValueError("t is not an integer")

    if t < 1:
        raise ValueError(f"t must be >= 1, got {t}")

    ns: List[int] = []
    impossible: List[bool] = []

    for case in range(1, t + 1):
        try:
            n = int(need_token())
        except Exception:
            raise ValueError(f"Case {case}: n is not an integer")
        if n < 1:
            raise ValueError(f"Case {case}: n must be >= 1, got {n}")

        ns.append(n)
        bad = False

        for r in range(1, n + 1):
            s = need_token()
            if len(s) != 4:
                raise ValueError(f"Case {case}: row {r} length is {len(s)}, expected 4")
            cnt_hash = 0
            for ch in s:
                if ch not in ".#":
                    raise ValueError(f"Case {case}: row {r} has invalid character {ch!r}")
                if ch == "#":
                    cnt_hash += 1
            if cnt_hash >= 3:
                bad = True

        impossible.append(bad)

    if idx != len(toks):
        raise ValueError("extra tokens at end of input")

    return t, ns, impossible


def check(input_text: str, output_text: str) -> Tuple[bool, str]:
    # Parse input to determine expected number of outputs and trivial impossibility
    try:
        t, ns, impossible = _parse_input(input_text)
    except ValueError as e:
        return False, f"Invalid input: {e}"

    # Normalize output newlines
    out = _normalize_newlines(output_text)

    # Strict EOF rule: allow at most one trailing '\n'
    if out.endswith("\n"):
        out = out[:-1]
        if out.endswith("\n"):
            return False, "Output has more than one trailing newline (extra blank line at EOF)"

    if out == "":
        return False, f"Expected exactly {t} lines of output, got 0"

    lines = out.split("\n")
    if len(lines) != t:
        return False, f"Expected exactly {t} lines of output, got {len(lines)}"

    for case_idx, line in enumerate(lines, start=1):
        if line == "":
            return False, f"Case {case_idx}: empty line; expected an integer"
        if line.strip() != line:
            return False, f"Case {case_idx}: leading/trailing whitespace is not allowed"
        if not _INT_RE.match(line):
            return False, f"Case {case_idx}: expected an integer, got {line!r}"

        try:
            ans = int(line)
        except Exception:
            return False, f"Case {case_idx}: cannot parse integer from {line!r}"

        n = ns[case_idx - 1]
        is_impossible = impossible[case_idx - 1]

        # Trivially checkable feasibility:
        # A tier with >=3 '#' is impossible; otherwise always possible (no other global constraints).
        if is_impossible:
            if ans != -1:
                return (
                    False,
                    f"Case {case_idx}: input contains a tier with >=3 '#', so output must be -1, got {ans}",
                )
            continue
        else:
            if ans == -1:
                return (
                    False,
                    f"Case {case_idx}: all tiers have <=2 '#', so the case is feasible; output must be >= 0, got -1",
                )

        # Basic range sanity (does not verify optimality)
        if ans < 0:
            return False, f"Case {case_idx}: answer must be non-negative (feasible case), got {ans}"

        # Upper bound: each of the n transitions costs at most 6 (3 per robot)
        max_possible = 6 * n
        if ans > max_possible:
            return (
                False,
                f"Case {case_idx}: answer {ans} is too large; must be <= 6*n = {max_possible} for n={n}",
            )

    return True, "OK"


if __name__ == "__main__":
    in_path = os.environ.get("INPUT_PATH")
    out_path = os.environ.get("OUTPUT_PATH")
    if not in_path or not out_path:
        raise SystemExit("INPUT_PATH and OUTPUT_PATH environment variables are required")

    with open(in_path, "r", encoding="utf-8") as f:
        input_text = f.read()
    with open(out_path, "r", encoding="utf-8") as f:
        output_text = f.read()

    ok, _reason = check(input_text, output_text)
    print("True" if ok else "False")
