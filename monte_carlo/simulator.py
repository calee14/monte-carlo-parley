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

        self.pocket_cards = pocket_cards
        # if player has predetermined pocket cards remove them from deck
        self.deck.remove_cards(pocket_cards)

        # for each Hand() obj the the first two indices (0 and 1) are reserved
        # for the players two pocket cards in hand and indices 2 - 6 are for the board
        self.player_hand = Hand()
        self.opps_hands = [Hand() for _ in range(num_opps)]

    def simulate_round(self) -> float:
        """
        Returns:
            float - probaility of player winning hand based on self.board and self.pocket_cards
        """
        # deal cards to player_hand if self.pocket_cards is empty

        # deal cards to opponents

        # update the player_hand and opps_hands m_cards by using
        # the modify_card_at() function.

        # deal the rest of the cards on the board
        # until there are 5 cards on the board

        # add the board cards to all hands (players and opps)
        # then compare all cards with player's hand

        # repeat simulation until we get a good approximation

        # this is dummy return
        return 0.8
