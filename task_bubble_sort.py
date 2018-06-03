
def bubble_sort(lst):
    counter = 0 

    while counter < len(lst): 
        for i in range(0, len(lst) - 1): 
            if lst[i] > lst[i+1]: 
                lst[i],lst[i+1] = lst[i+1],lst[i] 
        counter += 1 
    return lst 
