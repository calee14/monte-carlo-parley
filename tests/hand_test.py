import unittest
from game_components.hand import Hand, HandRank
from game_components.card import Card, CardValue, Suit


class TestHand(unittest.TestCase):
    def setUp(self):
        # Setup cards for testing
        pass

    def hand_rank_determination(self, cards: list[Card]):
        my_hand = Hand(cards=cards)
        my_hand.determine_hand_rank()

        # Print for debugging
        print(
            "\n----------------------------------------------------------------------"
        )
        print("Cards:", my_hand)
        print("Top value:", my_hand.top_value)
        print("Kickers:", my_hand.kickers)
        print("Rank:", my_hand.m_rank)

        # Add assertions to verify the hand is ranked correctly
        # For example, with a pair of aces:
        self.assertEqual(my_hand.top_value, CardValue.ACE)
        self.assertEqual(my_hand.m_rank, HandRank.PAIR)

    def test_pair_hand_scenario(self):
        # For example, test a flush, straight, etc.
        cards = [
            Card(CardValue.ACE, Suit.CLUBS),
            Card(CardValue.EIGHT, Suit.SPADES),
            Card(CardValue.ACE, Suit.HEARTS),
            Card(CardValue.JACK, Suit.CLUBS),
            Card(CardValue.TWO, Suit.CLUBS),
            Card(CardValue.KING, Suit.DIAMONDS),
            Card(CardValue.SEVEN, Suit.SPADES),
        ]

        self.hand_rank_determination(cards)


# This allows the test to be run when the file is executed directly
if __name__ == "__main__":
    unittest.main()
