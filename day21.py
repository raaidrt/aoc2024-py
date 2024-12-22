import sys 

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
    
    def bfs(self, frontier: set[str], dest: str) -> int | None:
        visited : set[str] = set()
        counter = 0
        while len(frontier) > 0 and dest not in frontier:
            # print(frontier)
            visited = visited.union(frontier)
            new_frontier : set[str] = set()
            for node in frontier:
                new_frontier = new_frontier.union(nbor for nbor in self.transition(node) if nbor not in visited)
            counter += 1
            frontier = new_frontier
        if dest in frontier: 
            return counter  
        else: return None

for l in range(2, 10):
    graph = Lattice([direction] * (l - 1) + [direction])
    start = "A" * (l - 1) + ">"
    end = "A" * (l - 1) + "^"

    print(f"{start} -> {end}, bfs = {graph.bfs({ start }, end)}")

LEVELS: int = 4

def main():
    codes = parse()
    graph = Lattice([direction] * (LEVELS - 1) + [keypad])
    total = 0
    for code in codes:
        num = int(code[:-1])
        init = "A" * LEVELS
        count = 0
        for c in code:
            dest = "A" * (LEVELS - 1) + c
            res = graph.bfs({ init }, dest)
            if res == None: 
                raise Exception(f"Failed for init = {init} dest = {dest} ")
            count += res            
            init = dest
        
        total += num * count
    print(total)

if __name__ == "__main__": 
    main()
