import unittest
from game_components.card import CardValue, Suit
from game_components.deck import Deck


class TestDeck(unittest.TestCase):
    def setUp(self):
        pass

    def test_deck_init(self):
        deck = Deck()
        self.assertEqual(len(deck.m_cards), 52)

    def test_draw_card(self):
        deck = Deck()
        for _ in range(52):
            deck.draw_card()

        self.assertEqual(deck.drawn_all_cards(), True)

    def test_shuffle(self):
        deck = Deck()
        first_shuffle = []
        second_shuffle = []
        for _ in range(52):
            rank, suit = deck.draw_card()
            first_shuffle.append((rank, suit))

        deck.shuffle()
        for _ in range(52):
            rank, suit = deck.draw_card()
            second_shuffle.append((rank, suit))

        self.assertEqual(first_shuffle == second_shuffle, False)

    def test_remove_cards(self):
        deck = Deck()
        cards = [
            (CardValue.ACE, Suit.CLUBS),
            (CardValue.EIGHT, Suit.SPADES),
            (CardValue.KING, Suit.HEARTS),
        ]

        deck.remove_cards(cards)

        for card in deck.m_cards:
            self.assertEqual((card.rank, card.suit) not in cards, True)

        self.assertEqual(len(deck.m_cards) == 52 - len(cards), True)


if __name__ == "__main__":
    unittest.main()
