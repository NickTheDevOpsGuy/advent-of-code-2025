# 🎄 Advent of Code 2025 — Day 5: Cafeteria Chaos

```text
        *     ✵         *  
   ✵     \ | /   *    ✵      ~ sniffs aggressively ~
    *     \|/  ✵
  ✵    * --🎄--   *      "WHO LEFT ALL THESE INGREDIENTS OUT?!"
    *     /|\      ✵
       ✵ / | \  *  
           *
```

Welcome to **Day 5**, also known as:

> “Why did the North Pole migrate to an inventory system  
> that looks like it was written by a sleep-deprived raccoon?”

The forklifts just punched through a wall, revealing a **cafeteria full of screaming Elves**, and now *you* have to determine which ingredients are spoiled before someone accidentally serves “mystery soup with a hint of tetanus.”

Inside this folder you’ll find:

- A **Python solution** for Part 1 and Part 2  
- A test suite so future-you doesn’t come back tomorrow yelling  
  “WHO BROKE MY RANGE MERGING?!”

---

## 🎅 Story Summary

### 🧩 Part 1 — *Is This Ingredient Fresh or a Biohazard?*

The Elves give you:

1. A list of **fresh ID ranges**  
2. A blank line  
3. A list of **ingredient IDs they found lying around**

Your job:

> For each ingredient ID, check if it falls inside *any* fresh range.  
> If yes: **fresh**.  
> If no: **straight to the trash chute, do not pass Go.**

### 🧩 Part 2 — *The Raccoon Approves of Unionizing the Ranges*

Now the Elves say:

> “Ignore the ingredient list entirely.  
> We want to know how many total IDs are fresh **in theory**.”

So you merge all overlapping ranges into mega-range-chimichangas and count how many IDs they cover.

Example ranges merge to:
- `3–5`
- `10–20`

Total fresh IDs = **14**

---

## 🔧 Project Structure

```
day05/
├── input.txt
├── solution.py
└── README.md
```

---

## ▶️ Running the Solution

```
python3 solution.py
```

---

## 🧪 Running the Test Suite

Turn tests on by setting:

```
RUN_TESTS = True
```

at the bottom of `solution.py`.

Run:

```
python3 solution.py
```

---

## 🦝 Built by NickDoesDevOps

Caffeinated, chaotic, and festive.  
#RaccoonDrivenDevelopment • #LearningInPublic • #BuiltInPublic
