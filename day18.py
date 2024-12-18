import sys
from tqdm import tqdm

def parse() -> list[tuple[int, int]]:
    result = []
    for line in sys.stdin:
        i, j = line.split(",")
        result.append((int(i), int(j)))
    return result

                    
def bfs(corrupted: list[list[bool]], frontier: set[tuple[int, int]], end: tuple[int, int], visited: set[tuple[int, int]] = set()) -> int | None:
    if end in frontier: return 0
    elif len(frontier) == 0: return None
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    next_frontier: set[tuple[int, int]] = set()
    for i, j in frontier:
        next_frontier = next_frontier.union(set((i + di, j + dj) for di, dj in dirs if 0 <= i + di < len(corrupted) and 0 <= j + dj < len(corrupted[0]) and not corrupted[i + di][j + dj] and (i + di, j + dj) not in visited))
    result = bfs(corrupted, next_frontier, end, visited.union(next_frontier))
    if result != None:
        return result + 1
    return None

def main():
    dims = (71,71)
    attack = parse()
    (rows, cols) = dims
    fallen = 1024
    corrupted = [[False for  _ in range(cols)] for _ in range(rows)]
    for i in range(fallen):
        corrupted[attack[i][0]][attack[i][1]] = True
    result = bfs(corrupted, { (0, 0) }, (rows - 1, cols - 1))
    print(result)
    
    result = 0, 0
    for i in tqdm(range(fallen, len(attack))):
        corrupted[attack[i][0]][attack[i][1]] = True
        result = bfs(corrupted, { (0, 0) }, (rows - 1, cols - 1))
        if result == None:
            result = attack[i][0], attack[i][1]
            break
    print(result)

if __name__ == "__main__": 
    main()
