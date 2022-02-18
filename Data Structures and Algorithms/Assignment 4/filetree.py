import os
import sys
from stat import *
from mylist import *
from random import randrange
from mystat import *


# cmp function for list lookups
# cmp node objects 
def node_obj_cmp(node, obj):
    if node.nobj == obj:
        return True
    else:
        return False

# compare object names

def node_objname_cmp(node, name):
    if node.nobjname == name:
        return True
    else:
        return False

def node_objid_cmp(node, id):
    if node.nobjid == id:
        return True
    else:
        return False

class FILEOBJ_FOUND(Exception):
    """File object found"""
    pass

def find_me(obj, path, fileobj):
    if obj.objid==fileobj.objid:
        fileobj.path=path
        raise FILEOBJ_FOUND

# file objects 
# mandatory to have  these members.
# name - file name (not the full path)
# objid - file object is thisis the inode no. in the stat
# stat - stat object of the file returned by os.stat api.
# dir 0 (default) implies it is not directory but a regular file.
# dir 1 implies it is a directory.
# 

class myfile():

    # look above for argument descriptions.
    # raise exception if dir is 1 and not a dir
    # raise exception fi dir is 0 and not a regular file.
    # DO NOT CHANGE THIS. 
    # you can add additional members if required.

    def __init__(self, objid, name=None, stat=None, dir=0):

        # leave the following in there.
        if name and '/' in name:
            raise Exception("Bad name in file")
        if dir and stat and not S_ISDIR(stat.st_mode):
            s=f'{name} is not a directory'
            raise Exception(s)
        if not dir and stat and not S_ISREG(stat.st_mode):
            s=f'{name} is not a file'
            raise Exception(s)

        self.name=name
        self.objid = objid
        self.stat=stat
        self.dir=dir
        self.path=None
        # raise NotImplementedError

    
    # return the file path from root of the tree to which it belongs.
    # eg., I will create a file object with
    # fobj=myfile(241573) ie. only with objectid.
    # print(fobj.path(tree))
    # where this file is part of the tree.  Note: not this instance
    # of the object but the same objectid.
    # it should print the file path.
    # the objectid is found by "ls -i1" in any of the subdirectory
    # of the kernel-0 folder sent to you.  you can do that even on windows
    # with powershell i believe.
    # this function should print the full path of that objectid starting
    # from the kernel-0 folder.
    # eg., if the file kernel-0/mm/f1.c and its objectid is 241573
    # then fobj.file_path(tree) should print kernel-0/mm/f1.c
    # Note: this has to be recalculated from the tree when this function
    # is called. Tree was the object obtained from convert_to tree function
    # at the end of this file.


    def file_path(self, tree):
        try:
            tree.func_traverse(find_me,self)
        except Exception as FILEOBJ_FOUND:
            return self.path
        return None 
        #raise NotImplementedError

    # return the file size
    # required for the binary tree organization of these file objects.
    # for assignment 6.


    def file_size(self):
        pass
        #raise NotImplementedError

    # this is just a helper. feel free to modify the way you want it to help
    # you.

    def __str__(self):
        return self.name

# directory objects inherit from file, uses 
# all of what file has plus some more interfaces.

def mydir_total_files(obj,path, self):
    if obj.dir==0:
        self.total_files+=1

def mydir_total_dirs(obj,path, self):
    if obj.dir==1:
        self.total_dirs+=1

class mydir(myfile):

    # DO NOT CHANGE THIS.
    # you can add any members below this.

    def __init__(self, objid, name=None, stat=None, ):
        super().__init__(objid, name, stat, 1)
        self.total_files=0
        self.total_dirs=0
        #raise NotImplementedError

    # find the total no. of files underneath this directory including 
    # the directories (as they are also files) as well. 
    # eg., if you have a folder : kernel-0/mm/f1.c and kernel-0/mm/f2.c
    # dir_total_files of the directory kernel-0 will print : 3. two regular
    # files and one directory file "mm".
    # use case will be :
    # dir=mydir(245173)
    # dir.dir_total_files(tree)
    # where this directory is part of the tree.  Note: not this instance
    # of the object but the same objectid.
    # Note this has to be "calculated" every time the function is called
    # from the passed tree. 

    def dir_total_files(self, tree):
        path=self.file_path(tree)
        dw=self.path.split('/')
        for i in range(0,len(dw)):
            if i == 0:
                pobj=tree.root
                continue
            pobj=tree.lookup(pobj,dw[i])
        if pobj==None:
            return None
        #pobj=tree.lookup(pobj, dw[-1])
        tree.func_node_traverse(pobj,mydir_total_files,self)
        return self.total_files
        #raise NotImplementedError
    
    # the below function is similar as above but should print the only the total
    # no. of directories underneath this directory.
    # Note this has to be "calculated" every time the function is called
    # from the passed tree. 

    def dir_total_dirs(self, tree):
        path=self.file_path(tree)
        dw=self.path.split('/')
        for i in range(0,len(dw)):
            if i == 0:
                pobj=tree.root
                continue
            pobj=tree.lookup(pobj,dw[i])
        if pobj==None:
            return None
        #pobj = tree.lookup(pobj, dw[-1])
        tree.func_node_traverse(pobj,mydir_total_dirs,self)
        return self.total_dirs
        #raise NotImplementedError


