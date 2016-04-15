from graphics import *
import random
win = GraphWin("Epidemic Game",900,450)
rect = Rectangle(Point(0,0), Point(600, 450))
rect.draw(win)
colors = ["red", "blue", "green", "yellow"]
print "The color of the board is red, blue, green, and yellow."
print "Please do not choose a color from the board"
player1 = raw_input("Player 1, please choose a color  ")
player2 = raw_input("Player 2, please choose a color  ")
players = [player1 ,player2, "grey"]
board = [[0 for i in range(9)] for i in range(12)]
for a in range (12):
    for b in range (9):
        col = random.choice(range(0,4))
        board[a][b] = colors[col]



def background():
    """input: none
       output: makes the background for the score board salmon color
    """
    background = Rectangle(Point(601,0),Point(900,450))
    background.draw(win)
    background.setFill("aquamarine")



def drawBoard():
    """input none:
        output: the grid filled with random colors"""
    for a in range (12):
        for b in range (9):
            up_left = Point((50*a),(50*b))
            low_right = Point((50*(a+1)), (50*(b+1)))
            rec = Rectangle(up_left, low_right)
            rec.setFill(board[a][b])
            rec.draw(win)



def build(a,b):
    """input: two numbers, a and b
       output: a list of the colors of the four squares surrounding square at a,b
    """
    adj = []
    if a> 0:
        adj = adj + [board[a-1][b]]
    if a <11:
        adj = adj + [board[a+1][b]]
    if b > 0:
        adj = adj + [board[a][b-1]]
    if b < 8:
        adj = adj + [board[a][b+1]]
    return adj



def adjacent(pcolor,colorlist):
    """input: a color, and a list of colors
       output: Returns true if the list of colors contains the color in the argument"""
    for e in colorlist:
        if e == pcolor:
            return True
    return False
    
    

def update(a, b):
    """input: a square on the board at a,b
       output: changes only the color of sqaure clicked at board a and b
    """
    up_left = Point((50*a),(50*b))
    low_right = Point((50*(a+1)), (50*(b+1)))
    rec = Rectangle(up_left, low_right)
    rec.setFill(board[a][b])
    rec.draw(win)



def moves(a, b, color, playerc):
    """input: a square on the board at a,b, the color of the clicked square, and the color of the player
       output: changes the color of all the adjacent squares to the clicked square, to the color of the player
    """   
    if a> 0:
        if board[a-1][b] == color:
            board[a-1][b] = playerc
            update(a-1, b)
            moves(a-1,b,color, playerc)
    if a <11:
        if board[a+1][b] == color:
            board[a+1][b] = playerc
            update(a+1, b)
            moves(a+1,b,color, playerc)
    if b > 0:
        if board[a][b-1] == color:
            board[a][b-1] = playerc
            update(a, b-1)
            moves(a,b-1,color, playerc)
    if b < 8:
        if board[a][b+1] == color:
            board[a][b+1] = playerc
            update(a, b+1)
            moves(a,b+1,color, playerc)


                 
def text(point, string, color, size):
    """input: point on the window, the text as a string, color
       output: the text centered at the point, with the color and size input
    """
    words = Text(point, string)
    words.setTextColor(color)
    words.setStyle('bold')
    words.setSize(size)
    words.draw(win)



def score():
    """input: none
       output: the score of each player
    """
    black = 0
    white = 0
    for a in range (12):
        for b in range (9):
            if board[a][b] == player1:
                white = white +1
            if board[a][b] == player2:
                black = black + 1
    text(Point(750,210), "Player 1: " +str(white), player1 , 20)
    text(Point(750,240), " Player 2: " + str(black), player2 , 20)
    return [black, white]

    

def moreMoves(color, adjlist):
    """input: a color and a list of colors
       output: returns false if the list only contains the entered color
    """
    nomove = 0
    for e in adjlist:
        if e==color:
            nomove = nomove + 1
    if nomove == len(adjlist):
        return False      
    return True
             


