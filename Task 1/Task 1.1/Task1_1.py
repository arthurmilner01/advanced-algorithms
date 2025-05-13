#Arthur Milner
#Student Number: 21035478
from collections import Counter #Built in python library which can count occurrences, works quickly for task required
import os

                
def main():
    absolutePath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(absolutePath, "task1_1_numbers.txt"), "r") as f: #Reading numbers from file into a list
        numberList = tuple([int(x) for x in f.read().split(' ')]) #Using tuple as there is no need to perform any operations on this list, saves memory
    
    #Get the count for each unique number in the file and add to a dictionary with number:count
    counts = Counter(numberList) #Creates the dictionary of (number:occurrences)

    counts2 = dict(counts.copy()) #Making a copy of the counter as a normal dictionary
    for key in counts:
        counts[key] = (counts[key]//2) + 1 #This operation changes overall occurrences into the occurrences we want to keep, dictionary is now (number:occurrence of number to keep)
        counts2[key] = 1 #Will be used to track how many times we've seen each respective number
        

    #Writing processed numbers to file
    with open(os.path.join(absolutePath, "task1_1_numbers_processed.txt"), "w") as f: #Writing to file
        for number in numberList: #For each number
            if counts[number] == counts2[number]: #If we are at the correct occurrence
                f.write(str(number) + ' ') #Writing to file
            else: #If not found the correct occurrence add one to the dictionary tracking current occurrences for each number
                counts2[number] += 1

if __name__ == "__main__":
    main()