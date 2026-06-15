import string
import sys

class IOCatcher:
    '''Accumulates IO into a string for later use.
    '''
    
    def __init__(self):
        self.clear()

    
    def clear(self):
        self.s = ''

    
    def write(self, data):
        self.s = self.s + data

    
    def getPrinted(self):
        return self.s



class IOLogger:
    '''The IOLogger class can catch writes as if it were a file class.  
    It attempts to collect lines of input before calling the user-supplied
    output function.  ctor takes logFunction(str) as its sole argument.'''
    
    def __init__(self, logFn):
        self.str = ''
        self.logFn = logFn

    
    def write(self, data):
        self.str = self.str + data
        pos = string.find(self.str, '\n')
        while pos != -1:
            tmp = self.str[0:pos]
            self.logFn('python: ' + tmp)
            self.str = self.str[pos + 1:]
            pos = string.find(self.str, '\n')


