def read_input():
    with open("input.txt") as f:
        lines = f.read().strip().splitlines()
    return lines

# -------------------------
#   Helpers
# -------------------------

def generate_double_ids_in_ranges(ranges):
    """Generate all double-pattern IDs that fall within any of the ranges"""
    invalid_ids = set()  # Use set to avoid duplicates

    # Find the max number of digits we need to handle
    max_id = max(end for _, end in ranges)
    max_digits = len(str(max_id))
    
    # Try all possible half-lengths (1 digit to half of max_digits)
    for half_len in range(1, (max_digits // 2) + 1):
        # Generate all possible "halves" of this length
        start = 10 ** (half_len - 1)  # e.g., 10 for 2-digit
        end = 10 ** half_len           # e.g., 100 for 2-digit
        for half in range(start, end):
            # Create the double ID: "123" + "123" = 123123
            s = str(half)
            double_id = int(s + s)
            
            # Check if this double_id falls in ANY of our ranges
            for range_start, range_end in ranges:
                if range_start <= double_id <= range_end:
                    invalid_ids.add(double_id)
                    break  # Found it in a range, no need to check others
    
    return invalid_ids

def is_repeating_pattern(number):
    num_str = str(number)
    total_length = len(num_str)
    
    for pattern_length in range(1, (total_length // 2) + 1):
        if total_length % pattern_length == 0:
            pattern = num_str[0:pattern_length]  # ← Extract chars
            repetitions = total_length // pattern_length
            if pattern * repetitions == num_str:  # ← Repeat and compare
                return True
    
    return False

def part1(lines):
    line = lines[0].strip().rstrip(',')
    raw_ranges = line.split(',')
    
    ranges = []
    for part in raw_ranges:
        if not part:
            continue
        start_str, end_str = part.split('-')
        ranges.append((int(start_str), int(end_str)))
    
    invalid_ids = generate_double_ids_in_ranges(ranges)
    return sum(invalid_ids)

def part2(lines):
    line = lines[0].strip().rstrip(',')
    raw_ranges = line.split(',')
    invalid_ids = set()
    
    ranges = []
    for part in raw_ranges:
        if not part:
            continue
        start_str, end_str = part.split('-')
        ranges.append((int(start_str), int(end_str)))
    
    for start, end in ranges:  # ← loop through each range
        for number in range(start, end + 1):  # ← check each number
            if is_repeating_pattern(number):  # ← test if invalid
                invalid_ids.add(number)  # ← collect it
    
    return sum(invalid_ids)  # ← sum them up

# -------------------------
#   Test Suite (Optional)
# -------------------------

def test_small_range():
    lines = ["11-22"]
    assert part1(lines) == 33  # 11 + 22
    result = part1(lines)

def test_no_doubles():
    lines = ["100-200"]
    assert part1(lines) == 0
    result = part1(lines)

def test_single_double():
    lines = ["1000-1020"]
    assert part1(lines) == 1010  # only 1010
    result = part1(lines)

def test_overlap():
    lines = ["10-15,12-18"]
    assert part1(lines) == 11  # 11 appears in both ranges, count once
    result = part1(lines)

def test_large_double():
    lines = ["123123-123124"]
    assert part1(lines) == 123123
    result = part1(lines)

def test_example():
    lines = ["11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"]
    assert part1(lines) == 1227775554
    result = part1(lines)

def test_part2_example():
    lines = ["11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"]
    assert part2(lines) == 4174379265

def test_triple_pattern():
    lines = ["110-112"]
    assert part2(lines) == 111  # "1" repeated 3 times

def test_triple_pattern():
    lines = ["110-112"]
    assert part2(lines) == 111  # "1" repeated 3 times

def test_part2_small():
    lines = ["11-22"]
    assert part2(lines) == 33  # Still just 11 + 22

def run_tests():
    print("Running tests...")
    
    test_small_range()
    test_no_doubles()
    test_single_double()
    test_overlap()
    test_large_double()
    test_example()

    print("All tests passed!")

if __name__ == "__main__":
    RUN_TESTS = False

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))