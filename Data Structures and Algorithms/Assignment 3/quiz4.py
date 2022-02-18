from mylist import *

#
#  the mylist object is initialized as follows.
#
#class myelem():
#    def __init__(self, obj):
#        self.next=self
#        self.prev=self
#        self.obj=obj
#
#class mylist():
#    list_type=['stack', 'list', 'queue']
#
#    # init function do not change this.
#
#    def __init__(self, type):
#        self.header=myelem(self)
#        self.size=0
#        if type not in self.list_type:
#            raise Exception("List type incorrect")
#        self.type=type
#        self.tail=self.header

# write the code to implement the following functions
# that correspond to mylist ADT but writteen one op at
# time here for testing purpose.
# assume that myl (mylist object) is initialized for the
# right queue type for appropriate function call.
# you can access members of mylist object listed above in 
# the __init__ function for mylist..


# NOTE: update all the members relevant for the operations below.
# like tail, size, etc.,


# Add the object to the list increment the size.

def myadd(myl: mylist, obj):
    elem=myelem(obj)
    if (myl.size==0):    
        myl.header.next=elem
        myl.header.prev=elem
        elem.next=myl.header
        elem.prev=myl.header
        myl.tail=elem
    else:
        elem.prev=myl.header
        elem.next=myl.header.next
        elem.next.prev=elem
        myl.header.next=elem
    
    myl.size+=1
    #raise NotImplementedError

# Enqueue the object as per the queue definition

def myenqueue(myl: mylist, obj):
    elem=myelem(obj)
    if (myl.size==0):
        myl.header.next=elem
        myl.header.prev=elem
        elem.next=myl.header
        elem.prev=myl.header
    else:
        myl.header.prev.next=elem
        elem.prev=myl.header.prev
        myl.header.prev=elem
        elem.next=myl.header
    myl.tail=elem
    myl.size+=1
    #raise NotImplementedError

# Push the object on the stack as per the definition

def mypush(myl: mylist, obj):
    elem=myelem(obj)
    if (myl.size==0):    
        myl.header.next=elem
        myl.header.prev=elem
        elem.next=myl.header
        elem.prev=myl.header
        myl.tail=elem
    else:
        elem.prev=myl.header
        elem.next=myl.header.next
        elem.next.prev=elem
        myl.header.next=elem
    myl.size+=1
    #raise NotImplementedError

# Delete the object from the list, be it a list, stack or queue

def mydelete(myl: mylist, obj):
    header_dummy=myl.header.next
    while (header_dummy!=myl.header):
        if (header_dummy!=myl.tail):
            if (header_dummy.obj == obj):
                header_dummy.next.prev=header_dummy.prev
                header_dummy.prev.next=header_dummy.next
                myl.size-=1 
            header_dummy=header_dummy.next
        else:
            if (header_dummy.obj == obj):
                header_dummy.prev.next=header_dummy.next
                header_dummy.next.prev=header_dummy.prev
                myl.tail=header_dummy.prev
                myl.size-=1
            header_dummy=header_dummy.next 
    #raise NotImplementedError

# mylookup returns the object if object is found else, None.
# cmp function is sent some time for users of
# the lookup to return the right object. Use it to compare
# the equality of the object.

def mylookup(myl: mylist, val, cmp=None):
    header_dummy=myl.header.next
    while (header_dummy!=myl.header):
        if (cmp == None):
            if (header_dummy.obj == val):
                return header_dummy.obj
        else:
            if cmp(header_dummy.obj,val):
                return header_dummy.obj
        header_dummy=header_dummy.next
    return None
    #raise NotImplementedError

# pop the stack element as per the definition
# return object

def mypop(myl: mylist):
    dummy_head=myl.header
    if (myl.size!=0):
        if (myl.size==1):
            myl.tail=myl.header
        dummy=dummy_head.next
        dummy.next.prev=dummy.prev
        dummy.prev.next=dummy.next
        myl.size-=1
        return dummy.obj
    #raise NotImplementedError

# give the peek value of the stack as per definition
# return object

def mypeek(myl: mylist):
    return myl.header.next.obj
    #raise NotImplementedError

# dequeue the object from the list as per the definition

def mydequeue(myl: mylist):
    dummy_head=myl.header
    if (myl.size!=0):
        if (myl.size==1):
            myl.tail=myl.header
        dummy=dummy_head.next
        dummy.next.prev=dummy.prev
        dummy.prev.next=dummy.next
        myl.size-=1
        return dummy.obj
    #raise NotImplementedError

# write the code to delete all the elements passed in 
# myl object.

def mydeleteall(myl:mylist):
    myl.header.next=myl.header
    myl.size=0
    myl.tail=myl.header
    #raise NotImplementedError

