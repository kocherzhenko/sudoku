import sys
import random
import copy
import signal
import numpy as np
import pygame as pg
from pygame.locals import *
from import_data import import_puzzles, import_solutions
from sudoku_model import define_model, predict_number
from solve_sudoku import checkGrid, fillSolveGrid
from check_sudoku import check_puzzle

WINDOWSIZE = 307
BLOCKSIZE = WINDOWSIZE // 3
CELLSIZE = BLOCKSIZE // 3
MARGIN = int(5.5*CELLSIZE)
FPS = 10

def signal_handler(signum, frame):
    raise Exception("Timed out!")

def drawGrid():
    for i in range(0, WINDOWSIZE, CELLSIZE):
        pg.draw.line(DISPLAYSURF, (200,200,200), (i,0), (i,WINDOWSIZE))
        if i % 3 == 0:    
            pg.draw.line(DISPLAYSURF, (0,0,0), (i,0), (i,WINDOWSIZE))
    for j in range(0, WINDOWSIZE, CELLSIZE):
        pg.draw.line(DISPLAYSURF, (200,200,200), (0,j), (WINDOWSIZE,j))
        if j % 3 == 0:    
            pg.draw.line(DISPLAYSURF, (0,0,0), (0,j), (WINDOWSIZE,j))

    return None

