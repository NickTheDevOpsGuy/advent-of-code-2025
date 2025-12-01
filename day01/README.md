## 🎄 Advent of Code — Day 1: Secret Entrance

Decorating the North Pole shouldn’t be this hard… but the Elves have discovered project management, realized they have no time left, and now you have to open a mysterious safe to save Christmas.

This repo contains a clean Python solution to Day 1, where we simulate a circular dial and count how many times it lands on 0.

---

## 🎅 Story Summary

You arrive at a hidden entrance to the North Pole base, but the password was changed!
The Elves left behind a sequence of rotations — each like:

```bash
L68
R12
L4
```

Each rotation tells you how far to turn the safe’s dial left or right.
The dial has positions 0–99 and wraps around (99 → 0, 0 → 99).

You start at 50, follow all rotations, and record how many times the dial lands on 0.

That count is the real password.

---

## 🔧 Project Structure

```plaintext
.
├── input.txt
├── README.md
└── solution.py
```

---

## ▶️ How to Use This Solution

1. Place your puzzle input in `input.txt` (one rotation per line).
2. Run the Python script:

```bash
python solution.py
```

3.	The output will look like:

```bash
Password: 997
```

Where *997* is the number of times the dial landed on 0 across all rotations.

---

## 🧠 How the Logic Works

• Dial starts at 50
• Each instruction is:
	• Lx → move x steps backward (subtract, wrap)
	• Rx → move x steps forward (add, wrap)
• After each rotation:
	• If dial is 0, increment the answer
	• Use modulo arithmetic to wrap around a 0–99 circle

---

## 🐍 Example Python Logic (concept only)

```python
pos = 50
zeros = 0

for line in lines:
    direction = line[0]
    steps = int(line[1:])

    if direction == "L":
        pos = (pos - steps) % 100
    else:
        pos = (pos + steps) % 100

    if pos == 0:
        zeros += 1

print("Password:", zeros)
```

---

🎁 Example Visualization

```bash
Start at 50
L30 → 20
R70 → 90
R10 → 0  🎉 (zero #1)
L1  → 99
...
```

You count each landing on 0 — that’s the puzzle’s answer.

---

## ❄️ Festive ASCII for vibes

        *    ✵
      ✵  \ | /   *
    *     \|/  ✵
  ✵    * --🎄--   *
    *     /|\      ✵
       ✵ / | \  *
           *

---

## 🦝 Built by NickDoesDevOps

Created with ☕, curiosity, and just enough chaos by:

[![GitHub](https://img.shields.io/badge/GitHub-@NickTheDevOpsGuy-181717?logo=github)](https://github.com/NickTheDevOpsGuy)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nicholas%20Clark-0A66C2?logo=linkedin)](https://www.linkedin.com/in/nicholas-a-clark/)
[![Email](https://img.shields.io/badge/Email-Contact-grey?logo=gmail)](mailto:nicholas.a.clark@outlook.com)

🏷 **#NickDoesDevOps** • **#LearningInPublic** • **#BuiltInPublic**