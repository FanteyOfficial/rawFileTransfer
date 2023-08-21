import os
import shutil
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askdirectory

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title('Raw File Transfer')

        self.appTitle = Label(self, text='RFT', font=('sans serif', 12))
        self.appTitle.grid(column=0, row=0, columnspan=2)

if __name__ == "__main__":
    App.mainloop()