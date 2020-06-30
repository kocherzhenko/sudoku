#!/usr/bin/env
from random import shuffle

# Check whether the grid is full
def checkGrid(n, grid):
    for row in range(0,n**2):
        for col in range(0,n**2):
            if grid[row][col]==0: # There is at least 1 empty cell!
                return False
    return True # The grid is full

# Fill or solve grid
def fillSolveGrid(n, grid, counter, opt):

    numberList=[i+1 for i in range(n**2)]
    
    #Find next empty cell
    for i in range(n**4):
        row = i // (n**2)
        col = i % (n**2)
        if grid[row][col]==0:
            if opt == 'fill': # If we are solving a puzzle,
                shuffle(numberList) # pick numbers from 1 to 9 in random order
            for value in numberList: # pick a number
                #Check that this value has not already be used on this row
                if not(value in grid[row]):
                    #Check that this value has not already be used on this column
                    num_in_col = []
                    for r in range(n**2):
                        num_in_col.append(grid[r][col]) 
                    if not value in (num_in_col):
                        #Check that this value has not already be used on this n x n block
                        num_in_block = []
                        for k in range(n):
                            for l in range(n):
                                num_in_block.append(grid[n*(row // n)+k][n*(col // n)+l])
                        if not value in (num_in_block):
                            # if the number is not yet in row, column, and block, place it in the empty cell on the grid
                            grid[row][col]=value
                            if checkGrid(n, grid): # if the grid is full
                                if opt == 'fill': # and we are filling it
                                    return True, counter # we are done!
                                elif opt == 'solve':
                                    counter+=1 # increment the number of possible solutions
                                               # only grids with a single solution are valid
                                    break
                            else: # if the grid is not full yet,
                                  # call function recursively to add a number to another empty cell
                                flag, counter = fillSolveGrid(n, grid, counter, opt)
                                if flag:
                                    return True, counter
            break

    grid[row][col]=0  
    return False, counter
