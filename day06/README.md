# 🎄 Advent of Code 2025 — Day 6: Trash Compactor (Cephalopod Math Edition)

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="Raccoon doing math it absolutely should not be trusted with"
    title="Cephalopod Homework Crisis 2025"
  >
</p>

Welcome to **Day 6**, where you fall into a garbage compactor, meet polite cephalopods,  
and immediately become responsible for tutoring their smallest tentacle gremlin in math.

This is not the job you applied for.  
But here we are.

---

# 🧩 Part 1 — *Vertical Math for Squishy Creatures*

Cephalopod homework looks normal until you unroll it and discover:

- The worksheet is **one gigantic horizontal strip**  
- Each **problem** is stacked vertically  
- Problems are separated by **one full blank column**  
- The **operator** (`+` or `*`) sits at the bottom  
- Alignment does not matter  
- Your emotional stability also does not matter

Example:

```
123 328  51 64 
 45  64 387 23 
  6   98 215 314
*    +   *   +  
```

Meaning:

- Problem #1 uses `*` → 123 * 45 * 6  
- Problem #2 uses `+` → 328 + 64 + 98  
- Problem #3 uses `*`  
- Problem #4 uses `+`  

Your job?

👉 **Evaluate all problems and sum their results.**

Example total: **4,277,556**

Your real input: **3,525,371,263,915**  
A number large enough to frighten weak calculators.

---

# 🧩 Part 2 — *Quantum Cephalopod Math (Why.)*

Just when you think you understand the rules…

The cephalopods return and say:

> “Oh! We forgot to tell you.  
> Cephalopod math is read **right‑to‑left**, and numbers are stored **one digit per column**."

You stare at them.

They stare back.

Suddenly, the worksheet becomes this strange columnwise puzzle:

- Each **column** becomes a number  
- You read them **top → bottom**  
- Digits stack vertically  
- Columns are grouped into problems using the same blank-column rule  
- Problems are evaluated **right→left**

Example problem now reads like:

```
356 * 24 * 1 = 8544
8 + 248 + 369 = 625
175 * 581 * 32 = 3,253,600
4 + 431 + 623 = 1,058
```

Grand total: **3,263,827**

Your real input?

A *much* larger number.  
A number that screams “quantum tentacle nonsense.”

---

# 🔧 Project Structure

```
day06/
├── input.txt
├── solution.py
└── README.md   ← this file
```

---

# ▶️ Running the Solution

```
python3 solution.py
```

You will see:

```
Part 1: <big number>
Part 2: <bigger number>
```

If you see a negative number,  
you have accidentally opened a wormhole and must flee immediately.

---

# 🧪 Test Suite

The `solution.py` includes tests covering:

- Block detection  
- Vertical number parsing  
- Columnwise reverse parsing  
- Example cases from the problem text  

To run them:

Edit:

```
RUN_TESTS = False
```

to:

```
RUN_TESTS = True
```

Then run:

```
python3 solution.py
```

If all tests pass, a raccoon somewhere nods approvingly.

---

# 🦝 Built by NickDoesDevOps

Powered entirely by:

- cephalopod nonsense  
- raccoon energy  
- garbage compactors  
- too much coffee  
- not enough sleep  

**#LearningInPublic #BuiltInPublic #RaccoonDrivenDevelopment**
