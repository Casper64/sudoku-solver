import sudoku_generator
import sys
import json
import numpy as np

def main():
    if len(sys.argv) > 1:
        grid_json = sys.argv[1]
        new_grid = json.loads(grid_json)
    else:
        print("Too few arguments!")
        sys.exit(1)

    new_grid = np.array(new_grid)
    result = sudoku_generator.sudoku(new_grid, 0, 0)
    if result:
        print("Array")
        print(new_grid)
        print("End")
    else:
        print(new_grid)
        print("FAIL")

if __name__ == "__main__":
    main()