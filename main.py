import os
import shutil
from tkinter.filedialog import askdirectory

#commonDir = input('Directory principale delle foto raw\n> ')
#destDir = input('Directory dove devono andare le foto raw\n> ')

commonDir = askdirectory(title='Directory principale delle foto raw')
destDir = askdirectory(title='Directory dove devono andare le foto raw')

print(commonDir)
print(destDir)

photosSelected = os.listdir(destDir)

for photo in photosSelected:
    try:
        shutil.copyfile(f'{commonDir}/{photo[:-4]}.CR2', f'{destDir}/{photo[:-4]}.CR2')
    except FileNotFoundError as e:
        print(f'{photo[:-4]}.CR2 not found')

print('Finished')