def drawButton(color, coords, title):
    pg.draw.rect(DISPLAYSURF, color, coords, 2)
    font = pg.font.Font('freesansbold.ttf', 20)
    text = font.render(title, True, (0,0,0), (255,255,255))
    textRect = text.get_rect()
    textRect.center = ( coords[0]+coords[2] // 2, coords[1] + coords[3] // 2 )
    DISPLAYSURF.blit(text, textRect)

    return None 



def main():
    global FPSCLOCK, DISPLAYSURF
    n = 3
    numerickeys = [str(i) for i in range(1,n**2+1)]
#    print (numerickeys)
    puzzles, num_examples = import_puzzles(n, 'Puzzles_001.txt')
#    snp = import_solutions(n, num_examples, 'Solutions_001.txt')
    choice = random.randint(0,num_examples-1)
    puzzle_np = (((puzzles[choice].reshape((9,9)) + 0.5) * n**2).astype(np.int)).T
#    print (puzzle_np)
#    print ((snp[choice].reshape((9,9)).astype(np.int)+1))
    puzzle = puzzle_np.tolist()
    mutable = (puzzle_np == 0)
#    print (mutable)
    solution = copy.deepcopy(puzzle)
#    print (solution)
    model = define_model(n) # define the neural network architecture
    model.load_weights('sudoku_weights.h5') # load weights

    pg.init()
    FPSCLOCK = pg.time.Clock()
    DISPLAYSURF = pg.display.set_mode((WINDOWSIZE,WINDOWSIZE+MARGIN))
    DISPLAYSURF.fill((255,255,255))
    pg.display.set_caption("Sudoku")    

    font = pg.font.Font('freesansbold.ttf', 20)
    cells = []
    numstrs = []
    chars = []
    charRects = []
    for i in range(n**2):
#        numstrs.append([ str(j) for j in range(n**2) ])
        numstrs.append([ '' for j in range(n**2) ])
        cells.append([ pg.Surface((CELLSIZE,CELLSIZE)) for j in range(n**2) ])
        chars.append([ font.render(numstrs[i][j], True, (0,0,0), (255,255,255)) for j in range(n**2) ])
        charRects.append([ chars[i][j].get_rect() for j in range(n**2) ])
        for j in range(n**2):
            cells[i][j].fill((255,255,255))
            charRects[i][j].center = ( (2*i+1) * CELLSIZE // 2, (2*j+1) * CELLSIZE // 2 )
            DISPLAYSURF.blit(cells[i][j],(i*CELLSIZE,j*CELLSIZE))
            DISPLAYSURF.blit(chars[i][j], charRects[i][j])

    for i in range(n**2):
        for j in range(n**2):
            if puzzle[i][j] != 0:
                 numstrs[i][j] = str(puzzle[i][j])
                 chars[i][j] = font.render(numstrs[i][j], True, (0,0,255), (255,255,255))
                 DISPLAYSURF.blit(chars[i][j], charRects[i][j])
                  

    mx = 0
    my = 0
    flag = False
    solution_flag = False
    while True:
        for event in pg.event.get():
            if solution_flag == True:
                solution_flag = False
                font_message = pg.font.Font('freesansbold.ttf', 20)
                text = font.render("                          ", True, (255,255,255), (255,255,255))
                textRect = text.get_rect()
                textRect.center = (WINDOWSIZE // 2, WINDOWSIZE + MARGIN - CELLSIZE // 2)
                DISPLAYSURF.blit(text, textRect)
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
# Unselect previously selected cell
                i = mx // CELLSIZE
                j = my // CELLSIZE
                if (mutable[i][j]):
                    cells[i][j].fill((255,255,255))
                    DISPLAYSURF.blit(cells[i][j],(i*CELLSIZE,j*CELLSIZE))
                    chars[i][j] = font.render(numstrs[i][j], True, (0,0,0), (255,255,255))
                    DISPLAYSURF.blit(chars[i][j], charRects[i][j]) 
# Detect position of the mouse and select corresponding cell
                mxp, myp = pg.mouse.get_pos()
                ip = mxp // CELLSIZE
                jp = myp // CELLSIZE
                if (ip < n**2) and (jp < n**2):
                    flag = True
                    mx = mxp
                    my = myp
                    i = ip
                    j = jp
                    if (mutable[i][j]):
                        cells[i][j].fill((255,0,0))
                        DISPLAYSURF.blit(cells[i][j],(i*CELLSIZE,j*CELLSIZE))
                        chars[i][j] = font.render(numstrs[i][j], True, (0,0,0), (255,0,0))
                        DISPLAYSURF.blit(chars[i][j], charRects[i][j])

# If clicked anywhere outside the sudoku grid, deselect previous cell
                if (myp > WINDOWSIZE):
                    flag = False
 
# Click and hold "Check" to see whether the puzzle is correct 
                if (mxp > CELLSIZE // 2) and (mxp < int(4.25*CELLSIZE) ) and (myp > WINDOWSIZE + CELLSIZE // 2) and (myp < WINDOWSIZE + 3 * CELLSIZE // 2):
                    solution_np = (np.asarray(solution)).T
                    solution_flag = True
                    font_message = pg.font.Font('freesansbold.ttf', 20)
                    if check_puzzle(solution_np) == True:
#                        print (solution_np)
                        text = font.render("Correct!", True, (0,255,0), (255,255,255))
                    else:
                        text = font_message.render("Wrong!", True, (255,0,0), (255,255,255))
                    textRect = text.get_rect()
                    textRect.center = (WINDOWSIZE // 2, WINDOWSIZE + MARGIN - CELLSIZE // 2)
                    DISPLAYSURF.blit(text, textRect)

# Click "Reset" to see remove all user-entered values and restart the current puzzle                        
                if (mxp > CELLSIZE // 2) and (mxp < int(4.25*CELLSIZE) ) and (myp > WINDOWSIZE + 2*CELLSIZE) and (myp < WINDOWSIZE + 3 * CELLSIZE):
                    for ir in range(n**2):
                        for jr in range(n**2):
                            cells[ir][jr].fill((255,255,255))
                            DISPLAYSURF.blit(cells[ir][jr],(ir*CELLSIZE,jr*CELLSIZE))
                            if puzzle[ir][jr] != 0:
                                numstrs[ir][jr] = str(puzzle[ir][jr])
                            else:
                                numstrs[ir][jr] = ''
                            chars[ir][jr] = font.render(numstrs[ir][jr], True, (0,0,255), (255,255,255))
                            DISPLAYSURF.blit(chars[ir][jr], charRects[ir][jr])
                            solution[ir][jr] = puzzle[ir][jr]

# Click "New" to select a new random puzzle
                if (mxp > CELLSIZE // 2) and (mxp < int(4.25*CELLSIZE) ) and (myp > WINDOWSIZE + int(3.5 * CELLSIZE)) and (myp < WINDOWSIZE + int(4.5 * CELLSIZE)):
                    choice = random.randint(0,num_examples-1)
                    puzzle_np = (((puzzles[choice].reshape((9,9)) + 0.5) * n**2).astype(np.int)).T
                    puzzle = puzzle_np.tolist()
                    mutable = (puzzle_np == 0)
                    solution = copy.deepcopy(puzzle)
                    for ir in range(n**2):
                        for jr in range(n**2):
                            cells[ir][jr].fill((255,255,255))
                            DISPLAYSURF.blit(cells[ir][jr],(ir*CELLSIZE,jr*CELLSIZE))
                            if puzzle[ir][jr] != 0:
                                numstrs[ir][jr] = str(puzzle[ir][jr])
                            else:
                                numstrs[ir][jr] = ''
                            chars[ir][jr] = font.render(numstrs[ir][jr], True, (0,0,255), (255,255,255))
                            DISPLAYSURF.blit(chars[ir][jr], charRects[ir][jr])

# Click "Blank" to create a blank sudoku grid for setting up a user-defined puzzle
                if (mxp > int(4.75*CELLSIZE)) and (mxp < int(8.5*CELLSIZE) ) and (myp > WINDOWSIZE + CELLSIZE // 2) and (myp < WINDOWSIZE + 3 * CELLSIZE // 2):
                    for ir in range(n**2):
                        for jr in range(n**2):
                            cells[ir][jr].fill((255,255,255))
                            DISPLAYSURF.blit(cells[ir][jr],(ir*CELLSIZE,jr*CELLSIZE))
                            puzzle[ir][jr] = 0
                            numstrs[ir][jr] = ''
                            mutable = np.ones(puzzle_np.shape)
                            solution[ir][jr] = 0

# Click "Solve" to solve the puzzle, if possible
                if (mxp > int(4.75*CELLSIZE)) and (mxp < int(8.5*CELLSIZE) ) and (myp > WINDOWSIZE + 2*CELLSIZE) and (myp < WINDOWSIZE + 3 * CELLSIZE):
                    x_np = np.asarray(solution) / 9 - 0.5
                    x_np2 = copy.deepcopy(x_np)
                    y_predict, index, ff = predict_number(x_np, model, n**2) # predict 1 number in an empty cell
                    while(ff): # while some cells are still empty
                        y_predict, index, ff = predict_number(x_np, model, n**2) # predict a number in an empty cell 
                        # place that number in an empty cell and use the result as input to predict the next number
                        x_np[index // n**2][index % n**2] = y_predict[index // n**2][index % n**2] / 9 - 0.5 

                    if not check_puzzle(y_predict): # If the neural network did not get correct answer,
                                                    # solve puzzle using backtracking
                        x_np = x_np2
                        x_np = (x_np + 0.5) * 9
                        counter = 1
                        signal.signal(signal.SIGALRM, signal_handler)
                        signal.alarm(120)
                        to = False
                        try:
                            fillSolveGrid(n, x_np, counter, opt='fill')
                            y_predict = np.asarray(x_np)
                            y_predict = y_predict.reshape((9,9))            
                            y_predict = y_predict.astype(int)
                        except Exception as msg:
                            y_predict = x_np
                            to = True
    
#                    print (y_predict)
                    check_correct = True
                    solution = y_predict.tolist()
                    for i in range(n**2):
                        if 0 in solution[i]:
                            check_correct = False
                    if (check_correct == False):
                        if to == False:
                            message = "Invalid puzzle!"
                        else:
                            message = "Timed out!"
                        solution_flag = True
                        font_message = pg.font.Font('freesansbold.ttf', 20)
                        text = font.render(message, True, (255,0,0), (255,255,255))
                        textRect = text.get_rect()
                        textRect.center = (WINDOWSIZE // 2, WINDOWSIZE + MARGIN - CELLSIZE // 2)
                        DISPLAYSURF.blit(text, textRect)
                    else:
                        for i in range(n**2):
                            for j in range(n**2):
                                if puzzle[i][j] == 0:
                                     numstrs[i][j] = str(solution[i][j])
                                     chars[i][j] = font.render(numstrs[i][j], True, (0,0,0), (255,255,255))
                                     DISPLAYSURF.blit(chars[i][j], charRects[i][j])
                        
                        
                    
# Click "Quit" to exit the game
                if (mxp > int(4.75*CELLSIZE)) and (mxp < int(8.5*CELLSIZE) ) and (myp > WINDOWSIZE + int(3.5 * CELLSIZE)) and (myp < WINDOWSIZE + int(4.5 * CELLSIZE)):
                    exit()

            if event.type == pg.KEYDOWN:
# If a number key, 1-9, has been pressed, a cell has been clicked, and that cell is mutable
                if (event.unicode in numerickeys) and (mutable[i][j]) and (flag):
                    cells[i][j].fill((255,255,255))
                    DISPLAYSURF.blit(cells[i][j],(i*CELLSIZE,j*CELLSIZE))
                    numstrs[i][j] = event.unicode
                    chars[i][j] = font.render(numstrs[i][j], True, (0,0,0), (255,255,255))
                    DISPLAYSURF.blit(chars[i][j], charRects[i][j])
                    solution[i][j] = int(event.unicode)
#                    print (solution)
                if (event.key == pg.K_BACKSPACE) and (mutable[i][j]):
                    cells[i][j].fill((255,255,255))
                    DISPLAYSURF.blit(cells[i][j],(i*CELLSIZE,j*CELLSIZE))
                    numstrs[i][j] = ''
                    chars[i][j] = font.render(numstrs[i][j], True, (0,0,0), (255,255,255))
                    DISPLAYSURF.blit(chars[i][j], charRects[i][j])
                    solution[i][j] = 0
#                    print (solution)
                    
                
                     
        drawGrid()
        drawButton((0,0,0),(CELLSIZE // 2, WINDOWSIZE + CELLSIZE // 2, int(3.75 * CELLSIZE), CELLSIZE ), 'Check')
        drawButton((0,0,0),(int (4.75*CELLSIZE), WINDOWSIZE + CELLSIZE // 2, int(3.75 * CELLSIZE), CELLSIZE ), 'Blank')
        drawButton((0,0,0),(CELLSIZE // 2, WINDOWSIZE + 2 * CELLSIZE, int(3.75 * CELLSIZE), CELLSIZE ), 'Reset')
        drawButton((0,0,0),(int (4.75*CELLSIZE), WINDOWSIZE + 2 * CELLSIZE, int(3.75 * CELLSIZE), CELLSIZE ), 'Solve')
        drawButton((0,0,0),(CELLSIZE // 2, WINDOWSIZE + int(3.5 * CELLSIZE), int(3.75 * CELLSIZE), CELLSIZE ), 'New')
        drawButton((0,0,0),(int (4.75*CELLSIZE), WINDOWSIZE + int(3.5 * CELLSIZE), int(3.75 * CELLSIZE), CELLSIZE ), 'Quit')
        pg.display.update()
        FPSCLOCK.tick(FPS)

    
if __name__ == "__main__":
    main()
