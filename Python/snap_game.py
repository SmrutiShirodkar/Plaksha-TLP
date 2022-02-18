import random
class snap:
    def __init__(self):
        print("We are solving snap game.")
        
    def create_decks(self):
        L=[1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.one_deck=L*4
        #this is my standard deck and I need to create 2 decks so I create 2
        #on basis of standard for two people
        print("Before shuffling")
        self.D1=self.one_deck.copy()
        self.D2=self.one_deck.copy()
        print(self.D1)
        print(self.D2)
        D=[]
        D.extend(self.D1)
        D.extend(self.D2)
        #added both the decks to D
        random.shuffle(D)
        self.D1=D[:len(D)//2]
        self.D2=D[len(D)//2:]
        print("After shuffling")
        print(self.D1)
        print(self.D2)

obj = snap()
obj.create_decks()
