import sys
import re

from functools import cache 

def parse():
    towels: list[str] = []
    patterns: list[str]= []
    for line in sys.stdin:
        if "," in line:
            for x in line.split(","):
                towels.append(x.strip())
        else:
            if line.strip() == "": continue
            patterns.append(line.strip())
    return towels, patterns

def create_re(towels: list[str]):
    return f"({'|'.join(towels)})*"

@cache
def num_combinations(towels: tuple[str], pattern: str, i: int) -> int:
    if i == len(pattern): return 1
    result = 0
    for towel in towels:
        if i + len(towel) <= len(pattern) and pattern[i:i + len(towel)] == towel:
            result += num_combinations(towels, pattern, i + len(towel))
    return result

def main():
    towels, patterns = parse()
    regex = create_re(towels)
    counter = 0
    print(regex)
    for x in patterns:
        result = re.fullmatch(regex, x)
        if result != None:
            counter += 1
    print(counter)

    print("counting combinations")
    result = [num_combinations(tuple(towels), pattern, 0) for pattern in patterns]
    print(sum(result))

    

if __name__ == "__main__": 
    main()
