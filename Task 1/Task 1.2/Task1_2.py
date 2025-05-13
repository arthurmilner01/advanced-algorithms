#Arthur Milner
#Student Number: 21035478
import os
import bisect #O(log(N)) insertion

def merge_sort(list):
    length = len(list)
    
    if length <= 1:
        return list
    
    mid = length//2
    left_list = merge_sort(list[:mid])
    right_list = merge_sort(list[mid:])
    
    return merge(left_list, right_list)
    
def merge(left_list, right_list):
    output_list =[]    
    lc = 0
    rc = 0 # left counter and right counter    
    while lc < len(left_list) and rc <len(right_list):
        if left_list[lc] < right_list[rc]:
            output_list.append(left_list[lc])
            lc += 1
        else:
            output_list.append(right_list[rc])
            rc += 1
    #move left elements in left and right lists into the output
    output_list.extend(left_list[lc:])
    output_list.extend(right_list[rc:])
    
    return output_list

def binarySearch(val, list):
    left = 0
    right = len(list)-1
    
    while left <= right:
        mid = left+(right-left)//2
        if val > list[mid]:
            left = mid+1
        elif val < list[mid]:
            right = mid-1
        else:
            return mid
    return None


def main():
    absolutePath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(absolutePath, "task1_2_numbers.txt"), "r") as f:
        line = f.read()
        list = [int(x) for x in line.split(' ')]
        list = merge_sort(list) #Merge sort as it has consistent performance on large datasets compared to quick sort

    with open(os.path.join(absolutePath, "task1_2_operations.txt"), "r") as f:
        lines= f.readlines()
        operations = [tuple(line.strip().split(' ')) for line in lines] #Tuple as data will not be touched, saves memory, will be stored like ((OPERATION, NUMBER), ...)

    for i in range(len(operations)):
        currentNum = int(operations[i][1])
        if operations[i][0] == "1": #Search
            index = binarySearch(currentNum, list) #Binary search, O(logN)
            if index != None: #Binary search returns none if number not in list
                print("Number "+ str(currentNum) + " is in the list.")
            else:
                print("Number "+ str(currentNum) + " is not in the list.")
        elif operations[i][0] == "2": #Insert
            #Inserts int in correct order, O(logN), similar to binary search above but also inserts for values not in the list
            bisect.insort_right(list, currentNum)
        elif operations[i][0] == "3": #Delete
            index = binarySearch(currentNum, list)
            while list[index] == currentNum: #While number still occurs in the list
                list.pop(index) #Removes value at that index
                index = binarySearch(currentNum, list)
                if index == None: #When number has no more occurrences
                    break
    
    print("List after operations:")
    print(list)
    

if __name__ == "__main__":
    main()