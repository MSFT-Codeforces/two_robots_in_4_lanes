
import sys

def is_single_int_line(line: str):
    # Allow leading/trailing spaces, but no extra tokens.
    parts = line.strip().split()
    if len(parts) != 1:
        return None
    try:
        return int(parts[0])
    except:
        return None

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        print("False")
        return

    idx = 0
    t = is_single_int_line(data[idx])
    if t is None or not (1 <= t <= 10**4):
        print("False")
        return
    idx += 1

    total_n = 0

    for _ in range(t):
        if idx >= len(data):
            print("False")
            return

        n = is_single_int_line(data[idx])
        if n is None or not (1 <= n <= 2 * 10**5):
            print("False")
            return
        idx += 1

        total_n += n
        if total_n > 2 * 10**5:
            print("False")
            return

        for _r in range(n):
            if idx >= len(data):
                print("False")
                return
            row = data[idx]

            # Strict row format: exactly 4 characters, no surrounding whitespace.
            if row != row.strip():
                print("False")
                return
            if len(row) != 4:
                print("False")
                return
            for ch in row:
                if ch not in ".#":
                    print("False")
                    return
            idx += 1

    # Strictly no extra lines beyond the expected input.
    if idx != len(data):
        print("False")
        return

    print("True")

if __name__ == "__main__":
    main()
