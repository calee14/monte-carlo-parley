from collections import Counter
from card import Card, CardValue
import enum


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
        self.kickers = []

    def add_card(self, card: Card):
        self.m_cards.append(card)

    # looks at the hand to determind hand rank
    def determine_hand_rank(self):
        if not self.m_cards or len(self.m_cards) < 5:
            self.m_rank = HandRank.HIGH_CARD
            return
        # cards will be sorted from highest CardValue lowest CardValue
        sorted_cards = sorted(
            self.m_cards, key=lambda card: card.rank.value, reverse=True
        )

        # maps for ranks and suits
        rank_counter = Counter(card.rank.value for card in self.m_cards)
        suit_counter = Counter(card.suit for card in self.m_cards)

        # start checking what kind of hands we have
        # top bottom alg:
        # royal flush
        if self._is_royal_flush(sorted_cards, suit_counter):
            self.m_rank = HandRank.ROYAL_FLUSH
            self.top_value = CardValue.ACE.value
            return
        # straight flush
        straight_flush_value = self._is_straight_flush(sorted_cards, suit_counter)
        if straight_flush_value:
            self.m_rank = HandRank.STRAIGHT_FLUSH
            self.top_value = straight_flush_value
            return
        # four of a kind
        four_kind = [rank for rank, count in rank_counter.items() if count == 4]
        if four_kind:
            self.m_rank = HandRank.FOUR_OF_A_KIND
            self.top_value = four_kind[0]
            # Find highest kicker
            for card in sorted_cards:
                if card.rank.value != self.top_value:
                    self.kickers = [card.rank.value]
                    break
            return
        # full house
        three_kind = [rank for rank, count in rank_counter.items() if count == 3]
        pairs = [rank for rank, count in rank_counter.items() if count == 2]

        if three_kind and pairs:
            self.m_rank = HandRank.FULL_HOUSE
            self.top_value = max(three_kind)
            self.kickers = [max(pairs)]
            return
        elif len(three_kind) >= 2:
            # Could have two three of a kinds with 7 cards
            self.m_rank = HandRank.FULL_HOUSE
            three_kind.sort(reverse=True)
            self.top_value = three_kind[0]
            self.kickers = [three_kind[1]]
            return
        # flush
        flush_suit = None
        for suit, count in suit_counter.items():
            if count >= 5:
                flush_suit = suit
                break

        if flush_suit is not None:
            self.m_rank = HandRank.FLUSH
            flush_cards = [card for card in sorted_cards if card.suit == flush_suit]
            self.top_value = flush_cards[0].rank.value
            self.kickers = [card.rank.value for card in flush_cards[:5]]
            return
        # straight
        straight_value = self._is_straight(sorted_cards)
        if straight_value:
            self.m_rank = HandRank.STRAIGHT
            self.top_value = straight_value
            return
        # Check for three of a kind
        if three_kind:
            self.m_rank = HandRank.THREE_OF_A_KIND
            self.top_value = max(three_kind)
            # Find top two kickers
            kickers = []
            for card in sorted_cards:
                if card.rank.value != self.top_value and len(kickers) < 2:
                    kickers.append(card.rank.value)
            self.kickers = kickers
            return
        # Check for two pair
        if len(pairs) >= 2:
            self.m_rank = HandRank.TWO_PAIR
            pairs.sort(reverse=True)
            self.top_value = pairs[0]
            self.kickers = [pairs[1]]
            # Find the highest kicker
            for card in sorted_cards:
                if (
                    card.rank.value != self.top_value
                    and card.rank.value != self.kickers[0]
                ):
                    self.kickers.append(card.rank.value)
                    break
            return
        # Check for one pair
        if pairs:
            self.m_rank = HandRank.PAIR
            self.top_value = pairs[0]
            # Find top three kickers
            kickers = []
            for card in sorted_cards:
                if card.rank.value != self.top_value and len(kickers) < 3:
                    kickers.append(card.rank.value)
            self.kickers = kickers
            return
        # High card
        self.m_rank = HandRank.HIGH_CARD
        self.top_value = sorted_cards[0].rank.value
        self.kickers = [card.rank.value for card in sorted_cards[:5]]

    # function for checking royal flush
    def _is_royal_flush(self, sorted_cards, suit_counter):
        # check for 14 13 12 11 10 and same suit
        for suit, count in suit_counter.items():
            if count >= 5:
                # Check if we have A-K-Q-J-10 of this suit
                royal_values = {
                    CardValue.ACE.value,
                    CardValue.KING.value,
                    CardValue.QUEEN.value,
                    CardValue.JACK.value,
                    CardValue.TEN.value,
                }
                suit_cards = [card for card in sorted_cards if card.suit == suit]
                suit_values = {card.rank.value for card in suit_cards}
                if royal_values.issubset(suit_values):
                    return True
        return False

    # funct to check to if straight flush
    def _is_straight_flush(self, sorted_cards, suit_counter):
        # check 5 consecutive numbers of the same suit
        for suit, count in suit_counter.items():
            if count >= 5:
                suit_cards = sorted(
                    [card for card in sorted_cards if card.suit == suit],
                    key=lambda card: card.rank.value,
                    reverse=True,
                )
                # Check for straight with the cards of the same suit
                straight_high = self._is_straight(suit_cards)
                if straight_high:
                    return straight_high
        return 0

    # funct to check if there is a straight
    def _is_straight(self, sorted_cards):
        """
        Check for a straight (5 consecutive ranks)
        Returns the high card value of the straight if found, 0 otherwise
        """
        values = [card.rank.value for card in sorted_cards]
        # Remove duplicates and sort
        unique_values = sorted(set(values), reverse=True)

        # Check for A-5-4-3-2 straight
        if (
            CardValue.ACE.value in unique_values
            and CardValue.FIVE.value in unique_values
            and CardValue.FOUR.value in unique_values
            and CardValue.THREE.value in unique_values
            and CardValue.TWO.value in unique_values
        ):
            return 5  # 5-high straight

        # Check for standard straights
        for i in range(len(unique_values) - 4):
            if unique_values[i] == unique_values[i + 4] + 4:
                # high card of the straight used to compare to other straights
                return unique_values[i]

        return 0

