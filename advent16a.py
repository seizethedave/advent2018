from advent16_ops import ops

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
    num_good = 0
    for register_before, command, register_after in iter_inputs():
        opcode, args = command[0], command[1:]
        compatible = 0
        for op in ops:
            register = register_before[:]
            op(register, *args)
            if register == register_after:
                compatible += 1
        # print "{} was compatible {} times.".format(command, compatible)
        if compatible >= 3:
            num_good += 1
    print "-->", num_good

if __name__ == "__main__":
    go()
