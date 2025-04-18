import enum
import random
from collections import Counter


class Suit(enum.IntEnum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

    def __str__(self):
        symbols = {
            self.CLUBS: "♣",
            self.DIAMONDS: "♦",
            self.HEARTS: "❤",
            self.SPADES: "♠",
        }
        return symbols.get(self, f"Unknown({self.value})")


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
        return f"{self.rank} {self.suit}"
