from random import randint

class Deck:
    def __init__(self, t):
        self.playerdeck = list(range(1,t+1))

    def shuffle_deck(self) :
        a = len(self.playerdeck)
        for i in range(a):
            j = randint(0, i)
            e = self.playerdeck[i]
            self.playerdeck[i] = self.playerdeck[j]
            self.playerdeck[j] = e
