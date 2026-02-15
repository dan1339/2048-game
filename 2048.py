"""
Daniel Rostin
2048
"""
#Imports
import random
import os 

#~~~~~~~~~~COLOUR CODES~~~~~~~~~
class Colour:
    Purple = "\033[95m"
    Blue = "\033[94m"
    Cyan = "\033[96m"
    Green = "\033[92m"
    Yellow = "\033[93m"
    Red = "\033[91m"
    LightCyan = "\033[96m"
    LightGreen = "\033[92m"
    LightBlue = "\033[94m"
    Magenta = "\033[95m"
    DarkGreen = "\033[32m"
    End = "\033[0m"

#~~~~~~~~~COLOUR ASSIGNMENT FOR NUMBERS~~~
ColourAssignment = {
    0: Colour.End,
    2: Colour.Cyan,
    4: Colour.Green,
    8: Colour.Yellow,
    16: Colour.Red,
    32: Colour.Purple,
    64: Colour.Blue,
    128: Colour.LightCyan,
    256: Colour.LightGreen,
    512: Colour.LightBlue,
    1024: Colour.Magenta,
    2048: Colour.DarkGreen,
}

#~~~BOARD~~~~
board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

#~~~~~~~~INTRO SCREEN~~~~~~~~~
def fnWelcome():
    #Pre: Display title page
    #Post: Clears screen once enter pressed and game starts
    os.system("cls")
    print(f"""{Colour.Blue}
 ________  ________  ________   ___  _______   ___       ________      
|\   ___ \|\   __  \|\   ___  \|\  \|\  ___ \ |\  \     |\   ____\     
\ \  \_|\ \ \  \|\  \ \  \  \  \ \  \ \   __/|\ \  \    \ \  \___|_    
 \ \  \  \ \ \   __  \ \  \  \  \ \  \ \  \_|/_\ \  \    \ \_____  \   
  \ \  \__\ \ \  \ \  \ \  \  \  \ \  \ \  \_|\ \ \  \____\|____|\  \  
   \ \_______\ \__\ \__\ \__\  \__\ \__\ \_______\ \_______\____\_\  \ 
    \|_______|\|__|\|__|\|__| \|__|\|__|\|_______|\|_______|\_________
                                                           \|_________|                                                      
  _______  ________  ___   ___  ________                               
 /  ___  \|\   __  \|\  \ |\  \|\   __  \                              
/__/|_/  /\ \  \|\  \ \  \__\  \ \  \|\  \                             
|__|//  / /\ \  \ \  \ \______  \ \   __  \                            
    /  /_/__\ \  \ \  \|_____|\  \ \  \|\  \                           
   |\________\ \_______\     \ \__\ \_______\                          
    \|_______|\|_______|      \|__|\|_______|                          
{Colour.End}""")
    print(f"{Colour.Cyan}Daniel's 2048 - Try to reach the number 2048 without filling up the board!{Colour.End}")
    input("""Press ENTER to start the game...""")
    os.system("cls")

#~~~~~~~~~~~GRID~~~~~~~~~~~~~
def fnDisplay(board):
    #Pre: Board is set up - list of lists with corresponding values for each tile
    #Post: Displays current state of board
    os.system("cls")
    print("_______" * 4 + "_")
    for row in range(4):
        line = ""
        for element in range(4):
            if board[row][element] == 0:
                line += "|      "
            else:
                colour = ColourAssignment.get(board[row][element], Colour.End)
                value = str(board[row][element])
                line += f"|{colour}{value.center(6)}{Colour.End}"
        print(line + "|")
        print("|______" * 4 + "|")

#~~~~~TRANPOSING/ROTATING BOARD~~~~~
def fnTranspose(board):
    #Pre: Board is set up as a list of lists 
    #Post: Switches all rows and columns by taking apart the lists and making tuples - used in up and down
    return [list(row) for row in zip(*board)]

#~~~~~~~LEFT~~~~~~~~~~
def fnMergeLeft(board):
    #Pre: Board is set up as a list of lists
    #Post: Moves all numbers to the left and merges any of the same number 
    moved = False
    for row in range(0, 4):
        NewRow = [tile for tile in board[row] if tile != 0]
        for num in range(len(NewRow) - 1):
            if NewRow[num] == NewRow[num + 1]:
                NewRow[num] *= 2
                NewRow[num + 1] = 0
                moved = True
        NewRow = [tile for tile in NewRow if tile != 0]
        if board[row] != NewRow + [0] * (4 - len(NewRow)):
            moved = True
        board[row] = NewRow + [0] * (4 - len(NewRow))
    return board, moved

#~~~~~~~RIGHT~~~~~~~~~~
def fnMergeRight(board):
    #Pre: Board is set up as a list of lists and fnMergeLeft is made
    #Post: All tiles are merged to the right
    ReverseBoard = [row[::-1] for row in board]
    ReverseBoard, moved = fnMergeLeft(ReverseBoard)  
    ReverseBoard = [row[::-1] for row in ReverseBoard] 
    return ReverseBoard, moved

