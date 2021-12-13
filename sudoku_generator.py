#!/usr/bin/env python

from random import randint, shuffle
import numpy as np
from time import sleep
import sys
numberlist = [1,2,3,4,5,6,7,8,9]
grid = np.array([[0 for j in range(0,9)] for i in range(0,9)])
counter = 1

def print_grid(grid):
    print("\r", end="")
    for row in grid:
        for col in row:
            print(f" {col} ", end="")
        print("\n", end="")


def fill_grid(grid):
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            shuffle(numberlist)
            for number in numberlist:
                # Check if the number is not in the same row
                if number not in grid[row]:
                    # Check if the number is not in the same column
                    if number not in grid[:,col]:
                        # Check if the number is not in the same square
                        square_col = i // 3 % 3
                        square_row = i // 27
                        square = [grid[i][square_col*3:square_col*3+3] for i in range(square_row*3, square_row*3+3)]
                        square = np.array(square)

                        if number not in square.flatten():
                            grid[row][col] = number
                            if 0 not in grid.flatten():
                                return True
                            elif fill_grid(grid):
                                return True
            break  
    grid[row][col] = 0
    
def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
    for x in range(9):
        if grid[x][col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True

def sudoku(grid, row, col, remove=False):
    global counter
    
    if row == 8 and col == 9:
        return True
    if col == 9:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return sudoku(grid, row, col + 1, remove=remove)
    for num in range(1, 10):
        if solve(grid, row, col, num):
            grid[row][col] = num
            if sudoku(grid, row, col + 1, remove=remove):
                counter += 1
                if not remove:
                    return True
        grid[row][col] = 0
    return False

def main():
    fill_grid(grid)
    print_grid(grid)

    global counter
    attempts = 5
    inc = 0
    while attempts > 0:
        row = randint(0, 8)
        col = randint(0, 8)
        while grid[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)
        backup = grid[row][col]
        grid[row][col] = 0
        copy_grid = np.copy(grid)

        # Count the number of times the grid can be solved, it should be 1
        counter = 0
        # solve_grid(copy_grid)
        sudoku(copy_grid, 0, 0, remove=True)
        if counter != 1:
            grid[row][col] = backup
            attempts -= 1
        else:
            inc += 1
            sys.stdout.flush()
            print(f" Removed {inc} numbers", end="\r")
    print()
    print("Array")
    print(grid)
    print("End")     

if __name__ == "__main__":
    main()