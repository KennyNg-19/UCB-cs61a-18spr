"""Lab 2: Lambda Expressions and Higher Order Functions"""

# Lambda Functions

def lambda_curry2(func):
    """
    Returns a Curried version of a two-argument function FUNC.
    >>> from operator import add
    >>> curried_add = lambda_curry2(add)
    >>> add_three = curried_add(3)
    >>> add_three(5)
    8
    """
    "*** YOUR CODE HERE ***"

    # return lambda func: lambda x: lambda y: func(x, y)
    # 写错了：多写了个func，导致 x is bound to func, y to x
    # 实际params 比如curried_add只有俩(x)(y)
    return lambda x: lambda y: func(x, y)
