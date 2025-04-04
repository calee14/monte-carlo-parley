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
    def __init__(self, cards: list[Card] = None):
        self.m_cards = cards if cards is not None else []
        self.m_rank = HandRank.HIGH_CARD
        self.top_value = 0
        self.secondary_value = 0
        self.kickers = []
    
    def add_card(self, card: Card):
        self.m_cards.append(card)