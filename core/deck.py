from core.card import Card
from random import seed,randint


class Deck:
    '''
    This class is part of the assignment specification.
    However, some of the code parts within this class needs to be changed.
    I will make some notes in which function I have made and the purpose for their creation.
    I should mention than I am using this class by referencing from
    http://moodle.vle.monash.edu/mod/assign/view.php?id=4411167
    '''
    def __init__(self, valueStart, valueEnd, numSuits):
        self.pile = []
        self.size = 0

        values = []

        i = valueStart

        while i <= valueEnd:
            values.append(i)
            i += 1

        i = 0

        while i < numSuits:
            for value in values:
                newCard = Card(value,i)
                self.pile.append(newCard)
                self.size += 1
            i += 1

    def __str__(self):
        newString = ""

        for card in self.pile:
            newString += (str(card) + ',')

        newString = newString[:-1]

        return newString

    def __len__(self):
        return self.size

    #adds an item at location where
    def addCard(self, card, where):
        if where > -1 and where <= self.size:
            self.pile = self.pile[:where] + [card] + self.pile[where:]
            self.size += 1
        else:
            print("I can't add there.")

    # draw a card from the top of the deck
    # I'm changing the name
    def drawCard(self):
        item = self.pile.pop()
        self.size -= 1

        return item

    def placeCardTop(self, card):
        self.addCard(card, self.size)

    def placeCardBottom(self,card):
        self.addCard(card, 0)

    def shuffle(self,**kwargs):

        newPile = []

        if "seed" in kwargs:
            seed(kwargs["seed"])

        while len(self.pile) > 0:
            item = randint(0, len(self.pile)-1)

            newPile.append(self.pile[item])

            del(self.pile[item])

        self.pile = newPile

    def is_empty(self):
        return len(self) == 0

    # Take 5 consecutive cards at the same time from the top to top - 5 and returns a list
    def draw_cards(self, amount=5):
        assert not self.is_empty(), "Cannot draw from an empty deck"
        cards = self.pile[-amount:]  # take n amount of cards from the top -- WROOONGG !!!!
        del self.pile[-amount:]  # delete n cards from the top
        self.size -= amount  # reduce the size number
        return cards

    # put the card list on top of the deck
    def place_cards(self, cards):
        assert not len(cards) == 0, "Card list cannot be empty"
        self.pile.extend(cards)  # place cards (list) to the top
        self.size += len(cards)

    # this magic function will return an iterator protocol object instead of iterable object
    # So, it can be used directly inside for loop inside implementation method of a class
    def __iter__(self):
        for item in self.pile:
            yield item
