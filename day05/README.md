# 🎄 Advent of Code 2025 — Day 5: Cafeteria Chaos (FULL RACCOON MODE)

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="Raccoon rummaging through a fridge full of questionable ingredients"
    title="Raccoon Culinary Incident #12"
  >
</p>

Welcome to Day 5, where the Elves are screaming about **inventory systems**,  
ingredients are aging faster than a cheese left in a microwave,  
and **you**, a raccoon with the moral restraint of a blender,
are now responsible for food safety at the North Pole.

Today’s puzzle asks the ancient culinary question:

> **“Is this ingredient fresh...  
> or is it basically a biohazard with dreams and opinions?”**

Let’s begin before a health inspector shows up.

---

## 🧩 Part 1 — “Fresh or Spoiled, There Is No In-Between”

You get:

1. A list of **fresh ID ranges** (e.g., `3-5`, `10-20`)  
2. A blank line  
3. A bunch of **ingredient IDs found lying around the cafeteria**

Your mission:

> **Determine how many of the ingredient IDs are considered fresh.**

If an ID fits inside *any* fresh range → **fresh**  
If not → **send it straight to the trash compactor**

This is easy raccoon math:

- Check the ID  
- If it fits in a range → eat it  
- If not → throw at an Elf  
- Count how many are edible (legally or not)

Congrats — you're now a **Food Safety Raccoon**.

---

## 🧩 Part 2 — “Merging Ranges Like Your Life Depends On It”

The Elves return with:

> “So, uh… ignore the ingredient list.  
> We want to know how many possible IDs *in theory* are fresh.”

So now you take all the ranges and:

1. Sort them  
2. Merge all overlapping or touching ranges  
3. Count how many integers those merged ranges cover

Example:

```
3-5
10-14
16-20
12-18
```

merge into:

```
3–5
10–20
```

Total fresh →  
- (3,4,5) = 3  
- (10..20) = 11  
→ **14**

This is peak raccoon data engineering.

---

## 🔧 Project Structure

```
day05/
├── input.txt
├── solution.py
└── README.md   <-- this glorious chaos document
```

---

## ▶️ Running the Solution

```
python3 solution.py
```

You’ll see something like:

```
Part 1: <number of ingredients not trying to kill you>
Part 2: <how many total IDs are considered fresh in theory>
```

If Part 2 prints `0`,  
you probably merged ranges *backwards*  
or a raccoon deleted your code out of spite.

---

## 🧪 Test Suite

Range logic is tricky.  
Off-by-one errors lurk everywhere like raccoons in dumpsters.

Turning tests on:

```
RUN_TESTS = True
```

Then run:

```
python3 solution.py
```

If life is good:

```
Running tests...
All tests passed!
```

If not, please imagine a raccoon gently tapping the screen in disappointment.

---

## 🎁 Tiny Example (with Raccoon Commentary)

Input:

```
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

Raccoon’s verdict:

- 1 → rancid  
- 5 → actually edible? shocking  
- 8 → nope  
- 11 → fresh  
- 17 → VERY fresh (double-certified)  
- 32 → burn it  

Part 1 total fresh = **3**

Part 2 merged range total = **14**

The raccoon approves.

---

## 🦝 Built by NickDoesDevOps

Fueled by:

- Python  
- chaotic interval logic  
- caffeine  
- questionable decision-making  
- and an unlicensed raccoon performing QA  

**#NickDoesDevOps • #LearningInPublic • #BuiltInPublic**
