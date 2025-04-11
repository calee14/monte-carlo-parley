from game_components.deck import Deck
from game_components.card import CardValue, Suit, Card
from game_components.hand import Hand


class Simulator(object):
    def __init__(
        self,
        num_opps: int,
        board: list[tuple[CardValue, Suit]],
        pocket_cards: list[tuple[CardValue, Suit]],
    ) -> None:
        """
        initializes the simulator with a Deck object and number of opponents.

        Args:
            deck (Deck): The deck object to use in the simulation.
            num_opps (int): Number of opponents at the table.
        """
        self.deck = Deck()

        # number of other players at the table
        self.num_opps = num_opps

        # store board and update deck
        self.board = board
        self.deck.remove_cards(self.board)

        # if player has predetermined pocket cards remove them from deck
        self.deck.remove_cards(pocket_cards)

        # for each Hand() obj the the first two indices (0 and 1) are reserved
        # for the players two cards in hand and indices 2 - 6 are for the board
        self.player_hand = Hand()
        self.opps_hands = [Hand() for _ in range(num_opps)]

    def simulate_round(
        self,
    ) -> tuple[list[tuple[CardValue, Suit]], list[tuple[CardValue, Suit]], float]:
        """
        Returns tuple[
            0. the cards on board (predetermined or chosen at random)
            1. the players pocket cards (predetermined or chosen at random)
            2. probability (float) of player winning board
            ]
        """
        # simulate shuffling deck to reset deck
        self.deck.shuffle()

        # deal cards to player_hand if self.pocket_cards is empty

        # deal cards to opponents

        # update the player and opp m_cards by using
        # the modify_card_at() function.

        # deal the cards on the board
        # until there are 5 cards on the board

        # add the board cards to all hands (players and opps)
        # then compare all cards with player's hand
        # repeat simulation until we get a good approximation

        # this is dummy return
        return (
            [
                (CardValue.SIX, Suit.HEARTS),
                (CardValue.TWO, Suit.HEARTS),
                (CardValue.NINE, Suit.HEARTS),
                (CardValue.KING, Suit.CLUBS),
                (CardValue.TWO, Suit.SPADES),
            ],
            [(CardValue.EIGHT, Suit.HEARTS), (CardValue.SEVEN, Suit.HEARTS)],
            0.8,
        )
