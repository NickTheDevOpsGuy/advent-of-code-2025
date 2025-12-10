import re

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

def parse_machine_line(line: str) -> tuple[int, list[int]]:
    """
    Parse one machine line like:
      [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    Returns:
        target_mask: int bitmask of desired final light pattern
        button_masks: list of int bitmasks (one per button)
    """

    # -----------------------
    # 1. Extract the [pattern]
    # -----------------------
    start_index = line.find('[')
    end_index = line.find(']')
    pattern = line[start_index + 1 : end_index]   # e.g. ".##."

    # -----------------------
    # 2. Extract (...) groups before the {curly} section
    # -----------------------

    # Find where { begins (ignore joltage section)
    curly_start = line.find('{')
    before_curly = line[:curly_start]

    # Extract all parenthesis contents: "3", "1,3", "0,2", etc
    raw_groups = re.findall(r"\(([^)]*)\)", before_curly)
    # raw_groups is a list of strings like:
    #   ["3", "1,3", "2", "2,3", "0,2", "0,1"]

    # -----------------------
    # 3. Convert pattern → bitmask
    # -----------------------
    target_mask = pattern_to_mask(pattern)

    # -----------------------
    # 4. Convert each (...) group → bitmask
    # -----------------------
    button_masks = []

    for group in raw_groups:
        # if group == "" → button toggles nothing (rare but allowed)
        if group.strip() == "":
            indices = []
        else:
            parts = group.split(",")
            indices = [int(p) for p in parts]

        mask = button_list_to_mask(indices)
        button_masks.append(mask)

    # -----------------------
    # 5. Return both masks
    # -----------------------
    return target_mask, button_masks

def pattern_to_mask(pattern: str) -> int:
    """
    Convert a pattern like '.##.' into a bitmask.

    Convention:
      - Rightmost character in the string = bit 0
      - Next = bit 1, etc.
    Example:
      '.##.' -> 0b0110
    """
    # Loop over pattern characters from right to left
    # Build up an integer where '#' sets the bit to 1, '.' leaves it 0
    

def button_indices_to_mask(indices: list[int]) -> int:
    """
    Given a list of light indices, return the corresponding toggle mask.

    Example:
      indices = [0, 3, 4]
      -> mask where bits 0, 3, 4 are 1.
    """
    # Start with mask = 0
    # For each index i in indices: set bit i in the mask
    for list in  machine:
    best = infinity
    for mask from 0 to (1<<num_buttons)-1:
        compute toggles
        if final == target:
            best = min(best, popcount(mask))
    add to total

def min_presses_for_machine(target_mask: int, button_masks: list[int]) -> int:
    """
    Given a target light pattern and a list of button masks,
    find the minimum number of button presses needed.

    Rules:
      - Each button is either pressed 0 or 1 time (because pressing twice cancels).
      - Start from all-lights-off (mask 0).
      - XOR all pressed buttons' masks to get the final mask.
      - Compare final_mask to target_mask.
      - Among all combinations that match, return the fewest presses.

    Brute force plan:
      - Let n = number of buttons.
      - For combo in [0 .. (1 << n) - 1]:
          - compute final_mask by XOR-ing masks where that button is "on" in combo.
          - if final_mask == target_mask:
              - count how many bits are 1 in combo (number of presses).
              - track the minimum.
    """
    # Use a small helper to count bits in combo.
    pass

def count_bits(x: int) -> int:
    """
    Return the number of 1-bits in x.

    Used to count how many buttons are pressed in a given combination.
    """
    # You can loop while x > 0 and peel off bits,
    # or use a built-in like bin(x).count("1") if you want something simple.
    pass


# -------------------------
#   Part 1 Logic
# -------------------------

def part1(lines: list[str]) -> int:
    """
    For each machine line:
      - parse it into (target_mask, button_masks)
      - compute min presses for that machine
      - sum all machines' min presses
    """
    total = 0
    for line in lines:
        # skip blank lines if any
        # parse line
        # add min presses to total
        pass

    return total
    
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
    pass
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
        print("Part 2:", part2(lines))