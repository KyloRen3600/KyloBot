import tkinter
from tkinter import *
from tkinter.messagebox import *

def alert():
    showinfo("alerte", "Bravo!")

class ChatWindow(tkinter.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		menubar = Menu(self)

		menu1 = Menu(menubar, tearoff=0)
		menu1.add_command(label="Créer", command=alert)
		menu1.add_command(label="Editer", command=alert)
		menu1.add_separator()
		menu1.add_command(label="Quitter", command=self.quit)
		menubar.add_cascade(label="Fichier", menu=menu1)

		menu2 = Menu(menubar, tearoff=0)
		menu2.add_command(label="Couper", command=alert)
		menu2.add_command(label="Copier", command=alert)
		menu2.add_command(label="Coller", command=alert)
		menubar.add_cascade(label="Editer", menu=menu2)

		menu3 = Menu(menubar, tearoff=0)
		menu3.add_command(label="A propos", command=alert)
		menubar.add_cascade(label="Aide", menu=menu3)

		self.config(menu=menubar)

window = ChatWindow()
window.mainloop()