def surrounding(playerc):
    """input: color of the player
       output: a list of all the board colors surrounding the player
    """
    sur = []
    for a in range(12):
        for b in range(9):
            if board[a][b]==playerc:
                sur = sur + build(a,b)
    if player1 in sur:
        sur = [x for x in sur if x != player1]
    if player2 in sur:
        sur = [x for x in sur if x != player2]
    return sur



def game():
    """input: none
       output: the epidemic game in graphic interface
    """
    board[0][0] = player1
    board[11][8] = player2
    play = 0
    color = [player1,player2] 
    drawBoard()
    background()
    text(Point(750,150), "Player " + str(players[play]) + " turn", "black", 22)
    score()  
    notOver = True
    while notOver:          
        valid = False
        while not valid:            #this while loop will keep looping until a click is valid
            mouse = win.getMouse()
            a = mouse.x/50
            b =  mouse.y/50
            adj = build(a,b)
            valid = adjacent(players[play], adj) and board[a][b] not in color
        color = [player1, player2 , board[a][b]]   #putting the color of the captured square in the list of colors     
        board[a][b] = players[play] 
        update(a,b)     #changes the color of clicked square to player color
        moves(a,b,color[-1],players[play])    #changes the adjacent squares of the same color to player color 
        background()
        play = (play + 1)%2     #makes the variable play alternate between 1 and 0
        text(Point(750,150), "Player " + str(players[play]) + " turn", "black", 22)
        score()
        text(Point(750,300), "last color: " + str(color[-1]), str(color[-1]) , 22)      
        notOver = moreMoves(color[-1], surrounding(players[play]))    #exits the loop if the player has no more possible moves
    scores = score()
    if scores[0] < scores[1]:
        winner = 0
        background() 
        text(Point(750,225), str(players[winner]) + " won!!!!", str(players[winner]), 22)
        text(Point(750,400), "(click anywhere to close window)", "black", 9)
    elif scores[1] < scores[0]:
        winner = 1
        background() 
        text(Point(750,225), str(players[winner]) + " won!!!!", str(players[winner]), 22)
        text(Point(750,400), "(click anywhere to close window)", "black", 9)
    else:
        scores[0] == scores[1]
        winner = 2
        background()
        text(Point(750,225), "It's a Tie!!", str(players[winner]), 22)
        text(Point(750,400), "(click anywhere to close window)", "black", 9)
    win.getMouse()          
    win.close()     #closes window when mouse is clicked

    

def MainMenu():
    rect.setFill("blue")
    text(Point(300,75), "Instructions", "white", 28)
    text(Point(300,225), "Play Game", "white", 28)
    text(Point(300,375), "Exit", "white", 22)
    mouse = win.getMouse()
    y =  mouse.y
    if 0 <= y <= 150:
        inst = Rectangle(Point(0,0), Point(600, 450))
        inst.draw(win)
        inst.setFill("white")
        text(Point(300,75), "Instructions", "black", 28)
        text(Point(300,110), "Player 1 starts the game off by clicking an adjacent square.", "black", 12)
        text(Point(300,130), "The clicked square and any adjacent squares with the same color", "black", 12)
        text(Point(300,150), "will turn the color of player 1. Then player 2 will also choose", "black", 12)
        text(Point(300,170), "an adjacent square, but the color that player 1 previously chose", "black", 12)
        text(Point(300,190), "is not an option for player 2 to claim. The goal is to try to get", "black", 12)
        text(Point(300,210), "as many squares on the board to turn the color of the player. The", "black", 12)
        text(Point(300,230), "game ends as soon as one of the players runs out of possible squares", "black", 12)
        text(Point(300,250), "to choose, and the player with the most squares at that point wins.", "black", 12)
        text(Point(300,400), "(click anywhere to start game)", "black", 9)
        win.getMouse()
        game()
    if 150 < y <= 300:
        game()
    if 300 < y <= 450:
        win.close()

MainMenu()
    





