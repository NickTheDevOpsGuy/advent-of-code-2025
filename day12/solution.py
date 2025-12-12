# solution_day12_part1.py
from __future__ import annotations

from typing import Dict, List, Tuple, Optional, Set

Cell = Tuple[int, int]
Cells = Tuple[Cell, ...]
Mask = int
Region = Tuple[int, int, List[int]]  # (W, H, counts)


def read_input(path: str = "input.txt") -> List[str]:
    """Read puzzle input as a list of raw lines."""
    with open(path) as f:
        return f.read().splitlines()


# -------------------------
#   Parsing
# -------------------------

def _is_region_line(s: str) -> bool:
    """True if the line starts a region definition like '12x5: 1 0 2'."""
    s = s.strip()
    if ":" not in s or "x" not in s:
        return False
    left, _ = s.split(":", 1)
    if "x" not in left:
        return False
    w_str, h_str = left.split("x", 1)
    return w_str.isdigit() and h_str.isdigit()


def _normalize_cells(cells: Cells) -> Cells:
    """Shift cells so min x/y is at (0,0)."""
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted(((x - min_x, y - min_y) for x, y in cells)))


def parse_shapes(lines: List[str]) -> Dict[int, Cells]:
    """
    Parse shape blocks at top of input:

      0:
      ###
      ##.
      ##.

    Returns {shape_id: normalized filled cells}.
    """
    shapes: Dict[int, Cells] = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if _is_region_line(line):
            break

        if line.endswith(":") and line[:-1].strip().isdigit():
            sid = int(line[:-1].strip())
            i += 1

            grid: List[str] = []
            while i < len(lines):
                row = lines[i].strip()
                if not row or _is_region_line(row):
                    break
                grid.append(row)
                i += 1

            cells: List[Cell] = []
            for y, row in enumerate(grid):
                for x, ch in enumerate(row):
                    if ch == "#":
                        cells.append((x, y))

            if not cells:
                raise ValueError(f"Shape {sid} has no filled cells (#).")

            shapes[sid] = _normalize_cells(tuple(cells))

            # skip blank lines between shapes
            while i < len(lines) and not lines[i].strip():
                i += 1
        else:
            i += 1

    return shapes


def parse_regions(lines: List[str], *, num_shapes: Optional[int] = None) -> List[Region]:
    """Parse region lines like '12x5: 1 0 1 0 2 2'."""
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
#   Geometry
# -------------------------

def _rotate90(cells: Cells) -> Cells:
    """Rotate cells 90 degrees: (x,y)->(y,-x), then normalize."""
    return _normalize_cells(tuple((y, -x) for x, y in cells))


def _flip_x(cells: Cells) -> Cells:
    """Flip across the Y axis: (x,y)->(-x,y), then normalize."""
    return _normalize_cells(tuple((-x, y) for x, y in cells))


