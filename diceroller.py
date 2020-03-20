from random import randint

def roll_xdy(numberToRoll, dieSides):
    """
    Returns a generator of dice roll results.

    Parameters:
        numberToRoll: Integer
            The number of dice to roll.
        dieSides: Integer
            The number of sides the dice being rolled have.
    """
    rolled = 0
    while rolled < numberToRoll:
        yield randint(1, dieSides)
        rolled += 1
