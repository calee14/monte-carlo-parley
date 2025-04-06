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

    def hand_rank_determination(self):
        self.hand.determine_hand_rank()

        # Print for debugging
        print(
            "\n----------------------------------------------------------------------"
        )
        print("Cards:", self.hand)
        print("Top value:", self.hand.top_value)
        print("Kickers:", self.hand.kickers)
        print("Rank:", self.hand.m_rank)

    def test_pair_hand_scenario(self):
        # For example, test a flush, straight, etc.
        self.hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.hand.modify_card_at(1, CardValue.EIGHT, Suit.SPADES)
        self.hand.modify_card_at(2, CardValue.ACE, Suit.HEARTS)
        self.hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.hand.modify_card_at(4, CardValue.TWO, Suit.CLUBS)
        self.hand.modify_card_at(5, CardValue.KING, Suit.DIAMONDS)
        self.hand.modify_card_at(6, CardValue.SEVEN, Suit.SPADES)

        self.hand_rank_determination()

        # Add assertions to verify the hand is ranked correctly
        self.assertEqual(self.hand.top_value, CardValue.ACE)
        self.assertEqual(self.hand.m_rank, HandRank.PAIR)

    def test_full_house_hand_scenario(self):
        # For example, test a flush, straight, etc.
        self.hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.hand.modify_card_at(1, CardValue.ACE, Suit.SPADES)
        self.hand.modify_card_at(2, CardValue.EIGHT, Suit.HEARTS)
        self.hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.hand.modify_card_at(4, CardValue.TWO, Suit.CLUBS)
        self.hand.modify_card_at(5, CardValue.ACE, Suit.DIAMONDS)
        self.hand.modify_card_at(6, CardValue.JACK, Suit.SPADES)

        self.hand_rank_determination()
        # Add assertions to verify the hand is ranked correctly
        self.assertEqual(self.hand.top_value, CardValue.ACE)
        self.assertEqual(self.hand.m_rank, HandRank.FULL_HOUSE)


class TestHandCompare(unittest.TestCase):
    def setUp(self):
        self.my_hand = Hand(
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
        self.opp_hand = Hand(
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

    def test_compare_full_house_pair(self):
        self.my_hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.my_hand.modify_card_at(1, CardValue.ACE, Suit.SPADES)
        self.my_hand.modify_card_at(2, CardValue.EIGHT, Suit.HEARTS)
        self.my_hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.my_hand.modify_card_at(4, CardValue.TWO, Suit.CLUBS)
        self.my_hand.modify_card_at(5, CardValue.ACE, Suit.DIAMONDS)
        self.my_hand.modify_card_at(6, CardValue.JACK, Suit.SPADES)

        self.my_hand.determine_hand_rank()

        self.opp_hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.opp_hand.modify_card_at(1, CardValue.EIGHT, Suit.SPADES)
        self.opp_hand.modify_card_at(2, CardValue.ACE, Suit.HEARTS)
        self.opp_hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.opp_hand.modify_card_at(4, CardValue.TWO, Suit.CLUBS)
        self.opp_hand.modify_card_at(5, CardValue.KING, Suit.DIAMONDS)
        self.opp_hand.modify_card_at(6, CardValue.SEVEN, Suit.SPADES)

        self.opp_hand.determine_hand_rank()

        self.assertEqual(self.my_hand.compare_hands(self.opp_hand), True)

    def test_compare_two_pairs(self):
        self.my_hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.my_hand.modify_card_at(1, CardValue.ACE, Suit.SPADES)
        self.my_hand.modify_card_at(2, CardValue.JACK, Suit.HEARTS)
        self.my_hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.my_hand.modify_card_at(4, CardValue.KING, Suit.CLUBS)
        self.my_hand.modify_card_at(5, CardValue.TWO, Suit.DIAMONDS)
        self.my_hand.modify_card_at(6, CardValue.KING, Suit.SPADES)

        self.my_hand.determine_hand_rank()

        self.opp_hand.modify_card_at(0, CardValue.ACE, Suit.CLUBS)
        self.opp_hand.modify_card_at(1, CardValue.ACE, Suit.SPADES)
        self.opp_hand.modify_card_at(2, CardValue.JACK, Suit.HEARTS)
        self.opp_hand.modify_card_at(3, CardValue.JACK, Suit.CLUBS)
        self.opp_hand.modify_card_at(4, CardValue.KING, Suit.CLUBS)
        self.opp_hand.modify_card_at(5, CardValue.SEVEN, Suit.DIAMONDS)
        self.opp_hand.modify_card_at(6, CardValue.SEVEN, Suit.SPADES)

        self.opp_hand.determine_hand_rank()

        self.assertEqual(self.my_hand.compare_hands(self.opp_hand), True)

    def test_compare_high_cards(self):
        self.my_hand.modify_card_at(0, CardValue.TWO, Suit.CLUBS)
        self.my_hand.modify_card_at(1, CardValue.FIVE, Suit.SPADES)
        self.my_hand.modify_card_at(2, CardValue.FOUR, Suit.HEARTS)
        self.my_hand.modify_card_at(3, CardValue.SEVEN, Suit.CLUBS)
        self.my_hand.modify_card_at(4, CardValue.QUEEN, Suit.CLUBS)
        self.my_hand.modify_card_at(5, CardValue.ACE, Suit.DIAMONDS)
        self.my_hand.modify_card_at(6, CardValue.KING, Suit.SPADES)

        self.my_hand.determine_hand_rank()

        self.opp_hand.modify_card_at(0, CardValue.TWO, Suit.CLUBS)
        self.opp_hand.modify_card_at(1, CardValue.FIVE, Suit.SPADES)
        self.opp_hand.modify_card_at(2, CardValue.FOUR, Suit.HEARTS)
        self.opp_hand.modify_card_at(3, CardValue.SEVEN, Suit.CLUBS)
        self.opp_hand.modify_card_at(4, CardValue.QUEEN, Suit.CLUBS)
        self.opp_hand.modify_card_at(5, CardValue.ACE, Suit.DIAMONDS)
        self.opp_hand.modify_card_at(6, CardValue.JACK, Suit.SPADES)

        self.opp_hand.determine_hand_rank()

        self.assertEqual(self.my_hand.compare_hands(self.opp_hand), True)


# This allows the test to be run when the file is executed directly
if __name__ == "__main__":
    unittest.main()
