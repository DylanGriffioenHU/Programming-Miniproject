import pyqrcode
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import os


path = "C:/Users/bowse/PycharmProjects/Test/venv/School/Project Blok A Jaar 1/Hoidoei.png"
root = Tk()
foto = ImageTk.PhotoImage(Image.open(path))
panel = Label(root, image = foto)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()






Username = ''
Email_user =''
def qrcode():
    global Username
    global Email_user
    Username = input("Enter username: ")
    Email_user = input("Enter email: ")
    QR = pyqrcode.create('{} \n{}'.format(Username,Email_user))
    QR.png('{}{}.png'.format(Username,Email_user), scale= 6)
    print('QR code generated...')

qrcode()
root = Tk()
img = ImageTk.PhotoImage(Image.open("{}{}.png".format(Username,Email_user)))
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()

# root = Tk()
# root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
# print (root.filename)

film_kiezen()