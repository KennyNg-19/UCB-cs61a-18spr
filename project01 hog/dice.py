"""Functions that simulate dice rolls.

A dice function takes no arguments and returns a number from 1 to n
(inclusive), where n is the number of sides on the dice.

Types of dice:

 -  Dice can be fair, meaning that they produce each possible outcome with equal
    probability. Examples: four_sided, six_sided

 -  For testing functions that use dice, deterministic test dice always cycle
    through a fixed sequence of values that are passed as arguments to the
    make_test_dice function.
"""

from random import randint

def make_fair_dice(sides):
    """Return a die that returns 1 to SIDES with equal chance."""
    assert type(sides) == int and sides >= 1, 'Illegal value for sides'
    def dice():
        return randint(1,sides) # int between [1, sides]
    return dice

# generate 2 kinds of dices, 本质是 function call：每次调用都会随机生成一个值在[1, sides]
# return 函数 dice: may have different return values each time they are called
four_sided = make_fair_dice(4) 
six_sided = make_fair_dice(6)

# *outcomes:  outcome u expected in for the dice
def make_test_dice(*outcomes): 
    """Return a die that cycles deterministically through OUTCOMES.

    >>> dice = make_test_dice(1, 2, 3)
    >>> dice()
    1
    >>> dice()
    2
    >>> dice()
    3
    >>> dice()
    1
    >>> dice()
    2

    This function uses Python syntax/techniques not yet covered in this course.
    The best way to understand it is by reading the documentation and examples.
    """
    assert len(outcomes) > 0, 'You must supply outcomes to make_test_dice'
    for o in outcomes:
        assert type(o) == int and o >= 1, 'Outcome is not a positive integer'

    index = len(outcomes) - 1 # max index: number of outcomes - 1
    def dice():
        nonlocal index # nonlocal: call the index above
        index = (index + 1) % len(outcomes) # 保证deterministic, index = 0, 1, .... max index, 0, 1 ....
        return outcomes[index] # outcomes[0], outcomes[1], outcomes[2]..., outcomes[0], outcomes[1], outcomes[2] ...
    
    return dice # 同理，must have different return values each time they are called