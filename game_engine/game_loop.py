import enum
from game_components.deck import Deck
from game_components.card import Card, CardValue, Suit


class PokerStage(enum.IntEnum):
    PREFLOP = 0
    FLOP = 3
    TURN = 4
    RIVER = 5


def game_loop():
    print("welcome to cappi and kk's gambling den!")
    print("enter ctrl+c or ctrl+d to quit.\n")

    num_players = int(input("enter number of players: "))
    print(f"there are {num_players} other players at the table\n")

    # choose stage
    stage = PokerStage[input("what stage? (preflop, flop, turn, river): ").upper()]
    print(f"the board is at the {stage.name}\n")

    while True:
        print(
            "enter cards (space seperated). ex: ace,spades queen,hearts jack,diamonds ten,clubs"
        )
        card_input = input("leave empty for random cards every round\ncards: ")
        board = [
            (CardValue[card.split(",")[0].upper()], Suit[card.split(",")[1].upper()])
            for card in card_input.split()
        ]
        if len(board) != stage:
            print("entered the wrong amount of cards, try again.\n")
            continue
        elif len(board) == 0:
            print("okay! we'll choose new random cards for you each round")
            break
        else:
            break
    # create deck
    deck = Deck()
    if len(board) > 0:
        deck.remove_cards(board)

    print("\n")
    while True:
        deck.shuffle()

        # show board
        print("here's the board:")
        for card in board:
            print(f"{card[0]} {card[1]}  ", end="")

        # draw your hand
        my_hand = [deck.draw_card(), deck.draw_card()]
        # display cards
        print("here is your hand:")
        for card in my_hand:
            print(f"{card[0]} {card[1]}  ", end="")
        print("\n")

        guess = input("guess your probability (in decimal):\n")

        probability = 0.1

        # compare guess with probablility calculated
        if probability - float(guess) <= 0.05:
            print("yes! your guess is good!")
        else:
            print("aww! your guess a little off.")
