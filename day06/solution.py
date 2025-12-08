#!/usr/bin/env python3
"""
Advent of Code 2025 – Tachyon Manifold (Beams & Splitters)

Part 1: classical beams (they merge when they overlap).
Part 2: quantum many-worlds beams (every path is its own timeline).
"""

# -------------------------
#   Input
# -------------------------


def read_input():
    """
    Read puzzle input from input.txt and return as list of lines.
    """
    with open("input.txt") as f:
        return f.read().rstrip("\n").splitlines()


# -------------------------
#   Helpers
# -------------------------


def find_start(grid):
    """
    Find the coordinates of 'S' in the grid.

    grid: list[str]
    returns: (row, col)
    """
    for r, row in enumerate(grid):
        c = row.find("S")
        if c != -1:
            return r, c
    raise ValueError("No starting 'S' found in grid")


def step_classical(grid, beams):
    """
    Single simulation step for Part 1 (classical tachyon beams).

    - Beams always move one cell DOWN.
    - If a beam enters a splitter '^':
        * That beam stops.
        * Two new beams are created: one to the LEFT, one to the RIGHT
          on the same row as the splitter.
    - If multiple beams overlap in the same cell, they are considered
      a single beam in the next step (we deduplicate positions).
      This matches the example where multiple splitters "dump into"
      the same spot and the diagram only shows a single beam there.

    grid: list[str]
    beams: list[(row, col)] – active beam positions for this step

    returns:
        next_beams: list[(row, col)]
        splits_this_step: int
    """
    h = len(grid)
    w = len(grid[0])

    # Classical mode: overlapping beams merge into one.
    beams = list(set(beams))

    next_beams = []
    splits_this_step = 0

    for (r, c) in beams:
        nr = r + 1  # one row down
        if nr < 0 or nr >= h or c < 0 or c >= w:
            # Falls out of the manifold; beam dies
            continue

        cell = grid[nr][c]

        if cell in ".S":
            # Just empty space (or the S row if we ever pass it):
            # beam continues straight down.
            next_beams.append((nr, c))

        elif cell == "^":
            # Beam stops, splits left and right (if in bounds).
            splits_this_step += 1

            if c - 1 >= 0:
                next_beams.append((nr, c - 1))
            if c + 1 < w:
                next_beams.append((nr, c + 1))

        else:
            # Unknown character: treat as empty space just in case.
            next_beams.append((nr, c))

    return next_beams, splits_this_step


def step_quantum(grid, beams):
    """
    Single simulation step for Part 2 (quantum many-worlds beams).

    Key difference from classical:
    - We DO NOT merge overlapping beams. Every beam is its own timeline.
    - Every beam that falls out the bottom creates a new finished timeline.

    grid: list[str]
    beams: list[(row, col)] – active beams

    returns:
        next_beams: list[(row, col)]
        exited_this_step: int – how many beams left the manifold this step
    """
    h = len(grid)
    w = len(grid[0])

    next_beams = []
    exited_this_step = 0

    for (r, c) in beams:
        nr = r + 1
        if nr < 0 or nr >= h or c < 0 or c >= w:
            # This beam has left the grid → it’s a completed timeline.
            exited_this_step += 1
            continue

        cell = grid[nr][c]

        if cell in ".S":
            # Keep going straight down.
            next_beams.append((nr, c))

        elif cell == "^":
            # Beam stops, but in this timeline it splits into
            # *two* separate timelines: left and right beams.
            # No merging here.
            if c - 1 >= 0:
                next_beams.append((nr, c - 1))
            if c + 1 < w:
                next_beams.append((nr, c + 1))

        else:
            # Unknown: treat as empty.
            next_beams.append((nr, c))

    return next_beams, exited_this_step


# -------------------------
#   Part 1 Logic
# -------------------------


def part1(lines):
    """
    Run classical beam simulation until all beams leave the grid.
    Return the total number of times a beam is split.

    This matches the example where the answer is 21 splits.
    """
    grid = lines
    start_r, start_c = find_start(grid)

    beams = [(start_r, start_c)]
    total_splits = 0

    # Keep ticking downward until no beams left.
    while beams:
        beams, splits = step_classical(grid, beams)
        total_splits += splits

    return total_splits


# -------------------------
#   Part 2 Logic
# -------------------------


def part2(lines):
    """
    Quantum many-worlds version.

    A single tachyon particle splits at each splitter, creating
    branching timelines. We simulate all beams independently
    without merging them, and count how many beams eventually
    fall out the bottom of the grid.

    That count = number of distinct timelines.
    """
    grid = lines
    start_r, start_c = find_start(grid)

    beams = [(start_r, start_c)]
    total_timelines = 0

    # As long as there is at least one active beam in some timeline,
    # keep simulating.
    while beams:
        beams, exited = step_quantum(grid, beams)
        total_timelines += exited

    return total_timelines


# -------------------------
#   Test Suite (Part 1)
# -------------------------


def test_part1_no_splitters():
    grid = [
        "..S..",
        ".....",
        ".....",
    ]
    # Beam just goes straight down and then leaves; no splits.
    assert part1(grid) == 0


def test_part1_single_splitter():
    grid = [
        "..S..",
        "..^..",
        ".....",
    ]
    # S (0,2) → (1,2) '^' → one split event.
    assert part1(grid) == 1


def test_part1_edge_splitter():
    grid = [
        "S....",
        "^....",
        ".....",
    ]
    # Beam drops onto '^' at (1,0).
    # Only right child is in bounds.
    assert part1(grid) == 1


def test_part1_example_prompt():
    # Example from the problem description:
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
    # The statement says: a tachyon beam is split 21 times.
    assert part1(grid) == 21


# -------------------------
#   Test Suite (Part 2)
# -------------------------


def test_part2_no_splitters():
    grid = [
        "..S..",
        ".....",
        ".....",
    ]
    # Single beam falls out bottom once → 1 timeline.
    assert part2(grid) == 1


def test_part2_single_splitter_two_paths():
    grid = [
        "..S..",
        "..^..",
        ".....",
        ".....",
    ]
    # Beam hits '^' once → left + right beams.
    # Both eventually fall off bottom, so 2 timelines.
    assert part2(grid) == 2


def test_part2_example_prompt():
    # Same big example, now quantum:
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
    # The prompt says there are 40 distinct timelines.
    assert part2(grid) == 40


def test_part2_multiple_layers_small():
    # Simple stacked splitters to sanity-check growth.
    grid = [
        "..S..",
        "..^..",
        "..^..",
        ".....",
        ".....",
    ]
    # Step summary:
    #   Start: 1 beam
    #   Hit first '^' → 2 beams
    #   Each hits next '^' → each splits into 2 → 4 beams
    #   All 4 eventually fall out → 4 timelines
    assert part2(grid) == 4


# -------------------------
#   Run Tests
# -------------------------


def run_tests():
    print("Running tests...")

    # Part 1 tests
    test_part1_no_splitters()
    test_part1_single_splitter()
    test_part1_edge_splitter()
    test_part1_example_prompt()

    # Part 2 tests
    test_part2_no_splitters()
    test_part2_single_splitter_two_paths()
    test_part2_example_prompt()
    test_part2_multiple_layers_small()

    print("All tests passed!")


# -------------------------
#   Main
# -------------------------

if __name__ == "__main__":
    RUN_TESTS = False  # set to True to run tests instead of solving

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))