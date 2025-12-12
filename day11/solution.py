# solution_day12_part1.py
from __future__ import annotations

from typing import Dict, List, Tuple

Cell = Tuple[int, int]
Cells = Tuple[Cell, ...]
Mask = int
Region = Tuple[int, int, List[int]]  # (W, H, counts)


# -------------------------
#   Read input
# -------------------------

def read_input(path: str = "input.txt") -> List[str]:
    with open(path) as f:
        return f.read().splitlines()


# -------------------------
#   Parsing
# -------------------------

def _is_region_line(s: str) -> bool:
    s = s.strip()
    if ":" not in s or "x" not in s:
        return False
    left, _ = s.split(":", 1)
    if "x" not in left:
        return False
    w_str, h_str = left.split("x", 1)
    return w_str.isdigit() and h_str.isdigit()


def parse_shapes(lines: List[str]) -> Dict[int, Cells]:
    """
    Parse shape blocks like:

    0:
    ###
    ##.
    ##.
    """
    shapes: Dict[int, Cells] = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Stop when we hit regions.
        if _is_region_line(line):
            break

        if line.endswith(":") and line[:-1].strip().isdigit():
            shape_id = int(line[:-1].strip())
            i += 1

            grid_rows: List[str] = []
            while i < len(lines):
                row = lines[i].strip()
                if not row or _is_region_line(row):
                    break
                grid_rows.append(row)
                i += 1

            cells: List[Cell] = []
            for y, row in enumerate(grid_rows):
                for x, ch in enumerate(row):
                    if ch == "#":
                        cells.append((x, y))

            if not cells:
                raise ValueError(f"Shape {shape_id} has no filled cells.")

            shapes[shape_id] = _normalize_cells(tuple(cells))

            # Skip blank lines between shapes.
            while i < len(lines) and not lines[i].strip():
                i += 1
        else:
            i += 1

    return shapes


def parse_regions(lines: List[str], num_shapes: int | None = None) -> List[Region]:
    """
    Parse region lines like: "12x5: 1 0 1 0 2 2"
    """
    regions: List[Region] = []

    for raw in lines:
        s = raw.strip()
        if not s or not _is_region_line(s):
            continue

        left, right = s.split(":", 1)
        w_str, h_str = left.split("x", 1)
        W = int(w_str)
        H = int(h_str)

        counts = [int(x) for x in right.strip().split()] if right.strip() else []
        if num_shapes is not None and counts and len(counts) != num_shapes:
            raise ValueError(
                f"Region '{s}' has {len(counts)} counts but expected {num_shapes}."
            )

        regions.append((W, H, counts))

    return regions


# -------------------------
#   Geometry helpers
# -------------------------

def _normalize_cells(cells: Cells) -> Cells:
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted(((x - min_x, y - min_y) for x, y in cells)))


def _rotate90(cells: Cells) -> Cells:
    rotated = tuple((y, -x) for x, y in cells)
    return _normalize_cells(rotated)


def _flip_x(cells: Cells) -> Cells:
    flipped = tuple((-x, y) for x, y in cells)
    return _normalize_cells(flipped)


def generate_variants(cells: Cells) -> List[Cells]:
    """
    All unique rotations + flips (<= 8).
    """
    seen = set()
    out: List[Cells] = []

    cur = _normalize_cells(cells)
    for _ in range(4):
        for v in (cur, _flip_x(cur)):
            if v not in seen:
                seen.add(v)
                out.append(v)
        cur = _rotate90(cur)

    return out


def placements_for_variant(variant: Cells, W: int, H: int) -> List[Mask]:
    """
    All placement masks for this variant on a WxH board.
    Bit index = y*W + x.
    """
    max_x = max(x for x, _ in variant)
    max_y = max(y for _, y in variant)
    width = max_x + 1
    height = max_y + 1

    if width > W or height > H:
        return []

    placements: List[Mask] = []
    for oy in range(H - height + 1):
        for ox in range(W - width + 1):
            mask = 0
            for x, y in variant:
                bit = (oy + y) * W + (ox + x)
                mask |= (1 << bit)
            placements.append(mask)

    return placements


# -------------------------
#   Solver
# -------------------------

def quick_area_check(W: int, H: int, counts: List[int], shape_sizes: List[int]) -> bool:
    required = 0
    for i, qty in enumerate(counts):
        required += qty * shape_sizes[i]
    return required <= W * H


