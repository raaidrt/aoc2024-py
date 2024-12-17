import sys

def parse():
    register = { }
    program = []
    for line in sys.stdin:
        if line[:8] == "Register": 
            reg = line[9]
            line = line.split(": ")[1]
            register[reg] = int(line.strip())
        elif line[:7] == "Program": 
            line = line.split(": ")[1]
            program = [int(x) for x in line.split(",")]
    return register, program

def get_a(a_values):
    result = 0
    for x in a_values:
        result <<= 3
        result |= x
    return result


def main():
    register, program = parse()
    reversed_program = list(reversed(program))
    def solve(i, stack = []):
        # print(f"trying i = {i}, stack = {stack}")
        if i == len(reversed_program): return { get_a(stack) }
        x = reversed_program[i]
        final = set()
        for candidate in range(8):
            if (candidate ^ 5 ^ 6 ^ (((get_a(stack) << 3) | candidate) >> (candidate ^ 5))) % 8 == x:
                stack.append(candidate)
                result = solve(i + 1, stack)
                if result != None:
                    final = final.union(result)
                stack.pop()
        return final
    
    result = [solve(0, stack=[]) for x in range(7)]
    result = set().union(*result)
    print(min(result))

    
    def trial_runs(result):
        register["A"] = result
        register["B"] = 0
        register["C"] = 0
        # print(register)
        # print(program)

        def combo(x):
            match x:
                case 0 | 1 | 2 | 3: 
                    return x
                case 4 | 5 | 6:
                    return register["ABC"[x - 4]]
                case 7:
                    raise Exception("Reserved Register Called")
        def literal(x):
            return x

        output = []
        pc = [0]
        
        def print_program_state():
            def combo(operand):
                match operand:
                    case 0 | 1 | 2 | 3:
                        return str(operand)
                    case 4 | 5 | 6:
                        return "ABC"[operand - 4]
                    case 7:
                        raise Exception("Reserved Register Call")
            def literal(x):
                return str(x)

            def print_opcode(opcode, operand):
                match opcode:
                    case 0: return "adv " + combo(operand)
                    case 1: return "bxl " + literal(operand)
                    case 2: return "bst " + combo(operand)
                    case 3: return "jnz " + literal(operand)
                    case 4: return "bxc " + "_"
                    case 5: return "out " + combo(operand)
                    case 6: return "bdv " + combo(operand)
                    case 7: return "cdv " + combo(operand)
            
            # print(f"Registers A = {register['A']}, B = {register['B']}, C = {register['C']}")
            # print(f"Out = {output}")
            # print(f"Processing `{print_opcode(program[pc[0]], program[pc[0] + 1])}`")
            

        def consume(opcode, operand):
            match opcode:
                case 0: # Adv
                    register["A"] >>= combo(operand)
                case 1: # Bxl
                    register["B"] ^= literal(operand)
                case 2: # bst
                    register["B"] = combo(operand) % 8
                case 3: # jnz
                    if register["A"] != 0:
                        pc[0] = literal(operand) - 2
                case 4: #bxc
                    register["B"] ^= register["C"]
                case 5: #out
                    output.append(combo(operand) % 8)
                case 6: #bdv
                    register["B"] = register["A"] >> combo(operand)
                case 7: #cdv
                    register["C"] = register["A"] >> combo(operand)

        while 0 <= pc[0] < len(program) - 1:
            # print_program_state()
            opcode, operand = program[pc[0]], program[pc[0] + 1]
            consume(opcode, operand)
            pc[0] += 2
        
        return ','.join(str(x) for x in output)

    

    print(trial_runs(min(result)))

    def print_program():
        def combo(operand):
            match operand:
                case 0 | 1 | 2 | 3:
                    return str(operand)
                case 4 | 5 | 6:
                    return "ABC"[operand - 4]
                case 7:
                    return "Danger![7]"
        def literal(x):
            return str(x)

        def print_opcode(opcode, operand):
            match opcode:
                case 0: return "adv " + combo(operand)
                case 1: return "bxl " + literal(operand)
                case 2: return "bst " + combo(operand)
                case 3: return "jnz " + literal(operand)
                case 4: return "bxc " + "_"
                case 5: return "out " + combo(operand)
                case 6: return "bdv " + combo(operand)
                case 7: return "cdv " + combo(operand)
        
        print("starting at 0")
        for i in range(0, len(program), 2):
            if i + 1 >= len(program): continue
            print(print_opcode(program[i], program[i + 1]))

    print_program()

    
if __name__ == "__main__": 
    main()
