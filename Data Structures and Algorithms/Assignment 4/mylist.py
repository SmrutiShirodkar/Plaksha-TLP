import os
import sys

# as discussed in the class and subsequent discussions 
# have an ADT for this and you can use this to create
# whatever you want.
# you are welcome to implement this in a way you want and use it.
# I am giving you a template where a single linked list
# can be used for multiple objects .. 
# to share code as much as possible in a single ADT.
# l1 = mylist(list) --> behaves like a list
# l2 = mylist(stack) --> supports stack and other operations(like push, pop
# etc.)  are disallowed.
# l3 = mylist(queue) --> same here. (like enqueue, dequeue etc.)

# you are welcome to use your own ADT whatever way.

class myelem():
    def __init__(self, obj):
        self.next=self
        self.prev=self
        self.obj=obj

class mylist():
    list_type=['stack', 'list', 'queue']

    # init function do not change this.

    def __init__(self, type):
        self.header=myelem(self)
        self.size=0
        if type not in self.list_type:
            raise Exception("List type incorrect")
        self.type=type
        self.tail=self.header

    # cmp function is sent some time for users of
    # the lookup to return the right object. See usage
    # below. See same_
    # see comment in mycrm.py above server_same and vm_same.. functions.
    # the cmp method is used if it is not None to check for object
    # equality. 
    # for each element in list:
    #        if (cmp(val, element) is true:
    # return object

    def lookup(self, val, cmp=None):
        header_dummy=self.header.next
        while (header_dummy!=self.header):
            if (cmp == None):
                if (header_dummy.obj == val):
                    return header_dummy.obj
            else:
                if cmp(header_dummy.obj,val):
                    return header_dummy.obj
            header_dummy=header_dummy.next
        return None
        # raise NotImplementedError
    
    # returns true if list is not empty
    # if it is empty, returns False.

    def not_empty(self):
        if (self.size>0):
            return True
        else:
            return False
        # raise NotImplementedError

    #  returns first element

    def first(self):
        return self.header.next.obj
        # raise NotImplementedError

    # returns last element

    def last(self):
        return self.header.prev.obj
        # raise NotImplementedError

    # adds the element to 
    def add(self, obj):
        if self.type != 'list':
            raise Exception("Add op supported only for list")
        elem=myelem(obj)
        if (self.size==0):    
            self.header.next=elem
            self.header.prev=elem
            elem.next=self.header
            elem.prev=self.header
            self.tail=elem
        else:
            elem.prev=self.header
            elem.next=self.header.next
            elem.next.prev=elem
            self.header.next=elem
        self.size+=1
    #raise NotImplementedError

    def push(self, obj):
        if self.type != 'stack':
            raise Exception("push op supported only for stack")
        elem=myelem(obj)
        if (self.size==0):    
            self.header.next=elem
            self.header.prev=elem
            elem.next=self.header
            elem.prev=self.header
            self.tail=elem
        else:
            elem.prev=self.header
            elem.next=self.header.next
            elem.next.prev=elem
            self.header.next=elem
        self.size+=1
        #raise NotImplementedError
    
    def pop(self):
        if self.type != 'stack':
            raise Exception("pop op supported only for stack")
        dummy_head=self.header
        if (self.size!=0):
            if (self.size==1):
                self.tail=self.header
            dummy=dummy_head.next
            dummy.next.prev=dummy.prev
            dummy.prev.next=dummy.next
            self.size-=1
            return dummy.obj
        # raise NotImplementedError

    def peek(self):
        if self.type != 'stack':
            raise Exception("peek op supported only for stack")
        return self.header.next.obj
        raise NotImplementedError

    def enqueue(self, obj):
        if self.type != 'queue':
            raise Exception("Enqueue op supported only for queue")
        elem=myelem(obj)
        if (self.size==0):
            self.header.next=elem
            self.header.prev=elem
            elem.next=self.header
            elem.prev=self.header
        else:
            self.header.prev.next=elem
            elem.prev=self.header.prev
            self.header.prev=elem
            elem.next=self.header
        self.tail=elem
        self.size+=1
        #raise NotImplementedError

    def dequeue(self):
        if self.type != 'queue':
            raise Exception("Dequeue op supported only for queue")
        dummy_head=self.header
        if (self.size!=0):
            if (self.size==1):
                self.tail=self.header
            dummy=dummy_head.next
            dummy.next.prev=dummy.prev
            dummy.prev.next=dummy.next
            self.size-=1
            return dummy.obj
        #raise NotImplementedError
   
   # works for all of the three types.

    def delete(self, obj):
        header_dummy=self.header.next
        while (header_dummy!=self.header):
            if (header_dummy!=self.tail):
                if (header_dummy.obj == obj):
                    header_dummy.next.prev=header_dummy.prev
                    header_dummy.prev.next=header_dummy.next
                    self.size-=1 
                header_dummy=header_dummy.next
            else:
                if (header_dummy.obj == obj):
                    header_dummy.prev.next=header_dummy.next
                    header_dummy.next.prev=header_dummy.prev
                    self.tail=header_dummy.prev
                    self.size-=1
                header_dummy=header_dummy.next 
        #raise NotImplementedError

    # iterator objects for all.

    def __iter__(self):
        self.dummy=self.header.next
        return self
        #raise NotImplementedError

    def __next__(self):
        if self.dummy!=self.header:
            val=self.dummy.obj
            self.dummy=self.dummy.next
            return val
        else:
            raise StopIteration

    def __str__(self):
        s=''
        h=self.header
        e=self.header.next
        s=f'List size: {self.size}'
        s += '\n'
        while e != h:
            s += f'{e.obj}'
            if (e.next != h):
                s += '\n'
            e = e.next
        s += '\n'
#       if e.prev != self.tail:
#            s += f'tail corrupt: tail: {self.tail.obj} list tail: {e.prev.obj}'

        if self.tail != self.header:
            s += f'Tail: {self.tail.obj}'
        s += '\n'
        return s
             

def main():
    # x = mylist("stack")
    # x.push(1)
    # x.push(34)
    # for i in range(10):
    #     x.push(i)
    # print(x)
    # for i in x:
    #     print(i)
    pass

if __name__ == "__main__":
    main()
