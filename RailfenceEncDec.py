import math
from itertools import cycle
import csv
import re
import numpy as np


#Railfence Encryption
def encryptrail(plaintext, rails, offset):
    #Create iteratble of rail height eg 0,1,2,1,0,1,2...
    it = cycle(list(range(0,rails-1)) + list(range(rails-1,0,-1)))

    
    #Initialise array of empty strings, length of height
    lines = []
    for i in range(0, rails):
        lines.append("")
        

    #Add letters to corresponding lines
    i = 0
    offsetcount = 0
    for line in it:
        #Cycle the line height to the starting offset value
        if(i==0 and offsetcount !=offset):
            offsetcount+=1
            continue

        if(i<len(plaintext)):   #Assign letters to the rails
            lines[line] = lines[line] + plaintext[i]
            i+=1
        else:
            break

    #Combine all lines for final ciphertext
    ciphertext = ""
    for line in lines:
        ciphertext += line
        
    return ciphertext


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


#In form: text, rails, offset
#hswyucwhdwXtp:/w.otb.o/ac?=Q49gct/wuemtvwWQ
print(encryptrail("https://www.youtube.com/watch?v=dQw4w9WgXcQ",3,4))

#https://www.youtube.com/watch?v=dQw4w9WgXcQ
print(decryptrail("hswyucwhdwXtp:/w.otb.o/ac?=Q49gct/wuemtvwWQ",3,4))

