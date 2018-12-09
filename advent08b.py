class Node(object):
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    @property
    def value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            return sum(
                self.children[meta - 1].value
                for meta in self.metadata
                if 1 <= meta <= len(self.children) 
            )

    @classmethod
    def from_stream(cls, stream):
        num_children = next(stream)
        metadata_length = next(stream)
        children = [Node.from_stream(stream) for _ in range(num_children)]
        metadata = [next(stream) for _ in range(metadata_length)]
        return cls(children, metadata)

def go():
    with open("advent08.txt") as f:
        in_txt = f.read()

    nums = (int(atom) for atom in in_txt.split())

    root = Node.from_stream(iter(nums))
    print root.value

if __name__ == "__main__":
    go()
