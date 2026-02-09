#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string>
#include <utility>
#include <vector>

using namespace std;

static vector<pair<int, int>> buildAllowedPairsForRow(const string &row) {
    vector<int> cols;
    for (int j = 0; j < 4; j++) {
        if (row[j] == '#') {
            cols.push_back(j + 1); // lanes are 1..4
        }
    }

    vector<pair<int, int>> allowed;

    if (cols.size() == 0) {
        // No constraint: robots can stand anywhere (including same lane).
        for (int a = 1; a <= 4; a++) {
            for (int b = 1; b <= 4; b++) {
                allowed.push_back({a, b});
            }
        }
    } else if (cols.size() == 1) {
        // At least one robot must stand on that lane.
        int c = cols[0];
        for (int a = 1; a <= 4; a++) {
            for (int b = 1; b <= 4; b++) {
                if (a == c || b == c) {
                    allowed.push_back({a, b});
                }
            }
        }
    } else if (cols.size() == 2) {
        // Robots must occupy exactly those two lanes (in any assignment).
        int c1 = cols[0], c2 = cols[1];
        allowed.push_back({c1, c2});
        allowed.push_back({c2, c1});
    } else {
        // 3 or 4 artifacts cannot be handled by only two robots.
        // allowed remains empty.
    }

    return allowed;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<string> rows(n);
        for (int i = 0; i < n; i++) {
            cin >> rows[i];
            // Input is guaranteed valid by the statement (length 4, '.' or '#').
        }

        // Build constraints in processing order: bottom tier to top tier.
        vector<vector<pair<int, int>>> allowedPairs(n);
        bool impossible = false;
        for (int i = 0; i < n; i++) {
            const string &row = rows[n - 1 - i];
            allowedPairs[i] = buildAllowedPairsForRow(row);
            if (allowedPairs[i].empty()) {
                impossible = true;
            }
        }

        if (impossible) {
            cout << -1 << "\n";
            continue;
        }

        // Brute-force enumeration of all possible robot positions for every tier.
        // This is intentionally exponential: product over tiers of allowedPairs[i].size().
        const long long inf = numeric_limits<long long>::max() / 4;
        long long best = inf;

        // Iterative DFS/backtracking to avoid recursion depth issues.
        vector<size_t> choiceIndex(n, 0);
        vector<int> prevAAtDepth(n + 1, 0), prevBAtDepth(n + 1, 0);
        vector<long long> costAtDepth(n + 1, 0);

        prevAAtDepth[0] = 1; // initial positions before the first processed tier
        prevBAtDepth[0] = 4;
        costAtDepth[0] = 0;

        int depth = 0;
        while (depth >= 0) {
            if (depth == n) {
                // Completed a full assignment for all tiers.
                if (costAtDepth[depth] < best) {
                    best = costAtDepth[depth];
                }
                depth--;
                continue;
            }

            if (choiceIndex[depth] >= allowedPairs[depth].size()) {
                // Exhausted all choices at this depth; backtrack.
                choiceIndex[depth] = 0;
                depth--;
                continue;
            }

            // Try next allowed pair at this tier.
            pair<int, int> nextPos = allowedPairs[depth][choiceIndex[depth]];
            choiceIndex[depth]++;

            int nextA = nextPos.first;
            int nextB = nextPos.second;

            long long moveCost = llabs((long long)nextA - prevAAtDepth[depth]) +
                                 llabs((long long)nextB - prevBAtDepth[depth]);

            prevAAtDepth[depth + 1] = nextA;
            prevBAtDepth[depth + 1] = nextB;
            costAtDepth[depth + 1] = costAtDepth[depth] + moveCost;

            depth++;
        }

        if (best == inf) {
            cout << -1 << "\n";
        } else {
            cout << best << "\n";
        }
    }

    return 0;
}