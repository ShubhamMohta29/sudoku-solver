# Sudoku Solver

A command-line Sudoku solver written in Python using backtracking with **constraint propagation** and the **Minimum Remaining Values (MRV) heuristic** — significantly faster than naive backtracking on real puzzles.

## How it works

### Algorithm

Instead of blindly trying the first empty cell, the solver always picks the **most constrained cell first** — the empty cell with the fewest valid candidates. This prunes the search tree dramatically.

1. Scan all empty cells and compute their candidate sets (valid digits for that cell)
2. Pick the cell with the fewest candidates (**MRV heuristic**)
3. If any cell has 0 candidates, backtrack immediately without going deeper (**forward checking**)
4. Try each candidate, recurse, and backtrack if needed

### Key functions

- `_candidates(board, row, col)` — returns the set of valid digits for a cell using set operations
- `_mrv_cell(board)` — finds the most constrained empty cell; returns immediately on a dead end
- `solve_board(board)` — recursive backtracking solver using MRV + forward checking
- `is_valid_board(board)` — validates the starting board for conflicts before solving

## Usage

Requires Python 3.10+ (uses `X | Y` union type syntax). No external libraries needed.

```bash
python sudoku_solver.py
```

Enter each row as a 9-digit string. Use `0` or `.` for empty cells. Spaces are ignored.

```
Enter each row as a 9-digit string.
Use 0 or '.' for empty cells. Spaces are ignored.
Example: 530070000  or  5 3 0 . 7 . . . .

  Row 1: 530070000
  Row 2: 600195000
  Row 3: 098000060
  ...
```

### Example

Input:
```
5 3 ·  · 7 ·  · · ·
6 · ·  1 9 5  · · ·
· 9 8  · · ·  · 6 ·
──────┼───────┼──────
8 · ·  · 6 ·  · · 3
4 · ·  8 · 3  · · 1
7 · ·  · 2 ·  · · 6
──────┼───────┼──────
· 6 ·  · · ·  2 8 ·
· · ·  4 1 9  · · 5
· · ·  · 8 ·  · 7 9
```

Solved:
```
5 3 4  6 7 8  9 1 2
6 7 2  1 9 5  3 4 8
1 9 8  3 4 2  5 6 7
──────┼───────┼──────
8 5 9  7 6 1  4 2 3
4 2 6  8 5 3  7 9 1
7 1 3  9 2 4  8 5 6
──────┼───────┼──────
9 6 1  5 3 7  2 8 4
2 8 7  4 1 9  6 3 5
3 4 5  2 8 6  1 7 9
```