#~~~~~~UP~~~~~~~
def fnMergeUp(board):
    #Pre: Board is set up as a list of lists and fnMergeLeft and fnTranspose are made 
    #Post: All tiles are merged upwards
    TransposedBoard = fnTranspose(board)  
    ReverseBoard, moved = fnMergeLeft(TransposedBoard)  
    return fnTranspose(ReverseBoard), moved 

#~~~~~~~~DOWN~~~~~~~~
def fnMergeDown(board):
    #Pre: Board is set up as a list of lists and fnMergeLeft are made
    #Post: All tiles are merged downwards
    TransposedBoard = fnTranspose(board) 
    ReverseBoard, moved = fnMergeRight(TransposedBoard)  
    return fnTranspose(ReverseBoard), moved

#~~~~~~~~TILE SPAWNING~~~~~~~~~
def fnAddTile(board):
    #Pre: Board is set up as a list of lists and random module imported
    #Post: New tiles will randomly spawn
    NewTile = 0
    while NewTile == 0:
        row = random.randint(0,3)
        element = random.randint(0,3)
        if int(board[row][element]) == 0:
            board[row][element] = random.randrange(2, 5, 2)
            NewTile += 1

#~~~~~~~CHECKS~~~~~~~~
def WinCheck(board):
    #Pre: Board is set up as a list of lists
    #Post: Returns true if tile 2048 is found on board
    return any(2048 in row for row in board)

def LoseCheck(board):
    #Pre: Board is set up as a list of lists
    #Post: Returns True if the board is full
    for row in range(4):
        for element in range(4):
            if board[row][element] == 0:
                return False
    return True  

#~~~~Gameplay~~~~~~~~
def fnGame():
    #Pre: Merge functions + Win/Lose Check are defined
    #Post: Continues gameplay until Win/Lose Checks are met
    board = [[0] * 4 for _ in range(4)]
    fnAddTile(board)
    fnAddTile(board)

    fnWelcome()
    fnDisplay(board)
    while True:
        Move = input("Enter move (wasd): ").lower()
        ReverseBoard = None
        BoardMoved = False 

        if Move == "w":
            ReverseBoard, BoardMoved = fnMergeUp(board)
        elif Move == "a":
            ReverseBoard, BoardMoved = fnMergeLeft(board)
        elif Move == 's':
            ReverseBoard, BoardMoved = fnMergeDown(board)
        elif Move == 'd':
            ReverseBoard, BoardMoved = fnMergeRight(board)
        else:
            print("Invalid input. Use 'w', 'a', 's', 'd'.")
            continue

        if BoardMoved:
            fnAddTile(ReverseBoard)
            board = ReverseBoard 
            fnDisplay(board)  

        if WinCheck(board):
            print("""
 ________  ________  ________  ________     
|\   ____\|\   __  \|\   __  \|\   ___ \    
\ \  \___|\ \  \|\  \ \  \|\  \ \  \_|\ \   
 \ \  \  __\ \  \ \  \ \  \ \  \ \  \  \ \  
  \ \  \|\  \ \  \ \  \ \  \ \  \ \  \_ \ \ 
   \ \_______\ \_______\ \_______\ \_______
    \|_______|\|_______|\|_______|\|_______|                              
    ___  ________  ________  ___            
   |\  \|\   __  \|\   __  \|\  \           
   \ \  \ \  \|\  \ \  \|\ /\ \  \          
 __ \ \  \ \  \ \  \ \   __  \ \  \         
|\  \ _\  \ \  \ \  \ \  \|\  \ \__\        
\ \________\ \_______\ \_______\|__|        
 \|________|\|_______|\|_______|   ___      
                                  |\__\     
                                  \|__|""")
            break

        if LoseCheck(board):
            print("""
 ___       __   ________  _____ ______   ________            
|\  \     |\  \|\   __  \|\   _ \  _   \|\   __  \           
\ \  \    \ \  \ \  \|\  \ \  \ \__\ \  \ \  \|\  \          
 \ \  \  __\ \  \ \  \ \  \ \  \ |__| \  \ \   ____\         
  \ \  \|\__\_\  \ \  \ \  \ \  \    \ \  \ \  \___|         
   \ \____________\ \_______\ \__\    \ \__\ \__\            
    \|____________|\|_______|\|__|     \|__|\|__|                                            
 ___       __   ________  _____ ______   ________  ___       
|\  \     |\  \|\   __  \|\   _ \  _   \|\   __  \|\  \      
\ \  \    \ \  \ \  \|\  \ \  \ \__\ \  \ \  \|\  \ \  \     
 \ \  \  __\ \  \ \  \ \  \ \  \ |__| \  \ \   ____\ \  \    
  \ \  \|\__\_\  \ \  \ \  \ \  \    \ \  \ \  \___|\ \__\   
   \ \____________\ \_______\ \__\    \ \__\ \__\    \|__|   
    \|____________|\|_______|\|__|     \|__|\|__|        ___ 
                                                        |\__|
                                                        \|__|""")
            break


fnGame() 