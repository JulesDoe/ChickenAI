from os import listdir
from PIL import Image, ImageStat
import shutil


dir = 'D:/chickenAI/'
dst_path = dir+ "removed2/"


filenames = listdir(dir)
for filename in filenames[::1]:
    if filename.endswith('.jpg'):
        try:
            # img = Image.open(dir+filename) # open the image file
            # img.verify() # verify that it is, in fact an image
            
            # brightness
            im = Image.open(dir+filename).convert('L')
            stat = ImageStat.Stat(im)
            brightness = stat.mean[0]
            print(f"{filename} {stat.mean[0]}")
            if brightness < 15:
                shutil.move(dir+filename, dst_path+filename)

        except (IOError, SyntaxError) as e:
            print('Bad file:', filename) # print out the names of corrupt files


