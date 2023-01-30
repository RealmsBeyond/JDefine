from tkinter import *
from PIL import ImageTk, Image
import JDefine

root = Tk()
root.title("JDefine")
root.geometry("337x300")

#Show image
main_img = ImageTk.PhotoImage(Image.open("Dictionary.jpg"))
main_label = Label(image=main_img)
main_label.grid(row=0, column=5, columnspan=2)

mainfile = JDefine.JDefine()
mainlabel = Label(root, text='''Welcome to JDefine! To look up words,
load a text document with a single Japanese word on each line.\n''').grid(row=2, column=5, columnspan=2)

inputbutton = Button(root, text="Select Input File",
command=mainfile.input_file).grid(row=3, column=5, columnspan=2)

inputbutton = Button(root, text="Select Output File",
command=mainfile.output_file).grid(row=4, column=5, columnspan=2)

start = Button(root, text="Retrieve Definitions",
command=mainfile.weblio).grid(row=5, column=5, columnspan=2)

root.mainloop()