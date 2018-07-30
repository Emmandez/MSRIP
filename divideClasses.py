import shutil
import os
import json
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mimg
import pandas as pd
import random

#Change to the root directory
os.chdir('../..')

mainFolder = os.getcwd()

folders    = os.listdir()
folders    = [f for f in folders if f != 'Dermoscopedia (CC-BY)' and f != 'moveFiles.py' and f != 'Train' and f!='Validation' and f != 'Test' and f!='SONIC']

benignClasses = {
    'Dermal': {
        'Dermatofibroma' : [],
        'Angiofibroma' : [],
        'Angioma' : []
    },
    'Epidermal':{
        'actinic keratosis':[],
        'pigmented benign keratosis':[],
        'seborrheic keratosis':[]
    },
    'Melanocytic':{
        'nevus':[],
        'solar lentigo':[],
        'atypical melanocytic proliferation':[],
        'lentigo simplex':[],
        'lentigo NOS':[]
    }
}

malignantClasses = {
    'Melanoma' : [],
    'Epidermal':[]
}


#####################################################################################
#                                                                                   #
#       Creating classes trees.                                                     #
#                                                                                   #
#       epidermal -------->     squamous cell carcinoma                             #
#                   |                                                               #
#                   ------>     basal cell carcinoma                                #
#                                                                                   #
#####################################################################################

weirdthings = []

def checkClass(diagnosis, path):
    if (diagnosis =='dermatofibroma'):
        if(isinstance(path, list)):
            benignClasses['Dermal']['Dermatofibroma'] += path
        else:    
            benignClasses['Dermal']['Dermatofibroma'].append(path)
    elif(diagnosis == 'angiofibroma or fibrous papule'):
        if(isinstance(path, list)):
            benignClasses['Dermal']['Angiofibroma'] += path
        else:    
            benignClasses['Dermal']['Angiofibroma'].append(path)
    elif(diagnosis == 'angioma'):
        if(isinstance(path, list)):
            benignClasses['Dermal']['Angioma'] += path
        else:    
            benignClasses['Dermal']['Angioma'].append(path)
    elif(diagnosis == 'actinic keratosis'):
        if(isinstance(path, list)):
            benignClasses['Epidermal']['actinic keratosis'] += path
        else:    
            benignClasses['Epidermal']['actinic keratosis'].append(path)
    elif(diagnosis == 'pigmented benign keratosis'):
        if(isinstance(path, list)):
            benignClasses['Epidermal']['pigmented benign keratosis'] += path
        else:    
            benignClasses['Epidermal']['pigmented benign keratosis'].append(path)
    elif(diagnosis == 'seborrheic keratosis'):
        if(isinstance(path, list)):
            benignClasses['Epidermal']['seborrheic keratosis'] += path
        else:    
            benignClasses['Epidermal']['seborrheic keratosis'].append(path)
    elif(diagnosis == 'nevus'):
        if(isinstance(path, list)):
            benignClasses['Melanocytic']['nevus'] += path
        else:    
            benignClasses['Melanocytic']['nevus'].append(path)
    elif(diagnosis == 'solar lentigo'):
        if(isinstance(path, list)):
            benignClasses['Melanocytic']['solar lentigo'] += path
        else:    
            benignClasses['Melanocytic']['solar lentigo'].append(path)
    elif(diagnosis == 'atypical melanocytic proliferation'):
        if(isinstance(path, list)):
            benignClasses['Melanocytic']['atypical melanocytic proliferation'] += path
        else:    
            benignClasses['Melanocytic']['atypical melanocytic proliferation'].append(path)
    elif(diagnosis == 'lentigo simplex'):
        if(isinstance(path, list)):
            benignClasses['Melanocytic']['lentigo simplex'] += path
        else:    
            benignClasses['Melanocytic']['lentigo simplex'].append(path)
    elif(diagnosis == 'lentigo NOS'):
        if(isinstance(path, list)):
            benignClasses['Melanocytic']['lentigo NOS'] += path
        else:    
            benignClasses['Melanocytic']['lentigo NOS'].append(path)
    elif(diagnosis == 'melanoma'):
        if(isinstance(path, list)):
            malignantClasses['Melanoma'] += path
        else:    
            malignantClasses['Melanoma'].append(path)
    elif(diagnosis == 'basal cell carcinoma'):
        if(isinstance(path, list)):
            malignantClasses['Epidermal'] += path
        else:    
            malignantClasses['Epidermal'].append(path)
    elif(diagnosis == 'squamous cell carcinoma'):
        if(isinstance(path, list)):
            malignantClasses['Epidermal'] += path
        else:    
            malignantClasses['Epidermal'].append(path)
    else:
        weirdthings.append([diagnosis,path])
    
