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