def can_fit_region(W: int, H: int, counts: List[int], shapes_by_id: Dict[int, Cells]) -> bool:
    """
    Fast backtracking with:
      - bitmask board
      - memoization
      - branching on the FIRST empty cell (huge pruning)
    """
    if not counts:
        return True

    N = len(counts)

    # Validate shape IDs exist when needed.
    for sid in range(N):
        if counts[sid] > 0 and sid not in shapes_by_id:
            raise ValueError(f"Missing shape id {sid} required by region counts.")

    shape_sizes = [len(shapes_by_id[i]) for i in range(N)]
    if not quick_area_check(W, H, counts, shape_sizes):
        return False

    # Precompute all placements per needed shape.
    placements_by_shape: List[List[Mask]] = [[] for _ in range(N)]
    for sid in range(N):
        if counts[sid] <= 0:
            continue
        masks: set[Mask] = set()
        for variant in generate_variants(shapes_by_id[sid]):
            masks.update(placements_for_variant(variant, W, H))
        placements_by_shape[sid] = list(masks)
        if not placements_by_shape[sid]:
            return False

    board_size = W * H
    board_bits = (1 << board_size) - 1

    # For each cell, list all placements that cover it: (sid, mask)
    cell_to_placements: List[List[Tuple[int, Mask]]] = [[] for _ in range(board_size)]
    for sid in range(N):
        if counts[sid] <= 0:
            continue
        for m in placements_by_shape[sid]:
            mm = m
            while mm:
                bit = mm & -mm
                idx = bit.bit_length() - 1
                cell_to_placements[idx].append((sid, m))
                mm ^= bit

    memo: Dict[Tuple[int, Tuple[int, ...]], bool] = {}

    def dfs(occupied: int, remaining: Tuple[int, ...]) -> bool:
        key = (occupied, remaining)
        if key in memo:
            return memo[key]

        if all(q == 0 for q in remaining):
            memo[key] = True
            return True

        empty_mask = board_bits & ~occupied
        if empty_mask == 0:
            memo[key] = False
            return False

        # Pick first empty cell
        lsb = empty_mask & -empty_mask
        cell_idx = lsb.bit_length() - 1

        # Try only placements that cover that cell
        for sid, pmask in cell_to_placements[cell_idx]:
            if remaining[sid] <= 0:
                continue
            if (pmask & occupied) != 0:
                continue

            new_remaining = list(remaining)
            new_remaining[sid] -= 1

            if dfs(occupied | pmask, tuple(new_remaining)):
                memo[key] = True
                return True

        memo[key] = False
        return False

    return dfs(0, tuple(counts))


# -------------------------
#   Part 1
# -------------------------

def part1(lines: List[str]) -> int:
    shapes = parse_shapes(lines)
    if not shapes:
        raise ValueError("No shapes found.")

    max_id = max(shapes.keys())
    if set(shapes.keys()) != set(range(max_id + 1)):
        raise ValueError("Expected shape ids to be 0..N-1 with no gaps.")

    num_shapes = max_id + 1
    regions = parse_regions(lines, num_shapes=num_shapes)

    total_fit = 0
    for (W, H, counts) in regions:
        if counts and can_fit_region(W, H, counts, shapes):
            total_fit += 1

    return total_fit


# -------------------------
#   Tests
# -------------------------

def test_example_from_prompt_part1():
    lines = [
        "0:",
        "###",
        "##.",
        "##.",
        "",
        "1:",
        "###",
        "##.",
        ".##",
        "",
        "2:",
        ".##",
        "###",
        "##.",
        "",
        "3:",
        "##.",
        "###",
        "##.",
        "",
        "4:",
        "###",
        "#..",
        "###",
        "",
        "5:",
        "###",
        ".#.",
        "###",
        "",
        "4x4: 0 0 0 0 2 0",
        "12x5: 1 0 1 0 2 2",
        "12x5: 1 0 1 0 3 2",
    ]
    assert part1(lines) == 2


def test_generate_variants_dedup_symmetry():
    domino: Cells = ((0, 0), (1, 0))
    vars_ = generate_variants(domino)
    assert len(vars_) == 2


def run_tests():
    print("Running tests...")
    test_generate_variants_dedup_symmetry()
    test_example_from_prompt_part1()
    print("All tests passed!")


# -------------------------
#   Main
# -------------------------

if __name__ == "__main__":
    RUN_TESTS = False

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))