def getPercentage(whole, percentage):
    return (percentage * whole)//100

def whichTree(tree1, tree2, label):
    n1 = 0
    n2 = 0
    try:
        n1 = tree1[label]
        n2 = tree2[label]
    except:
        pass
    return n1>n2

class Tree:
    
    def __init__(self, root):
        self.root = root

class Node2:

    children = {}
    
    def __init__(self, name):
        self.name = name
        self.size = 0

    def increase_size(self,n):
        self.size +=n
    
    def increase_occurences(self,diagnosis,n):
        self.children[diagnosis] += n
        self.increase_size(n)

    def add_child(self, diagnosis,*args):

    #    if diagnosis in self.children:
    #        if child_name:
    #            if child_name in self.children[diagnosis]:
    #                self.children[diagnosis][child_name] +=1
    #            else:
    #                self.children[diagnosis][child_name] = 1
    #        else:
    #            self.children[diagnosis]['unknown'] +=1
    #    else:
    #        self.children[diagnosis] = {child_name : 1}

        if diagnosis in self.children:
            if args:
                #print('optional arguments: ',args[0])
                #print('tipo',type(self.children[diagnosis]))
                #print(self.children[diagnosis].keys())
                #print('something',args[0] in self.children[diagnosis])
                if args[0] in self.children[diagnosis]:
                    print('disease added if statemet')
                    self.children[diagnosis][args[0]] += 1
                else:
                    print('disease added else statemet')
                    self.children[diagnosis][args[0]] = 1
            else:
                self.children[diagnosis] +=1
                self.size+=1
        else:
            if args:
                print('has')
                name = args[0]
                self.children[diagnosis] = {args[0]:1}
                self.size+=1
            else:
                self.children[diagnosis] = 1
                self.size+=1
        
        
    
    #def add_child_diagnosis(self, diagnosis, child)

    def get_size(self):
        return self.size   

class Node:

    children = {}
    

    def __init__(self, name):
        self.name = name
        self.size = 0
        self.unknownN = 0

    def get_size(self):
        return self.size
    
    def increase_size(self,n):
        self.size +=n
    
    def increase_occurences(self,diagnosis,n):
        if(diagnosis in self.children):
            self.children[diagnosis] += n
            self.increase_size(n)
        else:
            self.add_child_diagnosis(diagnosis)
            self.increase_occurences(diagnosis,n)

    def add_child(self, diagnosis,child_name):

        if diagnosis in self.children:
            if child_name:
                if child_name in self.children[diagnosis]:
                    self.children[diagnosis][child_name] +=1
                    self.size+=1
                else:
                    self.children[diagnosis][child_name] = 1
                    self.size+=1
                    if(child_name == "squamous cell carcinoma"):
                        print('squamous cell carcinoma')
            else:
                self.children[diagnosis]['unknown'] +=1
                self.unknownN+=1
                self.size+=1
        else:
            self.children[diagnosis] = {child_name : 1}
            self.size+=1
            #self.children[diagnosis][child_name] = 1
    
    def add_child_diagnosis(self,diagnosis):
        if diagnosis in self.children:
            self.children[diagnosis]+=1
            self.size+=1
        else:
            self.children[diagnosis] = 1
            self.size+=1

    #else:
        #if child_name in self.children:
         #   self.children[child_name] +=1
        #else:
       #     self.children[child_name] = 1


