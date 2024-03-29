import operator
from collections import defaultdict

class Computer():
    def __init__(self):
        self.memory = [0] * 10000
        self.ptr = 0
        self.rel_base = 0
        self.input = []
        self.output = []

    def __repr__(self):
        status = ''
        status += "Pointer: {}\n".format(self.ptr)
        status += "Relative base: {}\n".format(self.rel_base)
        status += "InStream: {}\n".format(self.input)
        status += "Output: {}\n".format(self.output)
        status += "Next op: {}\n".format(self.memory[self.ptr])
        return status

    def load_program(self, code):
        for i in range(len(code)):
            self.memory[i] = code[i]

    def reset(self):
        self.memory = [0] * 10000
        self.ptr = 0
        self.rel_base = 0
        self.input = []
        self.output = []

    def set_input(self, inp):
        self.input.append(inp)

    def _parse_opcode(self, code):
        if len(str(code)) <= 2:
            params = [0, 0, 0]
            return code, params
        else:
            filled = str(code).zfill(5)
            code = int(filled[-2:])
            params = list(reversed(list(map(int, filled[:-2]))))
            return code, params

    def _get_data(self, params, args):
        data = []
        for p, v in zip(params, args):
            if p == 0: # POSITION MODE
                data.append(self.memory[v])
            elif p == 1: # IMMEDIATE MODE
                data.append(v)
            elif p == 2: # RELATIVE MODE
                data.append(self.memory[self.rel_base + v])
        return data

    def _get_write_addr(self, op, params, args):
        write_mode = params[0] if op == 3 else params[-1]
        if write_mode == 0: # POSITION MODE
            target = args[-1]
        elif write_mode == 2: # RELATIVE MODE
            target = args[-1] + self.rel_base
        return target
    
    def _get_op_len(self, code):
        op_len = 1
        if code in (3, 4, 9):
            op_len = 2
        elif code in (5, 6):
            op_len = 3
        elif code in (1, 2, 7, 8):
            op_len = 4
        return op_len

def run(c, noun=None, verb=None, debug=False, stop_output=False):
    if noun:
        c.memory[1] = noun
    if verb:
        c.memory[2] = verb
    
    while c.memory[c.ptr] != 99:
        op, params = c._parse_opcode(c.memory[c.ptr])
        op_len = c._get_op_len(op)
        args = c.memory[c.ptr + 1:c.ptr + op_len]
        data = c._get_data(params, args)
        exit_code = 0

        if debug: print("Operation: ", c.memory[c.ptr:c.ptr+op_len], "ptr", c.ptr, "rb", c.rel_base)
        if op == 1: # ADD
            target = c._get_write_addr(op, params, args)
            c.memory[target] = data[0] + data[1]
            c.ptr += op_len
        if op == 2: # MULTIPLY
            target = c._get_write_addr(op, params, args)
            c.memory[target] = data[0] * data[1]
            c.ptr += op_len
        if op == 3: # INPUT
            target = c._get_write_addr(op, params, args)
            try:
                inp = c.input.pop(0)
            except:
                inp = int(input("?: "))
            c.memory[target] = inp
            c.ptr += op_len
        if op == 4: # OUTPUT
            if debug: print("Output: ", data[0])
            c.output.append(data[0])
            c.ptr += op_len
            if stop_output: 
                exit_code = 1
                break
        if op == 5: # JUMP IF TRUE
            if data[0]:
                c.ptr = data[1]
            else:
                c.ptr += op_len
        if op == 6: # JUMP IF FALSE
            if not data[0]:
                c.ptr = data[1]
            else:
                c.ptr += op_len
        if op == 7: # LESS THAN
            target = c._get_write_addr(op, params, args)
            if data[0] < data[1]:
                c.memory[target] = 1
            else:
                c.memory[target] = 0
            c.ptr += op_len
        if op == 8: # EQUALS
            target = c._get_write_addr(op, params, args)
            if data[0] == data[1]:
                c.memory[target] = 1
            else:
                c.memory[target] = 0
            c.ptr += op_len
        if op == 9: # CHANGE REL BASE
            c.rel_base += data[0]
            c.ptr += op_len
    return exit_code

def paint(computer, directions, dir_ptr, current, visited, exit_code):
    while True:
        c = tuple(current)
        inp = visited[c] if c in visited else 0
        cx.set_input(inp)
        exit_code = run(cx,stop_output=True)
        if exit_code == 0: break
        result = cx.output.pop(0)
        visited[tuple(current)] = result
        exit_code = run(cx,stop_output=True)
        if exit_code == 0: break
        result = cx.output.pop(0)
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

def paint_sign(visited):
    xs = [a[0] for a in visited]
    ys = [a[1] for a in visited]
    table_x = abs(max(xs)) + abs(min(xs)) + 1
    table_y = abs(max(ys)) + abs(min(ys)) + 1
    table = [[' ' for i in range(table_x)] for j in range(table_y)]

    for k in visited:
        x = k[0]
        y = k[1] - 1
        if visited[k] == 1:
            table[y][x] = '#'

    for i in range(len(table)):
        print(i, "->", "".join(table[i]))


try:
    with open("input11", mode='r') as inp11:
        prog = list(map(lambda x: int(x), inp11.read().rstrip().split(',')))
except:
    print("File not found")


cx = Computer()
cx.load_program(prog)

directions = ((-1,0,"L"),(0,1,"U"),(1,0,"R"),(0,-1,"D"))
dir_ptr = 1
current = [0, 0]
visited = defaultdict(int)
visited[(0,0)] = 0
exit_code = 1

paint(cx, directions, dir_ptr, current, visited, exit_code)
print("Day 11 pt. 1: ", len(visited))

cx.reset()
cx.load_program(prog)
dir_ptr = 1
current = [0, 0]
visited = defaultdict(int)
visited[(0,0)] = 1
exit_code = 1

paint(cx, directions, dir_ptr, current, visited, exit_code)
print("Day 11 pt. 2:")
paint_sign(visited)

