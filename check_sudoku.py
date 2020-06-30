import numpy as np

# Check whether any number in a row of a matrix occurs more than once
def row_correct(y_list):

    correct = True
    rows_correct = []
    for row in y_list: # For each row
        row_correct = True
        for i, el in enumerate(sorted(row)): # check whether any 2 subsequent elements are the same
            if (i > 0) and (el == sorted(row)[i-1]): # if they are, the row is wrong
                row_correct = False
        rows_correct.append(row_correct)
    if False in rows_correct: # If any row is wrong, the matrix is wrong
        correct = False

    return correct

# Split grid into n blocks with size n x n (n = 3 for standard sudoku)
def get_blocks(y_list):
    
    n2 = len(y_list)
    n = int(np.sqrt(n2))

    blocks = [ [] for i in range(n2) ]
    for i in range(n2):
       ic = i // n 
       for j in range(n2):
           jc = j // n
           blocks[ic*n + jc].append(y_list[i][j])

    return blocks
    
# Check whether the solution of a sudoku puzzle is correct
def check_puzzle(y):

    y_list = y.tolist()
    blocks = get_blocks(y_list)
    correct = row_correct(blocks) # are any numbers repeated in any blocks?
    correct *= row_correct(y_list) # are any numbers repeated in any rows?
    y_list = (y.T).tolist()
    correct *= row_correct(y_list) # are any numbers repeated in any column?
    for i in range(len(y_list)): # if any of the cells are unfilled, the solution is wrong
       if 0 in y_list[i]:
          correct = False

    # all four conditions must hold for the solution to be correct (correct = True)
    return correct
