'''
import random

def initialise(faces,num):
    i=[]
    for k in range(20):
        total=0
        for i in range(num):
            total=total+random.randint(1,faces)
        L.append(total)
    return L
'''


import random
class dice:
    def fix_faces(self,k):
        self.faces=k
    def roll(self):
        answer=random.randint(1,self.faces)
        return answer
    def roll_many(self,n):
        total=0
        for i in range(n):
            total=total+random.randint(1,self.faces)
        return total
    def exp(self):
        self.faces(6)
        count=0
        flag=0
        while (flag==0):
            answer=self.roll_many(5)
            count=count+1
            if (answer==5):
               flag=1
       return count
    