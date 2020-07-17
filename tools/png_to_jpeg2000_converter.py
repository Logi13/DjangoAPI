import os

from PIL import Image

directory = r'C:\Users\johnn\Documents\Dev\Leapian\leapian-site-prototype\tools'

print("Searching: ", directory)

for subdir, dirs, files in os.walk(directory):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith(".png"):
            print("Converting...... Filename:", filename.split('.png')[0] )
            try:
                im = Image.open(filename)
                im.convert("RGBA").save(filename.split('.png')[0] + '.webp', 'WEBP')
            except:
                print("Error! Try again.")