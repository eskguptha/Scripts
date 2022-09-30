def SplitListByBatches(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

def SplitListBySize(inputList, n):
    n = max(1, n)
    return (inputList[i:i + n] for i in range(0, len(inputList), n))
