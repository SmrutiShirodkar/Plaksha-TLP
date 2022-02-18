from myerror import *
from ctypes import *

#exceptions for bitvector.

class mybit_error(myerror):
    pass
class mybit_size_bad(mybit_error):
    def __init__(self, size, message="size not aligned or large"):
        self.size=size
        self.message=message
    def __str__(self):
        return f'{self.size} -> {self.message}'

class mybit_overflow(mybit_error):
    def __init__(self, size, bitv, message="bitindex larger than bitvector size"):
        self.size=size
        self.bitvectorsize=bitv.bit_total_bits
        self.message=message
    def __str__(self):
        return f'bitindex: {self.size} bitvector size: {self.bitvectorsize} -> {self.message}'

# bit vector implementation
# size in bytes
# bit vector allocates bits for every byte
# and sets state of 1 and 0 via
#  the methods set_bit, clear_bit, and is_free
# is_free returns 1 if bit is not set.
# is_set returns 1 if bit is set.

class mybit_vector:

# bit_vector -- byte array for states
# bit_nbytes - total bytes in the bit_vector
# bit_total_bits - size of the memory passed in the __init__
# bit_free - total bits that are free   
# bit_alloc - total bits that are alloced

    def __init__(self, size):
        if size % 8 != 0:
            raise mybit_size_bad(size)
        self.bit_vector=(c_ubyte * (size//8))()
        self.bit_nbytes=size//8
        self.bit_total_bits=size
        self.bit_free=size
        self.bit_alloc=0
        #self.bbin = 0

# Returns 1 if the bit is 0 ie. free
# Returns  0 if the bit is 1
    
    def is_free(self, bit):
        if bit >= self.bit_total_bits:
            raise mybit_overflow(bit,self)
        else:
            byte_index = bit // 8
            bit_index = bit % 8
            flag = self.bit_vector[byte_index] >> bit_index & 1
            if flag == 0:
                return 1
            else:
                return 0 
        #raise NotImplementedError 
# Returns 1 if the bit is set
# Returns 0 if the bit is not set

    def is_set(self, bit):
        if bit >= self.bit_total_bits:
            raise mybit_overflow(bit,self)
        else:
            byte_index = bit // 8
            bit_index = bit % 8
            flag = self.bit_vector[byte_index] >> bit_index & 1
            if flag == 1:
                return 1
            else:
                return 0  
        #raise NotImplementedError 

#sets the bit passed in "bit" (used by mem_alloc in the mymemory class)
# if the bit is > bit_total_bits it raises the mybit_overflow exception 
#defined above.

    def set_bit(self, bit):
        if bit >= self.bit_total_bits:
            raise mybit_overflow(bit,self)
        else:
            byte_index = bit // 8
            bit_index = bit % 8
            self.bit_vector[byte_index]=self.bit_vector[byte_index] + 1 << bit_index
        #raise NotImplementedError 

#clears the bit passed in "bit" (used by mem_free in the mymemory class)
# if the bit is > bit_total_bits it raises the mybit_overflow exception 
#defined above.

    def clear_bit(self, bit):
        if bit >= self.bit_total_bits:
            raise mybit_overflow(bit,self)
        else:
            byte_index = bit // 8
            bit_index = bit % 8
            if self.is_set(bit):
                self.bit_vector[byte_index]=self.bit_vector[byte_index] & (0b11111111 - (0b1 << bit_index))
        #raise NotImplementedError 

# prints the bit state. Dont print if the size is large. it will loop
# for ever trying to form the string. Do unit test with this though.

    def __str__(self):
        s=f'total_bytes: {self.bit_nbytes} total_bits: {self.bit_total_bits}'
        s=s+'\n'
        for i in range(0,self.bit_nbytes):
            if i%4==0:
                s=s+'\n'
            bb=self.bit_vector[i]
            for b in range(0,8):
                mask=1 << b
                if bb & mask:
                    s=s+'1'
                else:
                    s=s+'0'
            s=s+"  "
        return s
