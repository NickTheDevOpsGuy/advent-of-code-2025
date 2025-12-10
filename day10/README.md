# 🎄 Advent of Code 2025 — Day 9: Secret Entrance

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="A raccoon confidently repairing a teleporter he absolutely should NOT touch"
    title="Quantum OSHA Incident #88"
  >
</p>

Decorating the North Pole shouldn’t be this hard… but the Elves have discovered project management, realized they have no time left, and now you have to open a mysterious safe to save Christmas.

This folder contains a clean **Python solution for both Part 1 and Part 2**, plus a tiny built-in test suite so you (or future you) can quickly verify the logic.

---

## 🎅 Story Summary

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