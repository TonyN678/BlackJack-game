class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank

    def set_rank(self, rank):
        self.rank = rank

    def get_suit(self):
        return self.suit

    def set_suit(self, suit):
        self.suit = suit

#    def __str__(self):
#       return self.rank, self.suit

    def __repr__(self):
        return "%s%s" % (self.rank, self.suit)