indeterminateN = 0
number = 0
unknownN = 0
malignantN = 0
benignN = 0
totalFiles = 0
final = 0
malignantWithoutMelclass = 0

malignant_tree = Tree(Node("Malignant"))
benign_tree = Tree(Node2("Benign"))

noneFiles = []
weirdfiles = []
mwmc = []

knownDiseases = []
unknownDiseases = {}

weirdfiles2 = {}

dontknow = 0

var2 = 0
namefile =''

fileNamesMalignant = {}


for folder in folders:
    current = mainFolder + '/' + folder
    os.chdir(current)

    jsonfiles = glob.glob('*.json')
    totalFiles +=len(jsonfiles)
    for i in range(len(jsonfiles)):
        
        jsonfile = json.load(open(jsonfiles[i]))
        number +=1
        try:
            #print('inside try')
            
            
            if( 'benign_malignant' not in jsonfile['meta']['clinical'].keys()):
                #print(jsonfile['meta']['clinical'].keys())
                #print(jsonfile['meta']['clinical']['diagnosis'] in malignant_tree.root.children)
                """ if(jsonfile['meta']['clinical']['diagnosis'] in malignant_tree.root.children):
                    #print('antes')
                    malignant_tree.root.add_child(jsonfile['meta']['clinical']['diagnosis'],'unknown')
                    malignantN+=1
                    #print('despues        .............................')
                    if jsonfile['meta']['clinical']['diagnosis'] in unknownDiseases.keys():
                        unknownDiseases[jsonfile['meta']['clinical']['diagnosis']]+=1
                    else:
                        unknownDiseases[jsonfile['meta']['clinical']['diagnosis']] = 1
                elif (jsonfile['meta']['clinical']['diagnosis'] in benign_tree.root.children):
                    print('elif no benign_malignant')
                    benign_tree.root.add_child(jsonfile['meta']['clinical']['diagnosis'])
                    benign_tree +=1
                    if jsonfile['meta']['clinical']['diagnosis'] in unknownDiseases.keys():
                        unknownDiseases[jsonfile['meta']['clinical']['diagnosis']]+=1
                    else:
                        unknownDiseases[jsonfile['meta']['clinical']['diagnosis']] = 1
                else:
                    if jsonfile['meta']['clinical']['diagnosis'] in unknownDiseases.keys():
                        unknownDiseases[jsonfile['meta']['clinical']['diagnosis']]+=1
                    else:
                        unknownDiseases[jsonfile['meta']['clinical']['diagnosis']] = 1
                    
                    if jsonfile['meta']['clinical']['diagnosis'] in weirdfiles2:
                        weirdfiles2[jsonfile['meta']['clinical']['diagnosis']]['quantity'] +=1
                        weirdfiles2[jsonfile['meta']['clinical']['diagnosis']]['files'] += jsonfile['name']
                    else:
                        weirdfiles2[jsonfile['meta']['clinical']['diagnosis']]['quantity'] = 1
                        weirdfiles2[jsonfile['meta']['clinical']['diagnosis']]['files'] = jsonfile['name']
                    weirdfiles.append(jsonfile['name']) """
                if( 'diagnosis' not in jsonfile['meta']['clinical'].keys()):
                    dontknow +=1
                else:
                    var2 +=1
                    namefile = jsonfile['name']

                #current+'/'+jsonfile['name']+'.jpg'
                """ diagnosis = jsonfile['meta']['clinical']['diagnosis']
                if diagnosis in weirdfiles2:
                    weirdfiles2[diagnosis]  +=1
                    
                else:
                    weirdfiles2[diagnosis] = 1 """

                diagnosis = jsonfile['meta']['clinical']['diagnosis']
                if diagnosis in weirdfiles2:
                    weirdfiles2[diagnosis].append(current+'/'+jsonfile['name']+'.jpg')
                else:
                    weirdfiles2[diagnosis] = [current+'/'+jsonfile['name']+'.jpg']
            
            else:
                malignant_benign = jsonfile['meta']['clinical']['benign_malignant']

                final +=1
                #print(malignant_benign)
                if (malignant_benign == 'malignant'):
                    malignantN +=1
                    if( 'mel_class' in jsonfile['meta']['clinical'].keys()):
                        #print('inside IF IF IF IF IF IF')
                        #Every json has a diagnosis
                        diagnosis = jsonfile['meta']['clinical']['diagnosis']
                        #print(diagnosis)
                        #Not every json has a mel_class field. this will be the *args
                        mel_class = jsonfile['meta']['clinical']['mel_class']
                        #print('MALIGNANT MALIGNANT MALIGNANT MALIGNANT MALIGNANT')
                        #print(diagnosis +' and '+mel_class)
                        
                        malignant_tree.root.add_child_diagnosis(diagnosis)
                        checkClass(diagnosis,current+'/'+jsonfile['name']+'.jpg')
                    else:
                        #print('MALIGNANT MALIGNANT MALIGNANT MALIGNANT MALIGNANT without mel_class')
                        diagnosis = jsonfile['meta']['clinical']['diagnosis']
                        #print(diagnosis)
                        malignantWithoutMelclass +=1
                        malignant_tree.root.add_child_diagnosis(diagnosis)
                        checkClass(diagnosis,current+'/'+jsonfile['name']+'.jpg')
                        mwmc.append(jsonfile['name'])

                        
            
                elif(malignant_benign == 'benign'):
                    benignN +=1
                    #print('BENIGN BENIGN BENIGN BENIGN')
                    diagnosis = jsonfile['meta']['clinical']['diagnosis']

                    if(len(diagnosis) <=0):
                        if("nevus_type" in jsonfile['meta']['clinical'].keys()):
                            #print("has nevus_type field")
                            name = jsonfile['meta']['clinical']["nevus_type"]
                            benign_tree.root.add_child(diagnosis)
                            checkClass(diagnosis,current+'/'+jsonfile['name']+'.jpg')
                        noneFiles.append(jsonfile['name'])

                    #print(diagnosis, ' Added to benign tree')
                    benign_tree.root.add_child(diagnosis)
                    checkClass(diagnosis,current+'/'+jsonfile['name']+'.jpg')
                    #print(benign_tree.root.children)
                elif( 'indeterminate' in malignant_benign):
                    indeterminateN +=1
                    diagnosis = jsonfile['meta']['clinical']['diagnosis']
                    if (diagnosis in malignant_tree.root.children):
                        #print('Malignant: '+diagnosis+" file: "+jsonfile['name'])
                        malignant_tree.root.add_child(diagnosis)
                        checkClass(diagnosis,current+'/'+jsonfile['name']+'.jpg')
                    elif (diagnosis in benign_tree.root.children):
                        if('nevus_type' in jsonfile['meta']['clinical'].keys()):
                            #print('has nevus type:'+jsonfile['name'])
                            benign_tree.root.add_child(diagnosis,jsonfile['meta']['clinical']['nevus_type'])
                            checkClass(diagnosis,current+'/'+jsonfile['name']+'.jpg')
                        else:
                            benign_tree.root.add_child(diagnosis)
                            checkClass(diagnosis,current+'/'+jsonfile['name']+'.jpg')
                    else:
                        pass

                else:
                    unknownN+=1
                    print('else statement')
                    noneFiles.append(jsonfile['name'])
        except:
            #print('except statement')
            noneFiles.append(jsonfile['name'])

