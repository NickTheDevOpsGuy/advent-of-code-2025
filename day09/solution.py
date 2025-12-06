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


# -------------------------
#   Part 1 Logic
# -------------------------

def part1(lines):
    


# -------------------------
#   Part 2 Logic
# -------------------------

def part2(lines):


# -------------------------
#   Part 1 Tests
# -------------------------



# -------------------------
#   Run the Tests
# -------------------------

def run_tests():
    print("Running tests...")


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
        #print("Part 2:", part2(lines))