

class Card:
    '''
        This class is part of the assignment specification.
        I should mention than I am using this class by referencing from
        http://moodle.vle.monash.edu/mod/assign/view.php?id=4411167
        '''
    def __init__(self,faceValue,suitType):
        self.face = faceValue
        self.suit = suitType

    def getFace(self):
        return self.face

    def getSuit(self):
        return self.suit

    def __str__(self):
        return str(self.getFace()) + ":" + str(self.getSuit())
