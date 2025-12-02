# 🎄 Advent of Code 2025 — Day 2: Secret Entrance

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="NES-style snowy pixel art banner with raccoon coder"
    title="NES Snowy Pixel Art Banner"
  >
</p>

The decorations are half-finished, the deadlines are actively smoking, and—because fate has a sense of humor—the Elves have discovered project management.
They’ve made a Gantt chart, argued about it for three hours, and now you have to open a mysterious safe so the North Pole doesn’t collapse into whimsical anarchy.
Typical Tuesday.

Inside this folder lives a clean Python solution for both Part 1 and Part 2, plus a tiny test suite so Future-You doesn’t have to guess whether the code still works after “refactoring.”

---

## 🎅 Story Summary

### 🧩 Part 1

You’ve got a dial from 0–99. The instructions tell you how far to rotate it.
Every time you complete a rotation, you check where it landed.

If the dial ends exactly on 0, congrats — that’s one point for the “prevent Christmas meltdown” scoreboard.

> Simple concept… until the Elves remember they’re Elves and ruin geometry.

### 🧩 Part 2 — Click-by-Click Mode

The Elves activate method 0x434C49434B (“CLICK”), which is basically:

> “What if we made this needlessly complicated… on purpose?”

Now you count every single click that passes through 0.
Doesn’t matter if you end there. Doesn’t matter if you were on your way to 87.
If you pass 0? Ding. Count it.

This makes the dial behave like a tiny chaotic Ferris wheel run by interns.

---

## 🔧 Project Structure

```plaintext
day02/
├── input.txt      # Your personal puzzle input
├── solution.py    # Python solution (part1, part2, tests)
└── README.md      # This file
```

---

## ▶️ How to Run the Solution


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

---

## 🦝 Built by NickDoesDevOps

Created with ☕, curiosity, and just enough chaos by:

- [![GitHub](https://img.shields.io/badge/GitHub-@NickTheDevOpsGuy-181717?logo=github)](https://github.com/NickTheDevOpsGuy)
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Nicholas%20Clark-0A66C2?logo=linkedin)](https://www.linkedin.com/in/nicholas-a-clark/)
- [![Email](https://img.shields.io/badge/Email-Contact-grey?logo=gmail)](mailto:nicholas.a.clark@outlook.com)

🏷 **#NickDoesDevOps** • **#LearningInPublic** • **#BuiltInPublic**