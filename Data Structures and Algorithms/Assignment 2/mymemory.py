from myerror import *
from ctypes import *
import mybit_vector as mybv

# exceptions for mymemory class
# need not edit these exceptions, keep it as is

class mymem_error(myerror):
    pass

class mymem_bad(mymem_error):
    def __init__(self, size, message="size not aligned or large"):
        self.size=size
        self.message=message
    def __str__(self):
        return f'{self.size} -> {self.message}'

class mymem_nomem(mymem_error):
    def __init__(self, mymem, message="Memory NOT AVAILABLE"):
        self.mymem = mymem
        self.message=message
    def __str__(self):
        return f'memtotal: {self.memsize} allocated: {self.allocated} free: {self.free}  -> {self.message}'

class mymem_invalidptr(mymem_error):
    def __init__(self, ptr, mymem, message="invalid memory ptr"):
        self.ptr=ptr
        self.ptr1=mymem.start
        self.ptr2=mymem.end
        self.message=message
    def __str__(self):
        return f'ptr: {self.ptr} ptr should be between:{self.ptr1} and {self.ptr2} -> {self.message}'

class mymem_badval(mymem_error):
    def __init__(self, val, message="bad or large value"):
        self.val=val
        self.message=message
    def __str__(self):
        return f'{self.val} -> {self.message}'

class mymem_invalid_alloctype(mymem_error):
    def __init__(self, type, mymem, message="invalid alloc type"):
        self.type=type
        self.mymem=mymem
        self.message=message
    def __str__(self):
        return f'type: {self.type} not in {self.mymem.types}-> {self.message}'

class mymem_corrupt(mymem_error):
    def __init__(self, ptr, nbytes=0, b=0, i=0, message="memory corrupted"):
        self.ptr=ptr
        self.nbytes=nbytes
        self.b=b
        self.i=i
        self.message=message
    def __str__(self):
        return f'ptr: {self.ptr} nbytes: {self.nbytes} b: {self.b} i: {self.i} -> {self.message}'

#implementation of mymemory class
# and all its methods

class mymemory():
    maxsize=1024*1024*1024
    int32_max=pow(2,31)-1
    int64_max=pow(2,63)-1

    # members:
    # byte_arr = linear memory array
    # start and end pointers for memory addresses handed out to callers.
    # The pointers map to the byte_arr index linearly.
    # current stores the current value of the index in the byte_arr from where
    # you will look for available memory in the byte_arr.
    # memsize = total memory size given by the test.py file or whoever uses it.
    # bv is the bitvector implementation object
    # free = total free memory (initial value is all memory is free)
    # allocated = total allocated memory (initial value is zero
    # alloc_types is a dictionary for storing what memory went to what data type
    # indicated by the mem_alloc and mem_free last argument strings. they
    # should be same as the self.types defined here. 
    # this helps in seeing who allocated how much and if there is a memory
    # leak you can figure it out.
    
    def __init__(self, size):
        if size > self.maxsize:
            raise mymem_bad(size)
        self.byte_arr=(c_ubyte*size)()
        self.start=0xfffffffc00000000
        self.end=self.start+size
        self.current = 0;
        self.memsize=size
        self.bv = mybv.mybit_vector(size)
        self.free=size
        self.allocated=0
        self.alloc_types={}
        self.types=['mybyte','mybool','myint32','myint64','mystr', 'myint32_array', 'myint64_array']

        for t in self.types:
            self.alloc_types[t]=0

# checks if the pointer is valid

    def ptr_check(self, ptr):
        if (ptr <self.start or ptr >= self.end):
            raise mymem_invalidptr(ptr, self)

# converts memory pointer value to index into byte_arr
# use this function in mem_free and in load_zzz
# and in store_zzz functions

    def ptr_to_index(self, ptr):
        self.ptr_check(ptr)
        return ptr-self.start

# converts index in byte_arr to memory pointer 
# this is just a linear mapping as you see.
# clients only see the memory pointer they dont understand the implementation
# of byte array index etc.
# use this function to convert the index to ptr in mem_alloc

    def index_to_ptr(self, index):
        ptr=self.start+index
        self.ptr_check(ptr)
        return ptr

# allocates memory for nbytes
# type should be one of types indicated above.
# returns memory pointer (not the index to byte arr)
# uses bit vector self.bv to invoke the right methods.
# raises mymem_nomem(self) exception if you dont find the 
# required memory.
# do the book keeping appropriately for allocated, free and alloc_types

    def mem_alloc(self, nbytes, type):
        if type not in self.types:
            raise mymem_invalid_alloctype(type, self)
        # YOUR CODE 
        found=0
        for i in range(0,len(self.byte_arr)):
            if self.bv.is_free(i):
                found=1
                for j in range(0,nbytes-1):
                    if self.bv.is_free(i+j+1):
                        found+=1
                if found==nbytes:
                    for j in range(nbytes):
                        self.bv.set_bit(i+j)
                    return i + self.start
        #raise NotImplementedError 

# free the memory at ptr for nbytes, for the type strings mentioned above.
# do the book keeping appropriately for allocated, free and alloc_types
# raises mymem_invalid_alloctype if type is not part of the string above.

    def mem_free(self, ptr, nbytes, type):
        if type not in self.types:
            raise mymem_invalid_alloctype(type, self)
        # YOUR CODE 
        raise NotImplementedError 