def generate_variants(cells: Cells) -> List[Cells]:
    """All unique rotations + flips (<= 8) for a piece."""
    seen: Set[Cells] = set()
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
    All placement masks for a single variant on a WxH board.
    Bit index = y*W + x.
    """
    max_x = max(x for x, _ in variant)
    max_y = max(y for _, y in variant)
    bw = max_x + 1
    bh = max_y + 1

    if bw > W or bh > H:
        return []

    placements: List[Mask] = []
    for oy in range(H - bh + 1):
        row_base = oy * W
        for ox in range(W - bw + 1):
            base = row_base + ox
            mask = 0
            for x, y in variant:
                bit = base + y * W + x
                mask |= (1 << bit)
            placements.append(mask)

    return placements


# -------------------------
#   Solver
# -------------------------

def can_fit_region(W: int, H: int, counts: List[int], shapes: Dict[int, Cells]) -> bool:
    """
    Returns True if all required pieces can be placed with no overlap.
    Empty space is allowed.
    """
    if not counts:
        return True

    N = len(counts)
    for sid in range(N):
        if sid not in shapes:
            raise ValueError(f"Missing shape id {sid} required by region counts.")

    shape_sizes = [len(shapes[i]) for i in range(N)]

    total_required = 0
    for sid, qty in enumerate(counts):
        total_required += qty * shape_sizes[sid]

    board_area = W * H
    if total_required > board_area:
        return False

    # Precompute unique placement masks per shape id.
    masks_by_shape: List[List[Mask]] = [[] for _ in range(N)]
    for sid in range(N):
        all_masks: Set[Mask] = set()
        for v in generate_variants(shapes[sid]):
            all_masks.update(placements_for_variant(v, W, H))
        masks = sorted(all_masks)
        masks_by_shape[sid] = masks
        if counts[sid] > 0 and not masks:
            return False

    # If pieces exactly fill the board, we can force each next placement to cover
    # the first empty cell (big speedup).
    full_tiling = (total_required == board_area)

    memo: Dict[Tuple[Mask, Tuple[int, ...]], bool] = {}

    def pick_next_shape(occupied: Mask, remaining: Tuple[int, ...]) -> Optional[int]:
        """Pick the shape with the fewest LEGAL placements under current occupied."""
        best_sid: Optional[int] = None
        best_legal: Optional[int] = None

        for sid, qty in enumerate(remaining):
            if qty <= 0:
                continue

            legal = 0
            for m in masks_by_shape[sid]:
                if (m & occupied) == 0:
                    legal += 1
                    if best_legal is not None and legal >= best_legal:
                        break

            if best_legal is None or legal < best_legal:
                best_legal = legal
                best_sid = sid
                if legal == 0:
                    break

        return best_sid

    def lowest_empty_bit(occupied: Mask) -> Optional[Mask]:
        all_cells_mask = (1 << board_area) - 1
        empty = all_cells_mask & (~occupied)
        if empty == 0:
            return None
        return empty & -empty

    def dfs(occupied: Mask, remaining: Tuple[int, ...], remaining_area: int) -> bool:
        key = (occupied, remaining)
        if key in memo:
            return memo[key]

        if remaining_area == 0:
            memo[key] = True
            return True

        # Not enough empty cells left
        empty_cells = board_area - occupied.bit_count()
        if remaining_area > empty_cells:
            memo[key] = False
            return False

        sid = pick_next_shape(occupied, remaining)
        if sid is None:
            memo[key] = True
            return True

        must_cover = lowest_empty_bit(occupied) if full_tiling else None

        rem_list = list(remaining)
        for m in masks_by_shape[sid]:
            if (m & occupied) != 0:
                continue
            if must_cover is not None and (m & must_cover) == 0:
                continue

            rem_list[sid] -= 1
            if dfs(occupied | m, tuple(rem_list), remaining_area - shape_sizes[sid]):
                memo[key] = True
                return True
            rem_list[sid] += 1

        memo[key] = False
        return False

    return dfs(0, tuple(counts), total_required)


# -------------------------
#   Part 1
# -------------------------

def part1(lines: List[str]) -> int:
    shapes = parse_shapes(lines)
    if not shapes:
        raise ValueError("No shapes found (expected shape blocks at top of input).")

    max_id = max(shapes.keys())
    if set(shapes.keys()) != set(range(max_id + 1)):
        raise ValueError("Expected shape ids to be 0..N-1 with no gaps.")

    num_shapes = max_id + 1
    regions = parse_regions(lines, num_shapes=num_shapes)

    total_fit = 0
    for W, H, counts in regions:
        if counts and can_fit_region(W, H, counts, shapes):
            total_fit += 1
    return total_fit


# -------------------------
#   Unit tests
# -------------------------

def test_example_from_prompt_part1() -> None:
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


def test_generate_variants_dedup_symmetry() -> None:
    domino = ((0, 0), (1, 0))
    assert len(generate_variants(domino)) == 2  # horizontal + vertical


def run_tests() -> None:
    print("Running tests...")
    test_generate_variants_dedup_symmetry()
    test_example_from_prompt_part1()
    print("All tests passed!")


if __name__ == "__main__":
    RUN_TESTS = False  # flip to True to run tests

    if RUN_TESTS:
        run_tests()
    else:
        lines = read_input()
        print("Part 1:", part1(lines))
