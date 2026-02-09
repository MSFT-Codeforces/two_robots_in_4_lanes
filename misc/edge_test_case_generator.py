
def make_input(testcases):
    # testcases: list of (n, rows_top_to_bottom)
    out = []
    out.append(str(len(testcases)))
    for n, rows in testcases:
        assert n == len(rows)
        out.append(str(n))
        for r in rows:
            assert len(r) == 4 and set(r) <= {".", "#"}
            out.append(r)
    return "\n".join(out) + "\n"

inputs = []

# Input 1: minimal, all empty (|S|=0)
inputs.append(make_input([
    (1, ["...."]),
]))

# Input 2: minimal, single # at col 1 (tests initial placement and |S|=1)
inputs.append(make_input([
    (1, ["#..."]),
]))

# Input 3: minimal, single # at col 4 (tests initial placement and |S|=1)
inputs.append(make_input([
    (1, ["...#"]),
]))

# Input 4: minimal, single # at inner col 2 (|S|=1)
inputs.append(make_input([
    (1, [".#.."]),
]))

# Input 5: minimal, forced pair adjacent (1,2) (|S|=2)
inputs.append(make_input([
    (1, ["##.."]),
]))

# Input 6: minimal, forced pair far apart (1,4) (|S|=2)
inputs.append(make_input([
    (1, ["#..#"]),
]))

# Input 7: minimal, forced pair middle (2,3) (|S|=2)
inputs.append(make_input([
    (1, [".##."]),
]))

# Input 8: minimal impossible (3 #'s) => must be -1
inputs.append(make_input([
    (1, ["###."]),
]))

# Input 9: minimal impossible (4 #'s) => must be -1
inputs.append(make_input([
    (1, ["####"]),
]))

# Input 10: direction-sensitivity (wrong processing order gives different cost)
# Input is top->bottom but must process bottom->top.
inputs.append(make_input([
    (2, [
        "#..#",  # processed last
        ".##.",  # processed first
    ]),
]))

# Input 11: unconstrained gaps between constraints (tests correct handling of |S|=0 tiers)
inputs.append(make_input([
    (5, [
        "#...",  # processed last
        "....",
        "....",
        "....",
        "...#",  # processed first
    ]),
]))

# Input 12: alternating forced pairs, many different column pairs (assignment/min over matchings)
inputs.append(make_input([
    (6, [
        "#..#",  # (1,4)
        ".##.",  # (2,3)
        "##..",  # (1,2)
        "..##",  # (3,4)
        "#.#.",  # (1,3)
        ".#.#",  # (2,4)
    ]),
]))

# Input 13: I/O + reset stress: many test cases (t=10000), n=1 each, mixed feasibility
tc13 = []
T = 10000
for i in range(1, T + 1):
    if i % 1000 == 0:
        row = "###."   # impossible occasionally
    elif i % 4 == 1:
        row = "...."   # empty
    elif i % 4 == 2:
        row = "#..."   # single #
    elif i % 4 == 3:
        row = ".##."   # forced pair
    else:
        row = "#..#"   # forced far pair
    tc13.append((1, [row]))
inputs.append(make_input(tc13))

# Input 14: late impossibility (impossible tier is at the TOP of input, processed LAST)
inputs.append(make_input([
    (4, [
        "###.",  # processed last -> still must output -1
        "#..#",
        "....",
        ".##.",  # processed first
    ]),
]))

# Input 15: maximum n stress (n=200000), feasible mix of |S|=0 and |S|=1
n15 = 200000
pattern = ["....", "#...", ".#..", "..#.", "...#"]
rows15 = [pattern[i % len(pattern)] for i in range(n15)]
inputs.append(make_input([
    (n15, rows15),
]))

print("Test Cases: ")
for idx, s in enumerate(inputs, 1):
    print(f"Input {idx}:")
    print(s, end="")  # avoid adding an extra newline beyond the one in s
    print()  # single blank line between inputs
