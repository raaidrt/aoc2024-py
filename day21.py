import sys 

keypad = [ "789" ,
                      "456" ,
                      "123 ",
                      ".0A" ]

direction = [".^A",
                        "<v>"]

from collections import defaultdict
from tqdm import tqdm

def parse():
    codes : list[str] = []
    for line in sys.stdin:
        codes.append(line.strip())
    return codes

from copy import deepcopy as dc

def collect_unique_and_in_order(l : list[str]) -> list[str]: 
    if l == []: return ["A"]
    res = [ x for x in l if x[:-2] == "A" * (len(x) - 2) ]
    return [ x[-2] for x in res ]

class Lattice:
    def __init__(self, grids: list[list[str]]): 
        self.maps: list[dict[str, tuple[int, int]]] = []
        self.grids: list[list[str]] = dc(grids)
        # print(self.grids)
        for g in grids:
            d : dict[str, tuple[int, int]] = { }
            for i, row in enumerate(g):
                for j, c in enumerate(row): 
                    d[c] = i, j
            self.maps.append(d)

    def transition(self, curr: str) -> set[str]:
        dirs = { "<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0) }
        result : set[str] = set()
        for move in ["<", ">", "^", "v", "A"]:
            curr = move + curr[1:]
            if move in dirs:
                di, dj = dirs[move]
                i, j = self.maps[1][curr[1]]
                if 0 <= i + di < len(self.grids[1]) and 0 <= j + dj < len(self.grids[1][0]):
                    result.add(move + self.grids[1][i + di][j + dj] + curr[2:])
            else:
                assert(move == "A")

                first_idx_non_a = len(curr)
                for i, c in enumerate(curr):
                    if c == "A": 
                        continue
                    first_idx_non_a = i
                    break

                if first_idx_non_a >= len(curr) - 1:
                    result.add(curr)
                
                if first_idx_non_a < len(curr) - 1:
                    move = curr[first_idx_non_a]
                    di, dj = dirs[move]
                    i, j = self.maps[first_idx_non_a + 1][curr[first_idx_non_a + 1]]
                    if 0 <= i + di < len(self.grids[first_idx_non_a + 1]) and 0 <= j + dj < len(self.grids[first_idx_non_a + 1][0]):
                        result.add(curr[:first_idx_non_a + 1] + self.grids[first_idx_non_a + 1][i + di][j + dj] + curr[first_idx_non_a + 2:])

        result = { s for s in result if "." not in s }
        return result

    
    def bfs(self, frontier: set[str], dest: str) -> list[str] | None:
        visited : set[str] = set()
        frontier_dict: dict[str, list[str]] =  { s : [] for s in frontier }
        while len(frontier_dict) > 0 and dest not in frontier_dict:
            # print(frontier)
            visited = visited.union(frontier_dict.keys())
            new_frontier : dict[str, list[str]] = { }
            for node in frontier_dict:
                for nbor in self.transition(node):
                    if nbor in visited: continue
                    new_frontier[nbor] = dc(frontier_dict[node]) + [ nbor ]
            frontier_dict = new_frontier
        if dest in frontier_dict: 
            return frontier_dict[dest]  
        else: return None

TRY_LEVEL: int = 5
graph = Lattice([direction] * (TRY_LEVEL - 1) + [keypad])

transitions : defaultdict[str, dict[str, list[str]]] = defaultdict(lambda: { })

print(f"Gathering transition information for keypad")
for i, row in tqdm(enumerate(keypad), desc="outer", position=0):
    for j, c in tqdm(enumerate(row), desc="inner", position=1, leave=False):
        for ni, nrow in enumerate(keypad):
            for nj, nc in enumerate(nrow):
                if '.' in { c, nc }: continue
                start = "A" * (TRY_LEVEL - 1) + c
                end = "A" * (TRY_LEVEL - 1) + nc

                res = graph.bfs({ start }, end)
                if res == None: continue
                res = collect_unique_and_in_order(res)
                transitions[c][nc] = res

graph = Lattice([direction] * TRY_LEVEL)
print(f"Gathering transition information for direction board")
for i, row in tqdm(enumerate(direction), desc="outer", position=0):
    for j, c in tqdm(enumerate(row), desc="inner", position=1, leave=False):
        for ni, nrow in enumerate(direction):
            for nj, nc in enumerate(nrow):
                if '.' in { c, nc }: continue
                start = "A" * (TRY_LEVEL - 1) + c
                end = "A" * (TRY_LEVEL - 1) + nc

                res = graph.bfs({ start }, end)
                if res == None: continue

                res = collect_unique_and_in_order(res)
                transitions[c][nc] = res

LEVELS: int = 26

def get_transitions(c: str) -> list[tuple[str, str]]:
    if c == "": return []
    b = c[0]
    result : list[tuple[str, str]]= []
    for x in c[1:]:
        result.append((b, x))
        b = x
    return result


def solve(code: str) -> int:
    t_d: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(lambda: 0))
    code = "A" + code

    # print(f"solving for {code} with transitions {get_transitions(code)}")

    for b, e in get_transitions(code):
        t_d[b][e] += 1


    for _ in tqdm(range(LEVELS)):
        t_d_n: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(lambda: 0))
        for b, next in t_d.items():
            for e, count in next.items():
                l = transitions[b][e]
                for bn, en in get_transitions("A" + ''.join(l)):
                    t_d_n[bn][en] += count
        t_d = t_d_n
    return sum(sum(x.values()) for x in t_d.values())


def main():
    codes = parse()
    total = 0
    print("Solving...")
    for code in tqdm(codes, desc="outer"):
        num = int(code[:-1])
        count = solve(code)
        
        total += num * count
    print(total)

if __name__ == "__main__": 
    main()
