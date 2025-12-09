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

def parse_points(lines):
    """
    Convert each 'x,y' line into (x, y) integer tuples.

    Returns:
        List[(x,y)] of red tile positions.
    """
    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        x_str, y_str = line.split(",")
        points.append((int(x_str), int(y_str)))
    return points


def rect_area(p1, p2):
    """
    Opposite red corners p1=(x1,y1), p2=(x2,y2)
    Return rectangle AREA in *tiles*.

    If same row or same column → area 0; cannot form a rectangle.
    """
    (x1, y1) = p1
    (x2, y2) = p2

    if x1 == x2 or y1 == y2:
        return 0

    width  = abs(x1 - x2) + 1
    height = abs(y1 - y2) + 1
    return width * height


def find_max_rectangle(points):
    """
    PART 1:
    Check every pair of red tiles as opposite corners.
    Return the largest rectangle area.
    """
    max_area = 0
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            area = rect_area(points[i], points[j])
            if area > max_area:
                max_area = area

    return max_area


# -------------------------
#   Helpers for PART 2
# -------------------------

def build_lines(points):
    """
    Build the boundary loop lines for red/green tiles.

    Each consecutive pair (including last→first) forms
    an axis-aligned segment. We store (x_min,x_max,y_min,y_max).
    """
    n = len(points)
    lines = []

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        if x1 == x2:
            # vertical
            y_min = min(y1, y2)
            y_max = max(y1, y2)
            lines.append((x1, x1, y_min, y_max))
        else:
            # horizontal
            x_min = min(x1, x2)
            x_max = max(x1, x2)
            y_min = min(y1, y2)
            y_max = max(y1, y2)
            lines.append((x_min, x_max, y_min, y_max))

    return lines


def rect_area_if_allowed(p1, p2, lines):
    """
    PART 2 helper:

    Check if the rectangle between p1 and p2 lies entirely within
    the red+green loop region.

    Reject if any boundary segment intersects the **interior**.
    """
    area = rect_area(p1, p2)
    if area == 0:
        return 0

    (x1, y1) = p1
    (x2, y2) = p2

    left   = min(x1, x2)
    right  = max(x1, x2)
    top    = min(y1, y2)
    bottom = max(y1, y2)

    # interior-intersection test
    for (lx_min, lx_max, ly_min, ly_max) in lines:
        if lx_max > left and lx_min < right and ly_max > top and ly_min < bottom:
            return 0

    return area


def find_max_rectangle_red_green(points):
    """
    PART 2:
    Largest rectangle whose interior lies entirely inside
    the red/green loop area.
    """
    lines = build_lines(points)
    max_area = 0
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            area = rect_area_if_allowed(points[i], points[j], lines)
            if area > max_area:
                max_area = area

    return max_area


# -------------------------
#   Part 1 Logic
# -------------------------

def part1(lines):
    points = parse_points(lines)
    return find_max_rectangle(points)


# -------------------------
#   Part 2 Logic
# -------------------------

def part2(lines):
    points = parse_points(lines)
    return find_max_rectangle_red_green(points)


# -------------------------
#   Tests
# -------------------------

def test_rect_area_basic():
    assert rect_area((0,0), (3,2)) == 12     # 4×3 rectangle


def test_rect_area_same_line():
    assert rect_area((2,5), (9,5)) == 0
    assert rect_area((7,1), (7,7)) == 0


def test_parse_points():
    pts = parse_points(["3,4", "10,20"])
    assert pts == [(3,4),(10,20)]


def example_points():
    return [
        (7,1),
        (11,1),
        (11,7),
        (9,7),
        (9,5),
        (2,5),
        (2,3),
        (7,3),
    ]


def test_part1_example():
    pts = example_points()
    assert find_max_rectangle(pts) == 50


def test_part2_example():
    pts = example_points()
    assert find_max_rectangle_red_green(pts) == 24


def run_tests():
    print("Running tests...")
    test_rect_area_basic()
    test_rect_area_same_line()
    test_parse_points()
    test_part1_example()
    test_part2_example()
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
        print("Part 2:", part2(lines))