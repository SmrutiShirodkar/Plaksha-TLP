
# returns the count of the binary tree nodes less than or equal to val.
# you can write your own sub-functions any for recursion or whatever. 
# the following are the variables and functions that you can access
# from the tree object.
# the tree object you will have access to tree.root variable.
# variables for access tree.root
# tree.root --> root node (mybnode object)
# each tree node is of class mybnode(). The only function you have to access
# in this is mynode.first() -> that will return the "object in the node". 
# mynode.first() --> returns the "first object in the node" 
#eg.
# node.obj_list.size -- >this will return the no. of objects in this node that
# has the same value. which means a binary tree node has multiple different objects if 
# they all have the same value. any counts should include this appropriately.
# valcmp--> function passed and should be called like "valcmp(val, obj)"
# this function returns 0 if the val is equal to value of the object
# returns <0 if the val is less than object value
# returns >0 if the val is greater than object value

# Other tree functions that you can use for this problem is given below:
# the left and right mybnode objects  are accessible via :
# the following are tree object functions (not of mybnode objects): 
# tree.myleft(node) -- returns left node
# tree.myright(node) -- returns right node
# tree.myleaf(node)-- returns True if node is a leaf node.
# tree.mycount(node)
# Note: if node is None, does not MEAN it is a leaf node. So, dont 
# use this to special case anything. Use  tree.myleaf(node) to check
# for leaf node.
# No other functions should be used. 

# no need to import any thing except to use the above functions.


def mycount_leq(tree, val, valcmp):
    #YOUR CODE
    return myz(tree,tree.root,val,valcmp)
    # raise NotImplementedError
def myz(tree, node, val, valcmp):
    count_z = 0

    if node is None:
        return count_z

    if tree.myleaf(node) is True:
        if valcmp(val,node.first()) >= 0:
            count_z = node.obj_list.size
        else:
            count_z = 0
        return count_z

    if valcmp(val,node.first()) ==0:
        count_z=node.obj_list.size + tree.mycount(tree.myleft(node))
        return count_z

    elif valcmp(val,node.first()) <0:
        count_z=myz(tree,tree.myleft(node),val,valcmp)
        return count_z

    elif valcmp(val,node.first()) >0:
        count_z=node.obj_list.size + tree.mycount(tree.myleft(node)) + myz(tree,tree.myright(node),val,valcmp)
        return count_z
    #raise NotImplementedError
