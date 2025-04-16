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
    stage = PokerStage[input("what stage? (preflop, flop, turn, river): ").upper()]
    print(f"the board is at the {stage.name}\n")

    # select predetermined pocket cards
    # empty list = randomly chosen every round
    pocket: list[Card] = []
    while True:
        print(
            "do you want to have a predetermined POCKET cards? if so here's example: eight,hearts seven,hearts"
        )
        card_input = input("leave field empty for random  cards every round\ncards: ")
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
    while True:
        print(
            "enter cards on the BOARD (space seperated). ex: ace,spades queen,hearts jack,diamonds ten,clubs"
        )
        card_input = input(
            "leave field empty for random board cards every round\ncards: "
        )
        board_temp = [
            (CardValue[card.split(",")[0].upper()], Suit[card.split(",")[1].upper()])
            for card in card_input.split()
        ]
        if len(board_temp) == 0:
            print("okay! we'll choose new random cards for you each round")
            break
        if len(board_temp) != stage:
            print("entered the wrong amount of cards, try again.\n")
            continue
        else:
            board = board_temp
            break

    # make simulator to create deck and setup board
    simulator = Simulator(num_opps, board, pocket)

    print("")
    while True:
        # reset odds by shuffling
        simulator.deck.shuffle()

        # show board
        if len(board) == 0:
            # choose # cards based on poker stage
            simulator.board = []
            for _ in range(stage.value):
                simulator.board.append(simulator.deck.draw_card())

        print("here's the board:")
        print("|", end=" ")
        for i in range(5):
            if i < len(simulator.board):
                card = simulator.board[i]
                print(f"{card[0]} {card[1]}", end=" | ")
            else:
                print("??", end=" | ")

        print("")

        # display cards
        if len(pocket) == 0:
            # choose # cards based on poker stage
            simulator.pocket_cards = []
            for _ in range(2):
                simulator.pocket_cards.append(simulator.deck.draw_card())

        print("here is your hand:")
        print("|", end=" ")
        for card in simulator.pocket_cards:
            print(f"{card[0]} {card[1]}", end=" | ")
        print("\n")

        # run simulation to get simulated board, player hand, and win probability
        prob_win = simulator.simulate_round()
        guess = input("guess your probability (in decimal):\n")

        # compare guess with probablility calculated
        if prob_win - float(guess) <= 0.13:
            print("yes! your guess is good!")
        else:
            print("aww! your guess a little off.")

        print("\nnew board!!\n")
