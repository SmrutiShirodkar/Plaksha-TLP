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
        #YOUR CODE
        raise NotImplementedError
    
    # returns true if list is not empty
    # if it is empty, returns False.

    def not_empty(self):
        #YOUR CODE
        raise NotImplementedError

    #  returns first element

    def first(self):
        #YOUR CODE
        raise NotImplementedError

    # returns last element

    def last(self):
        #YOUR CODE
        raise NotImplementedError

    # adds the element to 
    def add(self, obj):
        if self.type != 'list':
            raise Exception("Add op supported only for list")
        #YOUR CODE
        raise NotImplementedError

    def push(self, obj):
        if self.type != 'stack':
            raise Exception("push op supported only for stack")
        #YOUR CODE
        raise NotImplementedError
    
    def pop(self):
        if self.type != 'stack':
            raise Exception("pop op supported only for stack")
        #YOUR CODE
        raise NotImplementedError

    def peek(self):
        if self.type != 'stack':
            raise Exception("peek op supported only for stack")
        #YOUR CODE
        raise NotImplementedError

    def enqueue(self, obj):
        if self.type != 'queue':
            raise Exception("Enqueue op supported only for queue")
        #YOUR CODE
        raise NotImplementedError

    def dequeue(self):
        if self.type != 'queue':
            raise Exception("Dequeue op supported only for queue")
        #YOUR CODE
        raise NotImplementedError
   
   # works for all of the three types.

    def delete(self, obj):
        #YOUR CODE
        raise NotImplementedError

    # iterator objects for all.

    def __iter__(self):
        #YOUR CODE
        raise NotImplementedError

    def __next__(self):
        #YOUR CODE
        raise NotImplementedError

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
    pass

if __name__ == "__main__":
    main()
