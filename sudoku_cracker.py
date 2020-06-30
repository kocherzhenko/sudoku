import copy
import time
import numpy as np
from import_data import import_puzzles, import_solutions
from sudoku_model import define_model, predict_number
from solve_sudoku import checkGrid, fillSolveGrid
from check_sudoku import check_puzzle

def main():

    n = 3
# Load puzzles
    x_long, num_examples = import_puzzles(n, 'testing_puzzles.txt')
    x_puzzles = x_long[:1000]


# Load model
    model = define_model(n) # define the neural network architecture
    model.load_weights('sudoku_weights.h5') # load weights

    seconds = time.time()
    print (time.ctime(seconds))
# Solve puzzles
    correct = 0 # number of correctly solved puzzles
    for i, x in enumerate(x_puzzles): # for all puzzles in the set
        x_copy = copy.copy(x) 
        x_copy = x_copy.squeeze() 

        y_predict, index, flag = predict_number(x_copy, model, n**2) # predict 1 number in an empty cell
        while(flag): # while some cells are still empty
            y_predict, index, flag = predict_number(x_copy, model, n**2) # predict a number in an empty cell 
            # place that number in an empty cell and use the result as input to predict the next number
            x_copy[index // n**2][index % n**2] = y_predict[index // n**2][index % n**2] / 9 - 0.5 

        if check_puzzle(y_predict): # If the neural network got correct answer, all is well
            print ("NN successful")
            print (y_predict)
            correct += 1
            continue
        else: # If the neural network didn't get correct answer, solve puzzle using backtracking
            print ("NN failed")
            print (y_predict)
            x = (x + 0.5) * 9
            counter = 1
            fillSolveGrid(n, x, counter, opt='fill')
            y_predict = np.asarray(x)
            y_predict = y_predict.reshape((9,9))            
            y_predict = y_predict.astype(int)
            if check_puzzle(y_predict):
                print ("Backtracking:")
                print (y_predict)

    print(correct/x_puzzles.shape[0]*100)
#        print (y_predict)
    seconds = time.time()
    print (time.ctime(seconds))
        
if __name__ == "__main__":
    main()
