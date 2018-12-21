import operator
import pprint

OPCODES = 16

def addr(REG, a, b, c):
    REG[c] = REG[a] + REG[b]
def addi(REG, a, b, c):
    REG[c] = REG[a] + b
def mulr(REG, a, b, c):
    REG[c] = REG[a] * REG[b]
def muli(REG, a, b, c):
    REG[c] = REG[a] * b
def banr(REG, a, b, c):
    REG[c] = REG[a] & REG[b]
def bani(REG, a, b, c):
    REG[c] = REG[a] & b
def borr(REG, a, b, c):
    REG[c] = REG[a] | REG[b]
def bori(REG, a, b, c):
    REG[c] = REG[a] | b
def setr(REG, a, b, c):
    REG[c] = REG[a]
def seti(REG, a, b, c):
    REG[c] = a
def gtir(REG, a, b, c):
    REG[c] = 1 if a > REG[b] else 0
def gtri(REG, a, b, c):
    REG[c] = 1 if REG[a] > b else 0
def gtrr(REG, a, b, c):
    REG[c] = 1 if REG[a] > REG[b] else 0
def eqir(REG, a, b, c):
    REG[c] = 1 if a == REG[b] else 0
def eqri(REG, a, b, c):
    REG[c] = 1 if REG[a] == b else 0
def eqrr(REG, a, b, c):
    REG[c] = 1 if REG[a] == REG[b] else 0

ops = [
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, gtri, gtrr,
    eqir, eqri, eqrr,
]

def iter_inputs():
    with open("advent16-1.txt", "r") as f:
        while True:
            before = f.readline()
            if not before:
                break
            command = f.readline()
            after = f.readline()
            yield (
                eval(before[8:]),
                tuple(int(c) for c in command.split()),
                eval(after[8:])
            )
            f.readline()

def go():
    codes = {code: set(ops) for code in range(OPCODES)}

    for register_before, command, register_after in iter_inputs():
        opcode, args = command[0], command[1:]
        for op in ops:
            register = register_before[:]
            op(register, *args)

            if register != register_after:
                codes[opcode].discard(op)

    final_opcodes = [None] * OPCODES

    # Fixpoint algo to figure out opcodes.
    did_change = True

    while did_change:
        did_change = False
        for opcode, members in codes.iteritems():
            if len(members) == 1:
                did_change = True
                op = members.pop()
                final_opcodes[opcode] = op
                for other_members in codes.itervalues():
                    other_members.discard(op)

    pprint.pprint(codes)
    pprint.pprint(final_opcodes)

    # Now execute program.

    register_file = [0, 0, 0, 0]

    with open("advent16-2.txt", "r") as program:
        for line in program:
            quad = tuple(int(c) for c in line.split())
            opcode, args = quad[0], quad[1:]
            op = final_opcodes[opcode]
            op(register_file, *args)

    print register_file[0]

if __name__ == "__main__":
    go()
