from tkinter import *
import time
import requests
import xmltodict
import pyqrcode
from io import BytesIO
from urllib.request import urlopen
from PIL import Image, ImageTk


vandaag = time.strftime("%d-%m-%Y")

api_url = 'http://api.filmtotaal.nl/filmsoptv.xml?apikey=8bgs2dsacfezw3eu04jetb4dcvon1a6i&dag={}&sorteer=0'.format(vandaag)
response = requests.get(api_url)

filmXML = xmltodict.parse(response.text)

def openFilm():
    """haalt alle info van de films uit de API"""
    with open("alleFilms.txt", "w", encoding='utf-8') as file:
        for film in filmXML['filmsoptv']['film']:
            titel = film['titel']
            cover = film['cover']
            jaar = film['jaar']
            regisseur = film['regisseur']
            regisseur = regisseur.replace(':',', ')
            cast = film['cast']
            cast = cast.replace(':', ', ')
            genre = film['genre']
            genre = genre.replace(':', ', ')
            duur = film['duur']
            synopsis = film['synopsis']
            info = "{}^{}^{}^{}^{}^{}^{}^{} \n".format(titel, cover, jaar, regisseur, cast, genre, duur, synopsis)
            file.write(info)

openFilm()


username = ''


def toonmachtiginscherm():
    'toont het scherm waarmee je kan kiezen of je als gebruiker of als aanbieder wilt aanmelden '
    loginFrame_aanbdr.pack_forget()
    loginFrame_gebr.pack_forget()
    customerMoviesFrame.pack_forget()
    aanbiedersFrame.pack_forget()
    gebruikersinfoFrame.pack_forget()
    filmKlantenOverzicht.pack_forget()
    machtigingFrame.pack()


def terug_naar_machtiginscherm_aanbdr():
    'deze knop gaat terug naar het beginscherm'
    loginFrame_aanbdr.pack_forget()
    machtigingFrame.pack()


def terug_naar_machtigingscherm_gebr():
    loginFrame_gebr.pack_forget()
    machtigingFrame.pack()


def toonloginFrame_aanbdr():
    'toont het scherm waarmee je kan inloggen als aanbieder'
    machtigingFrame.pack_forget()
    loginFrame_aanbdr.pack()


def toonloginFrame_gebr():
    'toont het scherm waarmee je kan inloggen als gebruiker'
    machtigingFrame.pack_forget()
    loginFrame_gebr.pack()

def toonOverzichtKlantenFrame():
    'toont het scherm waarop je een overzicht ziet van alle aangeboden films, alle klanten en klanten per film'
    machtigingFrame.pack_forget()
    filmKlantenOverzicht.pack()

def toonfilmselectie():
    'toon het scherm met de selectie van films voor gebruikers'
    loginFrame_gebr.pack_forget()
    customerMoviesFrame.pack()

def toonFilmAanbieden():
    'toon het scherm waarin de aanbieders films kunnen aanbieden'
    aanbiedersFrame.pack_forget()
    filmAanbiedenFrame.pack()


def terug_naar_loginscherm_aanbdr():
    """deze functie gaat terug naar het loginscherm van de aanbieders"""
    aanbiedersFrame.pack_forget()
    loginFrame_aanbdr.pack()


def terug_naar_loginscherm_gebr():
    """deze functie gaat terug naar het loginscherm van de gebruikers"""
    customerMoviesFrame.pack_forget()
    loginFrame_gebr.pack()


def terug_naar_aanbiederscherm():
    gebruikersinfoFrame.pack_forget()
    filmAanbiedenFrame.pack_forget()
    aanbiedersFrame.pack()


def toonaanbiederFrame():
    'toont het scherm waarbij je kan kiezen tussen gebruikers en nog aan te bieden films'
    loginFrame_aanbdr.pack_forget()
    aanbiedersFrame.pack()


def toongebruikersinfoFrame():
    'toont het scherm met de gebruikers informatie'
    aanbiedersFrame.pack_forget()
    gebruikersinfoFrame.pack()




email = ''
naam = ''


def login_gebr():
    'logged in als gebruiker en slaat email en username op en gebruikt de functie'
    global email
    email = entry_email.get()
    global naam
    naam = entrygebr_ww.get()
    toonfilmselectie()


