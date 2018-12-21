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
