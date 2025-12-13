# solution_day12_part1.py
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

# -------------------------
#   Types
# -------------------------

Cell = Tuple[int, int]
Cells = Tuple[Cell, ...]
Mask = int
Region = Tuple[int, int, List[int]]  # (W, H, counts)


# -------------------------
#   Input
# -------------------------

def read_input(path: str = "input.txt") -> List[str]:
    """Read puzzle input as raw lines."""
    with open(path) as f:
        return [ln.rstrip("\r") for ln in f.read().splitlines()]


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
    w, h = left.split("x", 1)
    return w.isdigit() and h.isdigit()


def parse_shapes(lines: List[str]) -> Dict[int, Cells]:
    """Parse shape blocks at top of input."""
    shapes: Dict[int, Cells] = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if _is_region_line(line):
            break

        if line.endswith(":") and line[:-1].isdigit():
            sid = int(line[:-1])
            i += 1
            rows: List[str] = []

            while i < len(lines):
                row = lines[i].strip()
                if not row or _is_region_line(row):
                    break
                rows.append(row)
                i += 1

            cells: List[Cell] = []
            for y, r in enumerate(rows):
                for x, ch in enumerate(r):
                    if ch == "#":
                        cells.append((x, y))

            if not cells:
                raise ValueError(f"Shape {sid} has no filled cells.")

            shapes[sid] = _normalize(tuple(cells))

            # consume blank lines after shape
            while i < len(lines) and not lines[i].strip():
                i += 1
            continue

        i += 1

    return shapes


def parse_regions(lines: List[str], n_shapes: int) -> List[Region]:
    regions: List[Region] = []
    for line in lines:
        s = line.strip()
        if not s or not _is_region_line(s):
            continue

        left, right = s.split(":", 1)
        W, H = map(int, left.split("x"))
        counts = list(map(int, right.split()))
        if len(counts) != n_shapes:
            raise ValueError("Region count length mismatch")

        regions.append((W, H, counts))

    return regions

# -------------------------
#   Geometry
# -------------------------

def _normalize(cells: Cells) -> Cells:
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))


def _rot90(cells: Cells) -> Cells:
    return _normalize(tuple((y, -x) for x, y in cells))


def _flip(cells: Cells) -> Cells:
    return _normalize(tuple((-x, y) for x, y in cells))


def variants(cells: Cells) -> List[Cells]:
    """Unique rotations + flips (<= 8 variants)."""
    seen = set()
    out: List[Cells] = []
    cur = _normalize(cells)
    for _ in range(4):
        for v in (cur, _flip(cur)):
            if v not in seen:
                seen.add(v)
                out.append(v)
        cur = _rot90(cur)
    return out

def placements(shape: Cells, W: int, H: int) -> List[Mask]:
    max_x = max(x for x, _ in shape)
    max_y = max(y for _, y in shape)
    if max_x + 1 > W or max_y + 1 > H:
        return []

    out: List[Mask] = []
    for oy in range(H - max_y):      # == H - (max_y+1) + 1
        for ox in range(W - max_x):  # == W - (max_x+1) + 1
            m = 0
            for x, y in shape:
                bit = (oy + y) * W + (ox + x)
                m |= 1 << bit
            out.append(m)
    return out


def iter_bits(m: int) -> Iterable[int]:
    while m:
        lsb = m & -m
        yield lsb.bit_length() - 1
        m ^= lsb

# -------------------------
#   Solver
# -------------------------

def can_fit(W: int, H: int, counts: List[int], shapes: Dict[int, Cells]) -> bool:
    N = len(counts)

    # sizes[i] = number of filled cells in shape i
    sizes = [len(shapes[i]) for i in range(N)]
    need = sum(counts[i] * sizes[i] for i in range(N))
    if need > W * H:
        return False

    board_cells = W * H
    board_mask = (1 << board_cells) - 1

    # Precompute placement masks per shape id (dedup variants)
    masks: List[List[int]] = [[] for _ in range(N)]
    for i in range(N):
        if counts[i] == 0:
            continue
        s: set[int] = set()
        for v in variants(shapes[i]):
            s.update(placements(v, W, H))
        if not s:
            return False
        masks[i] = list(s)

    # cell_to[c] = list of (sid, mask) placements that cover cell c
    cell_to: List[List[Tuple[int, int]]] = [[] for _ in range(board_cells)]
    for sid in range(N):
        if counts[sid] == 0:
            continue
        for m in masks[sid]:
            # if any bit is outside the board, ignore the placement
            if m & ~board_mask:
                continue
            for c in iter_bits(m):
                # c is guaranteed < board_cells here
                cell_to[c].append((sid, m))

    memo: Dict[Tuple[int, Tuple[int, ...], int], bool] = {}

    def dfs(occ: int, left: Tuple[int, ...], placed: int) -> bool:
        key = (occ, left, placed)
        if key in memo:
            return memo[key]
        if placed == need:
            memo[key] = True
            return True

        # Compute all currently placeable cells (union of non-overlapping placements)
        coverable = 0
        for i in range(N):
            if left[i]:
                for m in masks[i]:
                    if not (m & occ):
                        coverable |= m
        coverable &= ~occ

        if not coverable:
            memo[key] = False
            return False

        # Pick the most constrained coverable cell (fewest legal placements now)
        best_cell = -1
        best_opts = 10**18

        tmp = coverable
        while tmp:
            lsb = tmp & -tmp
            c = lsb.bit_length() - 1
            tmp ^= lsb

            opts = 0
            for sid, m in cell_to[c]:
                if left[sid] and not (m & occ):
                    opts += 1
                    if opts >= best_opts:
                        break

            if opts == 0:
                memo[key] = False
                return False

            if opts < best_opts:
                best_opts = opts
                best_cell = c
                if best_opts == 1:
                    break

        cell = best_cell

        # Try every legal placement covering that cell
        for sid, m in cell_to[cell]:
            if left[sid] and not (m & occ):
                nl = list(left)
                nl[sid] -= 1
                if dfs(occ | m, tuple(nl), placed + sizes[sid]):
                    memo[key] = True
                    return True

        memo[key] = False
        return False

    return dfs(0, tuple(counts), 0)


# -------------------------
#   Part 1
# -------------------------

def part1(lines: List[str]) -> int:
    shapes = parse_shapes(lines)
    if not shapes:
        raise ValueError("No shapes found (wrong input file?)")

    n = max(shapes) + 1
    regions = parse_regions(lines, n)

    return sum(
        1 for W, H, c in regions
        if c and can_fit(W, H, c, shapes)
    )


# -------------------------
#   Tests
# -------------------------

def test_example():
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


def test_placements_never_spill():
    # Any generated placement mask must only touch bits < W*H.
    shape = _normalize(((0, 0), (1, 0), (0, 1)))
    W, H = 3, 3
    for v in variants(shape):
        for m in placements(v, W, H):
            assert m < (1 << (W * H))


def run_tests():
    test_example()
    test_placements_never_spill()
    print("All tests passed")


# -------------------------
#   Main
# -------------------------

if __name__ == "__main__":
    lines = read_input()
    # Uncomment to sanity check locally:
    # run_tests()
    print("Part 1:", part1(lines))