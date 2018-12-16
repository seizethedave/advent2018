TARGET = tuple(reversed([2,8,6,0,5,1]))

def go():
    elf1 = 0
    elf2 = 1
    board = [3, 7]
    tail_stack = list(TARGET)
    recipes = len(board)

    while True:
        for tail_char in (int(c) for c in str(board[elf1] + board[elf2])):
            recipes += 1
            board.append(tail_char)

            if tail_char == tail_stack[-1]:
                tail_stack.pop()
                if not tail_stack:
                    # this is it.
                    print recipes - len(TARGET)
                    return
            elif len(tail_stack) < len(TARGET):
                # Start tail over again.
                tail_stack = list(TARGET)

        elf1 = (elf1 + board[elf1] + 1) % len(board)
        elf2 = (elf2 + board[elf2] + 1) % len(board)

if __name__ == "__main__":
    go()