def login_aanbdr():
    """laat de beheerder inloggen"""
    global username
    infile = open('aanbiedersInfo.txt', 'r')
    username = entry_user.get()
    password = entry_ww.get()
    y = 0
    for line in infile.readlines():
        content = line.strip('\n')
        content_2 = content.split(';')
        if username == content_2[0] and password == content_2[1]:
            y += 1
            if y > 0:
                toonaanbiederFrame()
                break
    gebruikersinfoGrid()


def gebruikersinfoGrid():
    """"haalt de globale username van de ingelogde aanbieder en toont hem all zijn klanten en heeft een knop naar de qr code van die klant"""
    global username
    infile = open('{}Klanten.txt'.format(username))
    terug_naar_aanbiederscherm_button = Button(master=gebruikersinfoFrame, text='<', font=('helvetica', 16), width=3,
                                               command=terug_naar_aanbiederscherm)
    terug_naar_aanbiederscherm_button.grid(row=0, column=0)
    tellercolumn = 1
    tellerrow = 0
    for line in infile.readlines():
        content = line.split('^')
        filmNaam = content[2].replace(" ","")
        klantNaam = content[0]
        button = Button(master=gebruikersinfoFrame,anchor=W, justify=LEFT, text="Film: {}\nKlant Naam: {}\nKlant Email: {}".format(content[2], content[0], content[1]), command=lambda filmNaam=filmNaam, username=username, klantNaam=klantNaam:showQRCode(klantNaam,filmNaam,username))
        button.grid(column=tellercolumn, row=tellerrow)
        tellercolumn += 1
        if tellercolumn > 2:
            tellerrow += 1
            tellercolumn = 0


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
    lab1 = Label(showFilmDescription, anchor=W, justify=LEFT,  text = '{} \n jaar: {} \n regisseur(s): {} \n cast: {} \n genre: {} \n duur: {} \n synopsis: {} \n aanbieder: {}'.format(gesplitteFilm[movieIndex][0], gesplitteFilm[movieIndex][2], gesplitteFilm[movieIndex][3], gesplitteFilm[movieIndex][4], gesplitteFilm[movieIndex][5], gesplitteFilm[movieIndex][6], gesplitteFilm[movieIndex][7], gesplitteFilm[movieIndex][8]))
    lab1.pack()
    movieDescriptionButton = Button(master=showFilmDescription, text='Reserveren', command= lambda:qrcode(gesplitteFilm[movieIndex][0],gesplitteFilm[movieIndex][8]))
    movieDescriptionButton.pack()



def qrcode(movieName, provider):
    """"pakt de globale username van de klant de titel van de film en de naam van de provider van die film en maakt daar een qrcode van slaat die op en toont het op het scherm"""
    global naam
    editedProvider = provider.replace("\n", "")
    QR = pyqrcode.create('{} \n{} \n{} \n{}'.format(naam, email,movieName, editedProvider))
    editedMovieName = movieName.replace(" ", "")
    QR.png('{}{}{}.png'.format(naam, editedMovieName, editedProvider), scale=6)

    novi = Toplevel()
    canvas = Canvas(novi, width=350, height=300)
    canvas.pack(expand=YES, fill=BOTH)
    qrImg = PhotoImage(file='{}{}{}.png'.format(naam, editedMovieName, editedProvider))
    # image not visual
    canvas.create_image(50, 10, image=qrImg, anchor=NW)
    # assigned the gif1 to the canvas object
    canvas.gif1 = qrImg
    qrCodeName = '{}{}{}.png'.format(naam, editedMovieName, editedProvider)
    with open('besteldeFilms.txt','a') as alleKlantenTXT:
        alleKlantenTXT.write(movieName+'\n')

    with open('{}Klanten.txt'.format(editedProvider),'a') as providerCustomers:
        bestelling = "{}^{}^{}^{}\n".format(naam, email, editedMovieName, qrCodeName)
        providerCustomers.write(bestelling)


def showQRCode(naam, film, provider):
    """"Ontvangt de filenaam van de qr code en toont die in een nieuw venster"""
    novi = Toplevel()
    canvas = Canvas(novi, width=350, height=300)
    canvas.pack(expand=YES, fill=BOTH)
    qrImg = PhotoImage(file='{}{}{}.png'.format(naam, film, provider))
    # image not visual
    canvas.create_image(50, 10, image=qrImg, anchor=NW)
    # assigned the gif1 to the canvas object
    canvas.gif1 = qrImg

root = Tk()