class mynode():
    # pobj - parent object
    # obj - this object
    # objname - name of this object
    # objid - unique id of this object. for file and dir it is inode numbes.
    # Do not change this.

    def __init__(self, pobj, obj, objname, objid):
        self.child_list=mylist("list")
        self.nobj=obj
        self.nobjname = objname
        self.nobjid=objid
        self.npobj = pobj

class mytree():

# init function for root object and name and its object id.
# (object id for these objects are all inode numbers).
# Do not change this.

    def __init__(self, obj, root_name, id):
        self.root=mynode(None, obj, root_name, id)
        self.total_nodes=1

# the following two functions are helper functions for 
# constructing the tree, insertions etc..


# Lookup objname from a parent node, if found return
# node object. 
# If it does not  exist, create a node for that objname,
# objid combinations, ensure to add it to the appropriate child
# list.

    def lookup_create(self, pobj:mynode, objname, objid, obj):
        for i in pobj.child_list:
            if i.nobjname == objname:
                return i
        n=mynode(pobj,obj,objname,objid)
        pobj.child_list.add(n)
        return n
        #raise NotImplementedError

# Lookup objname from a parent node, if found return
# node object. If not, return None.

    def lookup(self, pobj:mynode, objname):
        for i in pobj.child_list:
            if i.nobjname == objname:
                return i
        return None
        #raise NotImplementedError


# Method on the tree object to traverse and it will call the function
# func with the passed arguments (variable argument args), for 
# every line of the object it will generate as output corresponding 
# to the input file in function convert_input_to_tree().
#
# for the eg. mentioned in the comments of that function
# the function func() will get called for each of the
# lines given there. And that string will be passed as first argument to the
# function.

# func_traverse(tree, test_func, argobj) returned by convert_input_to_tree() will call 
# test_func(fobj, "kernel-0", argobj) where fobj is the mydir obj for kernel-0.
# test_func(fobj, "kernel-0/arch", argobj) where fobj is the mydir obj for kernel-0/arch.
# test_func(fobj, "kernel-0/arch/boot", argobj) where fobj is the mydir obj for kernel-0/arch/boot.
# test_func(fobj, "kernel-0/arch/boot/bootloader.lds", argobj) where fobj is the  myfile obj 
# for kernel-0/arch/boot/bootloader.lds.

# you can test this function by putting the string in some file or std output
# and then compare the entire output with the original input file (sort both to
# avoid any ordering issues).
    def __traverse__(self,node,prefix,func,*args):
        if prefix== "":
            prefix=node.nobjname
        else:
            prefix=prefix + "/" + node.nobjname
        func(node.nobj,prefix,*args)
        
        for c in node.child_list:
            self.__traverse__(c, prefix,func,*args)

    def func_traverse(self, func, *args):
        self.__traverse__(self.root,"",func,*args)
        #raise NotImplementedError
        

# exactly same as above function except that the traversal starts
# from an intermediary mynode() object ie., an interior node.

    def func_node_traverse(self, node, func, *args):
        self.__traverse__(node,"",func,*args)
        #raise NotImplementedError
        

# some debug stuff may be useful.

    def dump1(self, root):
        print(root.obj)
        print(f'{root.obj} Child: ', end="")
        for i in root.child_list:
            print(f'{i.obj}, ', end="")
        print('\n')
        for i in root.child_list:
            self.dump1(i)

# some debug stuff may be useful.

    def dump(self):
        print(f'Total Nodes: {self.total_nodes}')
        self.dump1(self.root)


# Function takes an input file name 
# and converts that into an object instance of 
# the tree class as defined above.
# you can only use the operations given above to construct the tree.
# no other functions should be added.
# input file will be of the form:
#kernel-0
#kernel-0/arch
#kernel-0/arch/alpha
#kernel-0/arch/alpha/boot
#kernel-0/arch/alpha/boot/bootloader.lds
# the above should be converted to tree with root object being the
# directory object - kernel-0, and there are arch, alpha and boot as
# directory objects below and bootloader.lds as a file object below.
# construct the appropriate hierarchy. The mynode.obj should be 
# either a mydir or myfile object as defined above.

# returns "tree" object.

# hint use readlines, strip, and split if required  and os.stat

def convert_input_to_tree(filename):
    #Open file and create tree
    fd = open(filename)
    myline=fd.readline()
    rootname=myline.strip()
    st=mystat(rootname)
    rootdir=mydir(st[ST_INO],rootname,st)
    tree=mytree(rootdir,rootname,st[ST_INO])

    myline=fd.readline()
    while (myline):
        myline=myline.strip()
        dw=myline.split('/')
        st=mystat(myline)
        if S_ISDIR(st.st_mode):
            obj=mydir(st[ST_INO],dw[-1],st)
        else:
            obj=myfile(st[ST_INO],dw[-1],st)
        for i in range(0,len(dw)-1):
            if i==0:
                pobj=tree.root
                continue
            pobj=tree.lookup(pobj,dw[i])
            assert(pobj)
        #print(tree.root.child_list)
        obj=tree.lookup_create(pobj,dw[-1],st[ST_INO],obj)
        # print(obj)
        myline=fd.readline()
    return tree
    #raise NotImplementedError

#convert_input_to_tree('kernel-0.files')

