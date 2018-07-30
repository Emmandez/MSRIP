import shutil
import os
import json
import glob


validationPath = os.getcwd() + '/Validation/'
trainingPath = os.getcwd() + '/Training/'

os.chdir('paths/training')

trainingFiles = os.listdir()
#print(trainingFiles)
for i in trainingFiles:
    with open(i) as f:
        lines = f.readlines()
        i = i[:-4]
        for j in lines:
            try:
                shutil.copy(j[:-1],trainingPath+i)
            except FileNotFoundError:
                print('file',j,' not found')



os.chdir('../validation')
validationFiles = os.listdir()
#print(validationFiles)
for i in validationFiles:
    with open(i) as f:
        lines = f.readlines()
        #print('lines of ',i,' ',len(lines))
        i = i[:-4]
        for j in lines:
            try:
                shutil.copy(j[:-1], validationPath+i)
            except FileNotFoundError:
                print('file: ',j,' not found')