machtigingFrame = Frame(master=root)
machtigingFrame.pack(fill='both', expand=True)
button_usr = Button(master=machtigingFrame, text='gebruiker', height=2, width=10, font=('helvetica', 16, 'bold italic'),command=toonloginFrame_gebr, foreground='blue')
button_usr.pack(padx=20, pady=6)
button_ww = Button(master=machtigingFrame, text='beheerder',height=2,width=10, font =('helvetica', 16, 'bold italic'), command=toonloginFrame_aanbdr, foreground='red')
button_ww.pack(padx=20, pady=6)
buttonOverzicht = Button(master=machtigingFrame, text='Overzicht',height=2,width=10, font =('helvetica', 16, 'bold italic'), command=toonOverzichtKlantenFrame, foreground='Black')
buttonOverzicht.pack(padx=20, pady=6)


loginFrame_aanbdr = Frame(master=root)
loginFrame_aanbdr.pack(fill='both', expand=True)
label_1 = Label(master=loginFrame_aanbdr, text='vul je username en password in')
label_1.pack()
label_user = Label(master=loginFrame_aanbdr, text='username')
label_user.pack()
entry_user = Entry(master=loginFrame_aanbdr, text='username')
entry_user.pack(padx=100)
label_ww = Label(master=loginFrame_aanbdr, text='password')
label_ww.pack()
entry_ww = Entry(master=loginFrame_aanbdr, text='password')
entry_ww.pack()
button_1 = Button(master=loginFrame_aanbdr, text='log in', command=login_aanbdr)
button_1.pack(pady=2)
back_to_machtiging_button = Button(master=loginFrame_aanbdr, text='<', font=('helvetica', 16), width=3, command=toonmachtiginscherm)
back_to_machtiging_button.place(x=10, y=20)

loginFrame_gebr = Frame(master=root)
loginFrame_gebr.pack(fill='both', expand=True)
labelgebr = Label(master=loginFrame_gebr, text='vul je Email en password in')
labelgebr.pack()
label_email = Label(master=loginFrame_gebr, text='Email')
label_email.pack()
entry_email = Entry(master=loginFrame_gebr)
entry_email.pack()
labelgebr_ww = Label(master=loginFrame_gebr, text='username')
labelgebr_ww.pack()
entrygebr_ww = Entry(master=loginFrame_gebr)
entrygebr_ww.pack(padx=100)
buttongebr= Button(master=loginFrame_gebr, text='log in', command=login_gebr)
buttongebr.pack(pady=2)
back_to_machtiging_button_2 = Button(master=loginFrame_gebr, text='<', font=('helvetica', 16), width=3, command=toonmachtiginscherm)
back_to_machtiging_button_2.place(x=10, y=20)


filmKlantenOverzicht = Frame(master=root)
label_1 = Label(master=filmKlantenOverzicht, text='Hier is een overzicht van\n'
                                                  'alle aangeboden films, hoeveel klanten een film gekocht hebben en hoeveel klanten er per film zijn')
label_1.pack(padx=100)
label_2 = Label(master=filmKlantenOverzicht, text="Alle aangeboden films:")
label_2.pack()
with open("aangebodenFilms.txt", "r", encoding='utf-8') as aangebodenFilms:
    films = aangebodenFilms.readlines()
    for film in films:
        film = film.split("^")
        aangebodenFilmLabel = Label(master=filmKlantenOverzicht, text="{}".format(film[0]))
        aangebodenFilmLabel.pack()
label_2 = Label(master=filmKlantenOverzicht, text="Totaal aantal klanten:")
label_2.pack()
with open("besteldeFilms.txt", "r", encoding='utf-8') as besteldeFilms:
    aantalfilms = besteldeFilms.readlines()
    aantalKlantenLabel = Label(master=filmKlantenOverzicht, text="Aantal Klanten: {}".format(len(aantalfilms)))
    aantalKlantenLabel.pack()
label_3= Label(master=filmKlantenOverzicht, text="Alle bestelde films en hoe vaak ze besteld zijn:")
label_3.pack()
with open("besteldeFilms.txt", "r", encoding='utf-8') as besteldeFilms:
    besteld = besteldeFilms.readlines()
    dictionary = {}
    for film in besteld:
        film = film.strip('\n')

        if film not in dictionary:
            dictionary.update({film: 1})
        else:
            waarde = dictionary[film] + 1
            dictionary.pop(film)
            dictionary.update({film: waarde})
    for film in dictionary:
        filmsMetAantalLabel = Label(master=filmKlantenOverzicht, text="{}: {}".format(film,dictionary[film]))
        filmsMetAantalLabel.pack()
