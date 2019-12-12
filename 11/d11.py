import operator
from collections import defaultdict
from time import sleep

print("Day 11 of Advent of Code!")

def less_than(a, b):
    return 1 if a < b else 0


def equal(a, b):
    return 1 if a == b else 0

MATH_OPS = {
    1: operator.add,
    2: operator.mul,
    7: less_than,
    8: equal
}

IO_OPS = (3, 4)
JUMP_OPS = (5, 6)
EXIT_OPS = (99, )
STEER_OPS = (9, )


def get_op_len(code):
    if code in EXIT_OPS:
        op_len = 1
    elif code in IO_OPS or code in STEER_OPS:
        op_len = 2
    elif code in JUMP_OPS:
        op_len = 3
    elif code in MATH_OPS:
        op_len = 4
    return op_len


def parse_opcode(code):
    if len(str(code)) <= 2:
        params = [0, 0, 0]
        return code, params
    else:
        filled = str(code).zfill(5)
        code = int(filled[-2:])
        params = list(reversed(list(map(int, filled[:-2]))))
        return code, params


def read(mem, cache, args, params, rel_base):
    data = []
    for p, v in zip(params, args):
        # POSITION MODE
        if p == 0:
            try:
                data.append(mem[v])
            except:
                data.append(cache[str(v)])
        # IMMEDIATE MODE
        elif p == 1:
            data.append(v)
        # RELATIVE MODE
        elif p == 2:
            try:
                data.append(mem[rel_base + v])
            except:
                data.append(cache[str(rel_base + v)])
    return data


def write(mem, cache, args, params, rel_base, to_write, op):
    if op == 3:
        write_mode = params[0]
    else:
        write_mode = params[-1]
    # POSITION MODE
    if write_mode == 0:
        target = args[-1]
    # RELATIVE MODE
    elif write_mode == 2:
        target = args[-1] + rel_base
    if target > len(mem):
        cache[str(target)] = to_write
    else:
        mem[target] = to_write


def output_value(mem, cache, args, params, rel_base):
    # POSITION MODE
    if params[0] == 0:
        output = mem[args[-1]]
    # IMMEDIATE MODE
    elif params[0] == 1:
        output = args[-1]
    # RELATIVE MODE
    elif params[0] == 2:
        try:
            output = mem[rel_base + args[-1]]
        except:
            output = cache[str(rel_base + args[-1])]
    return output


def run(code, inp=[0], noun=None,
        verb=None, stop_at_output=False,
        last_ptr=0, last_rel_base=0, debug=False):
    mem = code
    mem[1] = noun if noun else mem[1]
    mem[2] = verb if verb else mem[2]
    cache = defaultdict(int)
    exit_code = 0
    output = inp[-1] if inp else 0
    ptr = last_ptr
    rel_base = last_rel_base

    while mem[ptr] not in EXIT_OPS:
        op, params = parse_opcode(mem[ptr])
        op_len = get_op_len(op)
        args = mem[ptr + 1:ptr + op_len]
        data = read(mem, cache, args, params, rel_base)
        if debug:
            print("Operation: {}\t Data: {}".format(mem[ptr:ptr+op_len], data))
            print("Params: {}\t Args: {}".format(params, args))
            print("Pointer: {}\t Relative base: {}".format(ptr, rel_base))
        if op in MATH_OPS:
            a, b = data[0], data[1]
            to_write = MATH_OPS[op](a, b)
            write(mem, cache, args, params, rel_base, to_write, op)
            ptr += op_len
        elif op == 3:
            if not inp:
                inp = list(map(lambda x: int(x), input("Input: ")))
            to_write = inp.pop(0)
            write(mem, cache, args, params, rel_base, to_write, op)
            ptr += op_len
        elif op == 4:
            output = output_value(mem, cache, args, params, rel_base)
            print("Output: ", output)
            ptr += op_len
            if stop_at_output:
                exit_code = 1
                return output, ptr, exit_code, rel_base
        elif op == 5:
            if data[0]:
                ptr = data[1]
            else:
                ptr += op_len
        elif op == 6:
            if not data[0]:
                ptr = data[1]
            else:
                ptr += op_len
        elif op in STEER_OPS:
            rel_base += data[0]
            ptr += op_len
        else:
            raise ValueError("Opcode {} not supported".format(op))
    return output, ptr, exit_code, rel_base

try:
    with open("input11", mode='r') as inp11:
        prog = list(map(lambda x: int(x), inp11.read().rstrip().split(',')))
except:
    print("File not found")

prog = [3,8,1005,8,330,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,29,2,9,4,10,1006,0,10,1,1103,17,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,61,1006,0,21,1006,0,51,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,89,1,102,19,10,1,1107,17,10,1006,0,18,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1001,8,0,123,1,9,2,10,2,1105,10,10,2,103,9,10,2,1105,15,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,161,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,182,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,205,2,1102,6,10,1006,0,38,2,1007,20,10,2,1105,17,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,241,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,263,1006,0,93,2,5,2,10,2,6,7,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,296,1006,0,81,1006,0,68,1006,0,76,2,4,4,10,101,1,9,9,1007,9,1010,10,1005,10,15,99,109,652,104,0,104,1,21102,825594262284,1,1,21102,347,1,0,1105,1,451,21101,0,932855939852,1,21101,358,0,0,1106,0,451,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,235152649255,1,21101,405,0,0,1105,1,451,21102,235350879235,1,1,21102,416,1,0,1106,0,451,3,10,104,0,104,0,3,10,104,0,104,0,21102,988757512972,1,1,21101,439,0,0,1106,0,451,21102,1,988669698828,1,21101,0,450,0,1106,0,451,99,109,2,22101,0,-1,1,21102,40,1,2,21102,1,482,3,21102,472,1,0,1106,0,515,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,477,478,493,4,0,1001,477,1,477,108,4,477,10,1006,10,509,1101,0,0,477,109,-2,2106,0,0,0,109,4,1202,-1,1,514,1207,-3,0,10,1006,10,532,21102,1,0,-3,21202,-3,1,1,21202,-2,1,2,21102,1,1,3,21102,1,551,0,1106,0,556,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,579,2207,-4,-2,10,1006,10,579,22101,0,-4,-4,1105,1,647,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,598,1,0,1105,1,556,21202,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,617,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,639,21202,-1,1,1,21102,1,639,0,105,1,514,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

directions = ((-1,0,"L"),(0,1,"U"),(1,0,"R"),(0,-1,"D"))
dir_ptr = 0
current = [0, 0]
visited = defaultdict(int)
ptr, rel_base, exit_code = 0, 0, 1

while exit_code == 1:
    c = tuple(current)
    inp = [visited[c]] if c in visited else [0]
    result, ptr, exit_code, rel_base = run(prog,inp=inp,last_ptr=ptr,last_rel_base=rel_base,stop_at_output=True)
    visited[tuple(current)] = result
    result, ptr, exit_code, rel_base = run(prog,inp=inp,last_ptr=ptr,last_rel_base=rel_base,stop_at_output=True)
    if result == 0:
        dir_ptr -= 1
        if dir_ptr < 0: 
            dir_ptr = 3
    else:
        dir_ptr += 1
        if dir_ptr > 3:
            dir_ptr = 0
        
    current[0] += directions[dir_ptr][0]
    current[1] += directions[dir_ptr][1]

print(len(visited))
