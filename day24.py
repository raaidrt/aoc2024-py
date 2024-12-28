from collections import defaultdict
from itertools import combinations
from tqdm import tqdm

NUM_VARS = 46

import sys

def pprint(msg: str | None = None):
    print(f"Line No: {sys._getframe().f_back.f_lineno}: {msg if msg is not None else ''}")

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

    def eval(self, mapping: defaultdict[str, int | None]) -> bool:
        topsorted = self.topsort()
        for u in topsorted:
            if ":" in u:
                [a, _] = u.split(":")
                [op1, op2] = self.edges[u]
                first, second = mapping[op1], mapping[op2]
                if first is None or second is None: return False
                match a.strip():
                    case "OR": 
                        mapping[u] = first | second
                    case "AND": 
                        mapping[u] = first & second
                    case "XOR": 
                        mapping[u] = first ^ second
                    case _:
                        raise Exception(f"Operand {a} not acceptableb")
            else:
                for v in self.edges[u]:
                    mapping[u] = mapping[v]
        return True

    def switch(self, wire1: str, wire2: str):
        [ op1 ] = self.edges[wire1]
        [ op2 ] = self.edges[wire2]

        self.edges[wire1] = [op2]
        self.edges[wire2] = [op1]
        self.rev[op1] = [wire2]
        self.rev[op2] = [wire1]

    def pprint_subgraph(self, start: str):
        affected: set[str] = set()
        def dag_add(u: str):
            affected.add(u)
            for v in self.edges[u]:
                dag_add(v)
        dag_add(start)
        for u in self.nodes:
            if u not in affected: continue
            for v in self.edges[u]:
                pprint(f"\t{u} --> {v}")

    
def parse() -> tuple[defaultdict[str, int | None], OpDag, int] :
    vars : defaultdict[str, int | None] = defaultdict(lambda: None)
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

def inputs(x: int, y: int) -> defaultdict[str, int | None]:
    result: defaultdict[str, int | None] = defaultdict(lambda: None)
    bits_x: list[int] = []
    for i in range(NUM_VARS - 1):
        bits_x.append((x >> i) & 1)
    bits_y: list[int] = []
    for i in range(NUM_VARS - 1):
        bits_y.append((y >> i) & 1)
    
    for i, xb in enumerate(bits_x):
        result[format('x', i)] = xb
    for i, yb in enumerate(bits_y):
        result[format('y', i)] = yb

    return result

def get(n: str, mapping: defaultdict[str, int | None], nv: int) -> int:
    result = 0
    for i in range(nv):
        bit = mapping[format(n, i)]
        if bit is None:
            bit = 0
        result |= bit << i
    return result

from copy import deepcopy as dc

def print_bin(x: int, b: int) -> str:
    res : list[str] = []
    for i in range(b - 1, -1, -1):
        res.append(str(x >> i & 1))
    return ''.join(reversed(res))


def differ_index(a: str, b: str) -> set[str]:
    assert(len(a) == len(b))
    result: set[str] = set()
    for i in range(len(a)):
        if a[i] != b[i]:
            result.add(format('z', i))
    return result

def solve(mapping: defaultdict[str, int | None], dag: OpDag) -> set[str] | None:
    success = dag.eval(mapping)
    if not success: return None 
    x = get('x', mapping, NUM_VARS)
    y = get('y', mapping, NUM_VARS)
    z = get('z', mapping, NUM_VARS)
    exp = x + y
    return differ_index(print_bin(z, NUM_VARS), print_bin(exp, NUM_VARS))

def solve_exp(d: defaultdict[str, int | None], dag: OpDag) -> set[str]:
    res = solve(d, dag)
    if res is None:
        raise Exception("Too bad")
    return res

def check_swaps(dag: OpDag, differ_sets: list[set[str]]) -> set[str]:
    to_check_swap : set[str] = set() # the candidates for swapping
    visited : set[str] = set() # visited nodes
    def add_to_check(u: str):
        if ":" not in u and len(dag.edges[u]) == 1 and ":" in dag.edges[u][0]:
            to_check_swap.add(u)
        visited.add(u)
        for v in dag.edges[u]:
            add_to_check(v)
    for u in dag.nodes:
        if u not in visited and any(u in s for s in differ_sets):  
            add_to_check(u)

    return to_check_swap

