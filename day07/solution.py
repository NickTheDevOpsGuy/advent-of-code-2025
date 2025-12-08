# -------------------------
#   Read in the file
# -------------------------

def read_input(path="input.txt"):
    """
    Reads the puzzle input and returns a list of lines.
    """
    with open(path) as f:
        return f.read().rstrip("\n").splitlines()


# -------------------------
#   Helpers
# -------------------------

def find_start(grid):
    """
    Find the coordinates of 'S' in the grid.
    Returns (row, col).
    """
    for r, row in enumerate(grid):
        c = row.find("S")
        if c != -1:
            return r, c
    raise ValueError("No 'S' found in grid.")


def build_classical_dp(grid):
    """
    Build and return a memoized function splits_from(r, c) for Part 1.

    splits_from(r, c) = number of splits caused by a single classical beam
    that is currently at position (r, c) in the grid, moving downward.
    """
    rows = len(grid)
    cols = len(grid[0])
    memo = {}

    def splits_from(r, c):
        # If next step would go off the bottom, we're done.
        nr = r + 1
        if nr >= rows or c < 0 or c >= cols:
            return 0

        key = (r, c)
        if key in memo:
            return memo[key]

        cell = grid[nr][c]

        if cell == '.':
            # keep going straight down
            result = splits_from(nr, c)
        elif cell == '^':
            # We split here
            total = 1  # this splitter itself

            # left branch
            if c - 1 >= 0:
                total += splits_from(nr, c - 1)
            # right branch
            if c + 1 < cols:
                total += splits_from(nr, c + 1)

            result = total
        elif cell == 'S':
            # If S ever appears below, treat it like empty space
            result = splits_from(nr, c)
        else:
            # Any other character: treat as empty space
            result = splits_from(nr, c)

        memo[key] = result
        return result

    return splits_from


def build_quantum_dp(grid):
    """
    Build and return a memoized function ways_from(r, c) for Part 2.

    ways_from(r, c) = number of quantum timelines that result from
    a single particle that is currently at position (r, c), moving downward.

    A timeline finishes when the beam leaves the grid
    (either off the bottom, or off the sides when splitting).
    """
    rows = len(grid)
    cols = len(grid[0])
    memo = {}

    def ways_from(r, c):
        # Next row the beam would move into
        nr = r + 1

        # If going off the bottom, that completes exactly one timeline.
        if nr >= rows:
            return 1

        if c < 0 or c >= cols:
            # Shouldn't happen for in-grid starting calls,
            # but treat it as an already-finished timeline.
            return 1

        key = (r, c)
        if key in memo:
            return memo[key]

        cell = grid[nr][c]

        if cell == '.':
            # keep going straight down
            result = ways_from(nr, c)
        elif cell == '^':
            # Particle hits splitter: time splits.

            # Left child appears at (nr, c-1)
            if c - 1 < 0:
                left_ways = 1  # immediately off the left side
            else:
                left_ways = ways_from(nr, c - 1)

            # Right child appears at (nr, c+1)
            if c + 1 >= cols:
                right_ways = 1  # immediately off the right side
            else:
                right_ways = ways_from(nr, c + 1)

            result = left_ways + right_ways
        elif cell == 'S':
            # Treat like empty path
            result = ways_from(nr, c)
        else:
            # Unknown char: treat like empty
            result = ways_from(nr, c)

        memo[key] = result
        return result

    return ways_from


# -------------------------
#   Part 1 Logic
# -------------------------

def part1(lines):
    """
    Classical beams: each time a beam hits '^', it splits left and right.
    Count how many times that happens in total.
    """
    grid = lines
    sr, sc = find_start(grid)

    splits_from = build_classical_dp(grid)

    # Beam starts at S, moving downward
    return splits_from(sr, sc)


# -------------------------
#   Part 2 Logic
# -------------------------

def part2(lines):
    """
    Quantum manifold: one particle, but every time it hits a splitter,
    time forks and we keep all branches.

    Return total number of distinct timelines after all paths finish.
    """
    grid = lines
    sr, sc = find_start(grid)

    ways_from = build_quantum_dp(grid)

    # Particle starts at S, moving downward
    return ways_from(sr, sc)


# -------------------------
#   Part 1 Tests
# -------------------------

def test_part1_prompt_example():
    """
    The example given in the prompt: total splits = 21.
    """
    grid = [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "...............",
    ]
    assert part1(grid) == 21


def test_part1_no_splitters():
    grid = [
        "....S....",
        ".........",
        ".........",
    ]
    # Just a straight beam, no splits
    assert part1(grid) == 0


def test_part1_one_splitter():
    grid = [
        "....S....",
        "....^....",
        ".........",
    ]
    # The beam hits exactly one splitter
    assert part1(grid) == 1


# -------------------------
#   Part 2 Tests
# -------------------------

def test_part2_prompt_example():
    """
    From the prompt: quantum version gives 40 timelines.
    """
    grid = [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "...............",
    ]
    assert part2(grid) == 40


def test_part2_no_splitters():
    grid = [
        "....S....",
        ".........",
        ".........",
    ]
    # Only one straight path down and off the bottom
    assert part2(grid) == 1


def test_part2_edge_splitter():
    grid = [
        "S.......",
        "^.......",
        "........",
    ]
    # At the splitter:
    # - left child would go off the left edge immediately → 1 timeline
    # - right child continues downward → another timeline
    # Total = 2
    assert part2(grid) == 2


# -------------------------
#   Run the Tests
# -------------------------

def run_tests():
    print("Running tests...")

    test_part1_prompt_example()
    test_part1_no_splitters()
    test_part1_one_splitter()

    test_part2_prompt_example()
    test_part2_no_splitters()
    test_part2_edge_splitter()

    print("All tests passed!")


# -------------------------
#   Main Code Section
# -------------------------

if __name__ == "__main__":
    RUN_TESTS = False  # flip to True to run tests instead of solving

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))