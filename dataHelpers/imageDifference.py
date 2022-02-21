from os import listdir
from PIL import Image, ImageStat, ImageFilter
import shutil
import numpy as np
from numpy import mean, sqrt, square, arange
from matplotlib import pyplot as plt
from time import sleep

dir = 'D:/chickenAI/'
dst_path = dir+ "badFiles/"

#rabithole:
#https://stackoverflow.com/questions/4196453/simple-and-fast-method-to-compare-images-for-similarity

plt.ion() # turn on interactive mode

filenames = listdir(dir)
lastImageBuffer =  np.zeros(shape=[1200, 1600])
lastMean = 0
# fig, ax = plt.subplots(1, 3, sharey=True)

for filename in filenames[::1]:
    if filename.endswith('.jpg'):
        try:
            print(filename)
            im = Image.open(dir+filename).convert('L') # greyscale
            # im = im.filter(ImageFilter.GaussianBlur(radius=3))
            # im = Image.open(dir+filename).convert('1') #Black and white
            # im.show()
            # plt.close()

            # ax1 = plt.imshow(im)

            currentImageBuffer = np.asarray(im)
            lastImage = Image.fromarray(lastImageBuffer, "L")
            currentImage = Image.fromarray(currentImageBuffer, "L")
            # ax[0].imshow(lastImage)
            # ax[1].imshow(currentImage)

            Mean = np.abs(np.mean(currentImageBuffer) - lastMean)
            # print(Mean)
            lastMean= np.mean(currentImageBuffer)

            # Subtract image2 from image1
            diffBuffer = lastImageBuffer - currentImageBuffer
            diffImage = Image.fromarray(diffBuffer, "L")
            # ax[2].imshow(diffImage)

            # plt.show()

            lastImageBuffer = currentImageBuffer
            # plt.pause(.1)
            # buffer2 = np.asarray(im)


            # differenceImage = Image.fromarray(buffer3);

        except (IOError, SyntaxError) as e:
            # print('%s', exc_info=e)
            print('Bad file:', filename) # print out the names of corrupt files
            shutil.move(dir+filename, dst_path+filename)
