import re
from fractions import Fraction

# -------------------------
#   Read in the file
# -------------------------


def read_input() -> list[str]:
    """
    Reads the puzzle input from input.txt and returns a list of lines.
    """
    with open("input.txt") as f:
        lines = f.read().strip().splitlines()
    return lines


# ============================================================
#   Part 1: Lights as bits (Lights Out over GF(2))
# ============================================================


def pattern_to_mask(pattern: str) -> int:
    """
    Convert a pattern like '.##.' into a bitmask.

    Convention (must match button indices!):
      - Leftmost character in the string = bit 0
      - Next = bit 1, etc.

    Example:
      pattern = ".##."
      indices:  0 1 2 3
      bits:     0 1 1 0  -> 0b0110
    """
    mask = 0
    for idx, ch in enumerate(pattern):
        if ch == "#":
            mask |= 1 << idx
    return mask


def button_indices_to_mask(indices: list[int]) -> int:
    """
    Given a list of light indices, return the corresponding toggle mask.

    Example:
      indices = [0, 3, 4]
      -> mask where bits 0, 3, 4 are 1.
    """
    mask = 0
    for i in indices:
        mask |= 1 << i
    return mask


def parse_machine_line_part1(line: str) -> tuple[int, list[int]]:
    """
    Parse one machine line like:
      [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    Returns:
        target_mask: int bitmask of desired final light pattern
        button_masks: list of int bitmasks (one per button)
    """
    # pattern in [...]
    m = re.search(r"\[([.#]+)\]", line)
    if not m:
        raise ValueError("No pattern found in line")
    pattern = m.group(1)
    target_mask = pattern_to_mask(pattern)

    # everything before the jolts { ... } is where the buttons live
    curly = re.search(r"\{", line)
    before_curly = line if not curly else line[:curly.start()]

    # extract all "( ... )" groups
    raw_groups = re.findall(r"\(([^)]*)\)", before_curly)
    button_masks: list[int] = []

    for g in raw_groups:
        g = g.strip()
        if not g:
            indices: list[int] = []
        else:
            indices = [int(x) for x in g.split(",") if x.strip() != ""]
        button_masks.append(button_indices_to_mask(indices))

    return target_mask, button_masks


def count_bits(x: int) -> int:
    """
    Return the number of 1-bits in x.
    """
    return x.bit_count()


def min_presses_for_machine(target_mask: int, button_masks: list[int]) -> int:
    """
    Given a target light pattern and a list of button masks,
    find the minimum number of button presses needed.

    Each button is either pressed 0 or 1 time (pressing twice cancels).
    Start from all-lights-off (mask 0).
    XOR all pressed buttons' masks to get the final mask.
    Among all combinations that match target_mask, return the fewest presses.
    """
    n = len(button_masks)
    best: int | None = None

    # brute force all subsets of buttons: 0..(2^n - 1)
    for combo in range(1 << n):
        presses = count_bits(combo)
        if best is not None and presses >= best:
            # no point computing final pattern for a worse or equal solution
            continue

        final_mask = 0
        for i in range(n):
            if combo & (1 << i):
                final_mask ^= button_masks[i]

        if final_mask == target_mask:
            if best is None or presses < best:
                best = presses

    if best is None:
        raise ValueError("No subset of buttons reaches the target light pattern.")
    return best


def part1(lines: list[str]) -> int:
    """
    For each machine line:
      - skip blanks
      - parse it
      - compute minimum button presses
      - accumulate total
    """
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        target_mask, button_masks = parse_machine_line_part1(line)
        presses = min_presses_for_machine(target_mask, button_masks)
        total += presses
    return total


# ============================================================
#   Part 2: Joltage counters as linear system over integers
# ============================================================


def parse_machine_line_part2(line: str) -> tuple[list[int], list[list[int]]]:
    """
    Parse one machine line into:

      jolt_targets: list[int]  (from {...})
      buttons:      list[list[int]] each is list of counters this button touches

    Example:
      line = "[.##.] (3) (1,3) (2) ... {3,5,4,7}"
      -> jolt_targets = [3,5,4,7]
         buttons = [[3], [1,3], [2], ...]
    """
    # extract {...} for jolts
    curly = re.search(r"\{([^}]*)\}", line)
    if not curly:
        raise ValueError("No joltage section found in line")

    jolts_str = curly.group(1)
    jolt_targets = [int(x) for x in jolts_str.split(",") if x.strip() != ""]

    before_curly = line[:curly.start()]

    # extract all "( ... )" groups before the jolts
    raw_groups = re.findall(r"\(([^)]*)\)", before_curly)
    buttons: list[list[int]] = []

    for g in raw_groups:
        text = g.strip()
        if text == "":
            buttons.append([])
        else:
            parts = text.split(",")
            indices = [int(p) for p in parts if p.strip() != ""]
            buttons.append(indices)

    return jolt_targets, buttons


