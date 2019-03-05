import tkinter
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk

class PowerButton(tkinter.Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.image = ImageTk.Image.open("src/NeoliaMC.png")
		self.photo = ImageTk.PhotoImage(self.image)
		global a
		self.canvas = Canvas(a, width=self.image.size[0], height=self.image.size[1])
		self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
		self.canvas.pack(expand=YES)

global a
a = Tk()
r = PowerButton()
a.mainloop()