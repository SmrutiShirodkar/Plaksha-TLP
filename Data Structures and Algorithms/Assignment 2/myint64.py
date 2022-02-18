import mymemory as mymem
from ctypes import *
class myint64:

    # implement the init
    # self.mymemobj = mymem.getmymemobj()
    # self.p = allocate the right space with type as this class name string
    # see myclass mem_alloc function
    # size is implemented as "s" property of the object implement gets
    # so that obj.s gives the size of this object.
    # value obj.v is implemented as getv and setv property functions
    def __init__(self, value):
        self.mymemobj = mymem.getmymemobj()
        # YOUR CODE 
        self.p=self.mymemobj.store_int64(value)
        #raise NotImplementedError 

# for the value property
    def getv(self):
        # YOUR CODE 
        return self.mymemobj.load_int64(self.p)
       #raise NotImplementedError 

# for setting the value 
    def setv(self, value):
        # YOUR CODE 
        self.mymemobj.store_int64(value,self.p)
        #raise NotImplementedError 

# this returns the size of the object
    def gets(self):
        # YOUR CODE 
        return 8
        #raise NotImplementedError 

# free the memory
    def __del__(self):
        # YOUR CODE 
        raise NotImplementedError 

    v = property(getv, setv, None, "I'm the 'value' property.")
    s = property(gets, None, None, "I'm the 'value' property.")

