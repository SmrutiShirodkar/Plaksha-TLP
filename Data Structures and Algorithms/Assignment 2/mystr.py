import mymemory as mymem

class mystr:

    # implement the init
    # self.mymemobj = mymem.getmymemobj()
    # self.p = allocate the right space with type as this class name string
    # see myclass mem_alloc function
    # size is implemented as "s" property of the object implement gets
    # so that obj.s gives the size of this object.
    # value obj.v is implemented as getv and setv property functions

    def __init__(self, value):
        self.mymemobj = mymem.getmymemobj()
        self.p=self.mymemobj.store_byte(value)
        # YOUR CODE 
        raise NotImplementedError 

# get the value of the string  same as it was initialized with or later set.

    def getv(self):
        # YOUR CODE 
        return self.mymemobj.load_byte(self.p)
        raise NotImplementedError 

# set the new value for string

    def setv(self, value):
        # YOUR CODE 
        self.mymemobj.store_byte(value,self.p)
        #raise NotImplementedError 

# return the size occupied by the string
# in bytes

    def gets(self):
        # YOUR CODE 
        return 1
        raise NotImplementedError 

    def __del__(self):
        # YOUR CODE 
        raise NotImplementedError 

    v = property(getv, setv, None, "I'm the 'value' property.")
    s = property(gets, None, None, "I'm the 'value' property.")

