import sys 

from collections import defaultdict
from itertools import combinations

from tqdm import tqdm

def parse() -> list[list[str]]:
    return [line.strip().split("-") for line in sys.stdin]

def main():
    edges: defaultdict[str, set[str]] = defaultdict(lambda: set())
    parsed = parse()
    
    nodes : set[str] = set()

    for [a, b] in parsed:
        edges[a].add(b)
        edges[b].add(a)
        nodes.add(a)
        nodes.add(b)

    triangles : set[tuple[str, str, str]] = set()
    for [a, b] in parsed:
        inter = edges[a].intersection(edges[b])
        for c in inter:
            l = sorted([a, b, c])
            triangles.add((l[0], l[1], l[2]))

    def chief(tri: tuple[str, str, str]):
        for x in tri:
            if x[0] == "t": return True 
        return False

    chiefs = set(tri for tri in triangles if chief(tri))
    print(len(chiefs))
    
    last_set : set[tuple[str, ...]] = triangles
    next_set: set[tuple[str, ...]] = set()
    for k in tqdm(range(4, len(nodes) + 1)):
        next_set = set()
        for s in last_set:
            inter = nodes.intersection(*(edges[x] for x in s))
            for x in inter:
                l = list(s)
                l.append(x)
                next_set.add(tuple(sorted(l)))
        if len(next_set) == 0: break
        last_set = next_set

    print(last_set)
    elem = list(last_set)[0]
    print(','.join(elem))



if __name__  == "__main__": 
    main()