# returns the value of the byte at ptr.

    def load_byte(self, ptr):
        #self.ptr_check(ptr)
        # YOUR CODE 
        if (ptr <self.start or ptr > self.start+self.size):
                return "Invalid pointer"
        else:
            value=self.byte_arr[ptr]
            return value
        raise NotImplementedError 

# stores the byte at ptr and if ptr is None, allocates memory for a byte
# and stores the value and returns. If ptr is not None it stores the value
# at pointer.

    def store_byte(self, value, ptr=None):
        # if ptr != None:
        #     self.ptr_check(ptr)
        # YOUR CODE 
        if ptr==None:
            ptr=self.mem_alloc(1,'mystr')
        else:
            if (ptr <self.start or ptr > self.start+self.size):
                return "Invalid pointer"

        # Add line to check if ptr is a valid pointer
        self.byte_arr[ptr-self.start]=value

        return ptr
        #raise NotImplementedError 

# 
# returns the value of the int32 at ptr.
# raises mymem_badval(value) exception if the value overflows on both sides
# negative or positive. (note this is only possible due to your bug as
# store_int32 checks the value for exactly the same.

    def load_int32(self,ptr):
        #self.ptr_check(ptr)
        # YOUR CODE 
        if (ptr <self.start or ptr > self.start+self.memsize):
                return "Invalid pointer"
        else:
            value=self.byte_arr[ptr - self.start ]|self.byte_arr[ptr - self.start +1]<<8|self.byte_arr[ptr - self.start +1]<<16|self.byte_arr[ptr - self.start +1]<<24
            return c_int32(value).value
        #raise NotImplementedError 

# stores the int32 at ptr and if ptr is None, allocates memory for the size
# of int32 bytes stores the value and returns. If ptr is not None it stores the value
# at pointer.
# raises mymem_badval(value) exception if the value overflows on both sides
# negative or positive.
# stores value in little indian format. (x86 way)


    def store_int32(self, val, ptr=None):
        # if ptr != None:
        #     self.ptr_check(ptr)
        # YOUR CODE 
        if ptr==None:
            ptr=self.mem_alloc(4,'myint32')
        else:
            if (ptr <self.start or ptr > self.start+self.memsize):
                return "Invalid pointer"

        # Add line to check if ptr is a valid pointer
        self.byte_arr[ptr-self.start]=val&0xff
        self.byte_arr[ptr+1-self.start]=val>>8&0xff 
        self.byte_arr[ptr+2-self.start]=val>>16&0xff 
        self.byte_arr[ptr+2-self.start]=val>>24&0xff
        return ptr
        #raise NotImplementedError 

# 
# returns the value of the int64 at ptr.
# raises mymem_badval(value) exception if the value overflows on both sides
# negative or positive. (note this is only possible due to your bug as
# store_int64 checks the value for exactly the same.

    def load_int64(self,ptr):
        #self.ptr_check(ptr)
        # YOUR CODE 
        if (ptr <self.start or ptr > self.start+self.memsize):
                    return "Invalid pointer"
        else:
            #value=self.byte_arr[ptr - self.start ]|self.byte_arr[ptr - self.start +1]<<8|self.byte_arr[ptr - self.start +2]<<16|self.byte_arr[ptr - self.start +3]<<24|self.byte_arr[ptr - self.start +4 <<32|self.byte_arr[ptr - self.start +5]<<40|self.byte_arr[ptr - self.start +6]<<48|self.byte_arr[ptr - self.start +7]<<56]           
            value=self.byte_arr[ptr - self.start ]
            return value
        #raise NotImplementedError 

# stores the int64 value at ptr and if ptr is None, allocates memory for the size
# of int64 bytes stores the value and returns. If ptr is not None it stores the value
# at pointer.
# raises mymem_badval(value) exception if the value overflows on both sides
# negative or positive.
# stores value in little indian format. (x86 way)

    def store_int64(self, val, ptr=None):
        # if ptr != None:
        #     self.ptr_check(ptr)
        # YOUR CODE 
        if ptr==None:
            ptr=self.mem_alloc(8,'myint64')
        else:
            if (ptr <self.start or ptr > self.start+self.memsize):
                return "Invalid pointer"

        # Add line to check if ptr is a valid pointer
        self.byte_arr[ptr-self.start]=val
        # self.byte_arr[ptr-self.start]=val&0xff
        # self.byte_arr[ptr+1-self.start]=val>>8&0xff 
        # self.byte_arr[ptr+2-self.start]=val>>16&0xff 
        # self.byte_arr[ptr+3-self.start]=val>>24&0xff
        # self.byte_arr[ptr+4-self.start]=val>>32&0xff
        # self.byte_arr[ptr+5-self.start]=val>>40&0xff
        # self.byte_arr[ptr+6-self.start]=val>>48&0xff
        # self.byte_arr[ptr+7-self.start]=val>>56&0xff
        return ptr
        #raise NotImplementedError 

# leave it as is it prints all values for testing purposes etc.

    def __str__(self):
        s=f'memtotal: {self.memsize} allocated: {self.allocated} free: {self.free}'
        s+= '\n'
        s+=f'membyalloctypes: {self.alloc_types}'
        s+= '\n'
        s1=f'start: {hex(self.start)} end: {hex(self.end)} current: {self.current}'
        s=s+s1
        return s

# the following helps get the memobj by the clients ie. the individual
# classes.

mymemobj=None


def getmemobj(size):
    global mymemobj
    if mymemobj:
        return mymemobj
    mymemobj=mymemory(size)
    return mymemobj
     

def getmymemobj():
	return mymemobj
          

