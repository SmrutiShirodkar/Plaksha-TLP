import os
import sys
from mylist import *
from collections import namedtuple
from myserver import *
from myvm import *

# Toy Cloud resource manager for compute servers and virtual machines.
# mycrm() object manages simple set of compute servers and virtual machines.
# myserver and myvm objects. these objects are instantiated when they are
# created via the specified interfaces below and uses the list class of data
# structures (list, stack, queues etc, ) whatever required to help you do the
# operations below. Please do not use python list except in the return value of
# the two functions listed here, and one function in myserver object. see
# myserver.py.
# This is a very simple assignment to manage '3' states of each object: 
# myserver - 'idle', 'active', 'fail'
# myvm - 'provision', 'idle', 'active'
# there are handful of operations listed here.
#see test.py for how it is being used. 
# and start with simple tests given in crm_server(), and crm_vm() tests, and
# then move to generic test in crm_nvms()
# The whole logic is very simple as per the state diagram in the pdf and as 
# discussed in the class..
# simple thought process, design and implementation. This is just the use case
# of how to maintain and implement a class of data structures belonging to lists
# (list, stack, queues etc.). Use the right one for the right purpose below.
# You are also supposed to implement mylist.py which will have all the ADT
# belonging to any list you create and you can utilise it below. No skeleton
# code will be given for that as it was already discussed in the class.
# it will typically implement things like: 
# add, delete, lookup, iterator for lists and push, pop, peek operators for the
# stack etc.


# The following has to be used as is. no changes
# and stored in the object in the init functions
# myserver init will store sconf
# myvm init will store vconf

sconf = namedtuple('sconf', 'name ncpu mem ')
vconf = namedtuple('vconf', 'name ncpu mem ')
# return this stat in get_stat
# see get_stat in mycrm
# these are statistics related myserver and myvm state transitions and total
# no.of objects, deleted objects etc., see comments above get_stat.
# 
crm_stat_fields=('stotal', 'sidle', 'sactive', 'sfail', 'sdeleted', 'vtotal', 'vprovision', 'vactive', 'vidle', 'vdeleted')
crm_stat=namedtuple('crm_stat', crm_stat_fields, defaults=(0,)*len(crm_stat_fields))

# You are welcome to add any helper functions for this class here.
# helper functions for lookup.
# mylist.lookup(obj, server_same) 
# will call this function  every time with the
# object object and name and you can use it compare the name and 
# if you return success here, lookup will return success.
# depending on what you want to compare you can add more such functions.
# this is a pattern of general list lookup(), where you can do 
# object specific comparisons the way you want, while not knowing
# how the list is stored.

def server_same(sobj, name):
    if sobj.sc.name == name:
        return 1
    return 0
def vm_same(vm, name):
    if vm.vc.name == name:
        return 1
    return 0

