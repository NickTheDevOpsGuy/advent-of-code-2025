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

def max_joltage_for_row(jolts):
    
    digits = [int(ch) for ch in jolts]
    best_ones = -1
    best_val = -1

    for digit in reversed(digits):
        if best_ones != -1:
            candidate = 10 * digit + best_ones
            best_val = max(best_val, candidate)
        best_ones = max(best_ones, digit)

    return best_val

def max_joltage12_for_row(jolts):

    digits = [int(ch) for ch in jolts]
    N = len(jolts)
    remaining = 12
    pos = 0
    result = []
    d = 0
    big_string = ""

    while remaining > 0:

        # figure out how far we’re allowed to look
        # so that there are still (remaining - 1) digits left after we pick one
        max_start_index = N - remaining

        # now search in the window [pos .. max_start_index]
        best_digit = -1
        best_index = -1

        for i in range(pos, max_start_index + 1):
            d = digits[i]
            if d > best_digit:
                best_digit = d
                best_index = i

        result.append(str(best_digit))  # keep track of best numbers
        pos = best_index + 1          # next pick must come after this
        remaining = remaining - 1

    big_string = "".join(result)
    return int(big_string)

def part1(lines):
    total = 0
    
    for line in lines:
        row_value = max_joltage_for_row(line)
        total += row_value

    return total

# -------------------------
#   Part 2 Logic
# -------------------------

def part2(lines):
    total = 0
    row_value = 0
    
    for line in lines:
        row_value = max_joltage12_for_row(line)
        total += row_value

    return total

#
# -------------------------
#   Part 1 Test Suite (Optional)
# -------------------------

def test_max_joltage_for_row_two_digits():
    assert max_joltage_for_row("98") == 98

def test_max_joltage_for_row_increasing_digits():
    assert max_joltage_for_row("123456") == 56

def test_max_joltage_for_row_decreasing_digits():
    assert max_joltage_for_row("987654") == 98

def test_max_joltage_for_row_sample1():
    assert max_joltage_for_row("987654321111111") == 98

def test_max_joltage_for_row_sample2():
    assert max_joltage_for_row("811111111111119") == 89

def test_max_joltage_for_row_all_same_digit():
    assert max_joltage_for_row("7777") == 77

#
# -------------------------
#   Part 2 Test Suite (Optional)
# -------------------------

def test_max_joltage12_sample1():
    # 987654321111111 -> 987654321111
    assert max_joltage12_for_row("987654321111111") == 987654321111


def test_max_joltage12_sample2():
    # 811111111111119 -> 811111111119
    assert max_joltage12_for_row("811111111111119") == 811111111119


def test_max_joltage12_sample3():
    # 234234234234278 -> 434234234278
    assert max_joltage12_for_row("234234234234278") == 434234234278


def test_max_joltage12_sample4():
    # 818181911112111 -> 888911112111
    assert max_joltage12_for_row("818181911112111") == 888911112111


def test_max_joltage12_exact_length():
    # Exactly 12 digits: should just use them all
    assert max_joltage12_for_row("123456789012") == 123456789012


def test_max_joltage12_all_same_digit():
    # All 1s: any 12-length subsequence is all 1s
    assert max_joltage12_for_row("11111111111111111111") == 111111111111


def test_max_joltage12_increasing_digits():
    # Increasing then wrap: tests windowing from the front
    assert max_joltage12_for_row("12345678901234567890") == 901234567890


def test_max_joltage12_decreasing_digits():
    # Decreasing: tests that we don't just take the first 12 blindly
    assert max_joltage12_for_row("98765432109876543210") == 989876543210


def test_max_joltage12_13_digit_input():
    # 13 digits: must drop exactly one, and drop the one that gives best overall result
    assert max_joltage12_for_row("9876543210987") == 987654321987


def test_max_joltage12_alternating_high_low_digits():
    # Alternating 9 and 0: make sure we always pick 9 when possible
    assert max_joltage12_for_row("90909090909090909090") == 999999999090

def test_part2_example_total():
    # Full example from the problem statement
    lines = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    assert part2(lines) == 3121910778619

#
# -------------------------
#   Run the Tests
# -------------------------

def run_tests():
    print("Running tests...")
    
    test_max_joltage_for_row_two_digits()
    test_max_joltage_for_row_increasing_digits()
    test_max_joltage_for_row_decreasing_digits()
    test_max_joltage_for_row_sample1()
    test_max_joltage_for_row_sample2()
    test_max_joltage_for_row_all_same_digit()
    test_max_joltage12_sample1
    test_max_joltage12_sample2()
    test_max_joltage12_sample3()
    test_max_joltage12_sample4()
    test_max_joltage12_increasing_digits()
    test_max_joltage12_decreasing_digits()
    test_max_joltage12_all_same_digit()
    test_max_joltage12_exact_length()
    test_max_joltage12_13_digit_input()
    test_max_joltage12_alternating_high_low_digits()

    print("All tests passed!")

#
# -------------------------
#   Main Code Section
# -------------------------

if __name__ == "__main__":
    RUN_TESTS = True

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))