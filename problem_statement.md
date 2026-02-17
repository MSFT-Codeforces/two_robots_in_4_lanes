Time Limit: **4 seconds**

Memory Limit: **32 MB**

In an underground archive there are $4$ parallel corridors (lanes) numbered $1$ to $4$. The archive has $n$ tiers stacked vertically. Each tier is described by a string of length $4$ consisting of characters `'#'` and `'.'`:

- `'#'` means there is an artifact to handle in that corridor on this tier.
- `'.'` means nothing to do there.

The $n$ strings are given from **top tier to bottom tier**, but the handling is performed from **bottom tier to top tier** (i.e., the last input row is processed first).

You control two robots:

- Robot $A$ (left robot)
- Robot $B$ (right robot)

Before processing begins (before the bottom tier), robot $A$ is in corridor $1$, and robot $B$ is in corridor $4$. The robots may move to satisfy the bottom tier's requirement, and that initial move cost is included.

### Movement Cost
On each processed tier, each robot must stand in exactly one corridor from $1$ to $4$. Robots may move from the initial position to the first processed tier, and between any two consecutive processed tiers.  
If robot $A$ moves from $A_{old}$ to $A_{new}$ and robot $B$ moves from $B_{old}$ to $B_{new}$, the energy cost is:
$$
|A_{new}-A_{old}| + |B_{new}-B_{old}|
$$

### Constraints per Tier
Let $S$ be the set of corridors that contain `'#'` in the currently processed tier.

- If $|S| = 0$: no constraint (robots may stand anywhere).
- If $|S| = 1$: at least one robot must stand on that corridor.
- If $|S| = 2$: both artifacts must be handled simultaneously, so the robots must occupy **exactly those two corridors** (in any assignment).
- If $|S| \ge 3$: it is impossible to handle this tier with only two robots.

Robots are distinct. They may share the same corridor unless $|S| = 2$ (which forces two different corridors). There is no ordering constraint such as $A \le B$; robots may cross or swap corridors between tiers.


For each test case, find the minimum total energy needed to process all tiers, or output $-1$ if impossible.

**Input Format:-**

The first line contains an integer $t$ — the number of test cases.  
For each test case:
- The first line contains an integer $n$ — the number of tiers.
- The next $n$ lines contain strings of length $4$ (top to bottom), consisting only of `'.'` and `'#'`.

**Output Format:-**

For each test case, output a single integer — the minimum total energy required, or $-1$ if it is impossible.

**Constraints:-**

- $1 \le t \le 10^4$
- $1 \le n \le 2 \cdot 10^5$
- The sum of $n$ over all test cases does not exceed $2 \cdot 10^5$

**Examples:-**
 - **Input:**
```
5
1
....
1
####
2
#...
....
2
.##.
#..#
3
....
.#..
..##
```

 - **Output:**
```
0
-1
0
2
3
```

 - **Input:**
```
1
6
..#.
#...
...#
#...
...#
.#..
```

 - **Output:**
```
3
```

**Note:-**

The following bullets explain how each sample’s output is derived. The first five bullets refer to **Sample 1** and map to its five output lines in order. The last bullet refers to **Sample 2** and explains why the program outputs $3$.

- **Sample 1, test case 1** (output line $0$): Only one tier "...." (no artifacts), so both robots can stay at their starting corridors $(1,4)$ and the total energy is $0$.

- **Sample 1, test case 2** (output line $-1$): One tier "####", so $|S|=4 \ge 3$ and it is impossible to handle all artifacts with two robots; the answer is $-1$.

- **Sample 1, test case 3** (output line $0$): Processed bottom-to-top: first "...." (no constraint), then "#..." (artifact in corridor $1$). Keeping $(A,B)=(1,4)$ throughout satisfies the last tier (robot $A$ is already in corridor $1$), so the total energy is $0$.

- **Sample 1, test case 4** (output line $2$): Processed bottom-to-top: first "#..#" forces the robots to be in corridors $\{1,4\}$, which matches the start $(1,4)$ with cost $0$. Then ".##." forces corridors $\{2,3\}$; choosing $(A,B)=(2,3)$ costs
  $$
  |2-1|+|3-4|=2,
  $$
  which is minimal, so the answer is $2$.

- **Sample 1, test case 5** (output line $3$): Processed bottom-to-top: first "..##" forces corridors $\{3,4\}$, best reached as $(3,4)$ with cost $|3-1|+|4-4|=2$. Then ".#.." requires at least one robot in corridor $2$, best done by moving to $(2,4)$ with additional cost $|2-3|+|4-4|=1$. The top tier "...." has no constraint, so no more movement is needed; total energy $2+1=3$.

- **Sample 2** (single output line $3$): The single test case is processed bottom-to-top. The bottom-to-top tier order is:
  1. ".#.." (bottom row)
  2. "...#"
  3. "#..."
  4. "...#"
  5. "#..."
  6. "..#." (top row)
  One optimal sequence of robot positions is:
  1. ".#.." (need corridor $2$): $(1,4)\rightarrow(2,4)$, cost $1$.
  2. "...#" (need corridor $4$): stay $(2,4)$, cost $0$.
  3. "#..." (need corridor $1$): $(2,4)\rightarrow(1,4)$, cost $1$.
  4. "...#" (need corridor $4$): stay $(1,4)$, cost $0$.
  5. "#..." (need corridor $1$): stay $(1,4)$, cost $0$.
  6. "..#." (need corridor $3$): $(1,4)\rightarrow(1,3)$, cost $1$.
  The total energy is $1+1+1=3$, which is the value printed in the **Sample 2 Output** block above.