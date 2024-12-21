import sys 

from collections import defaultdict

keypad = [ "789" ,
                      "456" ,
                      "123 ",
                      ".0A" ]

direction = [".^A",
                        "<v>"]

def parse():
    codes : list[str] = []
    for line in sys.stdin:
        codes.append(line.strip())
    return codes

from copy import deepcopy as dc

def bfs(grid: list[str], i: int, j: int) -> defaultdict[str, list[str]]: 
    frontier: dict[tuple[int, int], list[str]] = { (i, j): [] }
    visited : set[tuple[int, int]] = set()
    result : defaultdict[str, list[str]] = defaultdict(lambda: [])
    while len(frontier) > 0:
        visited = visited.union(frontier)
        for node, ls in frontier.items(): 
            result[grid[node[0]][node[1]]] = dc(ls)
        new_frontier: dict[tuple[int, int], list[str]] = { }
        for node, ls in frontier.items():
            i, j = node
            for (di, dj), d in {(0, 1):'>', (0, -1):'<', (1, 0):'v', (-1, 0):'^'}.items():
                if not (0 <= i + di < len(grid) and 0 <= j + dj < len(grid[0])): continue 
                if grid[i + di][j + dj] == '.': continue
                if (i + di, j + dj) in visited: continue
                new_frontier[(i + di, j + dj)] = ls + [ d ]
        frontier = new_frontier
    return result
        

def apsp(grid: list[str]) -> defaultdict[str, defaultdict[str, list[str]]]:
    def generate_default_dict() -> defaultdict[str, list[str]]:
        return defaultdict(lambda: [])

    result : defaultdict[str, defaultdict[str, list[str]]] = defaultdict(generate_default_dict)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            result[c] = bfs(grid, i, j)
    return result

def coords(grid: list[str]) -> defaultdict[str, tuple[int, int] | None]:
    result : defaultdict[str, tuple[int, int] | None]= defaultdict(lambda: None)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            result[c] = i, j
    return result

def directions(pad: list[str], code: str): 
    curr = "A"
    dirs = apsp(pad)

    seq: list[str] = []
    for c in code:
        d = dirs[curr][c]

        seq.append(''.join(d))
        seq.append("A")
        curr = c

    return ''.join(seq)


def main():
    codes = parse()
    
    total = 0
    for code in codes:
        num = int(code[:-1])

        dirs = directions(keypad, code)
        print(dirs)
        dirs = directions(direction, dirs)
        print(dirs)
        dirs = directions(direction, dirs)
        print(dirs)
        dirs = directions(direction, dirs)
        print(dirs)

        total += num * len(dirs)

    print(total)

if __name__ == "__main__": 
    main()
