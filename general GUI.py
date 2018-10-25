from tkinter import *
import time
import requests
import xmltodict
import pyqrcode
from PIL import ImageTk, Image


vandaag = time.strftime("%d-%m-%Y")
api_url = 'http://api.filmtotaal.nl/filmsoptv.xml?apikey=8bgs2dsacfezw3eu04jetb4dcvon1a6i&dag={}&sorteer=0'.format(vandaag)

response = requests.get(api_url)

filmXML = xmltodict.parse(response.text)
print('Dit zijn de films van vandaag:')



for film in filmXML['filmsoptv']['film']:
    titel = film['titel']

    print('Vandaag draait {}'.format(titel))


username = ''


def toonmachtiginscherm():
    'toont het scherm waarmee je kan kiezen of je als gebruiker of als aanbieder wilt aanmelden '
    loginFrame_aanbdr.pack_forget()
    loginFrame_gebr.pack_forget()
    filmselectieFrame.pack_forget()
    aanbiedersFrame.pack_forget()
    gebruikersinfoFrame.pack_forget()
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


def toonfilmselectie():
    'toon het scherm met de selectie van films voor gebruikers'
    loginFrame_gebr.pack_forget()
    filmselectieFrame.pack()


def terug_naar_loginscherm_aanbdr():
    """deze functie gaat terug naar het loginscherm van de aanbieders"""
    aanbiedersFrame.pack_forget()
    loginFrame_aanbdr.pack()


def terug_naar_loginscherm_gebr():
    """deze functie gaat terug naar het loginscherm van de gebruikers"""
    filmselectieFrame.pack_forget()
    loginFrame_gebr.pack()


def terug_naar_aanbiederscherm():
    gebruikersinfoFrame.pack_forget()
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
    infile = open('gebruikerinfo.txt', 'a')
    infile.write(email)
    infile.write(';')
    infile.write(naam)
    infile.write('\n')
    toonfilmselectie()


def login_aanbdr():
    """laat de beheerder inloggen"""
    global username
    infile = open('aanbiederinfo.txt', 'r')
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
    if y < 1:
        print('fout')
    gebruikersinfoGrid()


def qrcode():
    QR = pyqrcode.create('{}{}'.format(naam, email))
    QR.png('myQR.png', scale= 6)
    print('QR code generated...')

def gebruikersinfoGrid():
    global username
    infile = open('{}Klanten.txt'.format(username))
    terug_naar_aanbiederscherm_button = Button(master=gebruikersinfoFrame, text='<', font=('helvetica', 16), width=3,
                                               command=terug_naar_aanbiederscherm)
    terug_naar_aanbiederscherm_button.grid(row=0, column=0)
    tellercolumn = 1
    tellerrow = 0
    for line in infile.readlines():
        content = line.split(';')
        button = Button(master=gebruikersinfoFrame, text=content[0])
        button.grid(column=tellercolumn, row=tellerrow)
        tellercolumn += 1
        if tellercolumn > 2:
            tellerrow += 1
            tellercolumn = 0


root = Tk()

machtigingFrame = Frame(master=root)
machtigingFrame.pack(fill='both', expand=True)
button_usr = Button(master=machtigingFrame, text='gebruiker', height=2, width=10, font=('helvetica', 16, 'bold italic'),command=toonloginFrame_gebr, foreground='blue')
button_usr.pack(padx=20, pady=6)
button_ww = Button(master=machtigingFrame, text='beheerder',height=2,width=10, font =('helvetica', 16, 'bold italic'), command=toonloginFrame_aanbdr, foreground='red')
button_ww.pack(padx=20, pady=6)


loginFrame_aanbdr = Frame(master=root)
loginFrame_aanbdr.pack(fill='both', expand=True)
label_1 = Label(master=loginFrame_aanbdr, text='vul je username en password in')
label_1.pack()
label_user = Label(master=loginFrame_aanbdr, text='username')
label_user.pack()
entry_user = Entry(master=loginFrame_aanbdr, text='username')
entry_user.pack()
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
entrygebr_ww.pack()
buttongebr= Button(master=loginFrame_gebr, text='log in', command=login_gebr)
buttongebr.pack(pady=2)
back_to_machtiging_button_2 = Button(master=loginFrame_gebr, text='<', font=('helvetica', 16), width=3, command=toonmachtiginscherm)
back_to_machtiging_button_2.place(x=10, y=20)

filmselectieFrame = Frame(master=root)
filmselectieFrame.pack(fill='both', expand=True)
labelfilm_1 = Label(master=filmselectieFrame, text="OWO", background='yellow', foreground='red', font=('helvetica', 60, 'bold italic'), height=20, width=20)
labelfilm_1.pack()
terug_naar_loginscherm_gebr_button = Button(master=filmselectieFrame, text='<', font=('helvetica', 16), width=3,
                                            command=terug_naar_loginscherm_gebr)
terug_naar_loginscherm_gebr_button.place(x=0, y=0)

aanbiedersFrame = Frame(master=root)
aanbiedersFrame.pack(fill='both', expand=True)
button_films = Button(master=aanbiedersFrame, text='Films', font=('helvetica', 20, 'bold italic'), height=3, width=18, foreground='blue')
button_films.pack(padx=30, pady=6)
button_gebrinfo = Button(master=aanbiedersFrame, text='gebruikersinfo',height=3,width=20,font=('helvetica', 18, 'bold italic'), foreground='red', command=toongebruikersinfoFrame)
button_gebrinfo.pack(padx=30, pady=6)
terug_button = Button(master=aanbiedersFrame, text='<', font=('helvetica', 16), width=3, command=terug_naar_loginscherm_aanbdr)
terug_button.place(x=0, y=0)


#toon de QRcode in tkinter
gebruikersinfoFrame = Frame(master=root)
gebruikersinfoFrame.pack()


toonmachtiginscherm()

root.mainloop()
