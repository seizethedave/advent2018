INDENT_STEP = 2

class TokState(object):
    def __init__(self, peekchar):
        self.peekchar = peekchar

TOKEN_CHARS = {'^', '$', '(', ')', '|'}

def tokenize(stream):
    state = TokState(peekchar=None)

    def peek():
        if state.peekchar is None:
            state.peekchar = next(stream)
        return state.peekchar

    def next_char():
        if state.peekchar is not None:
            c = state.peekchar
            state.peekchar = None
            return c
        else:
            return next(stream)

    def read_string():
        buf = []
        try:
            while peek() not in TOKEN_CHARS:
                buf.append(next_char())
        except StopIteration:
            # String is at end of input stream, which is fine.
            pass
        return "".join(buf)

    while True:
        char = next_char()

        if char in TOKEN_CHARS:
            yield char
        else:
            # Consume and yield string literal.
            yield char + read_string()

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
            print "{}  next: (None)".format(" " * indent)

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
            print "{}  next: (None)".format(" " * indent)

    @staticmethod
    def from_stream(stream):
        """
        parses an expression like
            ^E(SS|)E$
        into a nested structure similar to:
            Exp(
                val="e"
                next=Disjunction(
                    options=[
                        Exp(
                            val="SS",
                            next=None
                        ),
                        Exp(
                            val="",
                            next=None
                        )
                    ],
                    next=Exp(
                        val=e,
                        next=None
                    )
                ),
            )
        """
        value = ""
        next_node = None
        options = []

        for c in stream:
            if c == "(":
                next_node = Exp.from_stream(stream)
            elif c == ")":
                next_node = Exp.from_stream(stream)
                break
            elif c == "|":
                if value:
                    options.append(value)
                    value = ""
            elif c == "$":
                next_node = TerminalExp()
            else:
                value += c

        options.append(value)

        elements = [Exp(seq) for seq in options]

        if len(elements) == 0:
            assert False
        elif len(elements) == 1:
            elements[0].next = next_node
            return elements[0]
        else:
            return Disjunction(elements, next_node)

class TerminalExp(Exp):
    def __init__(self):
        self.value = None
        self.next = None
    def debug_print(self, indent=0):
        print "{}TERMINAL".format(" " * indent)

def parse_exp(exp):
    return Exp.from_stream(iter(exp.lstrip("^")))

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
    exp = parse_exp(input_str)
    exp.debug_print()
    for step in navigate_exp(exp):
        print step

def test():
    for expr in [
            "^EN$",
            "^EE|W(S|N)W|N$",
            "^E(SS|)E$",
            "^EN(W|E)$",
            "^E(S|N)N(W|E)E$",
            "^E(S|W(N|E(S|W)))E$"
            ]:
        exp = parse_exp(expr)
        print expr
        exp.debug_print()

if __name__ == "__main__":
    test()
    #go()
