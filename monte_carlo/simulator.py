from game_components.deck import Deck
from game_components.card import CardValue, Suit, Card
from game_components.hand import Hand


class Simulator(object):
    def __init__(self, num_opps: int, board: list[tuple[CardValue, Suit]]) -> None:
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

        # for each Hand() obj the the first two indices (0 and 1) are reserved
        # for the players two cards in hand and indices 2 - 6 are for the board
        self.players_hand = Hand()
        self.opps_hands = [Hand() for _ in range(num_opps)]

    def simulate_round(self):
        # deal cards to player and opponents
        # update the player and opp m_cards by using
        # the modify_card_at() function.

        # deal the cards on the board
        # until there are 5 cards on the board

        #
        pass
