# 🎄 Advent of Code 2025 — Day 1: Secret Entrance

<p align="center">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="NES-style snowy pixel art banner with raccoon coder"
    title="NES Snowy Pixel Art Banner"
  >
</p>

Decorating the North Pole shouldn’t be this hard… but the Elves have discovered project management, realized they have no time left, and now you have to open a mysterious safe to save Christmas.

This folder contains a clean **Python solution for both Part 1 and Part 2**, plus a tiny built-in test suite so you (or future you) can quickly verify the logic.

---

## 🎅 Story Summary

You arrive at a hidden entrance to the North Pole base, but the password has changed!

The Elves left behind a document full of rotations like:

```text
L68
R12
L4
```

Each instruction turns the safe’s dial:

- `Lx` → rotate **left** toward lower numbers  
- `Rx` → rotate **right** toward higher numbers  

The dial has **100 positions** (`0`–`99`) and wraps around:

- left from `0` → `99`  
- right from `99` → `0`  

You always begin at **50**.

### 🧩 Part 1

Follow all rotations from the input.  
After **each full rotation**, check where the dial ends up.  

> The Part 1 password is the number of times the dial is exactly on **0** at the *end* of a rotation.

### 🧩 Part 2 — Click-by-Click Mode

The Elves switch to “method `0x434C49434B`”, which means:

> Count **every single click** that lands on `0`, even if it happens *during* a rotation (not just at the end).

So for each instruction, instead of doing one big jump, you simulate the dial **one click at a time**, wrapping around the `0`–`99` circle, and count every time the dial hits `0`.

---

## 🔧 Project Structure

```plaintext
day01/
├── input.txt      # Your personal puzzle input
├── solution.py    # Python solution (part1, part2, tests)
└── README.md      # This file
```

---

## ▶️ How to Run the Solution

1. Put your puzzle input into `input.txt`  
   (one rotation per line, e.g. `L68`, `R12`, `R1000`, etc.)

2. Make sure you’re in the `day01` folder:

   ```bash
   cd day01
   ```

3. Run the Python script:

   ```bash
   python3 solution.py
   ```

4. With normal (non-test) mode enabled, you’ll see:

   ```text
   Part 1: 997
   Part 2: 5978
   ```

   Where:

   - **Part 1** → count of times the dial is on `0` **after** a rotation  
   - **Part 2** → count of times the dial hits `0` on **any click** during all rotations

---

## 🧠 How the Logic Works (High Level)

Both parts share the same basic idea:

- Start at `position = 50`
- Parse each line:
  - `direction = line[0]` → `'L'` or `'R'`
  - `distance = int(line[1:])`
- The dial is always kept in the range `0–99` using modulo:

  ```python
  position = (position + step) % 100
  ```

### Part 1

- For each instruction:
  - Move the dial once by `+distance` (right) or `-distance` (left), using modulo for wrapping.
  - If the final `position` is `0`, increment the counter.

### Part 2

- For each instruction:
  - Instead of one big jump, simulate **`distance` single-click moves**:
    - Right → `position = (position + 1) % 100`
    - Left → `position = (position - 1) % 100`
  - After each click, if `position == 0`, increment the counter.

This matches the problem’s “count every click that lands on zero” requirement and correctly handles big distances like `R1000`.

---

## 🧪 Running the Optional Test Suite

`solution.py` includes a small, built-in test suite that checks:

- The official example from the problem statement (Part 1 & Part 2)
- Some custom scenarios that stress wrapping and multiple zero crossings

The tests are **off by default** so normal runs just solve the puzzle.

### 🔄 Turn Tests On

1. Open `solution.py`
2. Scroll to the bottom and find:

   ```python
   if __name__ == "__main__":
       RUN_TESTS = False
   ```

3. Switch it to:

   ```python
   if __name__ == "__main__":
       RUN_TESTS = True
   ```

4. Run:

   ```bash
   python3 solution.py
   ```

You’ll see something like:

```text
Running tests...
All tests passed!
```

If any `assert` fails, Python will raise an error so you can investigate.

### 🔁 Switch Back to Puzzle Mode

Once you’re done testing, set:

```python
RUN_TESTS = False
```

again so `solution.py` runs against `input.txt` and prints your actual answers.

---

## 🎁 Example Walkthrough (Tiny Sample)

Imagine this tiny input:

```text
R50
R50
```

Start at `50`.

- `R50`:
  - Part 1: end on `0` → counts as 1 hit
  - Part 2: during the 50 clicks, you land on `0` exactly once → 1 hit
- `R50` again:
  - Part 1: end on `50` → 0 additional
  - Part 2: another 1 time hitting `0` during the path

So for that input:

- Part 1: `1`  
- Part 2: `2`

This is the kind of scenario covered by the tests in `solution.py`.

---


## 🦝 Built by NickDoesDevOps

Created with ☕, curiosity, and just enough chaos by:

- [![GitHub](https://img.shields.io/badge/GitHub-@NickTheDevOpsGuy-181717?logo=github)](https://github.com/NickTheDevOpsGuy)
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Nicholas%20Clark-0A66C2?logo=linkedin)](https://www.linkedin.com/in/nicholas-a-clark/)
- [![Email](https://img.shields.io/badge/Email-Contact-grey?logo=gmail)](mailto:nicholas.a.clark@outlook.com)

🏷 **#NickDoesDevOps** • **#LearningInPublic** • **#BuiltInPublic**
