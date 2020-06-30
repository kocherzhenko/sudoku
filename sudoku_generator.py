#!/usr/bin/env
from random import randint, shuffle
import time
from solve_sudoku import checkGrid, fillSolveGrid

def writeGrid2File(n, grid, filename):
    
    f = open(filename, 'a')
    for i in range(n**2):
        for j in range(n**2):
            f.write(str(grid[i][j])+' ')
#        f.write('\n')
    f.write('\n')
    f.close()
    
    return 0


def main():
    puzzles_filename = 'Puzzles.txt'
    solutions_filename = 'Solutions.txt'
    
    # Grid size will be n**2 x n**2
    n = 3
    # More attempts to remove numbers => harder puzzles
    no_attempts = 5
    # Number of puzzles to generate
    puzzles = 100
    
    # Create or overwrite puzzle file and solutions file
    f = open(puzzles_filename, 'w')
    f.write('\n')
    f.close()
    f = open(solutions_filename, 'w')
    f.write('\n')
    f.close()
    
    # Generate puzzles
    seconds = time.time()
    print (time.ctime(seconds))
    for p in range(puzzles):
        if (p+1) % 10 == 0:
            print ('Step ', p+1)
        
        # Initialize empty grid
        grid = []
        for row in range(n**2):
            grid.append([0 for col in range(n**2)])
        
        # Generate a solved grid
        counter = 1
        fillSolveGrid(n, grid, counter, opt='fill')
        writeGrid2File(n, grid, solutions_filename)
    
        # Remove numbers from grid one by one, checking that puzzle has exactly 1 solution
        counter = 1
        attempts = no_attempts
        while attempts > 0:
            # Select a random cell that is not already empty
            row = randint(0, n**2 - 1)
            col = randint(0, n**2 - 1)
            while grid[row][col] == 0:
                row = randint(0, n**2 - 1)
                col = randint(0, n**2 - 1)
            # Save its contents in case we need to put it back  
            backup = grid[row][col]
            grid[row][col]=0
      
            # Copy entire grid
            copyGrid = []
            for r in range(0, n**2):
                copyGrid.append([])
                for c in range(0, n**2):
                    copyGrid[r].append(grid[r][c])
      
            # Find the number of solutions
            counter = 0      
            flag, counter = fillSolveGrid(n, copyGrid, counter, opt='solve') 
            # If the number of solution is != 1 => place removed value back on the grid
            if counter != 1:
                grid[row][col] = backup
                attempts -= 1
    
        writeGrid2File(n, grid, puzzles_filename)
    
    seconds = time.time()
    print (time.ctime(seconds))

if __name__ == "__main__":
    main()

