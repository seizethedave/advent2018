RECIPES = 286051

def go():
    elf1 = 0
    elf2 = 1
    board = [3, 7]

    while True:
        new_scores = [int(c) for c in str(board[elf1] + board[elf2])]
        board.extend(new_scores)

        if len(board) >= RECIPES + 10:
            print ''.join(str(c) for c in board[RECIPES:RECIPES+10])
            return

        elf1 = (elf1 + board[elf1] + 1) % len(board)
        elf2 = (elf2 + board[elf2] + 1) % len(board)

if __name__ == "__main__":
    go()
