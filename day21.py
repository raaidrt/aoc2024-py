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

def coords(grid: list[str]) -> defaultdict[str, tuple[int, int] | None]:
    result : defaultdict[str, tuple[int, int] | None]= defaultdict(lambda: None)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            result[c] = i, j
    return result

def directions(pad: list[str], code: str): 
    cmap = coords(pad)
    curr = "A"

    seq: list[str] = []
    for c in code:
        res = cmap[c]
        if res is None: 
            raise Exception("Missing map")
        i, j = res
        res = cmap[curr]
        if res is None: 
            raise Exception("Missing map")
        ci, cj = res
        hori = ">"
        if j < cj:
            hori = "<"
        vert = "v"
        if i < ci:
            vert = "^"
        
        s = ""
        v_seq = vert * abs(i - ci)
        h_seq = hori * abs(j - cj)

        if len(pad) == 4:
            match (hori, vert):
                case ("<", "^"): 
                    s = v_seq + h_seq
                case (">", "v"): 
                    s = h_seq + v_seq
                case _:
                    s = h_seq + v_seq
        elif len(pad) == 2:
            match (hori, vert):
                case (">", "^"): 
                    s = h_seq + v_seq
                case ("<", "v"): 
                    s = v_seq + h_seq
                case _:
                    s = h_seq + v_seq

        seq.append(s)
        seq.append("A")
        curr = c

    return ''.join(seq)

def verify(grid: list[str], moves: str) -> str:
    result : list[str] = []
    cmap: dict[str, tuple[int, int]] = { }
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            cmap[c] = i, j
    curr = "A"
    dirs = { ">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0) }
    for move in moves:
        if move == "A": 
            result.append(curr)
        else:
            di, dj = dirs[move]
            i, j = cmap[curr]
            curr = grid[i + di][j + dj]
    return ''.join(result)

def check(levels: int, moves: str) -> str:
    for level in range(levels):
        grid = direction
        if level == levels - 1:
            grid = keypad
        
        moves = verify(grid, moves)
        print(f"\t level = {level} verification = {moves}")
    return moves

DEBUG: bool = True
def dp(x):
    if DEBUG:
        print(x)

print(f"verification for 379A = {check(3, '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A')}")

def main():
    codes = parse()
    
    total = 0
    for code in codes:
        num = int(code[:-1])
        
        dp(f"processing code {code}")
        dirs = directions(keypad, code)
        dp(dirs)
        print(f"verification {check(1, dirs)}")
        dirs = directions(direction, dirs)
        dp(dirs)
        print(f"verification {check(2, dirs)}")
        dirs = directions(direction, dirs)
        dp(dirs)

        print(f"verification {check(3, dirs)}")
        
        dp("")

        total += num * len(dirs)

    print(total)

if __name__ == "__main__": 
    main()
