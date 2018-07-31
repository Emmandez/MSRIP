#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 15:12:03 2018

@author: emmanuel


ALL THE LAYERS ARE BEIGN TRAINED
"""

import numpy as np
from keras.applications.resnet50 import ResNet50
import matplotlib.pyplot as plt
import itertools
import os

from sklearn.metrics import confusion_matrix
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Activation, GlobalAveragePooling2D

def plot_confusion_matrix(cm, classes,
                         normalize=False,
                         title="Confusion matrix",
                         cmap=plt.cm.Blues):
    plt.imshow(cm,interpolation="nearest",cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    if(normalize):
        cm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")
    
    print(cm)
    
    thresh = cm.max()/2
    for i,j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j,i, cm[i,j], horizontalalignment="center",
                color="white" if cm[i,j] > thresh else "black")
    
    plt.tight_layout()
    plt.xlabel("Predicted label")
    plt.ylabel("True Label")

def get_true_predict_labels(predictions, trueLabels):
    benign_columns = []
    malignant_columns = []
    
    #Dividing the 5 main classes into two main classes(Benign and malignant)
    for i in predictions:
        #columns 0, 1 and 3 belong to the benign class
        benign_columns.append(i[[0,1,3]])
        malignant_columns.append(i[[2,4]])
    
    #Adding up all the probabilities for each class
    sumBenign = np.sum(benign_columns, axis=1)
    sumMalignant = np.sum(malignant_columns, axis=1)
    
    #dividing the probabilities into 
    pred = []
    for i in range(sumBenign.shape[0]):
        if(sumBenign[i] > sumMalignant[i]):
            pred.append(1)
        else:
            pred.append(0)
    
    #dividing the 5 main classes into two main classes for the true labels
    trueL = []
    for i in range(len(trueLabels)):
        if(trueLabels[i] == 1 or trueLabels[i] == 2 or trueLabels[i]==4):
            trueL.append(1)
        else:
            trueL.append(0)
            
    return (pred,trueL)

def get_accuracy(predictions, trueLabels):
    label, labels_2 = get_true_predict_labels(predictions, trueLabels)
    
    #Calculating how 
    good = 0
    for i in range(len(labels_2)):
        if label[i] == labels_2[i]:
            good+=1
    
    return (good/len(labels_2))


train_path = '/media/emmanuel/DATA/ISIC Dataset/ISIC-images/python files/vgg162507v2/Training 2/'
val_path = '/media/emmanuel/DATA/ISIC Dataset/ISIC-images/python files/vgg162507v2/Validation/'

os.chdir(train_path)

train_batches = ImageDataGenerator().flow_from_directory(train_path, 
                                                       target_size=(224,224), 
                                                         classes=['Dermal','EpidermalB','EpidermalM',
                                                                  'Melanocytic','Melanoma'],
                                                        batch_size=10)

test_batches   = ImageDataGenerator().flow_from_directory(val_path, target_size=(224,224),
                                                        classes=['Dermal','EpidermalB','Melanocytic',
                                                                  'Melanoma','EpidermalM'],
                                                        batch_size=4)


HEIGHT = 224
WIDTH = 224
CHANNELS = 3

model = ResNet50(include_top=False, weights='imagenet',input_shape=(HEIGHT, WIDTH, CHANNELS))
#model.summary()

last_layer = model.output
x = GlobalAveragePooling2D()(last_layer)

x = Dense(128, activation='relu')(x)
out = Dense(5, activation='softmax')(x)

custom_model = Model(inputs=model.input, output=out)
custom_model.summary()

for layer in custom_model.layers:
    layer.trainable = True
    
custom_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

his = custom_model.fit_generator(train_batches, steps_per_epoch=625, validation_data = test_batches, 
                          epochs=100, shuffle=True, verbose=2)
loss = his.history['loss']
plt.plot('loss')

os.chdir('/media/emmanuel/DATA/ISIC Dataset/ISIC-images/python files/vgg162507v2')

#Save model's architechture and weights
model_json = custom_model.to_json()
with open('resnet128.json','w') as file:
    file.write(model_json)

custom_model.save_weights('resnetweights128')


#Predictions
testImages = np.load('testingImages.npz', mmap_mode='r+')
testLabels = testImages['testlabels']

predictions = custom_model.predict(testImages['testImages'], verbose=1)

print('Accuracy:',get_accuracy(predictions, testLabels))

predictions, testLabels = get_true_predict_labels(predictions, testLabels)

cm = confusion_matrix(testLabels, predictions)
plot_confusion_matrix(cm, ['Benign','Malignant'], title='Confusion Matrix')

    
    
    