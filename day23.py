import sys 

from collections import defaultdict
from itertools import combinations

import matplotlib.pyplot as plt
from collections import defaultdict


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
    
    edge_freq: defaultdict[int, int] = defaultdict(lambda: 0)
    for n in nodes:
        edge_freq[len(edges[n])] += 1

    # Assuming you have your frequency map like this:
    # freq_map = defaultdict(int)  # Your existing frequency map

    # Convert defaultdict to regular dict for plotting
    dict_data = dict(edge_freq)

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.bar(list(dict_data.keys()), list(dict_data.values()))

    # Customize the plot
    plt.title('Frequency Distribution')
    plt.xlabel('Values')
    plt.ylabel('Frequency')

    # Rotate x-axis labels if needed
    plt.xticks(rotation=45)

    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Show the plot
    plt.show()

    print(f"max degree = {max(edge_freq.keys())}")
    
if __name__  == "__main__": 
    main()