class mycrm ():

    # The members listed must be present and should not be changed.
    # You are welcome to add new members as required to accomplish
    # the results of the assignment.

    def __init__(self):
        self.stat_types=['stotal', 'sidle', 'sactive', 'sfail', 'sdeleted', 'vtotal',
                'vprovision', 'vactive', 'vidle', 'vdeleted' ]
        self.stats={}
        for i in self.stat_types:
            self.stats[i]=0
        self.myservers=mylist("list")
        self.myvms=mylist("list")       
        self.prov_vms = mylist('stack') 
        # raise NotImplementedError

    # Add the new compute server with name, and ncpu and mem.
    # eg., mycrm.add("s1", 2, 1000) --> adds the server with name s1, 
    # no. of cpus (cores) as 2, and memory as 1000 Gigabyte. All units
    # are same. So dont bother about any unit conversions.
    # see test.py for how it is being used.
    # raises exception if name already exists.
    # It creates a new myserver object in a state='idle'
    # After which, if there are unprovisioned idle vms, it will
    # provision them to this new server if possible by calling
    # the routine self.provision_idle_vms(s). See below.
    # the moment any VMs provisioned to this server becomes active this server
    # state becomes active.
    # eg. after creation of myserver object state='idle', and if
    # provision_idle_vms() provisions one and activates it, state ='active'. If
    # provision_idle_vms() wont provision a vm on this server and activate it,
    # the server state will continue to be state='idle'. 

    def add(self, name, ncpu, mem):
        sc=sconf(name,ncpu,mem)
        sr=self.myservers.lookup(name)
        if sr != None:
            raise Exception("Already exists")  
        self.sr=myserver(sc,self.stats)
        self.myservers.add(self.sr)
        return self.sr 
        # raise NotImplementedError

    # deletes the server from the system if its state is not 'active'.
    # state will be 'active' when there are active vm's provisioned
    # on the server. If there are no vm's server will go to 'idle'
    # state. Therefore delete works if the state of the server is 
    #either 'idle' or 'fail' state.

    def delete_server(self, name):
        sr=self.myservers.lookup(name, server_same)
        if sr == None:
            raise Exception("Server not found")
        sr.delete()
        self.myservers.delete(sr)
        # raise NotImplementedError

    # fail, fails the server if it is not already in 'fail' state. 
    # All the vm's that are running in the server will be
    # moved to 'idle' state. Thus vm's will be drained and this server
    # moved to 'fail' state.
    # at the end of the operation, this server will be in 'fail' state
    # and all the vm's provisioned to this server will go to 'idle' state.

    # name is a string of the name of the server
    # eg., fail("s1")

    def fail(self, name):
        sr=self.myservers.lookup(name, server_same)
        if sr == None:
            raise Exception("Server ",sr," not found")
        sr.set_fail()
        # raise NotImplementedError

    # Unfail a server in 'fail' state. 
    # simply makes it 'idle' and reactivates it. state will be similar
    # to what it was right after its creation (as part of addition).
    # and similar to add() above, it will call provision_idle_vms() routine
    # to provision the vms that are not on any server. ie. idle

    # name is - string of the name of the server eg., "s1"
    #eg., unfail('s1')

    def unfail(self, name):
        sr=self.myservers.lookup(name, server_same)
        if sr == None:
            raise Exception("Server ",sr," not found")
        sr.unfail()
        # raise NotImplementedError
        # raise NotImplementedError


    # Provision a VM of config vconf (see above) with name, ncpu and mem.
    # eg., provision_vm("vm1", 2, 1) will try to provision a vm for 2 cpus
    # and 1 G of memory.
    # Raises exception if the name already exists.
    # At the end of this routine vm is successfully in 'provision' state
    # and bound to a server. However until "commit_provisioned_vms()" see below
    # is called the vm wont move to 'active' state.

    def provision_vm(self, name, ncpu, mem):
        vc=vconf(name,ncpu,mem)
        vm=self.myvms.lookup(name,vm_same)
        if vm != None:
            raise Exception("Already exists")
        for i in self.myservers:
            if i.can_provision(vc):
                vm=myvm(vc,i,self.stats)
                self.myvms.add(vm)
                self.prov_vms.push(vm)
                self.sr.provision_vm(vc,vm)
                return vm
        return None
        # raise NotImplementedError 
    
    # This routine just moves all the Vm's in the 'provision' state to 'active'
    # state and commits the provisioning process. At the end of this servers
    # which were idle can move to 'active' state if one of these provisioned
    # vm's on it becomes the first one to become active.

    def commit_provisioned_vms(self):
        for i in self.prov_vms:
            i.sr.commit_vm(i)
        self.prov_vms = mylist('stack')
        # raise NotImplementedError

    # provision undo : just deletes all the vm's in 'provision' state that were
    # created in provision_vm() routines before. And accordingly the resource
    # allocation if any from the server (cpu and memory) are undone and all
    # sanity returned as if the previous provision_vm() did not happen.
    # as discussed in the class 
    # people could  do:
    # mycrm.add(s1)
    # mycrm.provision_vm(vm1)
    # mycrm.provision_vm(vm2)
    # mycrm.commit_provisioned_vms() OR mycrm.provision_undo().
    # If provision is undone, vm1, and vm2 will be deleted.
    # if provision is committed, vm1 and vm2 will move to 'active' state and the
    # server s1's state will move accordingly.

    # provision_undo(10) --> undo the last 10 provision_vm() operation.
    # provision_undo(1) --> undo the last 1 provision_vm() operation.
    # this command can never fail, except that if there is no operation to undo
    # it raises the exception saying rase Exception ("NothingToUndo")

    def provision_undo(self, num):
        for i in range(num):
            if self.prov_vms.not_empty:
                vm = self.prov_vms.pop()
                vm.sr.deprovision_vm(vm)
                vm.delete(vm.sr)
                self.myvms.delete(vm)
            else:
                raise Exception("NothingToUndo")
        # raise NotImplementedError

    # deletes a vm from the system. Again all state transitions are maintained
    # properly. One can delete a vm when vm is in 'idle' 'active' state OR in
    # 'provision' state. If it is in 'provision' state provision_undo can come
    # and delete it as part of the undo operation. It can always be deleted thus
    # and all the state transitions and stats happen correctly as part of it.
    # eg., delete_vm (vm1)
    # if name does not exist, it raises an exception saying vm not found.

    def delete_vm(self, name):
        vm=self.myvms.lookup(name,vm_same)
        if vm == None:
            raise Exception("VM did not found") 
        # If vm is still bound to server, then deprovision vm from server 
        # This is happening through undo, but it is not happening through this function              
        if vm.sr:
            vm.sr.deprovision_vm(vm)    
        vm.delete(vm.sr)
        self.myvms.delete(vm)
        # raise NotImplementedError

    # reprovision the idle vms
    # method to provision any idle vm's to a server.
    # note: for this implementation provisioning implies that you are 
    # maintaining association in your list/state etc. that shows that 
    # the vm's are bound to the server. that's all. nothing fancy !
    # returns a count of vm's that are successfully provisioned to this
    # server sr.
    # sr - myserver object.
    # 

    def provision_idle_vms(self, sr):
        for i in self.myvms:
            if(i.state == "idle"):
                v = sr.provision_vm(i.vc,i)
                if(v==None):
                    break
            return self.nvms
        # raise NotImplementedError

    # method to provision all idle vms. Useful when some vm's are deleted
    # from the system and more slots are opened on the server. 
    #
    # it just runs through the idle vms and tries to provision it on every
    # server possible.
    # returns the count of the no. successfully provisioned to any server

    def provision_all_idle_vms(self):
        for k in self.myservers:
            for i in self.myvms:
                if(i.state == "idle"):
                    v = k.provision_vm(i.vc,i)
                    if(v==None):
                        break
            return self.nvms
            
        # raise NotImplementedError

    # this function returns a list of servers (the only place where "python list" can
    # be used) but all internal operations should not use python list or arrays
    # or any thing.
    # given a state it returns the list of objects corresponding to the state
    # passed.
    # get_servers('active') -> returns all active servers
    # get_servers('idle') -> returns all idle servers
    #
    # get_servers('any') -> is special it returns all servers irrespective of
    # the state.

    # state of the servers are :
    # 'active', 'idle', 'fail', final state 'deleted' at which point the object
    # will cease to exist. so that cannot be passed as an argument below.
    # any other state passed it will return empty string.
    # returns a python list of myserver objects for state. 
    # only place where python list can be used.

    def get_servers(self, state):
        srl=[]
        for i in self.myservers:
            if state != 'any' and i.state!=state:
                continue
            srl.append(i)
        return srl
        # raise NotImplementedError

    # This function just returns a list of all vms similar to the servers above.
    # get_vms('active')-- > returns all active vms
    # get_vms('idle') --> returns all idle vms  etc.
    # 
    # get_vms('any') -> is special it returns all servers irrespective of
    # the state.
    # state of the vms are : 'provision', 'idle', 'active', final state
    # 'deleted' at which point the object will cease to exist. so that cannot be
    # passed as an argument below.
    # returns a python list of myserver objects for state. 
    # only place where python list can be used.


    def get_vms(self, state):
        # vml=[]
        # for i in self.myvms:
        #     if state != 'any' and i.state!=state:
        #         continue
        #     vml.append(i)
        # return vml
        vml=[]
        vm = []
        for i in self.myvms:
            if i.state==state:
                vml.append(i)
            vm.append(i)
        if(state == "any"):
            print(vm)
            return vm
        else:
            return vml

        # raise NotImplementedError

    # statistics and book keeping. Each object myserver and myvm init functions
    # will be passed this stat object and that should be updated as required
    # when state transitions happen. eg., if myvm state changes from 'active' to
    # 'idle' the 'vactive' stat below will be decremented by 1, and 'vidle' stat
    # will be incremented by 1. On instantiation, myvm will  be in 'provision'
    # state and myserver will be in 'idle' state. 
    # see state diagram
    # DO NOT CHANGE THIS

    def get_stat(self):
        cs=crm_stat(self.stats['stotal'], \
                    self.stats['sidle'],\
                    self.stats['sactive'],\
                    self.stats['sfail'],\
                    self.stats['sdeleted'],\
                    self.stats['vtotal'],\
                    self.stats['vprovision'],\
                    self.stats['vactive'], \
                    self.stats['vidle'], \
                    self.stats['vdeleted'])
        return cs




def main():
    pass

if __name__ == "__main__":
    main()
