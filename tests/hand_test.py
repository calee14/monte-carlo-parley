import unittest
from game_components.hand import Hand, HandRank
from game_components.card import Card, CardValue, Suit


class TestHand(unittest.TestCase):
    def setUp(self):
        # Setup cards for testing
        self.hand = Hand(
            [
                Card(CardValue.ACE, Suit.CLUBS),
                Card(CardValue.EIGHT, Suit.SPADES),
                Card(CardValue.ACE, Suit.HEARTS),
                Card(CardValue.JACK, Suit.CLUBS),
                Card(CardValue.TWO, Suit.CLUBS),
                Card(CardValue.KING, Suit.DIAMONDS),
                Card(CardValue.SEVEN, Suit.SPADES),
            ]
        )

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

        return my_hand

    def test_pair_hand_scenario(self):
        # For example, test a flush, straight, etc.
        self.hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.hand.modify_card_at(1, CardValue.EIGHT, Suit.SPADES)
        self.hand.modify_card_at(2, CardValue.ACE, Suit.HEARTS)
        self.hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.hand.modify_card_at(4, CardValue.TWO, Suit.CLUBS)
        self.hand.modify_card_at(5, CardValue.KING, Suit.DIAMONDS)
        self.hand.modify_card_at(6, CardValue.SEVEN, Suit.SPADES)

        hand = self.hand_rank_determination(self.hand.m_cards)

        # Add assertions to verify the hand is ranked correctly
        self.assertEqual(hand.top_value, CardValue.ACE)
        self.assertEqual(hand.m_rank, HandRank.PAIR)

    def test_full_house_hand_scenario(self):
        # For example, test a flush, straight, etc.
        self.hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.hand.modify_card_at(1, CardValue.ACE, Suit.SPADES)
        self.hand.modify_card_at(2, CardValue.EIGHT, Suit.HEARTS)
        self.hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.hand.modify_card_at(4, CardValue.TWO, Suit.CLUBS)
        self.hand.modify_card_at(5, CardValue.ACE, Suit.DIAMONDS)
        self.hand.modify_card_at(6, CardValue.JACK, Suit.SPADES)

        hand = self.hand_rank_determination(self.hand.m_cards)
        # Add assertions to verify the hand is ranked correctly
        self.assertEqual(hand.top_value, CardValue.ACE)
        self.assertEqual(hand.m_rank, HandRank.FULL_HOUSE)


# This allows the test to be run when the file is executed directly
if __name__ == "__main__":
    unittest.main()
