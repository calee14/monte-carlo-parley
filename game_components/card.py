import enum

class Suit(enum.IntEnum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4
    
    def __str__(self):
        return self.name()

class CardValue(enum.IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        if self.value <= 10:
            return str(self.value)
        elif self.value == 11:
            return "Jack"
        elif self.value == 12:
            return "Queen"
        elif self.value == 13:
            return "King"
        elif self.value == 14:
            return "Ace"
        return ""
    
    def high_value(self):
        return self.value
    
    def low_value(self):
        if self == CardValue.ACE:
            return 1
        return self.value

class Card:
    def __init__(self, rank: CardValue, suit: Suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class HandRank(enum.IntEnum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9
    
    def __str__(self):
        return self.name.replace("_", " ").title()

class Hand:
    # def __init__(self, cards: List[Card] = None):
    #     self.m_cards = cards or []
    #     self.m_rank = HandRank.HIGH_CARD
    #     self.m_rank_values = []
        
class Deck:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.m_cards = []
        
        for suit in Suit:
            for value in CardValue:
                self.m_cards.append(Card(value, suit))
    
    def shuffle(self):
        random.shuffle(self.m_cards)
    
    def draw_card(self):
        if not self.m_cards:
            raise RuntimeError("Empty deck")
        return self.m_cards.pop()