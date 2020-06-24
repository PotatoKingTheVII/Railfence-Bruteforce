import math
from itertools import cycle
import csv
import re
import numpy as np
from multiprocessing import Pool

####USER INPUT####
ciphert = "Whnet oTia l reHor s epcexell! sxmihtldiap"  #Put ciphertext here
threads = 4 #Advised to set it to your actual thread count or less
railMlt = 1     #Change these two between 0 and 1.0 to lower the amount brute forced, 1 means it checks all possible combinations
offsetMlt = 1   #Which can take very long for longer ciphertexts


ciphert = ciphert.lower()
#Railfence decryption
def decryptrail(ciphertext, rails, offset):
    #Create iteratble of rail height eg 0,1,2,1,0,1,2...
    it = cycle(list(range(0,rails-1)) + list(range(rails-1,0,-1)))

    
    #Initialise array of empty strings, length of height
    lines = []
    for i in range(0, rails):
        lines.append([])
        

    #Make the railfence mask grid before adding the ciphertext
    i = 0
    offsetcount = 0
    for line in it:
        #Cycle the line height to the starting offset value
        if(i==0 and offsetcount !=offset):
            offsetcount+=1
            continue
        if(i<len(ciphertext)):  #Do for all letters
            for j in range(0, rails):
                if(j == line):   #If current line then mark true
                    lines[line].append("1")
                else:   #Else mark all other lines false
                    lines[j].append("0")
            i+=1
        else:
            break   #End of ciphertext, break out

    cipherletter = 0
    #Now we need to insert the actual letters into the mask
    for i in range(0,rails*len(ciphertext)):
        line = math.floor(i/len(ciphertext))
        charachter = i%len(ciphertext)

        if(lines[line][charachter]=="1"): #Check each char at a time for each line
            lines[line][charachter] = ciphertext[cipherletter]
            cipherletter += 1

            
    #And then read off the ciphertext from the completed rails in correct order;
    it = cycle(list(range(0,rails-1)) + list(range(rails-1,0,-1)))  #Reset iterable
    plaintext = ""
    i = 0
    offsetcount = 0
    for line in it:
        #Cycle the line height to the starting offset value
        if(i==0 and offsetcount !=offset):
            offsetcount+=1
            continue
        
        if(i<len(ciphertext)):
            for j in range(0, rails):
                if(j == line):   #If current line then mark true
                    plaintext+= lines[line][i]

            i+=1
        else:
            break   #End of ciphertext, break out    
        
    return plaintext


def actual_percentage(text):    #Return percentages of listed bigrams from file in text
    occurances = []
    for bigram in data: #Cycle through all bigrams
        if(text.find(bigram[0])!=-1):   #Check if any actually exist in text
            occurances.append(len(re.findall(bigram[0],text)))  #If so check how many (intensive)
        else:
            occurances.append(0)    #Otherwise there aren't any so set to 0
    actual_percentages = np.divide(occurances,sum(occurances))
    return actual_percentages


def fitness(text):  #Calc with chi squared bigram comparison
    text = (text.replace(" ",""))   #Takes ages but has to be done for each combo as they're different for bigram comparison
    freq = actual_percentage(text)
    #####CHI SQUARED#####
    expected = expected_percentages
    chi = 0
    for i in range(0,len(freq)):
        chitop = (freq[i]-expected[i])**2
        chibottom= expected[i]

        chi+=(chitop/chibottom)
    return chi

def fitnessList(textList):  #For use with multiprocess, does fitness on a list of texts
    fullList = []
    for i in range(0,len(textList)):    #Add chi values to each possibility
        #fullList.append([textList[i][0],fitness(textList[i][0]),textList[i][1]])
        fullList.append([textList[i],fitness(textList[i][0])])
 
    return fullList


def decryptrailList(keyList):  #For use with multiprocess, decrypts text with the given list of keys
    fullList = []
    for i in range(0,len(keyList)):    #Add chi values to each possibility
        fullList.append([decryptrail(ciphert,keyList[i][0],keyList[i][1]),keyList[i][0],keyList[i][1]])  #Add the used key along with the decrypted result to keep track
 
    return fullList



#####Chi squared section with bigrams#####
expected_percentages = []
with open('bigramfreq.csv', newline='') as csvfile:    #Get expected freq from file
    data = list(csv.reader(csvfile))
    for bigram in data:
        expected_percentages.append(float(bigram[1]))
#File from http://practicalcryptography.com/media/cryptanalysis/files/english_bigrams_1.txt






if __name__ == '__main__':  #Only run this section if it's the main script running, not a sub-process from multiprocessing

    #Run through all combinations of railfence
    length = len(ciphert)
    railsmax = length
    key_list = []
    for i in range(2, math.floor(railsmax * railMlt)):
        offsetmax = (i*2)
        for j in range(0,(math.floor(offsetmax * offsetMlt))):
            key_list.append([i,j])    #Add each railfence permutation and the respective rail+offset


    #We split the list of combinations up into chunks for the number of processes we're using
    comboChunks = np.array_split(key_list, threads)
    with Pool(threads) as p:
        results = (p.map(decryptrailList, comboChunks ))
        
    allcombos = [item for sublist in results for item in sublist] #Combine each thread's sublist

    #Write the unsorted combos to file
    with open("RawCombos.txt", "w") as fout:
        for combination in allcombos:
            fout.write(combination[0] + "    Rail: " + str(combination[1]) +  " Offset: " + str(combination[2]) + "\n")
    print("Dumped raw combinations, calculting fitness...")


    #We split the list of combinations up into chunks for the number of processes we're using
    comboChunks = np.array_split(allcombos, threads)
    with Pool(threads) as p:
        results = (p.map(fitnessList, comboChunks))

      
    orderedlist = [item for sublist in results for item in sublist] #Combine each thread's sublist
    orderedlist = sorted(orderedlist, key=lambda chi: chi[1])   #Sort list for lowest chi score first


    #Output results to ordered file
    with open("OrderedList.csv", "w") as fout:
        for i in range(0,len(orderedlist)): #Write combo, rail, offset and fitness to file
            fout.write(orderedlist[i][0][0]+"    Rail: " + str(orderedlist[i][0][1]) + " Offset: " + str(orderedlist[i][0][2]) +", Fitness: " +str(orderedlist[i][1])+"\n")


    print("\n\nDumped ordered list to file, finished\n")
