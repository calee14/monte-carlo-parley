import enum
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
        self.player_hand = Hand([Card(CardValue.TWO, Suit.DIAMONDS) for _ in range(7)])
        self.opps_hands = [
            Hand([Card(CardValue.TWO, Suit.DIAMONDS) for _ in range(7)])
            for _ in range(num_opps)
        ]

    def simulate_round(self, stage=None) -> float:
        """
        Simulates multiple rounds of poker to estimate the win probability.

        Args:
            stage (int): current poker stage (number of cards on board)
                        - 0: preflop (no community cards)
                        - 3: flop (three community cards) +3 cards
                        - 4: turn (four community cards) +1 card
                        - 5: river (five community cards) +1 card
        Returns:
            float - probaility of player winning hand based on self.board and self.pocket_cards
        """
        if stage is None:
            stage = len(self.board)

        NUM_SIMULATIONS = 100000
        wins = 0
        for _ in range(NUM_SIMULATIONS):
            self.deck.shuffle()
            # create a copy of thd deck
            current_board = self.board

            # deal cards to player_hand if self.pocket_cards is empty
            player_pocket = self.pocket_cards
            if len(self.pocket_cards) == 0:
                player_pocket = [self.deck.draw_card(), self.deck.draw_card()]

            # add pocket cards to players hands
            for i, card in enumerate(player_pocket):
                self.player_hand.modify_card_at(i, card[0], card[1])

            # deal cards to opponents
            for i in range(self.num_opps):
                opp_cards = [self.deck.draw_card(), self.deck.draw_card()]
                for j, card in enumerate(opp_cards):
                    self.opps_hands[i].modify_card_at(j, card[0], card[1])

            # add the rest of the cards to the board no matter which stage
            while len(current_board) < 5:
                current_board.append(self.deck.draw_card())

            # add the board cards to all hands (players and opps)
            # then compare all cards with player's hand
            for board_idx, card in enumerate(current_board):
                board_start_idx = 2
                self.player_hand.modify_card_at(
                    board_start_idx + board_idx, card[0], card[1]
                )
                for opp_hand_idx in range(len(self.opps_hands)):
                    self.opps_hands[opp_hand_idx].modify_card_at(
                        board_start_idx + board_idx, card[0], card[1]
                    )
            # determine if player wins this simulation
            player_wins = True
            self.player_hand.determine_hand_rank()
            for opp_hand in self.opps_hands:
                opp_hand.determine_hand_rank()
                # if any opponent has a better hand (lower score in poker), the player loses
                if not self.player_hand.compare_hands(opp_hand):
                    player_wins = False
                    break

            if player_wins:
                wins += 1

        win_probability = wins / NUM_SIMULATIONS
        # repeat simulation until we get a good approximation
        return win_probability

    def get_next_card(self) -> tuple[CardValue, Suit]:
        """
        Draws the next card for board progression.

        Returns:
            tuple[CardValue, Suit]: The next card drawn from the deck
        """
        return self.deck.draw_card()

    def progress_to_next_stage(self) -> None:
        """
        Adds one more card to the board, progressing to the next stage.
        """
        # draw a new card and add it to the board
        new_card = self.get_next_card()
        self.board.append(new_card)

        # remove this card from the deck to ensure it's not reused
        self.deck.remove_cards([new_card])

