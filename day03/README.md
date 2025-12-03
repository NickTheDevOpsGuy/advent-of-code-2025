# 🎄 Advent of Code 2025 — Day 1: Secret Entrance

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="NES-style snowy pixel art banner with raccoon coder"
    title="NES Snowy Pixel Art Banner"
  >
</p>

Today's challenge answers the age-old holiday question:

> "What if the **entire underground North Pole complex** depended on
> escalators powered by **loose experimental batteries**
> sorted by an elf who definitely failed orientation?"

Welcome to Day 3.

Inside this folder you'll find a clean Python solution for Part 1 and
Part 2 *and* a mini-test suite to keep everything from catching fire
when Future-You decides to "refactor" at 2:13am.

------------------------------------------------------------------------

## 🎅 Story Summary

### 🧩 **Part 1 --- Pick Two Batteries, Don't Die**

You walk into the lobby.
All the elevators are dead.
The escalator is also dead.
The Elf at the console gives you a look that says:

> "I have absolutely no idea how any of this works, but can YOU fix it?"

You get a table of digits.
Each row is a "battery bank."
You must choose **two digits** from each row --- in the **same order**
as they appear --- to create the **largest possible two-digit joltage**
like some kind of festive number-heist.

Example:

    Row:  987654321111111
    Pick: 98
    Why:  Because you have taste

You do this across every row and add them up.
The escalator coughs but does not move.
Standard North Pole engineering.

------------------------------------------------------------------------

### 🧩 **Part 2 --- Now Make It Twelve Digits, Because Elves**

The Elf slaps the **"Joltage Limit Safety Override"** button 14 times.

Suddenly you're told:

> "Actually you need **twelve** digits.
> Yes, from each row.
> Yes, in order.
> Yes, the biggest number you can possibly make.
> Why? ...Look, I don't make the rules."

Now you're essentially:

-   constructing a 12-digit mega-battery
-   one digit at a time
-   using a sliding "choose-the-best-digit-you-can-reach" strategy
-   while a raccoon inside your brain screams about window boundaries

It's delightfully awful.

------------------------------------------------------------------------

## 🔧 Project Structure

``` plaintext
day03/
├── input.txt      # Your personal puzzle input
├── solution.py    # Python solutions (part1, part2, tests)
└── README.md      # This majestic chaos document
```

------------------------------------------------------------------------

## ▶️ Running the Solution

``` bash
python3 solution.py
```

This prints something like:

    Part 1: <number that hopefully isn’t zero>
    Part 2: <ungodly large number that makes your CPU sweat>

------------------------------------------------------------------------

## 🧪 Running the Optional Test Suite

Because Day 3 involves:

-   greedy logic
-   window bounds
-   off-by-one nightmares
-   raccoon-induced hallucinations
-   the number 12

...we added a test suite so you can sanity-check behavior after
"cleanups" that really aren't clean.

Tests are OFF by default.

### 🔄 Turn Them On

Find this at the bottom of `solution.py`:

``` python
RUN_TESTS = False
```

Flip it:

``` python
RUN_TESTS = True
```

Run:

``` bash
python3 solution.py
```

If all goes well:

    Running tests...
    All tests passed!

If a test fails:

-   You get a stack trace
-   You get sadness
-   But also clarity
-   And maybe snacks

Switch back to puzzle mode afterward:

``` python
RUN_TESTS = False
```

------------------------------------------------------------------------

## 🧪 What Our Tests Cover

-   Official example results from the problem
-   Increasing sequences (should take the last 12)
-   Decreasing sequences (should take the first 12)
-   Identical digits (chaos but predictable chaos)
-   Exactly 12 digits
-   13 digits (the brutal edge case)
-   Alternating high-low patterns (stress test)

Basically:
**If you've made a mistake, a test somewhere will bully you about it.**

------------------------------------------------------------------------

## 🎁 Tiny Example Walkthrough

Row:

    234234234234278

Your brain:

> "Ahhhhhgh I have to choose TWELVE digits?!"

Greedy logic:

> "Pick the strongest digit you can reach for slot 1,
> then the next,
> then the next,
> until you've crafted a glorious 12-digit escalator battery
> that would absolutely void its warranty."

Result:

    434234234278

It's weirdly beautiful.

------------------------------------------------------------------------

## 🦝 Built by NickDoesDevOps

Created with ☕, curiosity, and just enough chaos by:

- [![GitHub](https://img.shields.io/badge/GitHub-@NickTheDevOpsGuy-181717?logo=github)](https://github.com/NickTheDevOpsGuy)
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Nicholas%20Clark-0A66C2?logo=linkedin)](https://www.linkedin.com/in/nicholas-a-clark/)
- [![Email](https://img.shields.io/badge/Email-Contact-grey?logo=gmail)](mailto:nicholas.a.clark@outlook.com)

🏷 **#NickDoesDevOps** • **#LearningInPublic** • **#BuiltInPublic**
