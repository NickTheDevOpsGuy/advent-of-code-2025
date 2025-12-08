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
#   Parse helpers
# -------------------------

def parse_points(lines):
    """
    Convert 'X,Y,Z' lines into a list of (x, y, z) integer tuples.
    Ignores empty lines.
    """
    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        x_str, y_str, z_str = line.split(",")
        points.append((int(x_str), int(y_str), int(z_str)))
    return points


# -------------------------
#   Union-Find (Disjoint Set)
# -------------------------

class UnionFind:
    """
    Simple Disjoint Set Union (Union-Find) structure.

    - parent[i] = parent representative of node i
    - size[root] = size of the component whose root is `root`
    - count = current number of connected components
    """

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n  # number of components

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        """
        Merge the sets containing a and b.
        Returns True if a merge happened (they were different components),
        False if they were already in the same component.
        """
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False

        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True

    def component_sizes(self):
        """
        Return a list of sizes of all components.
        """
        root_to_size = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            root_to_size[r] = root_to_size.get(r, 0) + 1
        return list(root_to_size.values())


# -------------------------
#   Distance helpers
# -------------------------

def squared_distance(p, q):
    """
    Squared Euclidean distance between two 3D points p and q.
    """
    x1, y1, z1 = p
    x2, y2, z2 = q
    dx = x1 - x2
    dy = y1 - y2
    dz = z1 - z2
    return dx * dx + dy * dy + dz * dz


def find_k_closest_pairs(points, k):
    """
    Given a list of 3D points, return the k closest pairs.

    points: list of (x, y, z) tuples
    k: how many pairs to keep

    Returns:
        A list of tuples (dist_sq, i, j), sorted by dist_sq ascending,
        where i and j are indices into `points`.
    """
    pairs = []
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = squared_distance(points[i], points[j])
            pairs.append((dist_sq, i, j))

    pairs.sort(key=lambda tup: tup[0])
    return pairs[:k]


def find_all_pairs(points):
    """
    Build all possible pairs (i, j) with i < j, returning a list
    of (dist_sq, i, j) sorted by dist_sq ascending.
    """
    pairs = []
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = squared_distance(points[i], points[j])
            pairs.append((dist_sq, i, j))

    pairs.sort(key=lambda tup: tup[0])
    return pairs


# -------------------------
#   Core solvers
# -------------------------

def solve_with_k(points, k):
    """
    Helper used by Part 1 and tests:

    - Build all pairs
    - Keep the k closest
    - Union them in order
    - Return product of the sizes of the three largest components
    """
    uf = UnionFind(len(points))
    pairs = find_k_closest_pairs(points, k)

    for dist_sq, i, j in pairs:
        uf.union(i, j)

    sizes = uf.component_sizes()
    sizes.sort(reverse=True)

    if len(sizes) < 3:
        # In pathological small examples, you might not have 3 components;
        # handle that gracefully.
        prod = 1
        for s in sizes:
            prod *= s
        return prod

    return sizes[0] * sizes[1] * sizes[2]


def part1(lines):
    """
    Connect the 1000 closest pairs, then multiply the sizes
    of the three largest circuits.
    """
    points = parse_points(lines)
    return solve_with_k(points, 1000)


def part2(lines):
    """
    Keep connecting pairs from closest to farthest until all junction
    boxes belong to a single circuit (one connected component).

    Return the product of the X-coordinates of the last two boxes
    that were successfully connected.
    """
    points = parse_points(lines)
    n = len(points)

    pairs = find_all_pairs(points)
    uf = UnionFind(n)

    last_i = None
    last_j = None

    for dist_sq, i, j in pairs:
        merged = uf.union(i, j)
        if not merged:
            # already in the same circuit
            continue

        last_i = i
        last_j = j

        # when everything is in one component, we're done
        if uf.count == 1:
            break

    if last_i is None or last_j is None:
        raise RuntimeError("Did not manage to connect all junction boxes.")

    x1 = points[last_i][0]
    x2 = points[last_j][0]
    return x1 * x2


# -------------------------
#   Tests (using sample from prompt)
# -------------------------

EXAMPLE_TEXT = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


def test_example_part1():
    """
    From the problem statement:

    After making the ten shortest connections, there are:
      - one circuit of size 5
      - one circuit of size 4
      - two circuits of size 2
      - seven circuits of size 1

    Product of three largest sizes = 5 * 4 * 2 = 40
    """
    lines = EXAMPLE_TEXT.strip().splitlines()
    points = parse_points(lines)
    result = solve_with_k(points, 10)
    assert result == 40, f"Expected 40, got {result}"


def test_example_part2():
    """
    From the problem statement:

    The first connection which causes all junction boxes to be in one
    single circuit is between the junction boxes at:

        216,146,977  and  117,168,530

    Product of X-coordinates = 216 * 117 = 25272
    """
    lines = EXAMPLE_TEXT.strip().splitlines()
    points = parse_points(lines)

    pairs = find_all_pairs(points)
    uf = UnionFind(len(points))

    last_i = None
    last_j = None

    for dist_sq, i, j in pairs:
        merged = uf.union(i, j)
        if not merged:
            continue
        last_i = i
        last_j = j
        if uf.count == 1:
            break

    x1 = points[last_i][0]
    x2 = points[last_j][0]
    result = x1 * x2

    assert result == 25272, f"Expected 25272, got {result}"


def run_tests():
    print("Running tests...")
    test_example_part1()
    test_example_part2()
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