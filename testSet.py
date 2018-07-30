#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 15:30:40 2018

@author: emmanuel
"""

import os
import PIL
from PIL import Image
import numpy as np
from tempfile import TemporaryFile

#os.getcwd()
#os.chdir('..')
mainFolder = os.getcwd() + '/Validation'
destFolder = os.getcwd() + '/Test'
testFolder = '/media/emmanuel/DATA/ISIC Dataset/ISIC-images/python files/vgg162507v2/Validation/'

height = 224
width = 224
channels = 3

label = 1
labels = []
n=0

totalImages = 0
foldersTest = os.listdir(testFolder)

for i in foldersTest:
    totalImages += len(os.listdir(testFolder+i))

test = np.zeros((totalImages,height,width,channels))
filesperfolder = []
for folder in foldersTest:
    current = mainFolder + '/'+folder
    os.chdir(current)
    filesperfolder.append(len(os.listdir()))
    for img in os.listdir():
        image = Image.open(img)
        image  = image.resize((height, width), PIL.Image.ANTIALIAS)
        test[n, :, :, :] = image
        labels.append(label)
        n+=1
    label+=1

os.getcwd()
os.chdir('../..')

with open('testLabels.txt','a+') as f:
    for i in labels:     
        f.write(str(i)+'\n')
        
np.savez('testingImages.npz',testImages=test, testlabels =labels)

