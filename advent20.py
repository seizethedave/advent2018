INDENT_STEP = 2

class Disjunction(object):
    def __init__(self, options):
        self.options = options

    def debug_print(self, indent=0):
        print "{}Disjunction:".format(" " * indent)
        for option in self.options:
            option.debug_print(indent + INDENT_STEP)

class Exp(object):
    def __init__(self, seq):
        self.seq = seq

    def debug_print(self, indent=0):
        if len(self.seq) == 0:
            print "{}Exp()".format(" " * indent)
            return
        elif len(self.seq) == 1 and isinstance(self.seq[0], str):
            print "{}Exp({})".format(" " * indent, self.seq[0])
            return

        print "{}Exp:".format(" " * indent)

        for item in self.seq:
            if isinstance(item, Exp) or isinstance(item, Disjunction):
                item.debug_print(indent + INDENT_STEP)
            else:
                print "{}{}".format(" " * (indent + INDENT_STEP), item)

    @staticmethod
    def from_stream(stream):
        """
        parses an expression like
            E(SS|)E
        into a nested structure similar to:
            Exp(
                Exp(E)
                Disjunction(
                    Exp(EE),
                    Exp()
                ),
                Exp(E)
            )
        """
        options = []
        this_option = []
        is_disjunction = False

        for c in stream:
            if c == "(":
                # Consume in subexpression.
                subexp = Exp.from_stream(stream)
                if subexp:
                    this_option.append(subexp)
            elif c == ")":
                options.append(this_option)
                break
            elif c == "|":
                is_disjunction = True
                options.append(this_option)
                this_option = []
            elif c == "$":
                this_option.append(c)
            else:
                # Regular ass character.
                if this_option and isinstance(this_option[-1], str):
                    # Compress adjacent regular-ass characters into strings.
                    this_option[-1] += c
                else:
                    this_option.append(c)
        else:
            if this_option:
                options.append(this_option)

        elements = [Exp(seq) for seq in options]

        if is_disjunction:
            return Disjunction(elements)
        elif len(elements) == 1:
            # Avoid Exp([Exp])
            return elements[0]
        else:
            return Exp(elements)

def parse_exp(exp):
    return Exp.from_stream(iter(exp.lstrip("^")))

class Backtrack(object):
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "Backtrack({})".format(self.n)

def navigate_exp(exp, offset=0, backtrack_stack=None):
    """
    Yields every item in the expression, following disjunctions. Backtracks are
    represented with an explicit Backtrack with an absolute offset to return to.
    """
    if backtrack_stack is None:
        backtrack_stack = []

    for item in exp.seq:
        if isinstance(item, str):
            if item == "$":
                # End of input. Process backtracks.
                while backtrack_stack:
                    offset, item, option = backtrack_stack.pop()
                    yield Backtrack(offset)
                    for sub in navigate_exp(option, offset, backtrack_stack):
                        yield sub
            else:
                for c in item:
                    yield c
                offset += len(item)
        elif isinstance(item, Disjunction):
            option_iter = iter(item.options)
            option1 = next(option_iter)

            # Save the rest for later.
            backtrack_stack.extend(
                (offset, item, option) for option in option_iter
            )

            for sub in navigate_exp(option1, offset, backtrack_stack):
                yield sub
        else:
            assert False

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
    #test()
    go()
