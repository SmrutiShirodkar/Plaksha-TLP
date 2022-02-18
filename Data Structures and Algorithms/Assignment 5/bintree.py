import os
import sys
from stat import *
from mylist import *
from random import randrange
from filetree import *

# different comparison functions for the 
# file objects.
# object equality of myfile objects is based on objectid
# which is the inode number

# def s_cmp(obj1,obj2):
#     if obj1==obj2:
#         return True
#     return False

# def sl_cmp_obj(obj1, obj2):
#     if len(obj1) == len(obj2):
#         return 0
#     if len(obj1) < len(obj2):
#         return -1
#     if len(obj1) > len(obj2):
#         return 1

# def sl_cmp_val(val, obj):
#     if val==len(obj):
#         return 0
#     if val < len(obj):
#         return -1
#     if val > len(obj):
#         return 1


def myfile_cmp(obj1, obj2):
    if obj1.objid == obj2.objid:
        return True
    return False

# size based comparison between two myfile objects

def myfile_size_cmp(obj1, obj2):
    if obj1.file_size() == obj2.file_size():
        return 0
    if obj1.file_size() < obj2.file_size():
        return -1
    if obj1.file_size() > obj2.file_size():
        return 1

# size comparison but val is "int" and obj is myfile object.

def myfile_val_cmp(val, obj):
    if val == obj.file_size():
        return 0
    if val < obj.file_size():
        return -1
    if val > obj.file_size():
        return 1


# return a list of sorted objects only by using the public functions of 
# the binary tree.
# the methods given below. No internal members are seen by this.
# use any of the methods defined in the tree as given below. No new methods
# can be added for this.

def sort_helper(o,sorted_list):
    sorted_list+=[o]
    return sorted_list

def sorted_bintree(tree):
    sorted_list=[]
    tree.traverse(tree.root,sort_helper,sorted_list)
    return sorted_list
    # raise NotImplementedError


# binary node
# with left and right child

class mybnode(mynode):
    # pnode - parent node
    # obj - this object
    # left and right and obj add the way you want
    # Do not change this.
    # you can add more members if you want

    def __init__(self, pnode, obj):
        self.left=None
        self.right=None
        self.pnode = pnode
        self.obj_list=mylist('list')
        if obj!=None:
            self.obj_list.add(obj)
        #raise NotImplementedError

    def first(self):
        return self.obj_list.first()


#mybintree class. 
# it stores objects of myfile . but it can be general.
# objcmp, objvalcmp, and valcmp are the functions
# for checking. see the comparison functions above.
# objcmp -- for comparing two object ids returns true if
# they are equal.
# objvalcmp(obj1, obj2) -- for comparing value of two objects 
# returns 0, -1 or 1. 0 if equal, -1 if obj1 < obj2, and 
# 1 if obj1 > obj2. 
# valcmp(val, obj)--. compares val (in this case it represents 
# the size ) with object value.


class mybintree():

# init functionf or root object and name and its object id.
# (object id for these objects are all inode numbers).
# Do not change this.

    def __init__(self, obj):
        self.root=mybnode(None, obj)
        self.total_nodes=1
        #YOUR CODE
        #raise NotImplementedError

    def __insert__(self, node, obj, objcmp,objvalcmp):

        if objvalcmp(obj,node.obj_list.first())==0:
            node.obj_list.add(obj)
            return node
        if objvalcmp(obj,node.obj_list.first())>0:
            if node.right == None:
                node.right=mybnode(node, obj)
                return node.right
            else:
                self.__insert__(node.right,obj,objcmp,objvalcmp)
            
        if objvalcmp(obj,node.obj_list.first())<0:
            if node.left == None:
                node.left=mybnode(node, obj)
                return node.left
            else:
                self.__insert__(node.left,obj,objcmp,objvalcmp)
            

# insert object into the binary tree. objcmp and objvalcmp corresponds to the
# definitions listed above.
# if the same object is trying to get  inserted twice, raise exception
# ensure all the objects from the file list kernel-0.files are inserted
# here appropriately.
# 

    def insert(self, obj, objcmp, objvalcmp):
        if self.root.first()==None:
            self.root.obj_list.add(obj)
            return     
        self.__insert__(self.root, obj, objcmp, objvalcmp)
        #raise NotImplementedError



# traverse the binary tree func is the passed function has to be invoked with
# the object and the variable args *args passed here.

    def traverse(self, node, func, *args):
        self.traverse_from_node(self.root,func,*args)
        # raise NotImplementedError

    def traverse_from_node(self,node, func, *args):
        if node==None:
            return
        self.traverse_from_node(node.left,func,*args)
        for obj in node.obj_list:    
            func(obj,*args)
        self.traverse_from_node(node.right,func,*args)
        # raise NotImplementedError