def get_affected_wire_outputs(dag: OpDag, differs: set[str]) -> set[str]:
    visited: set[str] = set()
    res: set[str] = set()
    def dag_dfs(u: str):
        if len(dag.edges[u]) == 1 and ":" in dag.edges[u][0]:
            res.add(u)
        visited.add(u)
        for v in dag.edges[u]:
            if v not in visited: dag_dfs(v)
    
    for u in dag.nodes:
        if u not in visited and u in differs: dag_dfs(u)

    return res

mapping, dag, num_ops = parse()

NUM_ADDITIONAL_TEST_CASES = 10

testcases = [
    (1 << 44, 1 << 44), 
    (0, 0),
    (get('x', mapping, NUM_VARS), get('y', mapping, NUM_VARS))
]

from random import randint as ri

def large(v: int) -> int:
    res: int = 0
    for i in range(v):
        res |= 1 << i

    return res

for _ in range(NUM_ADDITIONAL_TEST_CASES): 
    testcases.append((ri(0, large(NUM_VARS)), ri(0, large(NUM_VARS))))

mappings=  [inputs(x, y) for x, y in testcases]

differs = [
    solve_exp(mapping, dag) for mapping in mappings
]

affected_wire_outputs = [get_affected_wire_outputs(dag, differ) for differ in differs]
combined_affected : set[str] = set().union(*affected_wire_outputs)

dag.switch('nnt', 'gws')
dag.switch('npf', 'z13')
dag.switch('cph', 'z19')
dag.switch('hgj', 'z33')


def is_xor_of(u: str, dag: OpDag, i: int) -> bool:
    [xor_node] = dag.edges[u]
    if not ":" in xor_node or xor_node.split(":")[0].strip() != "XOR":
        return False
        
    [a, b] = dag.edges[xor_node]
    return { a, b } == { format('x', i), format('y', i) }

def is_and_of(u: str, dag: OpDag, i: int) -> bool:
    [and_node] = dag.edges[u]
    if not ":" in and_node or and_node.split(":")[0].strip() != "AND":
        return False
        
    [a, b] = dag.edges[and_node]
    return { a, b } == { format('x', i), format('y', i) }

for i in range(2, NUM_VARS - 1):
    pprint(f"Checking state {i}")
    if len(dag.edges[format('z', i)]) != 1:
        pprint(f"No xor assignment here\n")
        continue
    [xor_node] = dag.edges[format('z', i)]
    if ":" not in xor_node or xor_node.split(":")[0].strip() != "XOR":
        pprint(f"XOR node not present\n")
        continue
    [a, b] = dag.edges[xor_node]
    other = a
    if is_xor_of(a, dag, i):
        other = b
    elif not is_xor_of(b, dag, i):
        pprint(f"No node calculates XOR of current guy, a = {a}, b = {b}\n")
        continue
    
    if len(dag.edges[other]) != 1:
        pprint(f"No or assignment here for other = {other} dag.edges[other] = {dag.edges[other]}\n")
        continue
    [or_node] = dag.edges[other]
    
    if not ":" in or_node or or_node.split(":")[0].strip() != "OR": 
        pprint(f"OR node not present\n")
        continue 

    [a, b] = dag.edges[or_node]
    other = a
    if is_and_of(a, dag, i - 1):
        other = b
    elif not is_and_of(b, dag, i - 1): 
        pprint(f"No node calculates AND of last guy\n")
        continue

    if len(dag.edges[other]) != 1: 
        pprint(f"No and assignment here")
        continue
    [and_node] = dag.edges[other]

    if not ":" in and_node or and_node.split(":")[0].strip() != "AND":  
        pprint(f"AND node not present calculating AND of last two carry accumulators\n")
        continue 
    [a, b] = dag.edges[and_node]
    
    if len(dag.edges[format('z', i - 1)]) != 1:
        pprint(f"Last node does not have an XOR at top level\n")
        continue 
    [xor_last] = dag.edges[format('z', i - 1)]
    if ":" not in xor_last or xor_last.split(":")[0].strip() != "XOR": 
        pprint(f"Last node does not have an XOR at top level\n")
        continue 
    [last_1, last_2] = dag.edges[xor_last]
    if { a, b } != { last_1, last_2 }: 
        pprint(f"We don't use last operation's binary operands in this operation\n")

final_list = ['nnt', 'gws', 'npf', 'z13', 'cph', 'z19', 'hgj', 'z33']
final_list.sort()
print(','.join(final_list))
