import pprint
from advent16_ops import ops

OPCODES = 16

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
    codes = [set(ops) for code in range(OPCODES)]

    for register_before, command, register_after in iter_inputs():
        opcode, args = command[0], command[1:]
        for op in ops:
            register = register_before[:]
            op(register, *args)

            if register != register_after:
                codes[opcode].discard(op)

    final_opcodes = [None] * OPCODES

    # Fixed point algo to figure out opcodes.
    did_change = True

    while did_change:
        did_change = False
        for opcode in range(OPCODES):
            members = codes[opcode]
            if len(members) == 1:
                op = members.pop()
                final_opcodes[opcode] = op
                for other_members in codes:
                    other_members.discard(op)
                did_change = True

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
