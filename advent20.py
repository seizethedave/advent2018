from itertools import izip_longest, islice, tee

INDENT_STEP = 2

TOKEN_CHARS = {'^', '$', '(', ')', '|'}

def pairwise(s):
    it1, it2 = tee(s)
    return izip_longest(it1, islice(it2, 1, None), fillvalue=None)

def tokenize(input_str):
    pairwise_iter = pairwise(input_str)

    while True:
        char, next_char = next(pairwise_iter)

        if char in TOKEN_CHARS:
            yield char
            if char == "|" and next_char in ")$|":
                # Make parse easier by emitting empty literal between | and ).
                yield ""
        else:
            # Consume and yield string literal.
            buf = [char]
            try:
                while next_char and next_char not in TOKEN_CHARS:
                    buf.append(next_char)
                    char, next_char = next(pairwise_iter)
            except StopIteration:
                # End of input.
                pass
            yield "".join(buf)

class Disjunction(object):
    def __init__(self, options, next_node):
        self.options = options
        self.next = next_node

    def debug_print(self, indent=0):
        print "{}Disjunction:".format(" " * indent)
        print "{}  options:".format(" " * indent)
        for option in self.options:
            option.debug_print(indent + INDENT_STEP + 2)
        if self.next is not None:
            print "{}  next:".format(" " * indent)
            self.next.debug_print(indent + INDENT_STEP + 2)
        else:
            print "{}  next: nil".format(" " * indent)

class Exp(object):
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

    def debug_print(self, indent=0):
        print "{}Exp({})".format(" " * indent, repr(self.value))

        if self.next is not None:
            print "{}  next:".format(" " * indent)
            self.next.debug_print(indent + INDENT_STEP + 2)
        else:
            print "{}  next: nil".format(" " * indent)

class TerminalExp(Exp):
    def __init__(self):
        self.value = None
        self.next = None
    def debug_print(self, indent=0):
        print "{}TERMINAL".format(" " * indent)



def parse_full_expression(input_str):
    stream = pairwise(tokenize(iter(input_str)))
    token, next_token = next(stream)
    assert token == "^"
    return parse_expression(token, next_token, stream)

def parse_expression(token, next_token, stream):
    if next_token == "(":
        return parse_disjunction(stream)
    else:
        return parse_exp(stream)

def parse_disjunction(stream):
    token, next_token = next(stream)
    assert token == "("
    # (A|B)
    options = []

    while next_token != ")":
        print token, next_token
        if next_token is None:
            assert False

        token, next_token = next(stream)
        if token == "|":
            continue
        else:
            options.append(parse_expression(token, next_token, stream))

    return Disjunction(options, parse_expression(token, next_token, stream))

def parse_exp(stream):
    """
    ^EN(W|E)$
    """
    token, next_token = next(stream)
    if token == "$":
        return TerminalExp()
    return Exp(token, parse_expression(token, next_token, stream))

class Backtrack(object):
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "Backtrack({})".format(self.n)

def navigate_exp(exp, offset=0):
    """
    Yields every item in the expression, following disjunctions.
    Backtracks are emitted with an absolute length to return to.
    """
    if exp is None:
        return
    elif isinstance(exp, TerminalExp):
        return
    elif isinstance(exp, Exp):
        for c in exp.value:
            offset += 1
            yield c
        for c in navigate_exp(exp.next, offset):
            yield c
    elif isinstance(exp, Disjunction):
        for ordinal, option in enumerate(exp.options, start=1):
            backtrack_offset = offset
            for c in navigate_exp(option, backtrack_offset):
                backtrack_offset += 1
                yield c
            for c in navigate_exp(exp.next, backtrack_offset):
                yield c
            if ordinal < len(exp.options):
                yield Backtrack(offset)

def go():
    with open("advent20.txt", "r") as input_file:
        input_str = input_file.read()

    #input_str = "^ENWWW(NEEE|SSE(EE|N))$"
    input_str = "^E(S|N)N(W|E)E$"
    exp = parse_full_expression(input_str)
    exp.debug_print()
    for step in navigate_exp(exp):
        print step

def test():
    for expr in [
            "^EN$",
            "^EEW(S|N)WN$",
            #"^E(SS|)E$",
            #"^EN(W|E)$",
            #"^E(S|N)N(W|E)E$",
            #"^(g|)$",
            #"^E(S|W(N|E(S|W)))E$"
            ]:
        print expr
        print list(tokenize(iter(expr)))
        exp = parse_full_expression(expr)
        exp.debug_print()

if __name__ == "__main__":
    test()
    #go()
