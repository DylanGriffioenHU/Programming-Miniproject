from tkinter import *
from PIL import ImageTk, Image
import pyqrcode
import os
root = Tk()

def showCustomerMoviesFrame():
    """"creert de movie frame voor klanten waarin ze een lijst met movie elementen zien die uit aangebodenFilms.txt gehaald worden"""
    customerMoviesFrame.pack()


def showFilmCustomer(movieIndex):
    """""neemt de megegeven film index om de gegevens van die film te openen in een nieuw venster"""
    infile = open("aangebodenFilms.txt", "r")
    films = infile.readlines()
    gesplitteFilm = []
    for waardes in films:
        gesplitteFilm.append(waardes.split('^'))

    root11 = Tk()
    showFilmDescription = Frame(master=root11)
    showFilmDescription.pack()
    lab1 = Label(showFilmDescription, anchor=W, justify=LEFT,  text = '{} \n jaar: {} \n regisseur(s): {} \n cast: {} \n genre: {} \n duur: {} \n synopsis: {} \n aanbieder: {}'.format(gesplitteFilm[movieIndex][0], gesplitteFilm[movieIndex][1], gesplitteFilm[movieIndex][2], gesplitteFilm[movieIndex][3], gesplitteFilm[movieIndex][4], gesplitteFilm[movieIndex][5], gesplitteFilm[movieIndex][6], gesplitteFilm[movieIndex][7]))
    lab1.pack()
    movieDescriptionButton = Button(master=showFilmDescription, text='Reserveren', command= lambda:qrcode(gesplitteFilm[movieIndex][0],gesplitteFilm[movieIndex][7]))
    movieDescriptionButton.pack()



def qrcode(movieName, provider):
    """"pakt de globale username van de klant de titel van de film en de naam van de provider van die film en maakt daar een qrcode van slaat die op en toont het op het scherm"""
    global Username
    Username = 'Dylan'
    editedProvider = provider.replace("\n", "")
    QR = pyqrcode.create('{} \n{} \n{}'.format(Username,movieName, editedProvider))
    editedMovieName = movieName.replace(" ", "")
    QR.png('{}{}{}.png'.format(Username, editedMovieName, editedProvider), scale=6)

    novi = Toplevel()
    canvas = Canvas(novi, width=350, height=300)
    canvas.pack(expand=YES, fill=BOTH)
    qrImg = PhotoImage(file='{}{}{}.png'.format(Username, editedMovieName, editedProvider))
    # image not visual
    canvas.create_image(50, 10, image=qrImg, anchor=NW)
    # assigned the gif1 to the canvas object
    canvas.gif1 = qrImg
    qrCodeName = '{}{}{}.png'.format(Username, editedMovieName, editedProvider)
    with open('{}Klanten.txt'.format(editedProvider),'a') as providerCustomers:
        bestelling = "{}^{}^{}\n".format(Username, editedMovieName, qrCodeName)
        providerCustomers.write(bestelling)


with open('aangebodenFilms.txt') as movies:
    splitMovieList = []
    for movie in movies:
        movieValues = movie.split("^")
        splitMovieList.append(movieValues)

with open('aangebodenFilms.txt') as movies:
    #genereert een blauw poster veld een titel en een beschrijving knop voor iedere film in aangebodenFilms.txt
    #Daarvan zet het 4 elementen op een rij en begint dan met een nieuwe rij
    customerMoviesFrame = Frame(master=root)
    teller = 1
    rowteller = 1
    row = 1
    row2 = 2
    row3 = 3
    for movie in movies:
        movieValues = movie.split("^")
        movieIndex = splitMovieList.index(movieValues)
        title = movieValues[0]
        movieCoverTitleLabel = Label(master=customerMoviesFrame,
                                  text=title,
                                  background='blue',
                                  foreground='black',
                                  font=('Helvetica', 12, 'bold italic'),
                                  width=25,
                                  height=5)
        customerMovieTitleLabel = Label(master=customerMoviesFrame, text='{}'.format(title))
        customerMovieButton = Button(master=customerMoviesFrame, text='Meer info', command=lambda movieIndex=movieIndex:showFilmCustomer(movieIndex))
        movieCoverTitleLabel.grid(row=row, column=teller)
        customerMovieTitleLabel.grid(row=row2, column=teller)
        customerMovieButton.grid(row=row3, column=teller)

        teller += 1
        rowteller += 1
        if rowteller == 5:
            teller = 1
            rowteller = 1
            row += 3
            row2 += 3
            row3 += 3


showCustomerMoviesFrame()
root.mainloop()