# ---------- Linear algebra helpers (Gaussian elimination over Q) ----------


def rref(A: list[list[int]], b: list[int]):
    """
    Compute Reduced Row Echelon Form of [A | b] over rationals.

    A: m x n matrix of ints
    b: length m list of ints

    Returns:
      R:  m x n matrix of Fractions (RREF of A)
      rb: length m list of Fractions (transformed b)
      pivot_cols: list of pivot column indices
    """
    m = len(A)
    if m == 0:
        return [], [], []

    n = len(A[0])
    R = [[Fraction(A[i][j]) for j in range(n)] for i in range(m)]
    rb = [Fraction(b[i]) for i in range(m)]

    pivot_cols: list[int] = []
    row = 0

    for col in range(n):
        if row >= m:
            break

        # find pivot row
        pivot = None
        for r in range(row, m):
            if R[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue

        # swap into place
        if pivot != row:
            R[row], R[pivot] = R[pivot], R[row]
            rb[row], rb[pivot] = rb[pivot], rb[row]

        # normalize pivot row
        pv = R[row][col]
        if pv != 1:
            inv = Fraction(1, 1) / pv
            R[row] = [val * inv for val in R[row]]
            rb[row] *= inv

        # eliminate in other rows
        for r in range(m):
            if r == row:
                continue
            factor = R[r][col]
            if factor != 0:
                R[r] = [R[r][c] - factor * R[row][c] for c in range(n)]
                rb[r] -= factor * rb[row]

        pivot_cols.append(col)
        row += 1

    # check for inconsistency (0 ... 0 | nonzero)
    for r in range(m):
        if all(R[r][c] == 0 for c in range(n)) and rb[r] != 0:
            raise ValueError("Inconsistent linear system")

    return R, rb, pivot_cols


def build_parametric_solution(
    A: list[list[int]], b: list[int]
) -> tuple[list[int], dict[int, tuple[Fraction, dict[int, Fraction]]]]:
    """
    Given integer matrix A (m x n) and vector b (length m), returns:

      free_vars: list of column indices that are *free*
      pivot_for_col: dict pivot_col -> (const, coeff_dict)

    Meaning: for each pivot column p:
        x_p = const + sum_{f in free_vars} coeff[f] * x_f

    where const and coeff[f] are Fractions (from RREF).
    """
    m = len(A)
    if m == 0:
        n = len(A[0]) if A else 0
        return list(range(n)), {}

    n = len(A[0])
    R, rb, pivot_cols = rref(A, b)
    pivot_set = set(pivot_cols)
    free_vars = [j for j in range(n) if j not in pivot_set]

    pivot_for_col: dict[int, tuple[Fraction, dict[int, Fraction]]] = {}
    col_to_row = {pivot_cols[i]: i for i in range(len(pivot_cols))}

    for p in pivot_cols:
        row = col_to_row[p]
        const = rb[row]
        coeff: dict[int, Fraction] = {}
        for f in free_vars:
            if R[row][f] != 0:
                # Row equation looks like:
                #   x_p + sum_f (R[row][f] * x_f) = const
                # so x_p = const - sum_f (R[row][f] * x_f)
                coeff[f] = -R[row][f]
        pivot_for_col[p] = (const, coeff)

    return free_vars, pivot_for_col


def min_presses_joltage_machine(jolts: list[int], buttons: list[list[int]]) -> int:
    """
    Solve Part 2 for a single machine.

    jolts:   list[int] length m (target joltage counters)
    buttons: list[list[int]] length n, each entry is list of counters
             this button increments when pressed once.

    We solve A x = b with:
      - A_ij = 1 if button j touches counter i, else 0
      - x_j >= 0 integer
      - minimize sum_j x_j
    """
    m = len(jolts)
    n = len(buttons)

    # Build A: m x n with 0/1 entries
    A = [[0] * n for _ in range(m)]
    touched_rows: list[set[int]] = [set() for _ in range(n)]
    for j, idxs in enumerate(buttons):
        for i in idxs:
            A[i][j] = 1
            touched_rows[j].add(i)
    b = jolts[:]

    # Build parametric solution x_p = const + Σ coeff[f] * x_f
    free_vars, pivot_expr = build_parametric_solution(A, b)

    # Precompute which rows each button touches and bounds per button
    rows_by_button: list[list[int]] = [list(touched_rows[j]) for j in range(n)]
    bounds: list[int] = [0] * n
    for j in range(n):
        rows = rows_by_button[j]
        if not rows:
            # button affects no counters; never useful to press
            bounds[j] = 0
        else:
            bounds[j] = min(b[i] for i in rows)

    # DFS over free variables (small dimension), with pruning on row sums
    x_free_vals: dict[int, int] = {j: 0 for j in free_vars}
    partial = [0] * m  # partial contribution to each row from assigned free vars
    best: int | None = None
    best_x: list[int] | None = None

    free_list = free_vars[:]
    d = len(free_list)

    def dfs(pos: int):
        nonlocal best, best_x
        if pos == d:
            # All free vars assigned; compute pivot vars and validate
            x = [0] * n
            for j in free_list:
                x[j] = x_free_vals[j]

            # Compute pivot variables from RREF expressions
            for p, (const, coeff) in pivot_expr.items():
                val = const
                for f, c in coeff.items():
                    val += c * x[f]

                if val.denominator != 1:
                    return  # non-integer
                v_int = val.numerator
                if v_int < 0:
                    return  # negative press count
                x[p] = v_int

            # Validate all equations explicitly: Σ_j A_ij x_j == b_i
            for i in range(m):
                s = 0
                row = A[i]
                for j in range(n):
                    if row[j]:
                        s += x[j]
                if s != b[i]:
                    return

            total_presses = sum(x)
            if best is None or total_presses < best:
                best = total_presses
                best_x = x[:]
            return

        j = free_list[pos]
        rows = rows_by_button[j]

        # Effective max for this variable, respecting row residuals
        eff_max = bounds[j]
        for i in rows:
            remaining = b[i] - partial[i]
            if remaining < eff_max:
                eff_max = remaining
        if eff_max < 0:
            return

        for val in range(eff_max + 1):
            x_free_vals[j] = val

            if val != 0:
                for i in rows:
                    partial[i] += val

            # Very simple bound: current free presses cannot already exceed best
            if best is not None:
                current_free_sum = sum(x_free_vals[k] for k in free_list[: pos + 1])
                if current_free_sum >= best:
                    if val != 0:
                        for i in rows:
                            partial[i] -= val
                    continue

            dfs(pos + 1)

            if val != 0:
                for i in rows:
                    partial[i] -= val

        x_free_vals[j] = 0

    dfs(0)

    if best is None:
        raise ValueError("No nonnegative integer solution found for joltage machine.")

    return best


def part2(lines: list[str]) -> int:
    """
    For each machine line:
      - parse joltage targets and button wiring
      - solve A x = b with x >= 0 integers
      - sum minimum presses over all machines
    """
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        jolt_targets, buttons = parse_machine_line_part2(line)
        presses = min_presses_joltage_machine(jolt_targets, buttons)
        total += presses
    return total


# ============================================================
#   Tests
# ============================================================


def run_tests() -> None:
    print("Running tests...")

    # ---- pattern_to_mask sanity check ----
    assert pattern_to_mask(".##.") == 0b0110
    assert pattern_to_mask("....") == 0
    assert pattern_to_mask("#..#") == (1 << 0) | (1 << 3)

    # ---- sample from the problem statement ----
    sample_lines = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
    ]

    # Part 1 sample: 2 + 3 + 2 = 7
    assert part1(sample_lines) == 7

    # Part 2 sample: 10 + 12 + 11 = 33
    assert part2(sample_lines) == 33

    print("All tests passed!")


# ============================================================
#   Main
# ============================================================


if __name__ == "__main__":
    RUN_TESTS = False  # flip to True to run tests instead of solving

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
        print("Part 2:", part2(lines))