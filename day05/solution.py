# -------------------------
#   Read in the file
# -------------------------

def read_input():
    """
    Reads the puzzle input from input.txt and returns a list of lines.
    """
    with open("input.txt") as f:
        lines = f.read().strip().splitlines()
    return lines


# -------------------------
#   Helpers
# -------------------------

def is_fresh(ingredient_id, ranges):
    """
    Given a single ingredient_id (int) and a list of ranges [(start, end), ...],
    return True if the id is inside ANY of the ranges (inclusive).
    Otherwise, return False.
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def total_fresh_from_ranges(ranges):
    """
    Given a list of (start, end) ranges, compute how many distinct IDs
    are considered fresh, accounting for overlaps.

    Strategy:
    - If no ranges, answer is 0.
    - Sort ranges by start.
    - Merge overlapping/touching ranges into one big segment at a time.
    - Sum the sizes of the merged segments.
    """
    if not ranges:
        return 0

    # Sort by start value (default tuple sort is fine).
    sorted_ranges = sorted(ranges)

    total = 0
    # Initialize current merged segment with the first range.
    current_start, current_end = sorted_ranges[0]

    # Walk through the remaining ranges.
    for start, end in sorted_ranges[1:]:
        if start <= current_end:
            # Overlaps or touches the current segment.
            # Maybe extend the right side.
            if end > current_end:
                current_end = end
        else:
            # No overlap: close the previous segment.
            total += current_end - current_start + 1
            # Start a new segment.
            current_start, current_end = start, end

    # Close the final segment.
    total += current_end - current_start + 1

    return total


# -------------------------
#   Part 1 Logic
# -------------------------

def part1(lines):
    """
    Count how many of the available ingredient IDs (after the blank line)
    are fresh according to the ranges (before the blank line).
    """

    # 1. Find the blank line that separates ranges from IDs.
    blank_index = None
    for i in range(len(lines)):
        if lines[i].strip() == "":
            blank_index = i
            break

    if blank_index is None:
        raise ValueError("Input missing blank line separator between ranges and IDs.")

    # 2. Build ranges list from lines before the blank.
    ranges = []
    for i in range(blank_index):
        line = lines[i].strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        start = int(start_str)
        end = int(end_str)
        ranges.append((start, end))

    # 3. Build IDs list from lines after the blank.
    ids = []
    for i in range(blank_index + 1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        ids.append(int(line))

    # 4. Count how many IDs are fresh.
    count = 0
    for ingredient_id in ids:
        if is_fresh(ingredient_id, ranges):
            count += 1

    return count


# -------------------------
#   Part 2 Logic
# -------------------------

def part2(lines):
    """
    Ignore the available IDs section. Instead, treat the ranges themselves
    as defining all possible fresh IDs, and count how many distinct IDs
    they cover in total (with overlaps merged).
    """

    # 1. Find the blank line that separates ranges from IDs.
    blank_index = None
    for i in range(len(lines)):
        if lines[i].strip() == "":
            blank_index = i
            break

    if blank_index is None:
        raise ValueError("Input missing blank line separator between ranges and IDs.")

    # 2. Build ranges list from lines before the blank.
    ranges = []
    for i in range(blank_index):
        line = lines[i].strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        start = int(start_str)
        end = int(end_str)
        ranges.append((start, end))

    # 3. Let the helper merge and count all fresh IDs.
    return total_fresh_from_ranges(ranges)


# -------------------------
#   Part 1 Tests
# -------------------------

def test_is_fresh_basic_inside_range():
    ranges = [(3, 5)]
    assert is_fresh(3, ranges)
    assert is_fresh(4, ranges)
    assert is_fresh(5, ranges)


def test_is_fresh_basic_outside_range():
    ranges = [(3, 5)]
    assert not is_fresh(2, ranges)
    assert not is_fresh(6, ranges)


def test_is_fresh_multiple_ranges():
    ranges = [(3, 5), (10, 14)]
    assert is_fresh(4, ranges)
    assert is_fresh(11, ranges)
    assert not is_fresh(9, ranges)


def test_is_fresh_overlapping_ranges():
    ranges = [(10, 14), (12, 18)]
    # 12–14 are in both; 15–18 in second.
    assert is_fresh(12, ranges)
    assert is_fresh(17, ranges)
    assert not is_fresh(9, ranges)
    assert not is_fresh(19, ranges)


def test_part1_example_from_prompt():
    lines = [
        "3-5",
        "10-14",
        "16-20",
        "12-18",
        "",
        "1",
        "5",
        "8",
        "11",
        "17",
        "32",
    ]
    # From the puzzle text: fresh IDs among these are 5, 11, 17 -> 3.
    assert part1(lines) == 3


def test_part1_all_spoiled():
    lines = [
        "10-20",
        "",
        "1",
        "2",
        "3",
    ]
    # All IDs are outside 10–20.
    assert part1(lines) == 0


def test_part1_all_fresh():
    lines = [
        "1-100",
        "",
        "1",
        "2",
        "50",
        "100",
    ]
    assert part1(lines) == 4


# -------------------------
#   Part 2 Helper Tests
# -------------------------

def test_total_fresh_from_ranges_empty():
    ranges = []
    assert total_fresh_from_ranges(ranges) == 0


def test_total_fresh_from_ranges_single_range():
    ranges = [(3, 7)]  # 3,4,5,6,7 → 5 IDs.
    assert total_fresh_from_ranges(ranges) == 5


def test_total_fresh_from_ranges_disjoint_ranges():
    ranges = [
        (1, 3),   # 3 IDs: 1,2,3
        (10, 11), # 2 IDs: 10,11
    ]
    # Total = 3 + 2 = 5.
    assert total_fresh_from_ranges(ranges) == 5


def test_total_fresh_from_ranges_overlapping_ranges():
    ranges = [
        (3, 5),   # 3,4,5
        (5, 10),  # 5..10
    ]
    # Union covers 3..10 → 8 IDs.
    assert total_fresh_from_ranges(ranges) == 8


def test_total_fresh_from_ranges_nested_ranges():
    ranges = [
        (3, 20),
        (5, 10),
        (7, 8),
    ]
    # Everything is inside 3..20 → 18 IDs.
    assert total_fresh_from_ranges(ranges) == 18


def test_total_fresh_from_ranges_example_from_prompt():
    ranges = [
        (3, 5),
        (10, 14),
        (16, 20),
        (12, 18),
    ]
    # From the description: total of 14 IDs.
    assert total_fresh_from_ranges(ranges) == 14


# -------------------------
#   Part 2 Integration Tests
# -------------------------

def test_part2_small_example_from_prompt():
    lines = [
        "3-5",
        "10-14",
        "16-20",
        "12-18",
        "",
        "1",
        "5",
        "8",
        "11",
        "17",
        "32",
    ]
    # From the description: 14 total fresh IDs across the ranges.
    assert part2(lines) == 14


def test_part2_only_one_range():
    lines = [
        "100-105",
        "",
        "50",
        "100",
        "103",
        "200",
    ]
    # Range 100..105 → 6 IDs total.
    assert part2(lines) == 6


# -------------------------
#   Run the Tests
# -------------------------

def run_tests():
    print("Running tests...")

    # Part 1 tests
    test_is_fresh_basic_inside_range()
    test_is_fresh_basic_outside_range()
    test_is_fresh_multiple_ranges()
    test_is_fresh_overlapping_ranges()
    test_part1_example_from_prompt()
    test_part1_all_spoiled()
    test_part1_all_fresh()

    # Part 2 helper tests
    test_total_fresh_from_ranges_empty()
    test_total_fresh_from_ranges_single_range()
    test_total_fresh_from_ranges_disjoint_ranges()
    test_total_fresh_from_ranges_overlapping_ranges()
    test_total_fresh_from_ranges_nested_ranges()
    test_total_fresh_from_ranges_example_from_prompt()

    # Part 2 integration tests
    test_part2_small_example_from_prompt()
    test_part2_only_one_range()

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