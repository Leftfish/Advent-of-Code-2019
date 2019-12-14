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

    def get_triplets(self):
        i = 0
        triples = []
        while i < len(self.output):
            triples.append(self.output[i:i+3])
            i += 3
        return triples

    def find_object(self, obj):
        obj_codes = {"PADDLE": 3, "BALL": 4, "SCORE": -1}
        board = self.get_triplets()
        for o in board:
            if obj != "SCORE" and o[2] == obj_codes[obj]:
                x, y = o[0], o[1]
                return x, y
            if obj == "SCORE" and o[0] == -1:
                return o[2], None

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

try:
    with open("input13", mode='r') as inp13:
        prog = list(map(lambda x: int(x), inp13.read().rstrip().split(',')))
except:
    print("File not found")

cmptr = Computer()
cmptr.load_program(prog)
run(cmptr)
blocks = sum([1 for i in range(2,len(cmptr.output),3) if cmptr.output[i] == 2])
print("Day 13 pt 1: ", blocks)


## TODO: implement AI for part 2. play the game until no blocks left.
## each time: it outputs board state, but if triple begins with -1, 0, last part == score
## first input 2    

