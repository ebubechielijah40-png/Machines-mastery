def first_descent(values):
    for i in range(len(values)-1):
        if values[i] > values[i+1]:
            return i
    return -1
