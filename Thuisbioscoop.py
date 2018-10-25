import requests
import time
import xmltodict
from tkinter import *

vandaag = time.strftime("%d-%m-%Y")

api_url = 'http://api.filmtotaal.nl/filmsoptv.xml?apikey=8bgs2dsacfezw3eu04jetb4dcvon1a6i&dag={}&sorteer=0'.format(vandaag)
response = requests.get(api_url)

filmXML = xmltodict.parse(response.text)

def openFilm():
    """haalt alle info van de films uit de API"""
    with open("alleFilms.txt", "w") as file:
        for film in filmXML['filmsoptv']['film']:
            titel = film['titel']
            jaar = film['jaar']
            regisseur = film['regisseur']
            regisseur = regisseur.replace(':',', ')
            cast = film['cast']
            cast = cast.replace(':', ', ')
            genre = film['genre']
            genre = genre.replace(':', ', ')
            duur = film['duur']
            synopsis = film['synopsis']
            info = "{}^{}^{}^{}^{}^{}^{} \n".format(titel, jaar, regisseur, cast, genre, duur, synopsis)
            file.write(info)

openFilm()

infile = open("alleFilms.txt", "r")
films = infile.readlines()
gesplitteFilm = []
for waardes in films:
    gesplitteFilm.append(waardes.split('^'))

def showFilm1(index):
    root11 = Tk()
    listb11 = Listbox(root11)
    button = Button(master=root11, text='AANBIEDEN', command=lambda index=index:aanbieden(index))
    lab1 = Label(root11, anchor=W, justify=LEFT, font=("Arial", 9),text='{} \nJAAR:  {} \n'
    'REGISSEUR(s):  {} \nCAST:  {} \nGENRE:  {} \nDUUR:  {} \nSYNOPSIS:  {} \n'.format( gesplitteFilm[index][0],
    gesplitteFilm[index][1], gesplitteFilm[index][2], gesplitteFilm[index][3], gesplitteFilm[index][4], gesplitteFilm[index][5],
    gesplitteFilm[index][6]))
    lab1.pack()
    button.pack()

def aanbieden(index):
    username = 'naam'
    infileAanbieden = open('aangebodenFilms.txt', 'a')
    woord =''
    gesplitteFilm1 = gesplitteFilm[index]
    for film in gesplitteFilm1:
        film = film.replace("\n", '')
        woord +="{}{}".format(film,'^')
    woord += username + '\n'
    infileAanbieden.write(woord)

root1 = Tk()
listb1 = Listbox(root1)
infileAangeboden = open('aangebodenFilms.txt','r')
leesAangeboden = infileAangeboden.readlines()
aangeboden = []
for line in leesAangeboden:
    splitline = line.split('^')
    aangeboden.append(splitline[0])
for titel in gesplitteFilm:
    index = gesplitteFilm.index(titel)
    if titel[0] in aangeboden:
        continue
    else:
        button = Button(master=root1, text=titel[0], command=lambda index=index: showFilm1(index))
    button.pack()

root1.mainloop()
