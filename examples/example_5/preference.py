#encoding:utf-8

def add(x, y):
    global result
    result = x+y
    
def mod(x, y):
    global result
    result = x%y

def _is(x):
    return result == x    