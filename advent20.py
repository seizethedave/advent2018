class Disjunction(object):
    def __init__(self, options):
        self.options = options

    def debug_print(self, indent=0):
        print "{}Disjunction:".format(" " * indent)
        for option in self.options:
            option.debug_print(indent + 2)

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
                item.debug_print(indent + 2)
            else:
                print "{}{}".format(" " * (indent + 2), item)

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
            # Avoid Exp(single exp)
            return elements[0]
        else:
            return Exp(elements)

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
