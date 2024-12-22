from ssl import VERIFY_ALLOW_PROXY_CERTS
import sys 

from collections import defaultdict

def parse()-> list[int]:
    result : list[int] = []
    for line in sys.stdin:
        result.append(int(line.strip()))
    return result

class Secret:
    def __init__(self, seed: int):
        self.seed: int = seed

    def mix(self, x: int) -> "Secret":
        return Secret(self.seed ^ x)

    def prune(self) -> "Secret": 
        return Secret(self.seed % 16777216)

    def next(self) -> "Secret": 
        next = self.mix(self.seed * 64).prune()
        next = next.mix(next.seed // 32).prune()
        return next.mix(next.seed * 2048).prune()

def sec_num(seed: int, pos: int) -> int:
    sec = Secret(seed)

    for _ in range(pos):
        sec = sec.next()

    return sec.seed

from collections import deque as dq

def changes(seed: int, until: int) -> defaultdict[tuple[int, int, int, int], None | int]:
    freqs: defaultdict[tuple[int, int, int, int], None | int] = defaultdict(lambda: None)
    sec = Secret(seed)

    changes : dq[int] = dq()
    
    for _ in range(3):
        next = sec.next()
        changes.append(next.seed % 10 - sec.seed % 10)
        sec = next

    for _ in range(3, until):
        next = sec.next()
        changes.append(next.seed % 10 - sec.seed % 10)
    
        l = list(changes)
        assert(len(l) == 4)
        if freqs[(l[0], l[1], l[2], l[3])] == None: 
            freqs[(l[0], l[1], l[2], l[3])] = next.seed % 10

        sec = next
        _ = changes.popleft()
    
    return freqs

def main():
    seeds = parse()
    # Part A
    # print(sum(sec_num(seed, 2000) for seed in seeds))

    # Part B
    master: defaultdict[tuple[int, int, int, int], int] = defaultdict(lambda: 0)
    for seed in seeds:
        for k, v in changes(seed, 2000).items():
            if v != None:
                master[k] += v

    max_val : None | int = None
    max_tup : tuple[int, int, int, int] | None = None
    for tup, val in master.items():
        if max_val == None or max_val < val: 
            max_val = val 
            max_tup = tup
    
    print(max_tup)
    print(max_val)
    
if __name__ == "__main__": 
    main()
