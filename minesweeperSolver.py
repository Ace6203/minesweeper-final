import random

#Ai assisted on lines 4-13 in showing how to tell where valid neighboring cells are
def get_neighbors(x, y, width, height):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width:
                neighbors.append((nx, ny))
    return neighbors

#Ai assisted in sections of generate_board
def generate_board(width, height, num_mines, safe_cell):
    board = [[0 for _ in range(width)] for _ in range(height)]
    mines = set()
    safe_x, safe_y = safe_cell

    while len(mines) < num_mines:
        x, y = random.randrange(height), random.randrange(width)
        if (x, y) not in mines and (x, y) != (safe_x, safe_y):
            mines.add((x, y))
            board[x][y] = -1

#Ai assisted on lines 28-36 in showing how to store the number of adjacent mines
    for x in range(height):
        for y in range(width):
            if board[x][y] == -1:
                continue
            count = sum(
                1 for (nx, ny) in get_neighbors(x, y, width, height)
                if board[nx][ny] == -1
            )
            board[x][y] = count

    return board

def create_visible_board(width, height):
    return [[-1 for _ in range(width)] for _ in range(height)]

def reveal_cell(board, visible, x, y):
    if visible[x][y] != -1:
        return True

    if board[x][y] == -1:
        visible[x][y] = -9
        return False

    visible[x][y] = board[x][y]

#Ai assisted on lines 54-57 in showing how to recursively reveal all connected empty cells if an empty cell is selected
    if board[x][y] == 0:
        for nx, ny in get_neighbors(x, y, len(board[0]), len(board)):
            if visible[nx][ny] == -1:
                reveal_cell(board, visible, nx, ny)

    return True

def print_board(board):
    for row in board:
        print(" ".join(
            '💣' if x == -9 else
            '🚩' if x == -2 else
            '⬜' if x == -1 else
            str(x)
            for x in row
        ))
    print()
#Ai assisted in sections of solve_visible_board
def solve_visible_board(visible):
    height, width = len(visible), len(visible[0])
    flags = set()
    safe = set()
    changed = True

    while changed:
        changed = False
        for x in range(height):
            for y in range(width):
                cell = visible[x][y]
                if cell <= 0:
                    continue
                # Ai assisted in lines 86-103 in showing how to write the solving algorithm
                neighbors = get_neighbors(x, y, width, height)
                unrevealed = [(nx, ny) for (nx, ny) in neighbors if visible[nx][ny] == -1]
                flagged = [(nx, ny) for (nx, ny) in neighbors if (nx, ny) in flags]

                if len(unrevealed) == 0:
                    continue

                if cell == len(unrevealed) + len(flagged):
                    for (nx, ny) in unrevealed:
                        if (nx, ny) not in flags:
                            flags.add((nx, ny))
                            visible[nx][ny] = -2
                            changed = True
                elif cell == len(flagged):
                    for (nx, ny) in unrevealed:
                        if (nx, ny) not in safe:
                            safe.add((nx, ny))
                            changed = True

    return flags, safe

#Ai assisted in sections of play_minesweeper
def play_minesweeper(width=7, height=11, num_mines=8):
    start_x, start_y = random.randrange(height), random.randrange(width)

    board = generate_board(width, height, num_mines, safe_cell=(start_x, start_y))
    visible = create_visible_board(width, height)

    reveal_cell(board, visible, start_x, start_y)

    print("🟩 Starting Minesweeper...")
    turn = 0

    while True:
        turn += 1
        print(f"🔁 Turn {turn}")
        flags, safe = solve_visible_board(visible)

        # Ai assisted on lines 125-133 in showing how to keep track of how many cells are revealed and if the game is solved
        before_revealed = sum(cell != -1 for row in visible for cell in row)
        for (x, y) in safe:
            reveal_cell(board, visible, x, y)
        after_revealed = sum(cell != -1 for row in visible for cell in row)

        unrevealed = [(x, y) for x in range(height) for y in range(width) if visible[x][y] == -1]
        if not unrevealed:
            print("🎉 Solved the board!")
            break

        if not safe or after_revealed == before_revealed:
            print("🤔 No safe moves left. Guessing...")
            candidates = [(x, y) for (x, y) in unrevealed if (x, y) not in flags]
            if not candidates:
                print("No candidates left.")
                break

            guess_x, guess_y = random.choice(candidates)
            print(f"🎯 Guessing cell ({guess_x}, {guess_y})")

            alive = reveal_cell(board, visible, guess_x, guess_y)
            if not alive:
                print("💥 Hit a mine! Game over.")
                break

        if any(visible[x][y] == -9 for x in range(height) for y in range(width)):
            break

        if turn > 200:
            print("⚠️ Too many turns — stopping to avoid infinite loop.")
            break

    print("Visible board:")
    print_board(visible)
    print("True board:")
    print_board(board)

if __name__ == "__main__":
    play_minesweeper()
