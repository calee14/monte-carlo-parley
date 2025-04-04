def game_loop():
    print("welcome to cappi and kk's gambling den!")
    print("enter ctrl+c or ctrl+d to quit.")

    num_players = input("enter number of players: ")

    # 0 - preflop, 1 - flop, 2 - turn, 3 - river
    state = int(input("what stage? (0 - preflop, 1 - flop, 2 - turn, 3 - river): "))

    while True:
        # run monte-carlo simulation

        probability = 0.10

        # show board
        if state > 0:
            print("here's the board:")

        # display cards
        print("here is your hand:")

        guess = input("guess your probability (in decimal):\n")

        # compare guess with probablility calculated
        if probability - float(guess) <= 0.05:
            print("yes! your guess is good!")
        else:
            print("aww! your guess a little off.")
    pass


if __name__ == "__main__":
    game_loop()
