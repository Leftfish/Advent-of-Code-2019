import operator
from collections import defaultdict

print("Day 9 of Advent of Code!")


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
                return output, ptr, exit_code
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
    return output, ptr, exit_code, mem

try:
    with open("input09", mode='r') as inp9:
        prog = list(map(lambda x: int(x), inp9.read().rstrip().split(',')))
except:
    print("File not found")

run(prog, inp=[])
