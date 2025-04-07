import random
from collections import Counter
from card import CardValue, Suit, Card


class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        """
        adds card objects into variable: self.m_cards
        """
        self.m_cards: list[Card] = []
        self.pointer = 0

        for suit in Suit:
            for value in CardValue:
                self.m_cards.append(Card(value, suit))

    def shuffle(self):
        """
        shuffles the deck by shuffling pointers to references of cards
        in self.m_cards
        """
        random.shuffle(self.m_cards)
        self.pointer = 0

    def drawn_all_cards(self):
        if self.pointer >= len(self.m_cards):
            return True

        return False

    def draw_card(self):
        """
        draws card at top of deck which is tracked by self.pointer
        """
        if not self.m_cards:
            raise RuntimeError("Empty deck")
        elif self.pointer >= len(self.m_cards):
            raise RuntimeError("Tried to draw card when all cards have been drawn")

        rank, suit = self.m_cards[self.pointer].rank, self.m_cards[self.pointer].suit
        self.pointer += 1
        return rank, suit
