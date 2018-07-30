import numpy as np
import keras
import matplotlib.pyplot as plt
import itertools
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from sklearn.metrics import confusion_matrix
from keras.applications.vgg16 import VGG16
from keras.layers import Dense, Flatten, Activation

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

def get_accuracy(trueLabels, predictions):
    label, labels_2 = get_true_predict_labels(trueLabels, predictions)    
    #Calculating how 
    good = 0
    for i in range(len(labels_2)):
        if label[i] == labels_2[i]:
            good+=1
    
    return (good/len(labels_2))

def get_true_predict_labels(truelabels, predictions):
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

train_path = '/media/emmanuel/DATA/ISIC Dataset/ISIC-images/python files/Training/'
val_path   = '/media/emmanuel/DATA/ISIC Dataset/ISIC-images/python files/Validation/'

trainPacks = ImageDataGenerator().flow_from_directory(train_path, target_size=(224,224), 
                                                         classes=['Dermal','EpidermalB','EpidermalM',
                                                                  'Melanocytic','Melanoma'],
                                                        batch_size=10)

test_batches   = ImageDataGenerator().flow_from_directory(val_path, target_size=(224,224),
                                                        classes=['Dermal','EpidermalB','Melanocytic',
                                                                  'Melanoma','EpidermalM'],
                                                        batch_size=4)



vggModel = VGG16(include_top=False, input_shape=(224,224,3))
new_model = Sequential()


for layer in vggModel.layers:
    new_model.add(layer)

for layer in new_model.layers:
    layer.trainable = False

new_model.add(Flatten())
new_model.add(Dense(5))
new_model.add(Activation('softmax'))

new_model.summary()

new_model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])
his = new_model.fit_generator(trainPacks, steps_per_epoch=625, validation_data=test_batches, epochs = 200, verbose=2, shuffle=True)
loss = his.history['loss']
plt.plot(loss)

new_model.save('vgg160725.h5')

testImages = np.load('testingImages.npz', mmap_mode = 'r+')
trueLabels = testImages['testlabels']
predictions = new_model.predict(testImages['testImages'], verbose=1)
print(get_accuracy(predictions,trueLabels))

trueL, pred = get_true_predict_labels(trueLabels,predictions)

cm = confusion_matrix(trueL, pred)
plot_confusion_matrix(cm,['Benign','Malignant'], title="Confusion Matrix")

