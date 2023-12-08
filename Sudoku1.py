import random
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox


class App(Tk):
    def __init__(self, *args, **kwargs): 
        Tk.__init__(self, *args, **kwargs)

        #adding title to window along with font
        self.wm_title("Sudoku")
        self.title_font = tkfont.Font(family="Georgia",size=50, weight="bold",slant="italic")
        self.second_font = tkfont.Font(family="Georgia",size=25, weight="bold")

        # container to contain all frames on top of each other
        self.container = Frame(self, height=500, width=500)
        self.container.pack(side="top",fill="both", expand=True)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PlayPage, EndPage):
            page_name = F.__name__
            frame = F(parent=self.container,controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(Frame):
    # forces user to choose difficulty before playing
    def check_choice(self,button_difficulty):
        option_chosen = False
        if button_difficulty:
            option_chosen = True
        if option_chosen: # start can be clicked when a difficulty is chosen
            self.play_button.config(state="normal")
        else:
            self.play_button.config(state="disabled")

    # takes chosen difficulty and removes squares respectively
    def set_difficulty(self, value):
        if value == 1:
            self.difficulty = 36
        elif value == 2:
            self.difficulty = 46
        elif value == 3:
            self.difficulty = 56


    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # initializing variables 
        self.controller = controller
        self.difficulty = 0
        label = Label(self, text="Sudoku", font=controller.title_font)
        label.pack(side="top", fill="x", pady=40)

        # difficulty buttons that check if button has been clicked and if so, set difficulty to chosen difficulty
        easy_button = ttk.Button(self, text="Easy", command=lambda: [self.check_choice(1), self.set_difficulty(1)])
        medium_button = ttk.Button(self, text="Medium", command=lambda: [self.check_choice(2), self.set_difficulty(2)])
        hard_button = ttk.Button(self, text="Hard", command=lambda: [self.check_choice(3), self.set_difficulty(3)])
        
        # packing all buttons in frame
        easy_button.pack()
        medium_button.pack()
        hard_button.pack()

        # initializes start button as disabled, clicking on it transfers to PlayPage
        self.play_button = Button(self, text="Play", state=DISABLED,
                            command=lambda: controller.show_frame("PlayPage"))
        self.play_button.bind("<Button-1>", self.check_choice)
        self.play_button.pack()

class PlayPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.complete = False # checks if sudoku board has been cleared

        # Create Sudoku object and generate board
        self.sudoku = Sudoku()
        self.sudoku.generate(self.controller.frames["StartPage"].difficulty)
        
        self.gui_frame = Frame(self)
        self.gui_frame.pack(side=TOP, pady=10)
        self.gui = SudokuGUI(self.gui_frame, self.sudoku, self.sudoku.solution, self.controller)

        # Back button at bottom of screen to return to start screen
        back_button = Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(fill=X,side=BOTTOM)

class EndPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        congrats_label = Label(self, text="Congratulations!", font=controller.second_font)
        congrats_label.pack(pady=10)

        play_again_button = Button(self, text="Play Again",
                                   command=lambda: controller.show_frame("StartPage"))
        play_again_button.pack(pady=2)

        quit_button = Button(self, text="Quit",
                             command=self.quit)
        quit_button.pack(pady=2)

        back_button = Button(self, text="Back to Menu",
                             command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=2)


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

    def generate(self, num_remove): # generates random possible inputs for 3 diagonal boxes from top left to bottom right

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

        self.removeSquares(46) # removes desired amount of squares and updates grid
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

class SudokuGUI:
    # creates gui for sudoku board, creating window and grid
    def __init__(self, parent, sudoku, solution, controller):
        self.sudoku = sudoku
        self.solution = solution
        self.controller = controller
        self.frame = Frame(parent)
        self.frame.pack()
        self.create_grid()

    def create_buttons(self):
        self.check_button = Button(self.frame, state=DISABLED, text="Check", command=self.check_solution)
        self.clear_button = Button(self.frame, text="Clear", command=self.clear_board)
        self.solve_button = Button(self.frame, text="Solve", command=self.solve)
        
        self.check_button.grid(row=9, column=0, columnspan=3, sticky="nsew")
        self.clear_button.grid(row=9, column=3, columnspan=3, sticky="nsew")
        self.solve_button.grid(row=9, column=6, columnspan=3, sticky="nsew")

    def check_input(self, event):
        has_input = False
        for i in range(9):
            for j in range(9):
                if self.entry_grid[i][j] is not None and self.entry_grid[i][j].get() != "":
                    has_input = True
                    break
            if has_input:
                break
        if has_input:
            self.check_button.configure(state=NORMAL)
        else:
            self.check_button.configure(state=DISABLED)

    # ensures that only digits 1-9 can be entered
    def check_number(self,P):
        digits = '123456789'
        try:
            if P in digits:
                if len(P) == 0 or len(P) <= 1 and P.isdigit():
                    return True
                else:
                    return False
            else:
                return False
        except TypeError:
            return False
            
        
    def create_grid(self):
        self.entry_grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.sudoku.board[i][j]

                if value == 0:
                    self.entry = Entry(self.frame, validate="key", validatecommand=(self.frame.register(self.check_number), '%P'), width=2, justify=CENTER, font=('Georgia 20'), relief=RAISED)
                    self.entry.grid(row=i, column=j, sticky="nsew")
                    self.entry.bind("<KeyRelease>",self.check_number)
                    self.entry.bind("<KeyRelease>", self.check_input)
                    # self.entry.bind("<Configure>", self.resize)
                    row.append(self.entry)
                else:
                    self.cell = Label(self.frame, text=value, borderwidth=1, relief="solid", font=('Georgia 20'), justify=CENTER)
                    self.cell.grid(row=i, column=j, sticky="nsew")
                    row.append(None)
            self.entry_grid.append(row)
        self.entry_copy = self.entry_grid

        self.create_buttons()

    def check_solution(self):
        error = 0
        error_message = ""
        for i in range(9):
            for j in range(9):
                if self.entry_grid[i][j] is not None:
                    value = self.entry_grid[i][j].get()
                    if value == "":
                        continue
                    if int(value) != self.sudoku.solution[i][j]:
                        error_message += f"Incorrect value at row {i+1} column {j+1}\n"
                        error += 1

        if error != 0:
            messagebox.showerror("Error", error_message) # returns popup of wrong cell input
            return
        messagebox.showinfo("Success", "Your solution is correct!") # message pop-up when correct solution
        self.controller.show_frame("EndPage")
        

    def clear_board(self): # clears all prior inputs on board
        for i in range(9):
            for j in range(9):
                if self.entry_grid[i][j] is not None:
                    self.entry_grid[i][j].delete(0, "end")
        # Reset the state of the check_button to "disabled"
        self.check_button.configure(state=DISABLED)

    def solve(self):
        self.check_button.configure(state=NORMAL)
        for i in range(9):
            for j in range(9):
                if self.entry_grid[i][j] is not None:
                    self.entry_grid[i][j].delete(0, "end")
                    self.entry_grid[i][j].insert(0, self.solution[i][j])


if __name__ == "__main__":
    app = App()
    app.mainloop()