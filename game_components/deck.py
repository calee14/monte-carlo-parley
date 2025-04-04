import enum
import random
from collections import Counter
    
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