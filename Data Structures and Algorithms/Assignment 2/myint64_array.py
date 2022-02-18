import mymemory as mymem

class myint64_array:

    # implement the init
    # self.mymemobj = mymem.getmymemobj()
    # self.p = allocate the right space with type as 'myint32_array'
    # see myclass mem_alloc function
    # self.len = size of the myint32_array (no. of elements)
    def __init__(self, size, init=0):
        self.mymemobj = mymem.getmymemobj()
        # YOUR CODE 
        raise NotImplementedError 

# A[i] will work with this function. returns the ith element.
# Ensure to raise Exception("Array out of index Exception") if the element
# goes out of bound.
    def __getitem__(self, i):
        # YOUR CODE 
        raise NotImplementedError 

# A[i] =5 will work with this function. returns the ith element.
# Ensure to raise Exception("Array out of index Exception") if the element
# goes out of bound.
    def __setitem__(self, i, value):
        # YOUR CODE 
        raise NotImplementedError 

# iterator function store whatever is required in self for iterating in
# combination with __next__ function.
# see example code in assignment unit that I added.
    def __iter__(self):
        # YOUR CODE 
        raise NotImplementedError 

# next function for iterator raises StopIteration once all array elements
# are iterated upon.
    def __next__(self):
        # YOUR CODE 
        raise NotImplementedError 

# get the property "s" 
# A.s as defined inthe spec by this function.
    def gets(self):
        # YOUR CODE 
        raise NotImplementedError 

# Free the element when this is called by garbage collector.
# right size etc.
    def __del__(self):
        # YOUR CODE 
        raise NotImplementedError 

    s = property(gets, None, None, "I'm the 'value' property.")

