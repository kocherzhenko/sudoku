import copy
import numpy as np
from keras.optimizers import Adam
from keras.backend import set_value
from import_data import import_puzzles, import_solutions
from sudoku_model import define_model, predict_number

def main():

    n = 3
    print ('Loading training set...')
# Read in puzzles for training set (inputs)
    x_train, num_examples = import_puzzles(n, 'training_puzzles.txt')
# Read in solutions for training set (labels)
    y_train = import_solutions(n, num_examples, 'training_solutions.txt')

    print ('Loading test set...')
# Read in puzzles for test set
    x_test, _ = import_puzzles(n, 'testing_puzzles.txt')
# Read in solutions for test set
    y_test = import_solutions(n, num_examples, 'testing_solutions.txt')

# Train model
    model = define_model(n) # define the neural network architecture
    adam = Adam(lr=0.001)   # use Adam optimizer with a learning rate of 0.001
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)
    print ("Initial learning rate: ", model.optimizer.learning_rate.numpy())
    model.fit(x_train, y_train, batch_size=32, epochs=1) # train for 1 epoch
    set_value(model.optimizer.learning_rate, 0.0001) # reduce learning rate to 0.0001
    print ("Updated learning rate: ", model.optimizer.learning_rate.numpy()) 
    model.fit(x_train, y_train, batch_size=32, epochs=1) # train for 1 more epoch
    model.save_weights('sudoku_weights.h5') # save weights to a file

# Test model
    correct = 0 # number of correctly solved puzzles
    for i, x in enumerate(x_test): # for all examples in the test set
        x_copy = copy.copy(x) 
        x_copy = x_copy.squeeze() 

        y_predict, index, flag = predict_number(x_copy, model, n**2) # predict 1 number in an empty cell
        while(flag): # while some cells are still empty
            y_predict, index, flag = predict_number(x_copy, model, n**2) # predict a number in an empty cell 
            # place that number in an empty cell and use the result as input to predict the next number
            x_copy[index // n**2][index % n**2] = y_predict[index // n**2][index % n**2] / 9 - 0.5 
        y = y_test[i].reshape((9,9)) + 1
        comparison = (y == y_predict)
        if comparison.all(): # if all numbers in label and predicted solution are identical
            correct += 1 # then the puzzle had been solved correctly
    
    print (correct/x_test.shape[0]*100, " % solved correctly")

if __name__ == "__main__":
    main()