finalweirds = []
popitems = []
for i in weirdfiles2:
    if(i in malignant_tree.root.children):
        malignant_tree.root.increase_occurences(i,len(weirdfiles2[i]))
        for j in weirdfiles2[i]:
            checkClass(i,j)
        popitems.append(i)
    elif (i in benign_tree.root.children):
        benign_tree.root.increase_occurences(i,len(weirdfiles2[i]))
        for j in weirdfiles2[i]:
            checkClass(i,j)
        popitems.append(i)
    elif('benign' in i):
        benign_tree.root.add_child(i)
        benign_tree.root.increase_occurences(i,len(weirdfiles2[i]))
        for j in weirdfiles2[i]:
            checkClass(i,j)
        popitems.append(i)
    else:
        finalweirds.append(i)
        finalweirds.append(weirdfiles2[i])



print('Total: ',number)
#print("Malignant without mel_class",malignantWithoutMelclass)
#print('Unknown: ',unknownN)
#print('\nNone files: ',noneFiles)
#print('MalignantN:',malignantN)
#print('benignN:',benignN)
#print('indeterminate Files: ',indeterminateN)
#print('totalFiles',totalFiles)
#print('Malignant + benign =', malignantN+benignN)
#print('final:',final)
#print('Weird Files:',weirdfiles)
#print('Weird Files len: ', len(weirdfiles))
#print('\nMalignant without mel_class field files', mwmc)
#print(knownDiseases)

