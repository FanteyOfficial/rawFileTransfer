import os
import shutil
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.firstFolderName = ""
        self.secondFolderName = ""

        self.isFirstFolderSelected = False
        self.isSecondFolderSelected = False

        self.title('Raw File Transfer')

        self.geometry("300x350")  # Adjusted width
        self.resizable(0, 0)
        self.eval('tk::PlaceWindow . center')

        self.appTitle = Label(self, text='RFT', font=('sans serif', 12))
        self.appTitle.pack()

        self.selectGeneralFolderBTN = Button(self, text="Seleziona la cartella con tutte le foto", font=('sans serif', 12),
                                             bg="#25cf88", command=self.selectFirstFolder)
        self.selectGeneralFolderBTN.pack(pady=10)
        self.firstFolderSelected = Label(self, text="❌", foreground="Red", font=('sans serif', 12))
        self.firstFolderSelected.pack()

        self.selectDestinationFolderBTN = Button(self, text="Seleziona la cartella di destinazione", font=('sans serif', 12),
                                                 bg="#25cf88", command=self.selectSecondFolder)
        self.selectDestinationFolderBTN.pack(pady=10)
        self.secondFolderSelected = Label(self, text="❌", foreground="Red", font=('sans serif', 12))
        self.secondFolderSelected.pack()

        self.transferButton = Button(self, text="Avvia trasferimento", font=('sans serif', 12), background="#255bcf",
                                     state=DISABLED, command=self.transferPhotos)
        self.transferButton.pack(pady=20)

        self.progressBarContainer = ProgressBar(self)
        self.progressBarContainer.pack(pady=10)

        self.transferStatus = Label(self, text="", font=('sans serif', 12))
        self.transferStatus.pack(pady=5)

    def selectFirstFolder(self):
        self.firstFolderName = askdirectory(title='Directory principale delle foto raw')

        if self.firstFolderName:
            self.firstFolderSelected.config(text="✔", foreground="Green")
            self.isFirstFolderSelected = True
        else:
            self.firstFolderSelected.config(text="❌", foreground="Red")
            self.isFirstFolderSelected = False

        self.checkFoldersSelected()

    def selectSecondFolder(self):
        self.secondFolderName = askdirectory(title='Directory dove devono andare le foto raw')

        if self.secondFolderName:
            self.secondFolderSelected.config(text="✔", foreground="Green")
            self.isSecondFolderSelected = True
        else:
            self.secondFolderSelected.config(text="❌", foreground="Red")
            self.isSecondFolderSelected = False

        self.checkFoldersSelected()

    def checkFoldersSelected(self):
        if self.isFirstFolderSelected and self.isSecondFolderSelected:
            self.transferButton['state'] = ACTIVE
        else:
            self.transferButton['state'] = DISABLED

    def transferPhotos(self):
        if not self.isFirstFolderSelected or not self.isSecondFolderSelected:
            messagebox.showerror("Error", "Please select both folders.")
            return

        photos_selected = os.listdir(self.firstFolderName)
        photos_selected = [file for file in photos_selected if file.lower().endswith('.jpg')]

        if not photos_selected:
            messagebox.showinfo("Info", "No photos found in the source folder.")
            return

        total_photos = len(photos_selected)
        self.progressBarContainer.set_total_photos(total_photos)

        def copy_next_photo(index):
            if index < total_photos:
                photo = photos_selected[index]
                try:
                    shutil.copyfile(
                        os.path.join(self.firstFolderName, photo),
                        os.path.join(self.secondFolderName, photo)
                    )
                    self.progressBarContainer.update_progress(index + 1)
                except FileNotFoundError as e:
                    messagebox.showerror(f'{photo} not found', str(e))

                # Schedule the next iteration with a delay (e.g., 100 milliseconds)
                self.after(1, copy_next_photo, index + 1)
            else:
                self.transferStatus['text'] = "Trasferimento completato!"

        # Start the copy process
        copy_next_photo(0)


class ProgressBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.pb = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate', length=280, maximum=0)
        self.pb.grid(column=0, row=0)

        self.value_label = ttk.Label(self, text=self.update_progress_label())
        self.value_label.grid(column=0, row=1, columnspan=2)

    def update_progress_label(self):
        return f"Current Progress: {self.pb['value']} / {self.pb['maximum']}"

    def set_total_photos(self, total_photos):
        self.pb.configure(maximum=total_photos)

    def update_progress(self, value):
        self.pb['value'] = value
        self.value_label['text'] = self.update_progress_label()


if __name__ == "__main__":
    App().mainloop()
