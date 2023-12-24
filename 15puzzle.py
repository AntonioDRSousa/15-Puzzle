###############################################
#                                             #
#                  15 PUZZLE                  #
#                                             #
###############################################

from tkinter import *
import random
import sys
import time

### control variables ###

# square width, dimension of window and position where board are drawn
sw = 50
dim = 600
pb = (dim-sw*4)//2

# informs if game are on, used for prevent bugs
game_on = True

# tick in seconds of game
tsec = -1

# id for stop timer
id_time = None

# help in game
inf = "Press key 'N' to new game and key 'Q' to quit game"

### show help information ###
def showInf():
    canvas.create_text(dim//2, pb//2 , text=inf, fill="black", font=('Helvetica 15 bold'))

### update clock in game ###
def timer():
    global label, tsec, game_on, id_time
    
    tsec+=1

    # convert tsec to Hours : Minutes : Seconds
    seconds = tsec%60
    minutes = (tsec//60)%60
    hours = (tsec//3600)
    
    label.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    # each 1 second execute timer()
    id_time=label.after(1000, timer) 
    

### function after key press events ###
def key(event):
    global canvas, board, ntext, hl, tsec, label, id_time
    
    # exit game
    if (event.char).lower() == "q":
        win.destroy()

    # new game
    elif (event.char).lower() == "n":
        
        # if timer is on then finish timer
        if id_time!=None:
            label.after_cancel(id_time)

        # init game
        canvas.delete("all")
        showInf()
        game_on = True    
        board, ntext, hl = createBoard()

        # init timer
        tsec = -1
        timer()
        
### check victory ###
def vict(board):
    # return correct number in victory position
    def calc(x,y):
        return (j*4)+(i+1)
    
    for i in range(0,4):
        for j in range(0,4):
            # flag for exit loop
            if ((i,j)==(3,3)):
                return True
            
            # check if square is empty or board hasn't correct number
            elif ((board[i][j]==" ")or(board[i][j]!=str(calc(i,j)))):
                return False

### function after event of mouse click ###            
def getorigin(eventorigin):
    global board, ntext, hl, pb, sw, game_on

    # get position in board
    def getPos(z):
        return (z-pb)//(sw+1)


    # check click in square of board
    def checkBoard(x,y):
        def checkB(z):
            return ((z>=0)and(z<=3))
        return (checkB(x) and checkB(y))

    # check if square empty are neighbor of square
    def checkEmpty(t1,t2):
        def cmp(x,y):
            return (abs(x-y)==1)
        b1 = ((t1[0]==t2[0])and(cmp(t1[1],t2[1])))
        b2 = ((t1[1]==t2[1])and(cmp(t1[0],t2[0])))
        return (b1 or b2)

    # flag
    if (not game_on):
        return

    # get position of click and convert to board coordenates
    x , y = getPos(eventorigin.x) , getPos(eventorigin.y)

    # move square
    if (checkBoard(x,y) and checkEmpty((x,y),hl)):
        canvas.itemconfig(ntext[x][y], text=board[hl[0]][hl[1]])
        canvas.itemconfig(ntext[hl[0]][hl[1]], text=board[x][y])
        board[x][y], board[hl[0]][hl[1]] = board[hl[0]][hl[1]], board[x][y]
        hl = (x,y)

        # check victory
        if vict(board):
            canvas.create_text(pb+(sw*2), pb+(sw*5), text="WIN", fill="black", font=('Helvetica 15 bold'))
            game_on = False

### create board of game ###            
def createBoard():
    global pb, sw

    # calculate position for place squares
    def cpos(z):
        return pb+(sw+1)*z

    # define numbers of game and shuffle them
    num = [str(x) for x in range(1,16)]+[" "]
    num_cpy = num.copy()
    while (num==num_cpy):
        random.shuffle(num)

    # create matrix of board and of text components
    board = [[None]*4 for _ in range(4)]
    ntext = [[None]*4 for _ in range(4)]

    # defined middle of width's square
    d = (sw//2)


    # draw squares of board and text of each square
    # build matrix of board
    for i in range(0,4):
        for j in range(0,4):
            # (x,y) define position of square
            # n is a number removed of list for insert in square
            x , y , n = cpos(i) , cpos(j) , num.pop()

            # draw square and text of square
            # build matrix board
            canvas.create_rectangle(x,y,x+sw,y+sw,fill="blue",width=4) 
            ntext[i][j]=canvas.create_text(x+d, y+d, text=n, fill="black", font=('Helvetica 15 bold'))
            board[i][j]=n

            # store square that has no number
            if (n==" "):
                hl=(i,j)
                
    return board, ntext, hl  

# init window and screen
win = Tk()
win.title("15 PUZZLE")
win.geometry(str(dim)+"x"+str(dim))
win.resizable(False,False)
canvas = Canvas(win,width=dim,height=dim-100,bg="cyan")
canvas.pack()
showInf()
label = Label(win, width = dim, font = ("arial", 50),bg="black",fg="#00FF00")
label.pack(expand=1,fill='both')

# events    
canvas.bind("<Button-1>",getorigin)
win.bind("<KeyPress>", key)

win.mainloop()
