# ----------------------------------------------------
#   Read Input
# ----------------------------------------------------

def read_input(path="input.txt"):
    with open(path) as f:
        return [line.rstrip("\n") for line in f]


# ----------------------------------------------------
#   Helpers
# ----------------------------------------------------

def extract_number_at(lines, r, col):
    """
    Given a position (r, col), return the full integer centered on that column.
    If that position is not a digit, return None.
    """
    row = lines[r]
    if col >= len(row) or not row[col].isdigit():
        return None

    # expand left
    left = col
    while left > 0 and row[left - 1].isdigit():
        left -= 1

    # expand right
    right = col
    while right + 1 < len(row) and row[right + 1].isdigit():
        right += 1

    return int(row[left:right + 1])


def find_blocks(lines):
    """
    Identify problem blocks as contiguous column ranges where at least
    one row has a non-space character.
    Returns a list of (start_col, end_col) inclusive.
    """
    width = max(len(row) for row in lines)
    blocks = []

    in_block = False
    start = None

    for col in range(width):
        col_all_space = True
        for row in lines:
            if col < len(row) and row[col] != " ":
                col_all_space = False
                break

        if col_all_space:
            if in_block:
                blocks.append((start, col - 1))
                in_block = False
                start = None
        else:
            if not in_block:
                in_block = True
                start = col

    if in_block:
        blocks.append((start, width - 1))

    return blocks


# ----------------------------------------------------
#   Part 1 — Top-Down Problems
# ----------------------------------------------------

def part1(lines):
    total = 0
    blocks = find_blocks(lines)
    bottom = len(lines) - 1

    for (start, end) in blocks:
        op = None
        # Find the operator inside this block
        for c in range(start, end + 1):
            if c < len(lines[bottom]) and lines[bottom][c] in "+*":
                op = lines[bottom][c]
                op_col = c
                break

        if op is None:
            continue

        # Collect numbers vertically above the operator
        nums = []
        r = bottom - 1
        while r >= 0:
            n = extract_number_at(lines, r, op_col)
            if n is None:
                break
            nums.append(n)
            r -= 1

        # Combine
        if op == "+":
            total += sum(nums)
        else:
            product = 1
            for x in nums:
                product *= x
            total += product

    return total


# ----------------------------------------------------
#   Part 2 — Right-to-Left Cephalopod Math
# ----------------------------------------------------

def part2(lines):
    total = 0
    blocks = find_blocks(lines)
    bottom = len(lines) - 1

    for (start, end) in blocks:
        digits = [[] for _ in range(end - start + 1)]

        # Read numbers RIGHT→LEFT
        for r in range(bottom - 1, -1, -1):
            for c in range(start, end + 1):
                idx = end - c  # flip horizontally
                if c < len(lines[r]) and lines[r][c].isdigit():
                    digits[idx].append(lines[r][c])

        # Build integers column-by-column
        nums = []
        for dlist in digits:
            if dlist:
                num = int("".join(reverse_list := dlist[::-1]))
                nums.append(num)

        # Find operator
        op = None
        for c in range(start, end + 1):
            if c < len(lines[bottom]) and lines[bottom][c] in "+*":
                op = lines[bottom][c]
                break

        if op is None:
            continue

        # Combine
        if op == "+":
            total += sum(nums)
        else:
            product = 1
            for x in nums:
                product *= x
            total += product

    return total


# ----------------------------------------------------
#   Tests — Part 1
# ----------------------------------------------------

def test_find_blocks_two_problems():
    lines = [
        "123   456",
        " 45   789",
        "  6   321",
        "*     +  "
    ]
    blocks = find_blocks(lines)
    assert blocks == [(0, 2), (6, 8)]


def test_part1_example():
    lines = [
        "123 328  51 64 ",
        " 45  64 387 23 ",
        "  6  98 215 314",
        "*   +   *   +  ",
    ]
    # Provided example result:
    # 123*45*6 = 33210
    # 328+64+98 = 490
    # 51*387*215 = 4243455
    # 64+23+314 = 401
    # sum = 4277556
    assert part1(lines) == 4277556


# ----------------------------------------------------
#   Tests — Part 2
# ----------------------------------------------------

def test_part2_example():
    lines = [
        "123 328  51 64 ",
        " 45  64 387 23 ",
        "  6  98 215 314",
        "*   +   *   +  ",
    ]
    # Provided part 2 example total: 3263827
    assert part2(lines) == 3263827


# ----------------------------------------------------
#   Run Tests
# ----------------------------------------------------

def run_tests():
    print("Running tests...")

    test_find_blocks_two_problems()
    test_part1_example()
    test_part2_example()

    print("All tests passed!")


# ----------------------------------------------------
#   Main
# ----------------------------------------------------

if __name__ == "__main__":
    RUN_TESTS = False

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))