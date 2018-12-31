import advent16_ops

ops = {op.__name__: op for op in advent16_ops.ops}

def iter_inputs():
    """
    Yields one instruction register, followed by a series of (op_fn, (arg1, arg2, arg3)) tuples.
    """
    with open("advent19.txt", "r") as f:
        yield int(next(f).rstrip("\n")[-1])

        for line in f:
            op_str, args_str = line.rstrip("\n").split(" ", 1)
            yield ops[op_str], tuple(int(a) for a in args_str.split(" "))

def interpret(instruction_register, instructions):
    register_file = [0, 0, 0, 0, 0, 0]
    instruction_pointer = 0

    while True:
        register_file[instruction_register] = instruction_pointer

        try:
            op, (a1, a2, a3) = instructions[instruction_pointer]
        except IndexError:
            break # Halt.

        op(register_file, a1, a2, a3)
        instruction_pointer = register_file[instruction_register]
        # print (instruction_pointer, op.__name__, (a1, a2, a3), register_file)

        instruction_pointer += 1

    return register_file

def go():
    input_stream = iter_inputs()
    reg = interpret(next(input_stream), list(input_stream))
    print reg[0]

if __name__ == "__main__":
    go()
