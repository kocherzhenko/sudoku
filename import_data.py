import numpy as np

# Read in unsolved puzzles, X, into a 4D numpy array with dimensions (# of samples, n**2, n**2, 1)
def import_puzzles(n, filename_x): # block size n = 3 for standard sudoku, filename for unsolved puzzles

    X = []
    f = open(filename_x, 'r')
    for line in f:
        X.append([])
        x = line.split()
        for i in range(n**2):
            X[-1].append([])
            for j in range(n**2):
                X[-1][i].append([])
                X[-1][i][j].append( int(x[i*n**2+j]) )
    f.close()
    num_examples = len(X)
    X_np = np.asarray(X)
    X_np = X_np / (n**2) - 0.5 # scale features to range [-0.5,+0.5]
    print ('X loaded!')

    return X_np, num_examples

# Read in solved puzzles, Y, into a 3D array with dimensions (# of samples, n**4, 1)
def import_solutions(n, num_examples, filename_y): # block size n = 3 for standard sudoku, filenames for solved puzzles

    Y_np = np.zeros((num_examples, n**4, 1)) 
    f = open(filename_y, 'r')
    i = 0
    for line in f:
        y = line.split()
        for j, el in enumerate(y):
            Y_np[i][j] = int(el) - 1 #  n**2 softmax classes numbered from 0 to n**2 -1]
        i += 1
    f.close()
    print ('Y loaded!')

    return Y_np
