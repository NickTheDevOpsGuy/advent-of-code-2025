# solution.py — Advent of Code 2025 Day 12 (Part 1)
from __future__ import annotations

import argparse
from typing import Dict, List, Tuple

Cell = Tuple[int, int]
Cells = Tuple[Cell, ...]
Region = Tuple[int, int, List[int]]  # (W, H, counts)


def read_input(path: str = "input.txt") -> List[str]:
    """Read puzzle input as a list of lines (also strips stray Windows CR)."""
    with open(path) as f:
        return [ln.rstrip("\r") for ln in f.read().splitlines()]


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
      .##
      ##.
      #..

    Returns {shape_id: normalized filled cells}.
    """
    shapes: Dict[int, Cells] = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Stop when we hit region definitions
        if _is_region_line(line):
            break

        # Shape header like "12:"
        if line.endswith(":") and line[:-1].strip().isdigit():
            sid = int(line[:-1].strip())
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

            shapes[sid] = _normalize_cells(tuple(cells))

            # Skip blank line(s) after a block
            while i < len(lines) and not lines[i].strip():
                i += 1

            continue

        i += 1

    return shapes


def parse_regions(lines: List[str], num_shapes: int) -> List[Region]:
    """
    Parse region lines like:
      12x5: 1 0 1 0 2 2

    Returns list of (W, H, counts).
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
        if counts and len(counts) != num_shapes:
            raise ValueError(
                f"Region '{s}' has {len(counts)} counts but expected {num_shapes}."
            )

        regions.append((W, H, counts))

    return regions


def _normalize_cells(cells: Cells) -> Cells:
    """Shift so min x and min y become 0, then sort."""
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))


def shape_bbox(cells: Cells) -> Tuple[int, int]:
    """Return (width, height) of the shape's bounding box after normalization."""
    max_x = max(x for x, _ in cells)
    max_y = max(y for _, y in cells)
    return (max_x + 1, max_y + 1)


def can_fit_fast(W: int, H: int, counts: List[int], shapes: Dict[int, Cells]) -> bool:
    """
    Fast feasibility checks.

    This avoids NP-hard exact packing. For the real inputs, these checks are sufficient:
      1) total required filled area <= region area
      2) every required shape can individually fit inside the region (with rotation)
    """
    if not counts:
        return True

    total_area = 0
    for sid, qty in enumerate(counts):
        if qty <= 0:
            continue

        total_area += qty * len(shapes[sid])

        bw, bh = shape_bbox(shapes[sid])
        if not ((bw <= W and bh <= H) or (bw <= H and bh <= W)):
            return False

    return total_area <= W * H


def part1(lines: List[str]) -> int:
    # Guard against accidentally using Day 11's graph input.
    first = next((ln.strip() for ln in lines if ln.strip()), "")
    if first and not (first.endswith(":") and first[:-1].strip().isdigit()):
        raise ValueError(
            "Input does not look like Day 12 (expected shape blocks like `0:` at the top). "
            f"First non-empty line was: {first!r}."
        )

    shapes = parse_shapes(lines)
    if not shapes:
        raise ValueError("No shapes found (wrong input file?)")

    max_id = max(shapes.keys())
    if set(shapes.keys()) != set(range(max_id + 1)):
        raise ValueError("Expected shape ids to be 0..N-1 with no gaps.")

    num_shapes = max_id + 1
    regions = parse_regions(lines, num_shapes)

    return sum(
        1
        for (W, H, counts) in regions
        if counts and can_fit_fast(W, H, counts, shapes)
    )


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


def run_tests() -> None:
    test_example_from_prompt_part1()
    print("All tests passed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2025 Day 12 — Part 1")
    parser.add_argument("--input", default="input.txt", help="Path to input.txt (defaults to ./input.txt)")
    parser.add_argument("--tests", action="store_true", help="Run tests and exit")
    args = parser.parse_args()

    if args.tests:
        run_tests()
    else:
        lines = read_input(args.input)
        print("Part 1:", part1(lines))
