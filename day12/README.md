# 🎄 Advent of Code 2025 – Day 11  

<p align="left">
  <img 
    src="../assets/adventOfCode2025.png"
    width="800"
    alt="A raccoon confidently repairing a teleporter he absolutely should NOT touch"
    title="Quantum OSHA Incident #88"
  >
</p>

### *Graph Paths, Server Racks, and Raccoons with Ethernet Cables*

Welcome to **Day 11**, where a million devices form a giant digital spaghetti mess and you must trace every possible path **from one node to another**.

---

## 🧩 Part 1 – Count Every Path  

You are looking for all possible directed paths from:

```
you → out
```

Each line in the input describes connections:

```
aaa: you hhh
you: bbb ccc
```

This forms a **directed acyclic graph**.

Your job:  
Count *every possible* path from `"you"` to `"out"`.

DFS + memoization does the trick.

Raccoon translation:  
> “Start at YOU. Run along every wire. If you fall off the table, that's a valid path only if it ends in OUT.”

---

## 🧩 Part 2 – Paths that Pass Through dac AND fft  

Now they want **all paths from `svr` to `out`**,  
but only those paths that visit BOTH:

```
dac
fft
```

Order doesn’t matter.  
Just visit both at some point in the path.

You track two flags:  
- `seen_dac`  
- `seen_fft`

Only count the path when **both are true at OUT**.

Raccoon translation:  
> “Find every cable route from the server to the reactor that passes by the noisy blue box AND the humming red box. Very important. Very dangerous. Very fun.”

---

## 🦝 Algorithmic Insights  

- DFS is your best friend  
- Memoization helps for Part 1  
- Cycle protection is needed for Part 2  
- Raccoons love recursion (and cables)

---

## 🎉 Final Notes  

This puzzle reinforces:  
- Graph traversal  
- Flag tracking  
- Avoiding infinite loops  
- Maintaining raccoon focus in large wirespaces  

---

Enjoy Day 11. And hide your Ethernet cables. The raccoons are learning too much.

