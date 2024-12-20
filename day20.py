import sys 
from collections import defaultdict
from tqdm import tqdm

sys.setrecursionlimit(10**6)

def parse():
    result: list[str] = []
    for line in sys.stdin:
        result.append(line.strip())
    
    start = 0, 0
    for i, row in enumerate(result):
        for j, c in enumerate(row):
            if c == 'S': 
                start = i, j
    end = 0, 0
    for i, row in enumerate(result):
        for j, c in enumerate(row):
            if c == 'E': 
                end = i, j


    return result, start, end

def bfs(grid: list[str], frontier: set[tuple[int, int]], visited: set[tuple[int, int]] = set()) -> defaultdict[tuple[int, int], None | int]:
    counter = 0
    distances : defaultdict[tuple[int, int], None | int]= defaultdict(lambda: None)
    while True:
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for node in frontier: 
            distances[node] = counter
        if len(frontier) == 0: 
            counter = None
            break
        visited = visited.union(frontier)
        new_frontier : set[tuple[int, int]] = set()
        for i, j in frontier:
            for di, dj in dirs:
                if 0 <= i + di < len(grid) and 0 <= j + dj < len(grid[0]) and (i + di, j + dj) not in visited:
                    if grid[i + di][j + dj] != '#':
                        new_frontier.add((i + di, j + dj))
                    else:
                        distances[(i + di), (j + dj)] = counter + 1
                        visited.add((i + di, j + dj))
        frontier = new_frontier 
        counter += 1
    return distances

def bfs_walls(grid: list[str], frontier: set[tuple[int, int]], at_most: int, visited: set[tuple[int, int]] = set())-> defaultdict[tuple[int, int], int | None]:
    counter = 0
    result : defaultdict[tuple[int, int], int | None]= defaultdict(lambda: None)
    while True:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if counter > at_most: break
        for node in frontier: result[node] = counter
        visited = visited.union(frontier)
        if len(frontier) == 0: break
        new_frontier: set[tuple[int, int]] = set() 
        for i, j in frontier: 
            for di, dj in dirs:
                if 0 <= i + di < len(grid) and 0 <= j + dj < len(grid[0]) and (i + di, j + dj) not in visited: 
                    new_frontier.add((i + di, j + dj))
        frontier = new_frontier
        counter += 1
    return result

def main():
    grid, start, end = parse()
    walls : list[tuple[int, int]] = []
    ok_cells: list[tuple[int, int]] = []
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == '#': 
                walls.append((i, j))
            elif c == '.' or c == 'E' or c == 'S': 
                ok_cells.append((i, j))

    distances_from_start = bfs(grid, { start })
    distances_from_end = bfs(grid, { end })
    actual = distances_from_start[end]
    if actual == None: 
        raise Exception("There needs to be an actual path from S to E")

    print(f"the actual time is {actual} seconds")
    
    results: defaultdict[int, int] = defaultdict(lambda: 0)
    
    activations : set[tuple[tuple[int, int], tuple[int, int]]]= set()
    for (si, sj) in walls:
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (si + di, sj + dj) in ok_cells:
                activations.add(((si, sj), (si + di, sj + dj)))
    for ((si, sj), (ei, ej)) in tqdm(activations):
        result = distances_from_start[(si, sj)]
        if result == None: continue
        to_add = distances_from_end[(ei, ej)]
        if to_add == None: continue
        result += to_add + 1
        results[result] += 1

    counter = 0
    final = reversed(sorted([(k, v) for k, v in results.items()]))
    for k, v in final:
        # if k < actual: print(f"{v} cheats save {actual - k} picoseconds")
        if k + 100 <= actual: counter += v
    print(f"{counter} many cheats save at least 100 picosends")

    wall_set = set(walls)
    print("Collecting bfs information")
    act_dict: defaultdict[tuple[tuple[int, int], tuple[int, int]], int | None] = defaultdict(lambda: None)
    """for si, sj in ok_cells:
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (si + di, sj + dj) in wall_set:
                for ei, ej in wall_set:
                    for dei, dej in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        if (ei + dei, ej + dej) in ok_cells:
                            if abs(si + di - ei) +\
                                abs(sj + dj - ej) <= 18:
                                d = abs(si + di - ei) +\
                                    abs(sj + dj - ej)
                                prev = act_dict[\
                                    ((ei + dei, ej + dej),\
                                    (si, sj))\
                                ]
                                act_dict[\
                                    (ei + dei, ej + dej),\
                                    (si, sj)\
                                ] = d + 2\
                                    if prev == None\
                                    else min(d + 2, prev) """
    
    print(f"wall set has len {len(wall_set)}")
    print(f"ok set has len {len(ok_cells)}")
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for si, sj in tqdm(ok_cells):
        for ei, ej in ok_cells:
            for dsi, dsj in dirs:
                if (si + dsi, sj + dsj) not in wall_set: continue
                for dei, dej in dirs:
                    if (ei + dei, ej + dej) not in wall_set: continue
                    if abs(si - ei) + abs(sj - ej) <= 20:  # wall to cell should be 20 - 1
                        d = abs(si - ei) + abs(sj - ej)
                        prev = act_dict[((si, sj), (ei, ej))]
                        act_dict[((si, sj), (ei, ej))] = d if prev == None else min(d, prev)

    """ a = set(x for x in act_dict.keys() if act_dict[x] != None)
    b = activations
    print(len(a))
    print(len(b)) """

    # pylint: disable=unused-argument
    def print_grid(grid: list[str], cs: tuple[int, int], ce: tuple[int, int]):
        for i, line in enumerate(grid):
            row: list[str] = []
            for j, c in enumerate(line):
                if (i, j) == cs: row.append('1')
                elif (i, j) == ce: row.append('N')
                else: row.append(c)
            print(''.join(row))
            

    results: defaultdict[int, int] = defaultdict(lambda: 0)
    for (((si, sj), (ei, ej)), d) in tqdm(act_dict.items()):
        if d == None: continue
        result = distances_from_start[(si, sj)]
        if result == None: continue
        to_add = distances_from_end[(ei, ej)]
        if to_add == None: continue
        result += to_add + d
        # if actual - result == 72: 
            # print(f"begin = {(si, sj)}, end = {(ei, ej)}")
            # print_grid(grid, (si, sj), (ei, ej))
            # print()
        results[result] += 1
    counter = 0
    final = reversed(sorted([(k, v) for k, v in results.items()]))
    for k, v in final:
        # #if k < actual: print(f"{v} cheats save {actual - k} picoseconds")
        if k + 100 <= actual: counter += v
    print(f"{counter} many cheats save at least 100 picosends")


if __name__ == "__main__": 
    main()
