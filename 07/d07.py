import operator
from itertools import permutations

print("Day 6 of Advent of Code!")


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
        if inp:
            mem[target_mem] = inp.pop(0)
        else:
            mem[target_mem] = int(input("Input: "))
        return 0
    elif op == 4:
        output = mem[mem[ptr+1]]
        return output


def run(code, inp=[0], noun=None,
        verb=None, stop_at_output=False,
        last_ptr=0, debug=False):
    mem = code
    output = inp[-1]
    exit_code = 0
    if noun:
        code[1] = noun
    if verb:
        code[2] = verb
    ptr = last_ptr
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
            output = perform_io(op, args, inp, mem, ptr)
            if op == 4 and debug:
                print("Output:", output, "From opcode:", op)
            ptr += op_len
            if stop_at_output and op == 4:
                exit_code = 1
                return output, ptr, exit_code
        elif op in JUMP_OPS:
            ptr = jump(op, op_len, data, ptr)
        else:
            raise ValueError("Opcode {} not supported".format(op))
    return output, ptr, exit_code


def run_test(prog, mode, inp=0, debug=False):
    inputs = [mode, inp]
    output = run(prog, inputs, debug=debug)
    return output


def run_set(prog, settings, debug=False):
    results = []
    for setting in settings:
        inp = 0
        for mode in setting:
            out = run_test(prog[:], mode, inp, debug=debug)[0]
            inp = out
        results.append(out)
    return max(results)


def run_feedback_test(no_amplifiers, prog, settings, debug=False):
    amplifiers = list(zip([prog[:]] * no_amplifiers, settings))
    pointers = [0 for i in range(no_amplifiers)]
    inputs = [[] for i in range(no_amplifiers)]
    inp = 0

    for i in range(len(amplifiers)):
        inputs[i].append(amplifiers[i][1])

    while True:
        for i in range(len(amplifiers)):
            inputs[i].append(inp)
            result, pointers[i], exit_code = run(amplifiers[i][0],
                                                 inputs[i],
                                                 stop_at_output=True,
                                                 last_ptr=pointers[i],
                                                 debug=debug)
            inp = result
            if exit_code == 0 and i == len(amplifiers) - 1:
                return result


def run_feedback_set(no_amplifiers, prog, settings):
    results = []
    for mode in settings:
        out = run_feedback_test(no_amplifiers, prog, mode)
        results.append(out)
    return max(results)

try:
    with open("input07", mode='r') as inp7:
        prog = list(map(lambda x: int(x), inp7.read().rstrip().split(',')))
except:
    print("File not found")

settings = list(permutations(range(5)))
print(run_set(prog, settings))

settings = list(permutations(range(5, 10)))
print(run_feedback_set(5, prog, settings))
