import shutil
import os
import json
import glob

#Change to the root directory
os.chdir('..')

mainFolder = os.getcwd()

folders    = os.listdir()
folders    = [f for f in folders if f != 'Dermoscopedia (CC-BY)' and f != 'moveFiles.py' and f != 'Train' and f!='Validation' and f != 'Test']



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


                diagnosis = jsonfile['meta']['clinical']['diagnosis']
                if diagnosis in weirdfiles2:
                    weirdfiles2[diagnosis]  +=1
                else:
                    weirdfiles2[diagnosis] = 1
            
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
                    else:
                        #print('MALIGNANT MALIGNANT MALIGNANT MALIGNANT MALIGNANT without mel_class')
                        diagnosis = jsonfile['meta']['clinical']['diagnosis']
                        #print(diagnosis)
                        malignantWithoutMelclass +=1
                        malignant_tree.root.add_child_diagnosis(diagnosis)
                        mwmc.append(jsonfile['name'])

                        if(diagnosis == 'seborrheic keratosis'):
                            print(jsonfile['name'])
            
                elif(malignant_benign == 'benign'):
                    benignN +=1
                    #print('BENIGN BENIGN BENIGN BENIGN')
                    diagnosis = jsonfile['meta']['clinical']['diagnosis']

                    if(len(diagnosis) <=0):
                        if("nevus_type" in jsonfile['meta']['clinical'].keys()):
                            print("has nevus_type field")
                            name = jsonfile['meta']['clinical']["nevus_type"]
                            benign_tree.root.add_child(diagnosis)
                        noneFiles.append(jsonfile['name'])

                    #print(diagnosis, ' Added to benign tree')
                    benign_tree.root.add_child(diagnosis)
                    #print(benign_tree.root.children)
                elif( 'indeterminate' in malignant_benign):
                    indeterminateN +=1
                    diagnosis = jsonfile['meta']['clinical']['diagnosis']
                    if (diagnosis in malignant_tree.root.children):
                        #print('Malignant: '+diagnosis+" file: "+jsonfile['name'])
                        malignant_tree.root.add_child(diagnosis)
                    elif (diagnosis in benign_tree.root.children):
                        if('nevus_type' in jsonfile['meta']['clinical'].keys()):
                            #print('has nevus type:'+jsonfile['name'])
                            benign_tree.root.add_child(diagnosis,jsonfile['meta']['clinical']['nevus_type'])
                        else:
                            benign_tree.root.add_child(diagnosis)
                    else:
                        print(jsonfile['name']+' Belongs to nothing. Located in'+current)

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
        malignant_tree.root.increase_occurences(i,weirdfiles2[i])
        popitems.append(i)
    elif (i in benign_tree.root.children):
        benign_tree.root.increase_occurences(i,weirdfiles2[i])
        popitems.append(i)
    elif('benign' in i):
        benign_tree.root.add_child(i)
        benign_tree.root.increase_occurences(i,weirdfiles2[i])
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
for i in popitems:
    weirdfiles2.pop(i)


#print('weird files 2: ',weirdfiles2)
#print('var2:',var2)
#print(namefile)
#print(dontknow)


#To add the diseases that have no malignant_benign label
#if "benign" in jsonfile['meta']['clinical']['diagnosis']:
#    benign_tree.root.add_child(diagnosis)


#####################################################################################
#                                                                                   #
#       Creating classes trees.                                                     #
#                                                                                   #
#       epidermal -------->     squamous cell carcinoma                             #
#                   |                                                               #
#                   ------>     basal cell carcinoma                                #
#                                                                                   #
#####################################################################################

benignClasses = {
    'Dermal': {
        'Dermatofibroma' : [],
        'Angiofibroma' : [],
        

    }
}


