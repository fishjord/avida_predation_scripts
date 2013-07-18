#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: create_pred_inserts.py <pred_org_file>"
    sys.exit(1)

grid_x = 251
grid_y = 251

max_preds = 200

fmt = "i InjectGroup {0} {1} -1 -2"
box_pix = 8

num_boxes = 26

change = ((grid_x) / 2) / num_boxes

print "i LoadPopulation seed.spop -1 0 0 0 0 0 1\n"

grid = []
for i in range(grid_y):
    grid.append([False] * grid_x)

for i in range(1, num_boxes):
    box = (change * i, change * i, grid_x - change * i, grid_y - change * i)

    grid[box[0]][box[1]] = True
    grid[box[2]][box[3]] = True

    grid[box[0]][box[3]] = True
    grid[box[2]][box[1]] = True

    grid[box[0]][(box[3] + box[1]) / 2] = True
    grid[box[2]][(box[3] + box[1]) / 2] = True

    grid[(box[2] + box[0]) / 2][box[1]] = True
    grid[(box[2] + box[0]) / 2][box[3]] = True

i = 0
for x in range(grid_x):
    for y in range(grid_y):
        i += 1
        if grid[x][y]:
            print fmt.format(sys.argv[1], i)
