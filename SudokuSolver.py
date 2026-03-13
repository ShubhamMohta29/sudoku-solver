"""Shubham Mohta

An optimized Sudoku solver using backtracking with constraint propagation
and the Minimum Remaining Values (MRV) heuristic.

Naive backtracking:         O(9^m)   — tries cells in fixed order
This solver (MRV + forward checking): much better in practice — always
picks the empty cell with the fewest valid candidates first, pruning the
search tree significantly. Worst-case is still exponential (NP-complete),
but on real puzzles it's orders of magnitude faster.

Space complexity: O(m) for the recursion stack, where m = number of empty cells.
"""


# ─────────────────────────────────────────────
# Board helpers
# ─────────────────────────────────────────────

def print_board(board: list[list[int]]) -> None:
    """Prints the board with sudoku grid lines. Empty cells shown as '·'."""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("──────┼───────┼──────")
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "│ "
            row_str += (str(num) if num != 0 else "·") + " "
        print(row_str)


def is_valid_board(board: list[list[int]]) -> bool:
    """Returns True if the starting board has no conflicting numbers.

    Preconditions:
    - board is a 9x9 matrix with values 0-9 (0 = empty)
    """
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                board[row][col] = 0
                if not _is_valid(board, row, col, num):
                    board[row][col] = num
                    return False
                board[row][col] = num
    return True


# ─────────────────────────────────────────────
# Constraint helpers
# ─────────────────────────────────────────────

def _is_valid(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Returns True if placing num at (row, col) violates no sudoku rules.

    Preconditions:
    - 0 <= row <= 8
    - 0 <= col <= 8
    - 1 <= num <= 9
    - board[row][col] == 0
    """
    if num in board[row]:
        return False
    for r in range(9):
        if board[r][col] == num:
            return False
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[sr + i][sc + j] == num:
                return False
    return True


def _candidates(board: list[list[int]], row: int, col: int) -> set[int]:
    """Returns the set of valid numbers that can be placed at (row, col).

    Preconditions:
    - 0 <= row <= 8
    - 0 <= col <= 8
    - board[row][col] == 0
    """
    used = set(board[row])
    used |= {board[r][col] for r in range(9)}
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    used |= {board[sr+i][sc+j] for i in range(3) for j in range(3)}
    return set(range(1, 10)) - used


# ─────────────────────────────────────────────
# MRV heuristic
# ─────────────────────────────────────────────

def _mrv_cell(board: list[list[int]]) -> tuple[int, int, set[int]] | None:
    """Finds the empty cell with the fewest valid candidates (MRV heuristic).

    Returns (row, col, candidates) for the most constrained empty cell,
    or None if there are no empty cells left (board is solved).

    If any empty cell has 0 candidates, returns it immediately so the
    solver can backtrack without wasted work (forward checking).

    Preconditions:
    - board is a 9x9 matrix with values 0-9
    """
    best = None
    best_count = 10

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                cands = _candidates(board, row, col)
                if len(cands) == 0:
                    return (row, col, cands)   # dead end — backtrack immediately
                if len(cands) < best_count:
                    best_count = len(cands)
                    best = (row, col, cands)
                    if best_count == 1:
                        return best            # can't do better than 1 candidate

    return best  # None if board is full


# ─────────────────────────────────────────────
# Solver
# ─────────────────────────────────────────────

def solve_board(board: list[list[int]]) -> bool:
    """Solves the sudoku board in-place using backtracking + MRV + forward checking.

    Returns True if a solution was found, False if no solution exists.

    Preconditions:
    - board is a valid 9x9 sudoku board with values 0-9
    """
    cell = _mrv_cell(board)
    if cell is None:
        return True  # No empty cells — solved!

    row, col, cands = cell
    if not cands:
        return False  # Dead end — backtrack

    for num in cands:
        board[row][col] = num
        if solve_board(board):
            return True
        board[row][col] = 0  # Backtrack

    return False


# ─────────────────────────────────────────────
# Input
# ─────────────────────────────────────────────

def get_input() -> list[list[int]]:
    """Prompts the user to enter the board one row at a time as a 9-digit string.

    Each character should be a digit 1-9 for a filled cell, or 0 (or '.')
    for an empty cell. Spaces are ignored.

    Example valid row inputs:
        530070000
        5 3 0 0 7 0 0 0 0
        53..7....

    Preconditions:
    - Each row input contains exactly 9 digits after stripping spaces and dots
    """
    print("Enter each row as a 9-digit string.")
    print("Use 0 or '.' for empty cells. Spaces are ignored.")
    print("Example: 530070000  or  5 3 0 . 7 . . . .\n")

    board = []
    for i in range(9):
        while True:
            raw = input(f"  Row {i + 1}: ").replace(" ", "").replace(".", "0")
            if len(raw) == 9 and raw.isdigit() and all(0 <= int(ch) <= 9 for ch in raw):
                board.append([int(ch) for ch in raw])
                break
            print("  Invalid. Enter exactly 9 digits (0-9). Try again.")

    print("\nBoard entered:")
    print_board(board)
    return board


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    board = get_input()

    if not is_valid_board(board):
        print("\nThis board is invalid — it already has conflicting numbers!")
    else:
        print("\nSolving...")
        if solve_board(board):
            print("Solved!\n")
            print_board(board)
        else:
            print("No solution exists for this board.")
