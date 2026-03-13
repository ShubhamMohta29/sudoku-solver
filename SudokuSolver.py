"""Shubham Mohta

This is a sudoku solver made by Shubham Mohta.

This is in O(9^m) time complexity and O(m) space complexity where m is the number of empty cells on the board (0 <= m <= 81)
"""

import time

def first_empty_cell(sudoku_board: list[list]) -> tuple[int,int]|None:
    """Finds the first empty cell on the board
    
    Preconditions:
    - sudoku_board is a 9x9 matrix
    """
    
    for row in range(9):
        for col in range(9):
            if sudoku_board[row][col] == 0:
                return (row,col)
    return None

def is_valid(sudoku_board: list[list], row: int, col: int, num: int) -> bool:
    """Check if adding a number at a certain position is a valid move
        
    Preconditions:
    - 0 < row < 10
    - 0 < col < 10
    - 0 < num < 10
    """
    # row check
    if num in sudoku_board[row]:
        return False
    
    # column check
    for r in range(9):
        if sudoku_board[r][col] == num:
            return False
    
    # subgrid check
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if sudoku_board[start_row + i][start_col + j] == num:
                return False
    return True          
    
def solve_board(sudoku_board: list[list]) -> bool:
    empty = first_empty_cell(sudoku_board)
    if not empty:
        return True  # Solved

    row, col = empty
    for num in range(1, 10):
        if is_valid(sudoku_board, row, col, num):
            sudoku_board[row][col] = num
            if solve_board(sudoku_board):
                return True
            sudoku_board[row][col] = 0  # Backtrack

    return False  # Trigger backtracking

def print_board(sudoku_board: list[list]) -> None:
    """Given the 2D list of the sudoku board, this will return it in a way that's easier to read"""
    for row in sudoku_board:
        print('  '.join(str(num) for num in row))

def get_input() -> list[list]:
    """Using a for loop that iterates a total of 81 times, this function will get the numbers that form the sudoku grid
    
    Precondition:
    - the user only inputs integers"""

    board = [[],[],[],[],[],[],[],[],[]]
    for row in range(9):
        for col in range(9):
            num = int(input("Number in the cell or 0 if empty:  "))
            board[row].append(num)
    print("Board has been input.")
    print("This is the board:")
    print_board(board)
    return board

board = get_input()
time.sleep(1.5)
print("\n\nSolving board:")
if solve_board(board):
    print("Board Solved!")
    print_board(board)
else:
    print("No solution exists.")