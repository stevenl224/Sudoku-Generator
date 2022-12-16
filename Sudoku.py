# Steven Lam
# 12/15/22
# Final Project

import random

class Sudoku:

    def __init__(self):
        # initialize the Sudoku board to 0's
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        # keep empty array for solution for Sudoku board
        self.solution = []

    def findEmptySpace(self):  # finds the first empty space of the board, trasverses through every value in row then moves to next row
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)

        # returns False when no spaces are empty
        return False

    def isValidPlacement(self, num, cell): # checks to see if a number can be fitted into a specifc cell (row,col)
        if not self.board[cell[0]][cell[1]] == 0: # check to see if cell is not 0
            return False

        for col in self.board[cell[0]]: # check to see if number is already in row
            if col == num:
                return False

        for row in range(len(self.board)): # check to see if number is already in column
            if self.board[row][cell[1]] == num:
                return False

        # finds smaller 3x3 box of the cell
        blockRow = cell[0] // 3
        blockCol = cell[1] // 3

        # check to see if the number is already in the 3x3 block
        for i in range(3):
            for j in range(3):
                if self.board[i + (blockRow * 3)][j + (blockCol * 3)] == num:
                    return False
        
        return True

    def generate(self): # generates random possible inputs for 3 diagonal boxes from top left to bottom right

        numList = list(range(1, 10)) # set of numbers 1-9
        for row in range(3):
            for col in range(3):
                num = random.choice(numList)
                self.board[row][col] = num
                # removes number after it is inserted in grid
                numList.remove(num)

        numList = list(range(1, 10))
        for row in range(3, 6):
            for col in range(3, 6):
                num = random.choice(numList)
                self.board[row][col] = num
                numList.remove(num)

        numList = list(range(1, 10))
        for row in range(6, 9):
            for col in range(6, 9):
                num = random.choice(numList)
                self.board[row][col] = num
                numList.remove(num)

        self.solve() # calls solve method to complete rest of puzzle

        # appends each value to code solution 
        for row in range(9):
            rowList = []
            for col in range(9):
                rowList.append(self.board[row][col])
            self.solution.append(rowList)

        while(1):
            choice = int(input('How difficult would you like the Sudoku puzzle to be (input 1, 2, or 3)?\n1. Easy (36 squares removed)\n2. Medium (46 sqaures removed)\n3. Hard (56 sqaures removed)\n'))
            
            # changes number of squares to remove based on user input
            if choice == 1:
                squaresToRemove = 36
                break
            elif choice == 2:
                squaresToRemove = 46
                break
            elif choice == 3:
                squaresToRemove = 56
                break
            else:
                print('That was invalid, please choose a proper input.\n')
        self.removeSquares(squaresToRemove) # removes desired amount of squares and updates grid
        return 

    
    
    def removeSquares(self, squaresToRemove): # removes squares from solution generated board
        removedSquares = squaresToRemove

        # loops while there are still squares to remove
        while(removedSquares > 0):
            for row in range(9):
                for col in range(9):
                    # base condition 
                    if removedSquares == 0:
                        return
    
                    rng = random.random()
                    # removes square when rng is < 0.5, on condition cell is not already 0
                    if rng < 0.5:
                        if self.board[row][col] != 0:
                            self.board[row][col] = 0
                            removedSquares -= 1
                        else:
                            continue
        
        return


    def solve(self): # recursively solves board
        # finds first empty cell in board
        spacesAvailable = self.findEmptySpace() 

        # If there are no empty spaces, board is solved, else store first empty cell
        if not spacesAvailable:
            return True
        else:
            row, col = spacesAvailable

        # try every value from 1 to 9 as a possible value
        for n in range(1, 10):
            # check if placing the number in the empty cell is a valid move
            if self.isValidPlacement(n, (row, col)):
                self.board[row][col] = n    # assign value to cell if it is possible

                # recursively call the solve method to try to solve the board              
                if self.solve():
                    return self.board
                
                # if the solve method returns True, the board is solved and is returned
                # else Falase, the board cell will be set back to 0 and the next number will be tried
                self.board[row][col] = 0

        # if none of the numbers work in the empty cell, return False to trigger backtracking
        return False

    # prints the Sudoku board
    def print(self):
        print('The generated random board is:\n=========================')
    
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end=" ")
                if (j + 1) % 3 == 0:
                    print("|", end=" ")
            print()
            if (i + 1) % 3 == 0:
                print("-" * 21)
    
    # prints solution for Sudoku board
    def printSolution(self):
        print(f'The solution for board:\n=====================')
        for i in range(9):
            for j in range(9):
                print(self.solution[i][j], end=" ")
                if (j + 1) % 3 == 0:
                    print("|", end=" ")
            print()
            if (i + 1) % 3 == 0:
                print("-" * 21)


# three examples for three different difficulties
sudoku = Sudoku()
sudoku1 = Sudoku()
sudoku2 = Sudoku()

sudoku.generate()
# sudoku1.generate()
# sudoku2.generate()

sudoku.print()
sudoku.printSolution()
# print('--------------------------------')
# sudoku1.print()
# sudoku1.printSolution()
# print('--------------------------------')
# sudoku2.print()
# sudoku2.printSolution()