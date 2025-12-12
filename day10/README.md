# Advent of Code 2025 – Day 10  
### *Lights, Buttons, and Raccoons – A Tale of Bitmasks and Finger Soreness*

Welcome to the raccoon‑powered explanation of **Day 10**, where lights blink, buttons flip, and your fingers get sore faster than a raccoon digging through a locked trash bin.

---

## 🧩 Part 1 Summary  

Each machine line contains:  
- A **pattern** like `[.##.]` representing target light states.  
- A set of **button wirings** like `(1,3)` meaning each press toggles those light bits.  
- A final `{jolts}` section we *ignore* in Part 1.

Lights are toggled using XOR logic:  
- Pressing a button applies a bitmask.  
- Pressing twice cancels out.  
- We brute-force all subsets of buttons and find the one matching the target pattern with **minimum presses**.

Raccoon translation:  
> “Try every combination of switches until the lights look right. Try not to electrocute yourself.”

---

## 🧩 Part 2 Summary  

Now the machines switch to **joltage mode**.

- Lights don’t matter anymore.  
- Each button increases specific counters.  
- Counters must match the `{3,5,4,7}` targets.  
- Buttons can be pressed **as many times as needed**.  
- This becomes a tiny integer-linear-system solver.

Raccoon translation:  
> “Mash buttons until the numbers match. Hope the reactor doesn’t explode.”

We solve it with BFS or greedy stepping until all counters reach the target vector.

---

## 🦝 Algorithmic Insights  

- Bitmask operations for Part 1  
- Vector increment search for Part 2  
- Efficient enumeration prevents reactor overheating  
- Commenting code prevents raccoon confusion  

---

## 🏁 Final Answer Logic  

Part 1 and Part 2 are summed separately.  
Your solver prints something like:

```
Part 1: <value>
Part 2: <value>
```

---

## 🎉 Closing Thoughts  

This puzzle teaches:  
- Practical XOR patterns  
- How to turn wiring diagrams into code  
- Why raccoons should NEVER operate nuclear equipment  

Enjoy Day 10. On to Day 11, where everything becomes a graph and the raccoons bring string to represent edges.