#print('unknown diseases: ',unknownDiseases)
#print('weird files 2: ',weirdfiles2)
#print(finalweirds)

#print('Sizes after new elements added')
#print('malignant size: ',malignant_tree.root.get_size())
#print('benign size: ',benign_tree.root.get_size())


print('Malginant tree')
print(malignant_tree.root.children)
print("Size: ",malignant_tree.root.get_size())

print('\nBenign tree')
print(benign_tree.root.children)
print("Size: ",benign_tree.root.get_size())

print('final sum: ',benign_tree.root.get_size()+malignant_tree.root.get_size())

#print(finalweirds)
""" for i in popitems:
    weirdfiles2.pop(i) """

""" print('\nBenign classes dermal dermatofibroma')
print(benignClasses['Dermal']['Dermatofibroma'])
print('len dermal dermatofibroma')
print(len(benignClasses['Dermal']['Dermatofibroma']))
print("#################Classes without slicing####################################################################") """

#shutil.copy(benignClasses['Dermal']['Dermatofibroma'][0], '/media/emmanuel/DATA')


#####################################################################################
#                                                                                   #
#       Moving images to the corresponding folders.                                 #
#                                                                                   #
#       We now have 2 dictionaries, benignClasses and MalignantClasses              #
#       This dictionaries contain the paths of the training images                  #
#                                                                                   #
#       Now we're gonna create the dictionaries that will contain the               #
#       paths of the validations images. We will take 10% of the images             #
#       only if we have more than 100 images on each class. if no                   #
#                                                                                   #
#                                                                                   #
#####################################################################################


#Taking only 2,000 images from the nevus list.
##### Change to increase the number of nevus images. code 135

benignClasses['Melanocytic']['nevus'] = benignClasses['Melanocytic']['nevus'][:2000]

#print(len(benignClasses['Melanocytic']['nevus']))
#benignClasses = {
#    'Dermal': {
#        'Dermatofibroma' : [],
#        'Angiofibroma' : [],
#        'Angioma' : []
#    },
#    'Epidermal':{
#        'actinic keratosis':[],
#        'pigmented benign keratosis':[],
#        'seborrheic keratosis':[]
#    },
#    'Melanocytic':{
#        'nevus':[],
#        'solar lentigo':[],
#        'atypical melanocytic proliferation':[]current+'/'+jsonfile['name']+'.jpg'
#        'lentigo simplex':[],
#        'lentigo NOS':[]
#    }
#}
#
#malignantClasses = {
#    'Melanoma' : [],
#    'Epidermal':[]
#
#
#}
#

validationBenign = {
    'Dermal': {
        'Dermatofibroma' : [],
        'Angiofibroma' : [],
        'Angioma' : []
    },
    'Epidermal':{
        'actinic keratosis':[],
        'pigmented benign keratosis':[],
        'seborrheic keratosis':[]
    },
    'Melanocytic':{
        'nevus':[],
        'solar lentigo':[],
        'atypical melanocytic proliferation':[],
        'lentigo simplex':[],
        'lentigo NOS':[]
    }
}

