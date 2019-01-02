class Disjunction(object):
    def __init__(self, options):
        self.options = options

    def debug_print(self, indent):
        print " " * indent, "Disjunction:"
        for option in self.options:
            option.debug_print(indent + 1)

class Exp(object):
    def __init__(self, seq):
        self.seq = seq

    def debug_print(self, indent=0):
        if len(self.seq) == 0:
            print " " * indent, "Exp()"
            return
        elif len(self.seq) == 1 and isinstance(self.seq[0], str):
            print " " * indent, "Exp({})".format(self.seq[0])
            return

        print " " * indent, "Exp:"

        for item in self.seq:
            if isinstance(item, Exp) or isinstance(item, Disjunction):
                item.debug_print(indent + 1)
            else:
                print " " * (indent + 1), item

    @staticmethod
    def from_stream(stream):
        """
        parses an expression like
            E(SS|)E
        into a nested structure similar to:
            Exp(
                Exp('E')
                Junction(
                    Exp('EE'),
                    Exp()
                ),
                Exp('E')
            )
        """
        options = []
        this_option = []
        is_disjunction = False

        for c in stream:
            if c == "(":
                if this_option:
                    options.append(this_option)
                this_option = []
                # Consume in subexpression.
                subexp = Exp.from_stream(stream)
                if subexp:
                    options.append(subexp)
            elif c == ")":
                options.append(this_option)
                break
            elif c == "|":
                is_disjunction = True
                options.append(this_option)
                this_option = []
            else:
                # Regular ass character.
                this_option.append(c)
        else:
            if this_option:
                options.append(this_option)

        elements = [Exp("".join(seq)) if isinstance(seq, list) else seq for seq in options]
        return Disjunction(elements) if is_disjunction else Exp(elements)


def parse_exp(exp):
    return Exp.from_stream(
        iter(
            exp.lstrip("^").rstrip("$")
        )
    )

def go():
    with open("advent20.txt", "r") as input_file:
        input_str = input_file.read()

    input_str = input_str.lstrip("^").rstrip("$")
    exp = Exp.from_string(iter(input_str))


def test():
    #navigate_expr("^EEN$")
    #navigate_expr("^EEEEEN$")
    #print list(navigate_expr("^E(S|W)N$"))
    #print list(navigate_expr("^E(S|W(N|E(S|W)))E$"))

    for expr in ["^E(SS|)E$", "^EN(W|E)$", "^E(S|N)N(W|E)$", "^E(S|W(N|E(S|W)))E$"]:
        exp = parse_exp(expr)
        print expr
        exp.debug_print()

if __name__ == "__main__":
    test()
    #go()
