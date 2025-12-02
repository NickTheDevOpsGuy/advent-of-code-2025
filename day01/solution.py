def read_input():
    with open("input.txt") as f:
        lines = f.read().strip().splitlines()
    return lines

def part1(lines):
    position = 50      # dial starts at 50
    zero_hits = 0      # how many times we land on 0

    for line in lines:
        direction = line[0]       # 'L' or 'R'
        distance = int(line[1:])  # the number after it

        if direction == 'L':
            position = (position - distance) % 100 
        else:
            position = (position + distance) % 100

        if position == 0:
            zero_hits += 1

    return zero_hits

def part2(lines):
    position = 50      # dial starts at 50
    zero_hits = 0      # how many times we land on 0

    for line in lines:
        direction = line[0]       # 'L' or 'R'
        distance = int(line[1:])  # the number after it

        for x in range(distance):
            if direction == 'R':
                position = (position + 1) % 100 
            else:
                position = (position - 1) % 100

            if position == 0:
                zero_hits += 1

    return zero_hits

# -------------------------
#   Test Suite (Optional)
# -------------------------

#[test]
def test_part1():
    # Example input from the problem statement
    lines = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
    ]
    assert part1(lines) == 3   # expected result is 3
    print(part2(lines))

#[test]
def test_part2():
    lines = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
    ]
    assert part2(lines) == 6   # expected result is 6
    print(part2(lines))

#[test]
def test_part2_exact_100():
    lines = [
        "R100",
        "L100",
        "L100",
        "R200",
    ]
    assert part2(lines) == 5 # expected result is 5
    print(part2(lines))

#[test]
def test_part2_multiple_crossings():
    lines = [
        "R250",
        "L500"
    ]
    assert part2(lines) == 8 # expected result is 8

#[test]
def test_part2_landing_on_zero():
        lines = [
            "L50",
            "R100",
            "L200",
        ]
        assert part2(lines) == 4 # expected result is 4
        print(part2(lines))

#[test]
def test_part2_zero_to_zero():
        lines = [
            "L50",
            "R100",
            "L100",
            "L100",
        ]
        assert part2(lines) == 4 # expected result is 4
        print(part2(lines))

def run_tests():
    print("Running tests...")
    
    test_part1()
    test_part2()
    test_part2_exact_100()
    test_part2_multiple_crossings()
    test_part2_landing_on_zero()
    test_part2_zero_to_zero()

    print("All tests passed!")

if __name__ == "__main__":
    RUN_TESTS = False

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))