from tkinter import *
import random
import time
import threading
from tkinter.messagebox import *
from playsound import *




root = Tk()
root.geometry('700x160')
root.resizable(width = False, height = False)
root.config(bg = 'orange')

root.title('Guess That Movie')
frame1 = Frame(root, bg='cyan', width = 700, height=50, pady=3).grid(row=0, columnspan = 120)


timeLabel = Label(frame1, text='Remaining Time: ', font = "times 15 bold" , fg = 'blue', bg='cyan').grid(row = 0)

timerDigit = Label(frame1, text="", font = "times 15 bold", bg='cyan')
timerDigit.grid(row = 0 , column = 1, sticky = 'W')

totalGuess = 5
defTime = 20

remainGuess= Label(frame1, text="Chances : ", font = "times 15 bold", bg='cyan',fg = "green")
remainGuess.grid(row= 0 , column = 39)

guess = Label(frame1, text=str(totalGuess ), font = "times 15 bold",bg='cyan')
guess.grid(row = 0 , column = 40)


movie = Label(root, text="Movie", bg='orange' ,font = "times 12 bold")
movie.grid(row = 1, column = 0, pady = 15)

frame2 = Frame(root, height = 100, width = 100)
frame2.grid(row = 1, column = 1, columnspan = 100, sticky = 'W')
movieName = Label(frame2, text = '', font = "times 20 bold", bg='orange', fg = 'blue')
movieName.grid(row = 0)


inputLabel = Label(root, bg='orange',text= "Type your guess : ", font = "times 12 bold")
inputLabel.grid(row = 3, column = 0)

yourGuess = Entry(root,font = "times 15 bold")
yourGuess.grid(row = 3, column = 1, sticky = 'W')

# newGenerateButton = Button(root, text="Generate")
# newGenerateButton.grid(row = 3, column = 2)


data = {
        'PACIFICRIM' : 'it is a movie about giant man made robots',
        'HARRY POTTER':'best fantasy movie with wizards',
        'I ROBOT':'best will smith movie with robots',
        'THIS IS THE END' : 'comedy movie with a lot of comdians and actors',
        'MEN IN BLACK' : 'secret agents protecting earth from alien activities',
        'PIRATES OF THE CARRIBEAN' : 'most popular movie about pirates',
        'INTERSTELLAR' : 'movie about space exploration from cristopher nolan',
        'AVATAR' : 'best CGI masterpiece from james cameron about lives on outer planet',
        'IRON MAN' : 'the one who saved the galaxy from thanos in the end',
        'KARATE KID' : 'debut movie of son of will smith'
        }

dupData = data.copy()
name = ''
repeated = []

def generateIt():
    global dupData, name, repeated
    print(dupData)
    #getting the movie randomly

    name = random.choice(list(dupData.keys()))

    while name in repeated:
        name = random.choice(list(dupData.keys()))
    else:
        repeated.append(name)

    # randomly selecting characters to show

    k = len(name) - (len(name) // 2)

    randLocation = []


    for i in range(k):
        l = random.randint(0, len(name) - 1)
        if l not in randLocation and name[l] != ' ':
            randLocation.append(l)
        else:
            k += 1

    # generating display name
    generatedMovieName = ''

    for i in range(len(name)):
        if i in randLocation:
            generatedMovieName = generatedMovieName + name[i]
        elif name[i] == " ":
            generatedMovieName = generatedMovieName + ' '
        else:
            generatedMovieName = generatedMovieName + '_'

    generatedMovieName = ' '.join(generatedMovieName)
    movieName['text'] = generatedMovieName


#wrong answer sound
def wrongAnswer():
    playsound("sounds/Wrong-answer.mp3")


def rightAnswer():
    playsound("sounds/anime-wow-sound-effect.mp3")



# checking the answer
def checkTheGuess(event):
    global totalGuess, yourGuess,defTime
    global name
    if yourGuess.get().upper() == name:
        threading.Thread(target=rightAnswer).start()
        defTime = 20
        generateIt()
        yourGuess.delete(0, END)
        hint['text'] = ''
        # threading.Thread(target=timer).start()
        print('this is check the guess')
    else:
        threading.Thread(target=wrongAnswer).start()
        if totalGuess == 0:
            totalGuess = 5
            title = 'CHANCES GONE!'
        else:
            title = 'WRONG ANSWER!'
        totalGuess -= 1
        msg = 'The correct answer is ' + name + '\n you want to continue?'
        playAgain = askyesno(title = title, message= msg)
        if playAgain:
            generateIt()
        else:
            quit()
        yourGuess.delete(0, END)
        hint['text'] = ''

        defTime = 20
        yourGuess.delete(0, END)


    guess['text'] = totalGuess

root.bind("<Return>", checkTheGuess)


#giving the hint
def giveTheHint(event):
    global data
    global name, totalGuess
    totalGuess -= 1
    if totalGuess == 0:
        title = 'CHANCES ARE GONE!'
        msg = 'The correct answer is ' + name + '\n you want to continue?'
        playAgain = askyesno(title=title, message=msg)
        if playAgain:
            generateIt()
        else:
            quit()

    guess['text'] = totalGuess
    hint['text'] = str.title(data[name])

    print('this showing hint')


hintLabel = Label(root, bg='orange',text="Hint : ", font = "times 12 bold")
hintLabel.bind('<Button-1>', giveTheHint)
hintLabel.grid(row = 4, column = 0, padx = 10)

hint = Label(root, text="", bg='orange', font = "times 12 bold", fg="blue")
hint.grid(row = 4, column = 1, columnspan = 100, sticky = "w")

def startTheTimer():
    threading.Thread(target=timer).start()


def timer():
    global name, defTime
     #in seconds
    while defTime > 0:
        timerDigit['text'] = defTime
        defTime-=1
        time.sleep(1)
    else:

        threading.Thread(target=wrongAnswer).start()
        msg = 'The correct answer is ' + name + '\n you want to continue?'
        playAgain = askyesno(title="Time Is Up!", message=msg)
        if playAgain:
            print('we are here')
            defTime = 20
            generateIt()
            yourGuess.delete(0, END)
            hint['text'] = ''
            threading.Thread(target=startTheTimer).start()
        else:
            quit()

        # timerDigit['text'] = 'Time Up'
        # timerDigit['fg'] = "Red"
        # print('timeUP')

threading.Thread(target=startTheTimer).start()





generateIt()

root.mainloop()
