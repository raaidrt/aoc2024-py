import sys 

from collections import defaultdict

class OpDag:
    def __init__(self):
        self.nodes: set[str] = set()
        self.edges: defaultdict[str, list[str]] = defaultdict(lambda: [])
        self.rev: defaultdict[str, list[str]] = defaultdict(lambda: [])

        self.op_count: int = 0

    def add_op(self, op1: str, op: str, op2: str, rhs: str):
        op_node = f"{op}:{str(self.op_count)}"
        self.nodes = self.nodes.union({op_node, rhs, op1, op2})
        self.edges[rhs].append(op_node)
        self.rev[op_node].append(rhs)
        self.edges[op_node].extend([op1, op2])
        self.rev[op1].append(op_node)
        self.rev[op2].append(op_node)
        self.op_count += 1

    def topsort(self): 
        visited: set[str] = set()
        result: list[str] = [ ]
        def dfs(u: str):
            visited.add(u)
            for v in self.edges[u]:
                if v not in visited: dfs(v)
            result.append(u)

        for u in self.nodes:
            if u not in visited: dfs(u)

        return result

    def wires(self) -> list[str]:
        result : set[str] = set()
        for n in self.nodes:
            if ":" in n: 
                result.add(self.rev[n][0])
        return list(result)

    def eval(self, mapping: defaultdict[str, int]):
        topsorted = self.topsort()
        for u in topsorted:
            if ":" in u:
                [a, _] = u.split(":")
                [op1, op2] = self.edges[u]
                match a.strip():
                    case "OR": 
                        mapping[u] = mapping[op1] | mapping[op2]
                    case "AND": 
                        mapping[u] = mapping[op1] & mapping[op2]
                    case "XOR": 
                        mapping[u] = mapping[op1] ^ mapping[op2]
                    case _:
                        raise Exception(f"Operand {a} not acceptableb")
            else:
                for v in self.edges[u]:
                    mapping[u] = mapping[v]

    def switch(self, wire: str):
        [ op ] = self.edges[wire]
        [ a, b ] = self.edges[op]
        self.edges[op] = [ b, a ]
    
def parse() -> tuple[defaultdict[str, int], OpDag, int] :
    vars : defaultdict[str, int] = defaultdict(lambda: 0)
    dag: OpDag = OpDag()
    num_vars = 0
    with open('_main.txt', 'r', encoding='utf-8') as inp:
        for line in inp:
            if ":" in line: 
                [a, b] = line.strip().split(": ")
                vars[a] = int(b)
                num_vars += 1
            elif "->" in line:
                [lhs, rhs] = line.strip().split(" -> ")
                [op1, op, op2] = lhs.split()
                dag.add_op(op1, op, op2, rhs)
                num_vars += 1

    return vars, dag, num_vars

def format(n: str, x: int):
    if x // 10 == 0:
        return f"{n}0{x}"
    else: 
        return f"{n}{x}"

def get(n: str, mapping: defaultdict[str, int], nv: int) -> int:
    result = 0
    for i in range(nv):
        result |= mapping[format(n, i)] << i
    return result

from copy import deepcopy as dc
import math

def print_bin(x: int, b: int) -> str:
    res : list[str] = []
    for i in range(b - 1, -1, -1):
        res.append(str(x >> i & 1))
    return ''.join(reversed(res))

mapping, dag, num_vars = parse()
new_map = dc(mapping)
dag.eval(new_map)

res = get('z', new_map, num_vars)
print(res)

result : tuple[str, str, str, str] = ("", "", "", "")
total_wires: int = len(dag.wires())
print(f"total wires = {total_wires}, num_combinations = {math.comb(total_wires, 4)}")

def differ_index(a: str, b: str) -> list[int]:
    assert(len(a) == len(b))
    result: list[int] = []
    for i in range(len(a)):
        if a != b:
            result.append(i)
    return result

x = get('x', new_map, num_vars)
print(print_bin(x, 47))
y = get('y', new_map, num_vars)
print(print_bin(y, 47))

z = get('z', new_map, num_vars)
print(print_bin(z, 47))

exp = x + y
print(print_bin(exp, 47))

"""for a, nbors in dag.edges.items():
    for n in nbors:
        print(f"\t{a} --> {n}")"""

differs = differ_index(print_bin(x, 47), print_bin(y, 47))
to_check_swap = set()

visited : set[str] = set()
def add_to_check(u: str):
    if ":" not in u and dag.edges[]:


