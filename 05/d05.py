import operator


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


def get_op_len(code):
    if code in EXIT_OPS:
        op_len = 1
    elif code in IO_OPS:
        op_len = 2
    elif code in JUMP_OPS:
        op_len = 3
    elif code in MATH_OPS:
        op_len = 4
    return op_len


def parse_opcode(code):
    if len(str(code)) <= 2:
        parameters = [0, 0, 0]
        return code, parameters
    else:
        filled = str(code).zfill(5)
        code = int(filled[-2:])
        parameters = reversed(list(map(int, filled[:-2])))
        return code, parameters


def extract_data(params, args, mem):
    data = []
    for p, v in zip(params, args):
        if p:
            data.append(v)
        else:
            data.append(mem[v])
    return data


def apply_math(op, data, args):
    a, b, c = data[0], data[1], args[-1]
    return MATH_OPS[op](a, b), c


def jump(op, op_len, data, ptr):
    if op == 5:
        return data[1] if data[0] else ptr + op_len
    if op == 6:
        return data[1] if not data[0] else ptr + op_len


def perform_io(op, args, inp, mem, ptr):
    if op == 3:
        target_mem = args[-1]
        mem[target_mem] = inp
    elif op == 4:
        print("Output:", mem[mem[ptr+1]])


def run(code, inp):
    mem = code
    ptr = 0
    while mem[ptr] not in EXIT_OPS:
        op, params = parse_opcode(mem[ptr])
        op_len = get_op_len(op)
        args = mem[ptr + 1:ptr + op_len]
        data = extract_data(params, args, mem)
        if op in MATH_OPS:
            res, target = apply_math(op, data, args)
            mem[target] = res
            ptr += op_len
        elif op in IO_OPS:
            perform_io(op, args, inp, mem, ptr)
            ptr += op_len
        elif op in JUMP_OPS:
            ptr = jump(op, op_len, data, ptr)
        else:
            raise ValueError("Opcode {} not supported".format(op))
    return mem

with open("input05", mode='r') as inp5:
    code = list(map(lambda x: int(x), inp5.read().rstrip().split(',')))

print("Day 5 of Advent of Code!")
print("First test...")
run(code[:], 1)
print("Second test...")
run(code[:], 5)
