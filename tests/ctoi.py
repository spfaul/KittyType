def ctoi(c):
    if type(c) == type(""):
        return ord(c)
    else:
        return c


print( ctoi(input('Enter: ')) )