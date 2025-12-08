# 🎄 Advent of Code 2025 — Day 6: Tachyon Manifold Mayhem (FULL RACCOON MODE)

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="A raccoon confidently repairing a teleporter he absolutely should NOT touch"
    title="Quantum OSHA Incident #88"
  >
</p>

Welcome to **Day 6**, where teleporters are broken, tachyons are upset,  
and **you** are somehow the raccoon chosen to “fix” quantum physics.

Today’s scientific objectives include:

- poking dangerous machinery  
- counting reality splits  
- questioning the fabric of spacetime  
- and yelling “WHY IS THIS LEAKING MAGIC SMOKE?!” every 4 seconds

Let’s jump in.

---

## 🧩 Part 1 — “Classical Tachyons and the Great Beam Spaghetti Incident”

A beam moves **straight down** through the manifold.  
It passes through dots (`.`) just fine.

But when it hits a splitter (`^`)?

👉 **The beam stops.**  
👉 **Two new beams spawn**: one going down-left, one down-right.  
👉 Your job is to count **how many total splits happen** before all beams disappear.

It’s basically:

- Plinko  
- but with lasers  
- and absolutely no regard for causality

Every splitter is a raccoon-operated “beam duplicator”  
and yes, they copied the design from a broken vending machine.

---

## 🧩 Part 2 — “Quantum Tachyons and the Multiverse Raccoon Explosion”

NOW we are told:

> “Oh yeah… it’s actually a *quantum* tachyon manifold.”

Which means:

- One particle enters  
- At every splitter, **time itself splits**  
- Each new timeline follows a different path  
- You must count **how many timelines exist at the end**

This is:

- the Many-Worlds Interpretation  
- but specifically the *raccoon edition*  
- where reality forks so often it develops PTSD

Your answer is the **total number of distinct leaf timelines**,  
not the number of beams in one simulation.

---

## 🔧 Project Structure

```
day06/
├── input.txt
├── solution.py
└── README.md
```

---

## ▶️ Running the Solution

```
python3 solution.py
```

Output looks like:

```
Part 1: <split_count>
Part 2: <timeline_count>
```

If Part 2 prints a number larger than the heat death of the universe,  
your raccoon probably forgot a memoization step.

---

## 🧪 Test Suite

We use tests because this puzzle is:

- recursive  
- branching  
- dimensionality‑exploding  
- and capable of accidentally simulating 10⁷⁰ universes

To run tests:

1. Set:

```
RUN_TESTS = True
```

2. Run:

```
python3 solution.py
```

You want:

```
Running tests...
All tests passed!
```

If you DON’T get that:

> a raccoon in another timeline is laughing at you

---

## 🎁 Tiny Example (Multiverse Edition)

A beam goes down.  
It hits a splitter.

Suddenly there are:

- two beams  
- two futures  
- two raccoons  
- twice as many OSHA violations

Repeat this across the whole grid  
and the number of timelines grows faster than raccoons at a dumpster buffet.

---

## 🦝 Built by NickDoesDevOps

Powered by:

- quantum anomalies  
- industrial-strength caffeine  
- duct tape  
- raccoon intuition  

**#NickDoesDevOps • #LearningInPublic • #BuiltInPublic**
