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

    def simulate_round(self, stage=None) -> float:
        """
        Simulates multiple rounds of poker to estimate the win probability.
    
        Args:
            stage (int): current poker stage (number of cards on board)
                        - 0: preflop (no community cards) 
                        - 3: flop (three community cards) +3 cards
                        - 4: turn (four community cards) +2 cards
                        - 5: river (five community cards) +1 card
        Returns:
            float - probaility of player winning hand based on self.board and self.pocket_cards
        """
        if stage is None:
            stage = len(self.board)

        NUM_SIMULATIONS = 10000
        wins = 0
        for _ in range(NUM_SIMULATIONS):
            # reset players hand in this situation
            # new hand for player
            self.player_hand = Hand()  
            self.opps_hands = [Hand() for _ in range(self.num_opps)]

            self.deck.shuffle()
            # create a copy of thd deck 
            current_board = list(self.board)
            temp_deck = Deck()
            # ensure new game by clearing the board and pocket cards 
            temp_deck.remove_cards(current_board)
            temp_deck.remove_cards(self.pocket_cards)
            # deal cards to player_hand if self.pocket_cards is empty
            player_pocket = list(self.pocket_cards)
            if not player_pocket:
                player_pocket = [temp_deck.draw_card(), temp_deck.draw_card()]

            # add pocket cards to players hands
            for card in player_pocket:
                
                self.player_hand.add_card(card[0], card[1])
            # deal cards to opponents
            for i in range(self.num_opps):
                opp_cards = [temp_deck.draw_card(), temp_deck.draw_card()]
                for card in opp_cards:
                    self.opps_hands[i].add_card(card[0], card[1])
            # add the rest of the cards to the board depending on which level
            while len(current_board) < stage: 
                current_board.append(temp_deck.draw_card())
            # deal the rest of the cards to complete a full 5-card board for evaluation
            # (These are only used for evaluation, not shown to the player if not at river)
            hidden_board = list(current_board)
            while len(hidden_board) < 5:
                hidden_board.append(temp_deck.draw_card())
            # add the board cards to all hands (players and opps)
            # then compare all cards with player's hand
            for card in hidden_board:
                self.player_hand.add_card(card[0], card[1])
                for opp_hand in self.opps_hands:
                    opp_hand.add_card(card[0], card[1])
            # determine if player wins this simulation
            player_wins = True
            player_score = self.player_hand.evaluate_hand()
            for opp_hand in self.opps_hands:
                opp_score = opp_hand.evaluate_hand()
                # if any opponent has a better hand (lower score in poker), the player loses
                if opp_score < player_score:
                    player_wins = False
                    break
                # in case of a tie (same hand value), we need to check kickers
                elif opp_score == player_score:
                    player_kickers = self.player_hand.get_kickers()
                    opp_kickers = opp_hand.get_kickers()
                    # compare kickers
                    for p_kick, o_kick in zip(player_kickers, opp_kickers):
                        if p_kick < o_kick:
                            player_wins = False
                            break
                        elif p_kick > o_kick:
                            # player's kicker is higher, so player wins
                            break  
            
            if player_wins:
                wins += 1

        win_probability = wins / NUM_SIMULATIONS
            # repeat simulation until we get a good approximation
            # this is dummy return
            # return 0.8
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