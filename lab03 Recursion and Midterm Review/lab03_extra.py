""" Optional problems for Lab 3 """

from lab03 import *

## Higher order functions

def cycle(f1, f2, f3):
    """Returns a function that is itself a higher-order function.

    >>> def add1(x):
    ...     return x + 1
    >>> def times2(x):
    ...         return x * 2
    >>> def add3(x):
    ...     return x + 3
    >>> my_cycle = cycle(add1, times2, add3)
    >>> identity = my_cycle(0)
    >>> identity(5)
    5
    >>> add_one_then_double = my_cycle(2)
    >>> add_one_then_double(1)
    4
    >>> do_all_functions = my_cycle(3)
    >>> do_all_functions(2)
    9
    >>> do_more_than_a_cycle = my_cycle(4)
    >>> do_more_than_a_cycle(2)
    10
    >>> do_two_cycles = my_cycle(6)
    >>> do_two_cycles(1)
    19
    """
    "*** YOUR CODE HERE ***"
    def my_cycle(n):
        '''
        技巧：return a f, composing other inner f
        '''
        def f(x): # 3rd params, x。犯错：my_cycle(n-1) 没有加(x), 导致报错return f2(my_cycle(n-1))
                # TypeError: unsupported operand type(s) for *: 'function' and 'int'
            if n == 0:
                return x
            elif n % 3 == 1:
                return f1(my_cycle(n-1)(x))
            elif n % 3 == 2:
                return f2(my_cycle(n-1)(x))
            else: # n % 3 == 0 and n != 0
                return f3(my_cycle(n-1)(x))

        return f

    return my_cycle

## Lambda expressions

def is_palindrome(n):
    """
    Fill in the blanks '_____' to check if a number
    is a palindrome.

    >>> is_palindrome(12321)
    True
    >>> is_palindrome(42)
    False
    >>> is_palindrome(2015)
    False
    >>> is_palindrome(55)
    True
    """
    x, y = n, 0
    # 不太会....
    # 以下的lambda，可以直接访问local var?
    f = lambda: y * 10 + (x % 10) # 很巧妙迭代构造(12321)：0+1， 1*10+2, 12*10+3, 123*10+2
    while x > 0:
        x, y = x // 10, f()
        
    return y == n

## More recursion practice

def skip_mul(n):
    """Return the product of n * (n - 2) * (n - 4) * ...

    >>> skip_mul(5) # 5 * 3 * 1
    15
    >>> skip_mul(8) # 8 * 6 * 4 * 2
    384
    """
    if n - 2 <= 0:
        return n
    else:
        return n * skip_mul(n - 2)

from ucb import trace


def is_prime(n):
    """Returns True if n is a prime number and False otherwise.

    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    """
    "*** YOUR CODE HERE ***"
    # 完全不会...用递归
    # 解析：思路和while 从 2 -> n - 1 一样，但可以优化 到sqrt(n)
    import math
    def helper(i):
        if n == i: # base case, n == 2
            return True
        elif n % i == 0: # n diviees i, not prime            
            return False
        elif i >= math.sqrt(n): # i >= sqrt(n), but still no divisor, it is prime
            # trace
            # print('i >= sqrt(n), stop')
            return True
        else: # not divise, then i + 1
            # trace 
            # print('divisor ', i, ' fails')
            return helper(i + 1)

    return helper(2)

# 简单 pass
def interleaved_sum(n, odd_term, even_term):
    """Compute the sum odd_term(1) + even_term(2) + odd_term(3) + ..., up
    to n.

    >>> # 1 + 2^2 + 3 + 4^2 + 5
    ... interleaved_sum(5, lambda x: x, lambda x: x*x)
    29
    """
    "*** YOUR CODE HERE ***"
    if n == 0:
        return 0
    elif n % 2 == 1:
        return odd_term(n) + interleaved_sum(n-1, odd_term, even_term)
    else:
        return even_term(n) + interleaved_sum(n-1, odd_term, even_term)

def ten_pairs(n):
    """Return the number of ten-pairs within positive integer n.

    >>> ten_pairs(7823952)
    3
    >>> ten_pairs(55055)
    6
    >>> ten_pairs(9641469)
    6
    """
    "*** YOUR CODE HERE ***"
    # 不会...用recursion好像很复杂？
    # 解析：此处helper function是O(n^2)复杂度的递归！！检测rightmost digit和rest left digits纸之和

    def check_last_digit(left_digits, digit):
        if left_digits == 0: # leftmost digit // 10 finally gets 0
            return 0
        else:
            if left_digits % 10 + digit==10:
                return 1 + check_last_digit(left_digits // 10, digit)
            else:
                return 0 + check_last_digit(left_digits // 10, digit)

    if n < 19: # 不考虑 <= 18的
        return 0
    else:
        # check_last_digit(n // 10, n % 10) 寻找个位n % 10, 和余下n//10的每一位
        # ten_pairs(n // 10)是recursion 左侧余下的
        return check_last_digit(n // 10, n % 10) + ten_pairs(n // 10)