back_to_machtiging_button = Button(master=filmKlantenOverzicht, text='<', font=('helvetica', 16), width=3, command=toonmachtiginscherm)
back_to_machtiging_button.place(x=10, y=20)

with open('aangebodenFilms.txt') as movies:
    splitMovieList = []
    for movie in movies:
        movieValues = movie.split("^")
        splitMovieList.append(movieValues)

with open('aangebodenFilms.txt') as movies:
    #genereert een blauw poster veld een titel en een beschrijving knop voor iedere film in aangebodenFilms.txt
    #Daarvan zet het 4 elementen op een rij en begint dan met een nieuwe rij
    customerMoviesFrame = Frame(master=root)
    teller = 2
    rowteller = 1
    row = 1
    row2 = 2
    row3 = 3
    for movie in movies:
        movieValues = movie.split("^")
        movieIndex = splitMovieList.index(movieValues)
        title = movieValues[0]
        cover = movieValues[1]

        start_screen_image_url = "{}".format(cover)
        u = urlopen(start_screen_image_url)
        raw_data = u.read()
        u.close()
        im = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(im)
        homeImageLabel = Label(master=customerMoviesFrame, image=photo)
        homeImageLabel.image = photo

        customerMovieTitleLabel = Label(master=customerMoviesFrame, text='{}'.format(title))
        customerMovieButton = Button(master=customerMoviesFrame, text='Meer info', command=lambda movieIndex=movieIndex:showFilmCustomer(movieIndex))
        homeImageLabel.grid(row=row, column=teller)
        customerMovieTitleLabel.grid(row=row2, column=teller)
        customerMovieButton.grid(row=row3, column=teller)

        teller += 1
        rowteller += 1
        if rowteller == 6:
            teller = 2
            rowteller = 1
            row += 3
            row2 += 3
            row3 += 3
terug_naar_loginscherm_gebr_button = Button(master=customerMoviesFrame, text='<', font=('helvetica', 16), width=3,
                                            command=terug_naar_loginscherm_gebr)
terug_naar_loginscherm_gebr_button.grid(row=1,column=1)

aanbiedersFrame = Frame(master=root)
aanbiedersFrame.pack(fill='both', expand=True)
button_films = Button(master=aanbiedersFrame, text='Films', font=('helvetica', 20, 'bold italic'), height=3, width=18, foreground='blue', command=toonFilmAanbieden)
button_films.pack(padx=100, pady=6)
button_gebrinfo = Button(master=aanbiedersFrame, text='gebruikersinfo',height=3,width=20,font=('helvetica', 18, 'bold italic'), foreground='red', command=toongebruikersinfoFrame)
button_gebrinfo.pack()
terug_button = Button(master=aanbiedersFrame, text='<', font=('helvetica', 16), width=3, command=terug_naar_loginscherm_aanbdr)
terug_button.place(x=10, y=20)

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
    gesplitteFilm[index][2], gesplitteFilm[index][3], gesplitteFilm[index][4], gesplitteFilm[index][5], gesplitteFilm[index][6],
    gesplitteFilm[index][7]))
    lab1.pack()
    button.pack()

def aanbieden(index):
    global username
    infileAanbieden = open('aangebodenFilms.txt', 'a')
    woord =''
    gesplitteFilm1 = gesplitteFilm[index]
    for film in gesplitteFilm1:
        film = film.replace("\n", '')
        woord +="{}{}".format(film,'^')
    woord += username + '\n'
    infileAanbieden.write(woord)

filmAanbiedenFrame = Frame(master=root)
listb1 = Listbox(filmAanbiedenFrame)
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
        button = Button(master=filmAanbiedenFrame, text=titel[0], command=lambda index=index: showFilm1(index))
    button.pack(padx=100)
terug_naar_aanbiederscherm_button = Button(master=filmAanbiedenFrame, text='<', font=('helvetica', 16), width=3, command=terug_naar_aanbiederscherm)
terug_naar_aanbiederscherm_button.place(x=10, y=20)


#toon de QRcode in tkinter
gebruikersinfoFrame = Frame(master=root)
gebruikersinfoFrame.pack()


toonmachtiginscherm()

root.mainloop()