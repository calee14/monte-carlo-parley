import enum
from game_components.deck import Deck
from game_components.card import Card, CardValue, Suit
from game_components.stage import PokerStage
from monte_carlo.simulator import Simulator


def game_loop():
    print("welcome to cappi and kk's gambling den!")
    print("enter ctrl+c or ctrl+d to quit.\n")

    num_opps = int(input("enter number of players (above 2): ")) - 1
    print(f"there are {num_opps} other players at the table\n")

    # choose stage
    # stage = PokerStage[input("what stage? (preflop, flop, turn, river): ").upper()]
    # print(f"the board is at the {stage.name}\n")

    # select predetermined pocket cards
    # empty list = randomly chosen every round
    pocket: list[Card] = []
    while True:
        print(
            "do you want to have a predetermined POCKET cards? if so here's example: eight,hearts seven,hearts"
        )
        card_input = input("leave field empty for random  cards every round\ncards: ")
        if not card_input.strip():
            print("okay! we'll choose new random cards for you each round")
            break
        pocket_temp = [
            (CardValue[card.split(",")[0].upper()], Suit[card.split(",")[1].upper()])
            for card in card_input.split()
        ]
        if len(pocket_temp) == 0:
            print("okay! we'll choose new random cards for you each round")
            break
        elif len(pocket_temp) != 2:
            print("entered the wrong amount of cards, try again.\n")
            continue
        else:
            pocket = pocket_temp
            break
    print("")

    # select predetermined board
    # empty list = randmly chosen every round
    board: list[Card] = []
    # simulator for board and deck setup
    simulator = Simulator(num_opps, board, pocket)
    # start at preflop 
    current_stage = 0
    stage_names = ["PREFLOP", "FLOP", "TURN", "RIVER"]
    # stage_card_counts = [0, 3, 4, 5]
    cards_per_stage = [0, 3, 1, 1]

    # main game loop
    while True:
        # preflop non no cards drawn it is just the pocket cards
        # reset for a new hand/rouch if needed 
        if current_stage == 0 and (len(simulator.board) > 0 or len(simulator.pocket_cards) == 0): 
            simulator.deck.shuffle()
            simulator.board = []
            # deal pocket cards to user
            if len(pocket) == 0:
                simulator.pocket_cards = []
                for _ in range(2):
                    simulator.pocket_cards.append(simulator.deck.draw_card())
        # this is the stage chosen by the user (preflop flop river turn)
        stage_name = stage_names[current_stage]
        # here is the current stage
        print(f"\ncurrent stage: {stage_name}\n")
        print("here's the board:")
        print("|", end=" ")
        # visible_cards = stage_card_counts[current_stage]
        # cards_visible = sum(cards_per_stage[:current_stage+1])
        cards_visible = 0
        # flop
        if current_stage == 1:  
            cards_visible = 3
        # turn
        elif current_stage == 2:  
            cards_visible = 4
        # river
        elif current_stage == 3: 
            cards_visible = 5
        for i in range(5):
            # if i < len(simulator.board) and i < visible_cards:
            if i < len(simulator.board) and i < cards_visible:
                card = simulator.board[i]
                print(f"{card[0]} {card[1]}", end=" | ")
            else:
                print("??", end=" | ")
        print("")

        # output player's hand
        print("here is your hand:")
        print("|", end=" ")
        for card in simulator.pocket_cards:
            print(f"{card[0]} {card[1]}", end=" | ")
        print("\n")

        # run simulation to get win probability for the current stage
        # use the number of board cards for the current stage
        # make sure we don't pass more cards than exist in the board
        num_board_cards = 0
        if current_stage == 0: 
            num_board_cards = 0
        elif current_stage == 1:  
            num_board_cards = min(3, len(simulator.board))
        elif current_stage == 2: 
            num_board_cards = min(4, len(simulator.board))
        else:
            num_board_cards = min(5, len(simulator.board))
        # num_board_cards = min(len(simulator.board), stage_card_counts[current_stage])
        # visible_cards = len(simulator.board)
        prob_win = simulator.simulate_round(num_board_cards)
        guess = input("guess your probability (in decimal):\n")

        try:
            if abs(prob_win - float(guess)) <= 0.13:
                print("yes! your guess is good!")
            else:
                print("aww! your guess a little off.")
            print(f"actual probability: {prob_win:.4f}")
        except ValueError:
            print(f"invalid input. The actual probability was {prob_win:.4f}")
        # ask what the player wants to do next
        # not yet at the river 
        if current_stage < 3: 
            while True:
                print("\nWhat would you like to do next?")
                print("1. Continue to the next stage with random cards")
                print("2. Continue to the next stage with custom cards")
                print("3. Start a new hand")
                choice = input("Enter your choice (1/2/3): ")
                
                if choice == "1":
                    # move to next stage with random cards
                    # current_stage += 1
                    new_stage = current_stage + 1
                    # cards_to_add = stage_card_counts[current_stage] - len(simulator.board)
                    cards_to_add = cards_per_stage[new_stage]
                    print(f"\nAdding {cards_to_add} random card(s) to the board.")
                    
                    # add random cards to the board
                    for _ in range(cards_to_add):
                        new_card = simulator.deck.draw_card()
                        simulator.board.append(new_card)
                    
                    current_stage = new_stage
                    print(f"\nMoved to {stage_names[current_stage]} stage.")
                    break
                    break
                    
                elif choice == "2":
                    # move to next stage with custom cards
                    new_stage = current_stage + 1
                    # cards_to_add = stage_card_counts[current_stage] - len(simulator.board)
                    cards_to_add = cards_per_stage[current_stage]
                    
                    # get custom cards
                    while True:
                        print(f"Enter {cards_to_add} card(s) (space separated). Example: ace,spades queen,hearts")
                        card_input = input("cards: ")

                        if not card_input.strip() and cards_to_add > 0:
                            print(f"Please enter {cards_to_add} card(s). Try again.\n")
                            continue
                        
                        try:
                            if not card_input.strip():
                                board_cards = []
                            else: 
                                board_cards = [
                                    (CardValue[card.split(",")[0].upper()], Suit[card.split(",")[1].upper()])
                                    for card in card_input.split()
                                ]
                            
                            if len(board_cards) != cards_to_add:
                                print(f"please enter exactly {cards_to_add} card(s). Try again.\n")
                                continue
                            
                            # check if cards are already in use
                            all_used_cards = simulator.pocket_cards + simulator.board
                            duplicate_found = False
                            
                            for card in board_cards:
                                if card in all_used_cards:
                                    print(f"Card {card[0]} of {card[1]} is already in use. Try again.\n")
                                    duplicate_found = True
                                    break
                                    
                            if duplicate_found:
                                continue
                                
                            # add custom cards to the board
                            simulator.board.extend(board_cards)
                            # Remove these cards from the deck
                            simulator.deck.remove_cards(board_cards)
                            current_stage = new_stage
                            break
                        except (KeyError, IndexError, ValueError):
                            print("Invalid card format. Try again.\n")
                    break
                    
                elif choice == "3":
                    # start a new hand
                    current_stage = 0
                    print("\ndealing a new hand!\n")

                    change_players = input("Do you want to change the number of players? (y/n): ")
                    if change_players.lower() == 'y':
                        num_opps = int(input("enter number of players (above 2): ")) - 1
                        print(f"there are {num_opps} other players at the table\n")
                        # Update the simulator with new number of opponents
                        simulator = Simulator(num_opps, [], pocket)
                    break   
                else:
                    print("invalid choice. Please enter 1, 2, or 3.")
        else:
            # at the river, only option is to start a new hand
            print("\nhand complete! dealing a new hand...\n")
            change_players = input("Do you want to change the number of players? (y/n): ")
            if change_players.lower() == 'y':
                num_opps = int(input("enter number of players (above 2): ")) - 1
                print(f"there are {num_opps} other players at the table\n")
                # Update the simulator with new number of opponents
                simulator = Simulator(num_opps, [], pocket)
    
            current_stage = 0