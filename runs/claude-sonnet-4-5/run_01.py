
def solve(n, tiers):
    # Process from bottom to top
    tiers = tiers[::-1]
    
    INF = float('inf')
    
    # dp[a][b] = minimum cost with robot A at a, robot B at b
    dp = [[INF] * 5 for _ in range(5)]
    dp[1][4] = 0  # Initial positions
    
    for tier_str in tiers:
        # Find artifact positions (1-indexed)
        artifacts = [i + 1 for i in range(4) if tier_str[i] == '#']
        
        # Impossible if more than 2 artifacts
        if len(artifacts) > 2:
            return -1
        
        new_dp = [[INF] * 5 for _ in range(5)]
        
        # Try all transitions
        for prev_a in range(1, 5):
            for prev_b in range(1, 5):
                if dp[prev_a][prev_b] == INF:
                    continue
                
                for curr_a in range(1, 5):
                    for curr_b in range(1, 5):
                        # Check if current state is valid
                        valid = False
                        
                        if len(artifacts) == 0:
                            # No constraints
                            valid = True
                        elif len(artifacts) == 1:
                            # At least one robot at artifact position
                            valid = (curr_a == artifacts[0] or curr_b == artifacts[0])
                        else:  # len(artifacts) == 2
                            # Both robots must occupy exactly these two positions
                            # and they must be at different positions
                            valid = (curr_a != curr_b and 
                                   set([curr_a, curr_b]) == set(artifacts))
                        
                        if valid:
                            cost = dp[prev_a][prev_b] + \
                                   abs(curr_a - prev_a) + abs(curr_b - prev_b)
                            new_dp[curr_a][curr_b] = min(new_dp[curr_a][curr_b], cost)
        
        dp = new_dp
    
    # Find minimum cost among all final states
    result = INF
    for a in range(1, 5):
        for b in range(1, 5):
            result = min(result, dp[a][b])
    
    return result if result != INF else -1

# Main
t = int(input())
for _ in range(t):
    n = int(input())
    tiers = [input().strip() for _ in range(n)]
    print(solve(n, tiers))
