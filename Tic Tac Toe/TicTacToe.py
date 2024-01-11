import random
from tkinter import *

Evaluation = 0
PlayerScore = 0
AIScore = 0
AIProcessing = False


def HoverEntre(List, num):
    global Board, Winner, AIProcessing
    k = 0
    nNum = num
    while nNum >= 3:
        nNum -= 3
        k += 1
    if Board[k][nNum] == 0 and Winner == "GameNotOver" and not AIProcessing:
        if Player == FirstPlayer:
            List[num].config(text="X", fg="#ffa8a8")
        else:
            List[num].config(text="0", fg="#a6a6ff")


def HoverExit(List, num):
    global Board
    k = 0
    nNum = num
    while nNum >= 3:
        nNum -= 3
        k += 1
    if Board[k][nNum] == 0:
        List[num].config(text="")


def PlayAgain():
    global Board, LabelList, FirstPlayer, Player, Winner
    WinLabel.config(text="")
    for i in range(9):
        LabelList[i].config(text="")
    for i in range(3):
        for j in range(3):
            Board[i][j] = 0
    Winner = "GameNotOver"
    if FirstPlayer == "Human":
        FirstPlayer = "AI"
    elif FirstPlayer == "AI":
        FirstPlayer = "Human"
    Player = FirstPlayer
    if Player == "AI":
        Turn(LabelList, 0)
    seperator4.pack()
    PlayAgainButton.pack_forget()


def AiMove():
    global Board, AIProcessing \
        , Evaluation
    AIProcessing = True
    bestscore = -100
    bestMove = ""
    for i in range(3):
        for j in range(3):
            if Board[i][j] == 0:
                Evaluation += 1
                Board[i][j] = "AI"
                score = minmax(False, 1, -100, 100)
                Board[i][j] = 0
                if bestscore < score:
                    bestscore = score
                    bestMove = i * 3 + j
    AIProcessing = False
    Turn(LabelList, bestMove)
    print(Evaluation)
    Evaluation = 0


def minmax(isMaximizing, Depth, alpha, beta):
    global Board \
        , Evaluation
    score = 0
    if isMaximizing:
        bestscore = -100
    else:
        bestscore = 100
    nWinner = CheckWinner()
    if nWinner == "AI":
        return 10 - Depth
    elif nWinner == "Human":
        return -10 + Depth
    elif nWinner == "Tie":
        return 0

    for i in range(3):
        for j in range(3):
            if Board[i][j] == 0:
                Evaluation += 1
                if isMaximizing:
                    Board[i][j] = "AI"
                else:
                    Board[i][j] = "Human"

                score = minmax(not isMaximizing, Depth + 1, alpha, beta)

                Board[i][j] = 0

                if isMaximizing:
                    bestscore = max(score, bestscore)
                    alpha = bestscore
                else:
                    bestscore = min(score, bestscore)
                    beta = bestscore
                if beta <= alpha:
                    break
    return bestscore


def CheckWinner():
    global Board

    for i in range(3):
        if Board[0][i] == Board[1][i] == Board[2][i] == "Human":
            return "Human"
        elif Board[0][i] == Board[1][i] == Board[2][i] == "AI":
            return "AI"

        if Board[i][0] == Board[i][1] == Board[i][2] == "Human":
            return "Human"
        elif Board[i][0] == Board[i][1] == Board[i][2] == "AI":
            return "AI"

    if Board[0][0] == Board[1][1] == Board[2][2] == "Human":
        return "Human"
    elif Board[0][0] == Board[1][1] == Board[2][2] == "AI":
        return "AI"

    if Board[0][2] == Board[1][1] == Board[2][0] == "Human":
        return "Human"
    elif Board[0][2] == Board[1][1] == Board[2][0] == "AI":
        return "AI"

    for i in range(3):
        for j in range(3):
            if Board[i][j] == 0:
                return "GameNotOver"

    return "Tie"