# returns the height of the binary tree
    def __leaf__(self,node):
        if node.left == None and node.right == None:
            return True
        return False

    def __height__(self,node):
        h1=0
        h2=0
        if node == None:
            return 0
        if node.left != None:
            h1=self.__height__(node.left)
        if node.right != None:
            h2=self.__height__(node.right)
        h=max(h1,h2)
        if self.__leaf__(node):
            return h
        else:
            return h+1
        
    def height(self):
        return self.__height__(self.root)
        #raise NotImplementedError

# returns the count of the binary tree nodes.

    def __count__(self,node):
        if node==None:
            return 0
        return self.__count__(node.left)+self.__count__(node.right)+node.obj_list.size
    def count(self):
        return self.__count__(self.root)
        #raise NotImplementedError


# returns the count of the binary tree nodes less than or equal to val.
# Note: This cannot use the traverse function has to calculate from the
# current tree by going through it. cannot use any other public functions.


    def __count_leq__(self, node, val, valcmp):
        count_z = 0
        if node is None:
            return count_z
        if self.__leaf__(node) is True:
            if valcmp(val,node.first()) >= 0:
                count_z = node.obj_list.size
            else:
                count_z = 0
            return count_z
        if valcmp(val,node.first()) ==0:
            count_z=node.obj_list.size + self.__count__(node.left)
            return count_z
        elif valcmp(val,node.first()) <0:
            count_z=self.__count_leq__(node.left,val,valcmp)
            return count_z
        elif valcmp(val,node.first()) >0:
            count_z=node.obj_list.size + self.__count__(node.left) + self.__count_leq__(node.right,val,valcmp)
            return count_z

    def count_leq(self, val, valcmp):
        return self.__count_leq__(self.root,val,valcmp)
        #raise NotImplementedError


# returns the count of the binary tree nodes greater than or equal to val.
# Note: This cannot use the traverse function has to calculate from the
# current tree by going through it. cannot use any other public functions.

    def __count_geq__(self, node, val, valcmp):
        count_z = 0
        if node is None:
            return count_z
        if self.__leaf__(node) is True:
            if valcmp(val,node.first()) <= 0:
                count_z = node.obj_list.size
            else:
                count_z = 0
            return count_z
        if valcmp(val,node.first()) ==0:
            count_z=node.obj_list.size + self.__count__(node.right)
            return count_z
        elif valcmp(val,node.first()) <0:
            count_z=node.obj_list.size + self.__count__(node.right) + self.__count_geq__(node.left,val,valcmp)
            return count_z
        elif valcmp(val,node.first()) >0:
            count_z=self.__count_geq__(node.right,val,valcmp)
            return count_z

    def count_geq(self, val, valcmp):
        return self.__count_geq__(self.root,val,valcmp)
        # raise NotImplementedError


# returns the count of the binary tree nodes equal to val.
# Note: This cannot use the traverse function has to calculate from the
# current tree by going through it. cannot use any other public functions.

    def __count_eq__(self, node, val, valcmp):
            count_z = 0
            if node is None:
                return count_z
            if self.__leaf__(node) is True:
                if valcmp(val,node.first()) == 0:
                    count_z = node.obj_list.size
                else:
                    count_z = 0
                return count_z
            if valcmp(val,node.first()) ==0:
                count_z=node.obj_list.size
                return count_z
            elif valcmp(val,node.first()) <0:
                count_z=self.__count_eq__(node.left,val,valcmp)
                return count_z
            elif valcmp(val,node.first()) >0:
                count_z=self.__count_eq__(node.right,val,valcmp)
                return count_z
                
    def count_eq(self, val, valcmp):
        return self.__count_eq__(self.root,val,valcmp)
        # raise NotImplementedError

#     def dump1(self, node):
#         if node==None:
#             return
#         print(f'(s) Node:')
#         for i in node.obj_list:
#             print(i)

#         self.dump1(node.left,"Left")
#         self.dump1(node.right, "Right")

#     def dump(self):
#         print("Root Object: ")
#         for i in self.root.obj_list:
#             print(i)
#         self.dump1(self.root.left, "Left")
#         self.dump1(self.root.right, "Right")

# def main(): 
#     btree=mybintree(None)
#     btree.insert("ta",s_cmp,sl_cmp_obj)
#     btree.dump()
#     btree.insert("td",s_cmp,sl_cmp_obj)
#     btree.insert("tc",s_cmp,sl_cmp_obj)
#     btree.dump()
#     btree.insert("sahil",s_cmp,sl_cmp_obj)
#     btree.dump()
#     btree.insert("t",s_cmp,sl_cmp_obj)
#     btree.dump()
#     btree.insert("shiva",s_cmp,sl_cmp_obj)
#     btree.dump()

# if __name__=="__main__":
#     main()
