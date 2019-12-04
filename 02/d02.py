print("Day 2 of Advent of Code!")

def is_opcode(code):
    return code == 1 or code == 2 or code == 99

def execute(commands, pos):
    code = commands[pos]
    if is_opcode(code):
        if code == 1:
            a, b, c = commands[pos+1], commands[pos+2], commands[pos+3]
            commands[c] = commands[a] + commands[b]
            return True
        if code == 2:
            a, b, c = commands[pos+1], commands[pos+2], commands[pos+3]
            commands[c] = commands[a] * commands[b]
            return True
        if code == 99:
            return False
    else:
        raise Exception

def parse_commands(commands):
    i = 0
    while True:
        e = execute(commands, i)
        i += 4
        if not e: 
            return commands

def find_input():
    for i in range(100):
        for j in range(100):
            memory = codes[:]
            memory[1], memory[2] = i, j
            try:
                output = parse_commands(memory)[0]
                if output == 19690720: 
                    return 100 * i + j
            except:
                pass


with open("input02", mode = 'r') as inp2:
    codes = [int(code.rstrip()) for code in inp2.read().split(',')]

codes1 = codes[:]
codes1[1], codes1[2] = 12, 2

print("Leftmost command: {}".format(parse_commands(codes1)[0]))
print("100 * verb + noun: ", find_input())