def Turn(List, Num):
    global Board, Player, Winner, PlayerScore, AIScore, AIProcessing

    k = 0
    nNum = Num
    while nNum >= 3:
        nNum -= 3
        k += 1
    if Board[k][nNum] == 0 and Winner == "GameNotOver" and not AIProcessing:
        if FirstPlayer == Player:
            List[Num].config(text="X", fg="Red")
        else:
            List[Num].config(text="0", fg="Blue")
        window.update()
        # time.sleep(1)
        # turnX0 = not turnX0

        Board[k][nNum] = Player
        if Player == "Human":
            Player = "AI"
        elif Player == "AI":
            Player = "Human"

        Winner = CheckWinner()
        if Winner == "GameNotOver":
            if Player == "AI":
                AiMove()
            # else:
            #     AiMove()
        else:
            if Winner == "Human":
                PlayerScore += 1
                HumanPlayerScoreLabel.config(text=PlayerScore)
                WinLabel.config(text="Player Wins!")
            elif Winner == "AI":
                AIScore += 1
                AIPlayerScoreLabel.config(text=AIScore)
                WinLabel.config(text="Computer Wins!")
            elif Winner == "Tie":
                WinLabel.config(text="Tie!")

            seperator4.pack_forget()
            PlayAgainButton.pack()


window = Tk()
window.geometry("700x700")
window.title("Tic-Tac-Toe")
icon = PhotoImage(file="Images\\tic-tac-toe.png")
window.iconphoto(True, icon)
window.config(background="white")

MainGame = Frame(window,
                 width=400,
                 height=400,
                 bg="White",
                 border=True)
MainGame.grid(row=0, column=0,
              padx=20, pady=20)
ScoreBoard = Frame(window,
                   width=400,
                   height=400,
                   bg="White",
                   border=True)
ScoreBoard.grid(row=0, column=1)

HumanPlayerLabel = Label(ScoreBoard, text="Player", border=True, height=1, width=10, relief="ridge", font=("Arial", 25),
                         bg="lightblue", compound="top")
HumanPlayerLabel.pack()

HumanPlayerScoreLabel = Label(ScoreBoard, text=PlayerScore, border=True, height=1, width=10, relief="ridge",
                              font=("Arial", 25), bg="White", compound="top")
HumanPlayerScoreLabel.pack()

seperator1 = Label(ScoreBoard, border=True, height=1, width=8, font=("Arial", 30), bg="white", compound="top")
seperator1.pack()

AIPlayerLabel = Label(ScoreBoard, border=True, text="Computer", height=1, width=10, relief="ridge", font=("Arial", 25),
                      bg="lightblue", compound="top")
AIPlayerLabel.pack()

AIPlayerScoreLabel = Label(ScoreBoard, border=True, text=AIScore, height=1, width=10, relief="ridge",
                           font=("Arial", 25),
                           bg="White", compound="top")
AIPlayerScoreLabel.pack()

seperator2 = Label(ScoreBoard, border=True, height=1, width=8, font=("Arial", 30), bg="white", compound="top")
seperator2.pack()

n = 0
LabelList = []
turnX0 = True
Winner = "GameNotOver"
Board = [[0 for x in range(3)] for y in range(3)]
Ran = random.randint(0, 1)
# Ran = 0
if Ran == 0:
    Player = "Human"
else:
    Player = "AI"
FirstPlayer = Player

for i in range(3):
    for j in range(3):
        LabelList.append(Label(MainGame,
                               border=True,
                               height=1,
                               width=2,
                               relief="ridge",
                               font=("Arial", 90),
                               bg="pink"))
        LabelList[n].grid(row=i, column=j)
        LabelList[n].bind("<Button>",
                          lambda event, Number=n:
                          Turn(LabelList, Number))
        LabelList[n].bind("<Enter>",
                          lambda event, Number=n:
                          HoverEntre(LabelList, Number))
        LabelList[n].bind("<Leave>",
                          lambda event, Number=n:
                          HoverExit(LabelList, Number))

        n += 1
seperator3 = Label(ScoreBoard, border=True, height=1, width=8, font=("Arial", 30), bg="white", compound="top")
seperator3.pack()

seperator4 = Label(ScoreBoard, border=True, height=1, width=1, font=("Arial", 34), bg="white", compound="top")
seperator4.pack()

PlayAgainButton = Button(ScoreBoard, text="Play Again", border=True, height=1, width=8, font=("Arial", 20),
                         bg="white", compound="top", command=PlayAgain)

# PlayAgainButton.bind("<Button>", PlayAgain)
# PlayAgainButton.pack()

WinLabel = Label(window, text="", border=True, font=("Arial", 25), bg="white")
WinLabel.grid(row=1, column=0)


def initializeAIMove():
    if Player == "AI":
        Turn(LabelList, 0)
    # else:
    #     AiMove()


window.after(100, initializeAIMove)
window.mainloop()
