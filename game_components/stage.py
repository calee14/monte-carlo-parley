import enum


class PokerStage(enum.IntEnum):
    # enum for number of cards in a poker stage
    PREFLOP = 0
    FLOP = 3
    TURN = 4
    RIVER = 5
