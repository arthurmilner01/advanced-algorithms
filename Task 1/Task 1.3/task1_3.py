#Arthur Milner
#Student Number: 21035478
import os
import multiprocessing as mp
from multiprocessing import Pool

def KMPSearch(pattern, chunk, text):
    start = int(chunk[0])
    end = int(chunk[1])
    lp = len(pattern)
    lps = calculateLPSArray(pattern)
    count = 0

    for lineno in range(start, end):
        i=0
        j=0
        lt = len(text[lineno])
        
        while i < lt:
            if pattern[j] == text[lineno][i]: 
                i += 1
                j += 1
                if j == lp:
                    #print ("Found pattern at index " + str(lineno-j))
                    count += 1
                    j = lps[j-1]
            else:
                if j == 0:
                    i += 1
                else:
                    j=lps[j-1]
    return int(count)

def calculateLPSArray(pattern):
    lp = len(pattern)   
    lps = [None]*lp
    i = 0
    j = 1
    lps[0] = 0
    while lps[lp-1] == None:
        if pattern[i] == pattern[j]:
                lps[j] = i+1 
                i += 1
                j += 1
        else:
            if i==0:
                lps[j] = 0
                j += 1
            else:
                i = lps[i-1]
    return lps

def parallelisedSearch(pattern, text , n=None): #Default number of proc if none specified, number of CPUs

    if n == None:
        n = mp.cpu_count()

    steps = len(text)//n
    
    chunks = []
    
    for i in range(n-1):
        chunks.append([i*steps, (i+1)*steps])

    chunks.append([(n-1)*steps, len(text)])


    #Using pool class as it makes the code more readable, pool also handles
    #a lot of the process management for you as it creates a pool of worker processes, the amount of worker processes is
    #dependant on the number of cores within the system it is running on.
    p = Pool(processes=n)

    results = []

    for chunk in chunks: #For each chunk of the text
        results.append(p.apply_async(KMPSearch, args=(pattern, chunk, text))) #async as no need for blocking, results do not rely on eachother
        

    p.close()
    p.join()


    return sum(result.get() for result in results) #Loops through results and adds values together for overall count of pattern frequency



def main():

    absolutePath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(absolutePath, "task1_3_text.txt"), encoding='utf8') as f:
        text = f.readlines()

    with open(os.path.join(absolutePath, "task1_3_names.txt"), encoding='utf8') as f:
        #read in names into tuple
        names= f.readlines()

    with open(os.path.join(absolutePath, "task1_3_solution.txt"), "w") as f:
        for name in names:
            name = name.strip()
            f.write(name + " = ")
            f.write(str(parallelisedSearch(name, text)))
            f.write("\n")

    

if __name__ == "__main__":
    main()