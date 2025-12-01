# Day 1: Secret Entrance

# Step 1: Read input file
with open("input.txt") as f:
    lines = f.read().strip().splitlines()

position = 50      # dial starts at 50
zero_hits = 0      # how many times we land on 0

for line in lines:
    direction = line[0]       # 'L' or 'R'
    distance = int(line[1:])  # the number after it

    if direction == 'L':
        position = (position - distance) % 100
        pass 
    else:
        position = (position + distance) % 100
        pass

    if position == 0:
        zero_hits += 1

print("Password:", zero_hits)