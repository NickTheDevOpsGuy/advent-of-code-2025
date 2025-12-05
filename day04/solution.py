# -------------------------
#   Read in the file
# -------------------------

def read_input():
    with open("input.txt") as f:
        lines = f.read().strip().splitlines()
    return lines

# -------------------------
#   Helpers
# -------------------------

def count_neighbors(lines, r, c):
    rows = len(lines)
    cols = len(lines[0])
    count = 0

    # All 8 directions around (r, c)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        # bounds check
        if 0 <= nr < rows and 0 <= nc < cols:
            if lines[nr][nc] == '@':
                count += 1

    return count

def find_accessible_positions(grid):
    rows = len(grid)
    cols = len(grid[0])
    positions = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                n = count_neighbors(grid, r, c)
                if n < 4:
                    positions.append((r, c))

    return positions

# -------------------------
#   Part 1 Logic
# -------------------------

def part1(lines):
    total = 0
    
    for r in range(len(lines)):             # loop rows
        for c in range(len(lines[r])):      # loop columns
            
            if lines[r][c] == '@':
                n = count_neighbors(lines, r, c)
                if n < 4:
                    total += 1

    return total

# -------------------------
#   Part 2 Logic
# -------------------------

def part2(lines):
    grid = [list(row) for row in lines]
    total_removed = 0

    while True:
        positions = find_accessible_positions(grid)
        if not positions:
            break

        for r, c in positions:
            grid[r][c] = '.'

        total_removed += len(positions)

    return total_removed

# -------------------------
#   Part 1 Test Suite (Optional)
# -------------------------

def test_single_roll_accessible():
    # Single roll with no neighbors – should be accessible
    grid = [".@."]
    assert part1(grid) == 1


def test_two_adjacent_rolls_both_accessible():
    # Two touching rolls – each has 1 neighbor (< 4), so both accessible
    grid = ["@@"]
    assert part1(grid) == 2


def test_center_roll_blocked_in_dense_cluster():
    # 3x3 block of rolls – corners have 3 neighbors (accessible),
    # edges have 5 neighbors (blocked), center has 8 (blocked)
    # Accessible: 4 corners only
    grid = [
        "@@@",
        "@@@",
        "@@@",
    ]
    assert part1(grid) == 4


def test_edge_roll_handled_correctly():
    # Top-left roll with no neighbors – must not wrap around
    grid = [
        "@.",
        "..",
    ]
    assert part1(grid) == 1


def test_diagonal_neighbors_counted():
    # Diagonal neighbors still count as adjacent
    grid = [
        "@.",
        ".@",
    ]
    # Each @ has exactly 1 neighbor -> both accessible
    assert part1(grid) == 2


def test_mixed_pattern():
    # Mixed layout with clusters and spacing
    grid = [
        ".@.@.",
        "@@.@.",
        ".@.@.",
    ]
    # By manual counting, all 7 rolls have fewer than 4 neighbors
    assert part1(grid) == 7


def test_no_rolls_returns_zero():
    grid = [
        "....",
        "....",
    ]
    assert part1(grid) == 0


def test_full_example_matches_expected():
    # Example from the problem statement – should have 13 accessible rolls
    grid = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
    assert part1(grid) == 13

# -------------------------
#   Part 2 Test Suite (Optional)
# -------------------------

def test_part2_no_rolls_returns_zero():
    grid = [
        "....",
        "....",
    ]
    assert part2(grid) == 0


def test_part2_single_accessible_roll_removed():
    # Single roll with no neighbors – should be removable
    grid = [".@."]
    # Part 1: accessible = 1, Part 2: it gets removed → total_removed = 1
    assert part2(grid) == 1


def test_part2_two_adjacent_rolls_both_removed():
    # Two touching rolls – each has 1 neighbor (< 4), both should be removed
    grid = ["@@"]
    assert part2(grid) == 2


def test_part2_dense_block_no_rolls_removed():
    # 3x3 block of rolls – only corners are accessible initially (3 neighbors each)
    # BUT after you remove the 4 corners, new edges become accessible, etc.
    # Eventually, everything is removable in Part 2.
    grid = [
        "@@@",
        "@@@",
        "@@@",
    ]
    # All 9 can be removed over multiple rounds
    assert part2(grid) == 9


def test_part2_example_total():
    # Example from the problem statement – should remove 43 rolls total
    grid = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
    assert part2(grid) == 43

#
# -------------------------
#   Run the Tests
# -------------------------

def run_tests():
    print("Running tests...")

    test_single_roll_accessible()
    test_two_adjacent_rolls_both_accessible()
    test_center_roll_blocked_in_dense_cluster()
    test_edge_roll_handled_correctly()
    test_diagonal_neighbors_counted()
    test_mixed_pattern()
    test_no_rolls_returns_zero()
    test_full_example_matches_expected()
    test_two_adjacent_rolls_both_accessible()
    test_center_roll_blocked_in_dense_cluster()
    test_edge_roll_handled_correctly()
    test_diagonal_neighbors_counted()
    test_mixed_pattern()
    test_no_rolls_returns_zero()
    test_full_example_matches_expected()
    test_part2_no_rolls_returns_zero()

    print("All tests passed!")

#
# -------------------------
#   Main Code Section
# -------------------------

if __name__ == "__main__":
    RUN_TESTS = False

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))