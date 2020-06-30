import numpy as np
from keras.models import Sequential
from keras.layers import Activation, Conv2D, BatchNormalization, Dense, Flatten, Reshape
from keras.optimizers import Adam
from keras.backend import set_value

# Define convolutional neural network for solving sudoku:
# 3 convolutional layers + 1 fully connected layer
def define_model(n):

    model = Sequential()

    model.add(Conv2D(64, kernel_size=(n,n), activation='relu', padding='same', input_shape=(n**2,n**2,1)))
# Dimensions after 1st convolution: (n**2, n**2, 64 channels)
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(n,n), activation='relu', padding='same'))
# Dimensions after 2nd convolution: (n**2, n**2, 64 channels)
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))
# Dimensions after 3rd convolution: (n**2, n**2, 128 channels)
    model.add(Flatten())
# Dimensions of flattened vector: n**4 * 128
    model.add(Dense(n**6))
# n**6 neurons in dense layer: n**4 total numbers in grid with n**2 possible classes for each number
    model.add(Reshape((-1, n**2)))
# Dimensions (n**4, n**2)
    model.add(Activation('softmax'))
    
    return model


# Predict the most likely number for one of the empty cells
def predict_number(X, model, n2):

    y_prelim = model.predict(X.reshape((1, n2, n2, 1))) # Predict probabilities for all possible values in all cells 
    y_prelim = y_prelim.squeeze()
    y_predict = np.argmax(y_prelim, axis=1).reshape((n2, n2)) + 1 # Select most likely value for each cell 
    y_prob = np.max(y_prelim, axis=1).reshape((n2, n2)) # Select the corresponding probability
    X = X.reshape((n2, n2))
    m = (X < -0.49) # n2 x n2 array, True if cell is still empty, False if it is filled
    flag = m.sum() # True if there are still empty cells
    prob_empty = m * y_prob # Only consider empty cells, and
    index = np.argmax(prob_empty) # select the one for which the probability is highest

    return y_predict, index, flag