validationMalignant = {
    'Melanoma' : [],
    'Epidermal' : []
}

for i in benignClasses:
    for j in benignClasses[i]:
        lon = len(benignClasses[i][j])
        if (lon>9):
            limit = getPercentage(lon,10)
            validationBenign[i][j] = benignClasses[i][j][:limit]
            for k in range(limit):
                benignClasses[i][j].pop(0)
            
        else:
            pass

for i in malignantClasses:
    lon = len(malignantClasses[i])
    if (lon>9):
        limit = getPercentage(lon,10)
        validationMalignant[i] = malignantClasses[i][:limit]
        print(limit)
        for k in range(limit):
            malignantClasses[i].pop(0)
    else:
        pass


#print(benignClasses['Dermal']['Dermatofibroma'])

print('##################BENIGN CLASSES#######################')
#print(validationBenign['Dermal']['Dermatofibroma'])

""" print('##############VALIDATION BENIGN###########################')
print(validationBenign)

print('#################VALIDATION MALIGNANT########################')
print(validationMalignant) """  


print('Lenghts of the different dictionaries')
print('Benign Training')
for i in benignClasses:
    print(i)
    for j in benignClasses[i]:
        print(j,'len:',len(benignClasses[i][j]))
    print('\n')
    

print('\nMalignant Trainig')
for i in malignantClasses:
    print(i,end=' ')
    print('len:',len(malignantClasses[i]))

print('\nValidation benign')
for i in validationBenign:
    print(i,end=' ')
    for j in validationBenign[i]:
        print(j,'len:',len(validationBenign[i][j]))
    print('\n')

print('\nValidation Malignant')
for i in validationMalignant:
    print(i,end=' ')
    print('len:',len(validationMalignant[i]))



#####################################################################################
#                                                                                   #
#           CREATING FILE WITH THE PATHS OF THE IMAGES                              #
#                                                                                   #
#                                                                                   #
#####################################################################################
os.chdir('../python files/vgg162507v2/paths/training')
print(os.getcwd())

#######################BENIGN#############################
##########################################################
##############Training Data###############################
for i in benignClasses['Dermal']:
    for j in benignClasses['Dermal'][i]:
        with open('Dermal.txt','a+') as f:
            f.write(j+'\n')

for i in benignClasses['Epidermal']:
    for j in benignClasses['Epidermal'][i]:
        with open('EpidermalB.txt','a+') as f:
            f.write(j+'\n')

for i in benignClasses['Melanocytic']:
    for j in benignClasses['Melanocytic'][i]:
        with open('Melanocytic.txt','a+') as f:
            f.write(j+'\n')

##############Training Data###############################
print('Training malignant data')
for i in malignantClasses['Melanoma']:
    with open('Melanoma.txt','a+') as f:
        f.write(i+'\n')

for i in malignantClasses['Epidermal']:
    with open('EpidermalM.txt','a+') as f:
        f.write(i+'\n')






os.chdir('../validation')
####################### MALIGNANT ########################
##########################################################


######################Validation Data####################
for i in validationMalignant['Melanoma']:
    with open('Melanoma.txt','a+') as f:
        f.write(i+'\n')

for i in validationMalignant['Epidermal']:
    with open('EpidermalM.txt','a+') as f:
        f.write(i+'\n')


############## Validation Data ###############################
for i in validationBenign['Dermal']:
    for j in validationBenign['Dermal'][i]:
        with open('Dermal.txt','a+') as f:
            f.write(j+'\n')

for i in validationBenign['Epidermal']:
    for j in validationBenign['Epidermal'][i]:
        with open('EpidermalB.txt','a+') as f:
            f.write(j+'\n')

for i in validationBenign['Melanocytic']:
    for j in validationBenign['Melanocytic'][i]:
        with open('Melanocytic.txt','a+') as f:
            f.write(j+'\n')
