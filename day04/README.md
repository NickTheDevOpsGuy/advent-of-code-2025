# 🎄 Advent of Code 2025 — Day 4: Printing Department (FULL RACCOON MODE)

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="Raccoon aggressively operating a forklift with zero qualifications"
    title="Raccoon OSHA Incident #47"
  >
</p>

Welcome to Day 4, where forklifts are emotionally fragile,
paper rolls are socially overwhelmed,
and **you** are now the designated raccoon responsible for “optimizing operations”
(translation: causing polite forklift chaos).

Today’s puzzle asks the key scientific question:

> **“How many paper tubes can a raccoon remove before the universe collapses?”**

Let’s get into it.

---

## 🧩 Part 1 — “Count the Lonely Paper Burritos”

You’re given a giant grid full of paper rolls (`@`),
arranged like a raccoon tried to assemble IKEA furniture without the manual.

A roll is **accessible** if it has:

🦝 **Fewer than four neighbors**  
(because forklifts don’t like crowds—forklifts are introverts)

To solve Part 1:

- Look at every roll  
- Count its 8 possible neighbors  
- If it has **0–3 friends**, a forklift can snatch it  
- If it has **4+**, it is too popular and therefore dead to us

You tally all the socially awkward rolls.
That’s Part 1.

Congratulations, you are now a Certified Raccoon Census Analyst.

---

## 🧩 Part 2 — “Forklift Mayhem Simulator 2025”

Now unleash the madness.

Once a roll is accessible…

👉 The forklift removes it.  
👉 Removing rolls makes NEW rolls accessible.  
👉 Those rolls also get removed.  
👉 The cycle continues until you’re left with emotional devastation.

This is basically:

- Minesweeper  
- + Jenga  
- + a raccoon driving heavy machinery  
- – any hope of structural stability

The final answer is:

**How many rolls vanish in this cascading forklift purge?**

In the example, a dramatic **43 rolls** get wiped out  
because the forklifts went full raccoon mode:
no logic, just vibes and removal.

---

## 🔧 Project Structure

```
day04/
├── input.txt
├── solution.py
└── README.md
```

This README is the chaotic one.  
Cherish it.

---

## ▶️ Running the Solution

```
python3 solution.py
```

Output looks like:

```
Part 1: 1370
Part 2: <a number that proves forklifts are too powerful>
```

If Part 2 prints **0**,  
a raccoon has almost certainly edited your code without permission.

---

## 🧪 Test Suite

Day 4 involves:

- adjacency math  
- recursion by removal  
- infinite-loop bait  
- forklift emotional instability  

So we wrote tests.  
These tests will **scream at you** if you break anything.

To run them:

Edit:

```
RUN_TESTS = False
```

to

```
RUN_TESTS = True
```

Run:

```
python3 solution.py
```

You want to see:

```
Running tests...
All tests passed!
```

If you see an error…  
just imagine a raccoon staring at you in disappointment.

---

## 🎁 Tiny Example (with Raccoon Commentary)

Initial:

```
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
...
```

Raccoon:

> “I will remove these 13.  
> And these 12.  
> And these 7.  
> And these 5.  
> Also 2.  
> Also 1.  
> Another 1.  
> Again.  
> Still bored.  
> One more.  
> Okay, done.”  

Total removed: **43**.

This is what peak forklift performance looks like.

---

## 🦝 Built by NickDoesDevOps

Powered by:

- caffeine  
- raccoon chaos  
- Python  
- questionable decision-making  
- forklifts that should NOT be trusted  

**#NickDoesDevOps • #LearningInPublic • #BuiltInPublic**
