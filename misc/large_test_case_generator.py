
import sys
import random

out = sys.stdout

def row_from_cols(cols):
    s = ['.'] * 4
    for c in cols:
        s[c - 1] = '#'
    return ''.join(s)

R_EMPTY = "...."
R_SINGLE = [row_from_cols([i]) for i in range(1, 5)]  # ["#...", ".#..", "..#.", "...#"]
R_14 = row_from_cols([1, 4])  # "#..#"
R_23 = row_from_cols([2, 3])  # ".##."
R_12 = row_from_cols([1, 2])  # "##.."
R_34 = row_from_cols([3, 4])  # "..##"
R_IMP3 = "###."               # impossible tier (|S|=3)

def emit_input_header(idx):
    out.write(f"Input {idx}:\n")

def emit_single_test(n, gen_row):
    out.write("1\n")
    out.write(f"{n}\n")
    for i in range(n):
        out.write(gen_row(i) + "\n")

def emit_many_tests(t, n_each, case_rows_func):
    out.write(str(t) + "\n")
    for tc in range(t):
        out.write(str(n_each) + "\n")
        for i in range(n_each):
            out.write(case_rows_func(tc, i) + "\n")

out.write("Test Cases:\n")

# Input 1: Max n, all unconstrained (all empty)
emit_input_header(1)
emit_single_test(200000, lambda i: R_EMPTY)
out.write("\n")

# Input 2: Max n, forced pairs alternating (|S|=2 every row)
emit_input_header(2)
emit_single_test(200000, lambda i: (R_14 if (i % 2 == 0) else R_23))
out.write("\n")

# Input 3: Max n, single '#' cycling through all columns (|S|=1)
emit_input_header(3)
emit_single_test(200000, lambda i: R_SINGLE[i % 4])
out.write("\n")

# Input 4: Max n, alternating single '#' on lane 1 and lane 4 (catches misread of |S|=1)
emit_input_header(4)
emit_single_test(200000, lambda i: (R_SINGLE[0] if (i % 2 == 0) else R_SINGLE[3]))
out.write("\n")

# Input 5: Max n, strong direction-sensitivity (processing is bottom->top)
# Top half requires {1,4}, bottom half requires {2,3}
emit_input_header(5)
n = 200000
emit_single_test(n, lambda i: (R_14 if i < n // 2 else R_23))
out.write("\n")

# Input 6: Max n, late impossibility (impossible tier is processed last => placed at top of input)
emit_input_header(6)
emit_single_test(200000, lambda i: (R_IMP3 if i == 0 else R_SINGLE[(i - 1) % 4]))
out.write("\n")

# Input 7: Max n, early impossibility (impossible tier is processed first => placed at bottom of input)
emit_input_header(7)
emit_single_test(200000, lambda i: (R_IMP3 if i == 200000 - 1 else R_SINGLE[i % 4]))
out.write("\n")

# Input 8: Max t (10000) with small n (20) summing to 200k, mixed patterns (reset/I/O stress)
emit_input_header(8)
def rows_small(tc, i):
    mode = tc % 5
    if mode == 0:
        return R_EMPTY
    if mode == 1:
        # alternating lane1/lane4 singles
        return R_SINGLE[0] if (i % 2 == 0) else R_SINGLE[3]
    if mode == 2:
        # alternating forced pairs
        return R_12 if (i % 2 == 0) else R_34
    if mode == 3:
        # cycle singles
        return R_SINGLE[i % 4]
    # mode == 4: direction-sensitivity within each small case
    return R_14 if i < 10 else R_23

emit_many_tests(t=10000, n_each=20, case_rows_func=rows_small)
out.write("\n")

# Input 9: Max n, pseudo-random mixture of |S|=0,1,2 (stress many viable states)
emit_input_header(9)
rng = random.Random(123456)
pair_choices = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
def rand_row(_i):
    x = rng.randrange(100)
    if x < 50:
        return R_EMPTY
    elif x < 80:
        c = 1 + rng.randrange(4)
        return R_SINGLE[c - 1]
    else:
        a, b = pair_choices[rng.randrange(len(pair_choices))]
        return row_from_cols([a, b])

emit_single_test(200000, rand_row)
out.write("\n")

# Input 10: Max n, lots of empty tiers with periodic forced pairs (tests correct handling of |S|=0 tiers)
emit_input_header(10)
block = ([R_EMPTY] * 50) + [R_12] + ([R_EMPTY] * 50) + [R_34]  # length 102
L = len(block)
emit_single_test(200000, lambda i: block[i % L])
