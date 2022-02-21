from os import listdir
from PIL import Image, ImageStat, ImageFilter
import shutil
import numpy as np
from numpy import mean, sqrt, square, arange
from matplotlib import pyplot as plt
from time import sleep

dir = 'D:/chickenAI/'
dst_path = dir+ "badFiles/"

plt.ion() # turn on interactive mode

filenames = listdir(dir)
# fig, ax = plt.subplots(1, 3, sharey=True)

for filename in filenames[:1000:500]:
    if filename.endswith('.jpg'):
        try:
            print(filename)
            im = Image.open(dir+filename)

            img = np.asarray(im)
            print(img.shape)
            rs = img.reshape(-1,3) # unpack rows and columns to one dimensional array of pixels
            print(rs.shape)

            unique,counts = np.unique(rs,axis=0, return_counts=True)
            # print(unique)
            # print(counts)

            maxElement = np.amax(counts)
            indexOfMax = np.where(counts == np.amax(maxElement))
            
            print(counts[indexOfMax])
            print(unique[indexOfMax])

        except(PermissionError):
            print('Bad file PermissionError:', filename) # print out the names of corrupt files
            pass

        except (IOError, SyntaxError) as e:
            # print('%s', exc_info=e)
            shutil.move(dir+filename, dst_path+filename)
            print('Bad file:', filename) # print out the names of corrupt files
