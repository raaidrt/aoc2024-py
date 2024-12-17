import sys

from heapq import heapify, heappop, heappush
from typing import List, Tuple
from collections import defaultdict
import time

def angle(dir):
    match dir:
        case (0, 1):
            return 0
        case (0, -1):
            return 180
        case (1, 0):
            return 90
        case (-1, 0):
            return 270
        case _:
            return 0

def neighbors(grid, node, dir):
    di, dj = dir
    i, j = node
    result = {}
    dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for ndi, ndj in dirs:
        score = 0
        if (i, j) == (-di, -dj):
            score = 2000 
        elif (i, j) == (di, dj):
            continue
        else:
            score = 1000
        result[(node, (ndi, ndj))] = score
    if 0 <= i + di < len(grid) and 0 <= j + dj < len(grid[0]):
        result[((i + di, j + dj), dir)] = 1
    return { ((i, j), (di, dj)): dscore for ((i, j), (di, dj)), dscore in result.items() if grid[i][j] != '#' }

def get_char(dir: Tuple[int, int]):
    match dir:
        case (0, 1):
            return '>'  
        case (0, -1):
            return '<'
        case (1, 0):
            return 'v'
        case (-1, 0):
            return '^'
        case _: 
            return ''

def print_grid(grid, pos, dir):
    i, j = pos 
    s = "\n".join(\
        "".join(\
            (\
             get_char(dir) \
             if (ri, rj) == (i, j) \
             else c) \
            for rj, c in enumerate(row)\
        ) for ri, row in enumerate(grid)\
    )
    print(s)

def dfs_set(parents, node, dir):
    return set().union(*(dfs_set(parents, n, d) for (n, d) in parents[(node, dir)])).union({node})

def main():
    grid = [line.strip() for line in sys.stdin]
    start = (0, 0)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
    end = (0, 0)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "E":
                end = (i, j)
    
    pq : List[Tuple[int, Tuple[int, int], Tuple[int, int]]] = [(0, start, (0, 1))]
    heapify(pq)
    min_costs = defaultdict(lambda: float('inf')) 
    min_costs[(start, (0, 1))] = 0     
    parents = defaultdict(lambda: set())
    while len(pq) > 0:
        best_cost, node, dir = heappop(pq)
        # time.sleep(0.5)
        # print(f"Score = {best_cost}, node = {node}, dir = {dir}")
        # print(f"neighbors = {neighbors(grid, node, dir)}")
        # print_grid(grid, node, dir)
        if min_costs[(node, dir)] < best_cost: continue
        # print(f"popped {node}, {dir}, {best_cost}, neighbors = {neighbors(grid, node, dir)}")
        for (nbor, direction), dscore in neighbors(grid, node, dir).items():
            if min_costs[(nbor, direction)] > best_cost + dscore:
                min_costs[(nbor, direction)] = best_cost + dscore
                parents[(nbor, direction)] = { (node, dir) }
                heappush(pq, (best_cost + dscore, nbor, direction))
            elif min_costs[(nbor, direction)] == best_cost + dscore:
                parents[(nbor, direction)].add((node, dir))
    end_score = min(score for (node, _), score in min_costs.items() if node == end)
    print(end_score)
    
    dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    s = set().union(*(dfs_set(parents, end, d) for d in dirs))
    print(len(s))
    # print(s)

if __name__ == "__main__":
    main()

