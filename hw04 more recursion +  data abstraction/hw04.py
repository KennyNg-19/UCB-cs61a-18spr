HW_SOURCE_FILE = 'hw04.py'

###############
#  Questions  #
###############

def intersection(st, ave):
    """Represent an intersection using the Cantor pairing function."""
    return (st+ave)*(st+ave+1)//2 + ave

def street(inter):
    return w(inter) - avenue(inter)

def avenue(inter):
    return inter - (w(inter) ** 2 + w(inter)) // 2

w = lambda z: int(((8*z+1)**0.5-1)/2)

def taxicab(a, b):
    """Return the taxicab distance between two intersections.

    >>> times_square = intersection(46, 7)
    >>> ess_a_bagel = intersection(51, 3)
    >>> taxicab(times_square, ess_a_bagel)
    9
    >>> taxicab(ess_a_bagel, times_square)
    9
    """
    "*** YOUR CODE HERE ***"
    return abs(street(a) - street(b)) + abs(avenue(a) - avenue(b))

def squares(s):
    """Returns a new list containing square roots of the elements of the
    original list that are perfect squares.

    >>> seq = [8, 49, 8, 9, 2, 1, 100, 102]
    >>> squares(seq)
    [7, 3, 1, 10]
    >>> seq = [500, 30]
    >>> squares(seq)
    []
    """
    "*** YOUR CODE HERE ***"
    from math import sqrt
    # one way to check perfect square: int(root + 0.5) ** 2 == number
    # return [int(sqrt(x)) for x in s if int(sqrt(x) + 0.5) ** 2 == x]

    # Official: round是四舍五入函数, 可以改用int()
    return [round(n ** 0.5) for n in s if round(n ** 0.5) ** 2 == n]

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n == 1 or n == 2 or n == 3:
        return n
    return g(n - 1) + 2 * g(n - 2) + 3 * g(n - 3)


def g_iter(n):
    """Return the value of G(n), computed iteratively. 其实就是和recursion反过来，从n==1开始

    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g_iter', ['Recursion'])
    True
    """
    "*** YOUR CODE HERE ***"
    # build a list to store computed value
    l = [1, 2, 3]

    if n == 1 or n == 2 or n == 3:
        return l[n-1]
    
    # n >= 4    
    count = 4
    while count <= n:
        l.append(l[count-2] + 2 * l[count-3] + 3 * l[count-4])
        count += 1
        
    return l[n-1]

    '''
    更简版： 一行多个 赋值法
    i== 3
    num_1, num_2, num_3 = 1, 2, 3
    if n <= 3:
        return n
    else:
        while i < n:
            num_1, num_2, num_3 = num_2, num_3, num_3 + 2 * num_2 + 3 * num_1
            i += 1
    return num_3
    '''

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    "*** YOUR CODE HERE ***"
    # 不太会...
    # official: mutual call
    def pingpong_next(k, p, up):
        if k == n:
            return p
        if up:
            return pingpong_switch(k + 1, p + 1, up)
        else:
            return pingpong_switch(k + 1, p - 1, up)

    def pingpong_switch(k, p, up):
        if k % 7 == 0 or has_seven(k):
            return pingpong_next(k, p, not up)
        else:
            return pingpong_next(k, p, up)

    return pingpong_next(1, 1, True)

def has_seven(k):
    """Returns True if at least one of the digits of k is a 7, False otherwise.

    >>> has_seven(3)
    False
    >>> has_seven(7)
    True
    >>> has_seven(2734)
    True
    >>> has_seven(2634)
    False
    >>> has_seven(734)
    True
    >>> has_seven(7777)
    True
    """
    if k % 10 == 7:
        return True
    elif k < 10:
        return False
    else:
        return has_seven(k // 10)


from ucb import trace

def count_change(amount):
    """Return the number of ways to make change for amount.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    """
    "*** YOUR CODE HERE ***"
    
    def get_coins(upper):
        '''denomination of every coin will be a power of two: 1-cent, 2-cent, 4-cent, 8-cent, etc. 
        There will be no limit to how much a coin can be worth'''
        from math import sqrt
        # int(sqrt(amount)) 下取整数: 无论amount是否是2的次幂 +1正好提升了上边界；
        return [ 2**x for x in range(0, int(sqrt(upper)) + 1)]

    # @trace
    # def count_partitions(n, coins):
    #     """Count the ways to partition n using parts up to m."""
    #     if n < 0: # n - coins[-1] < 0 is possible
    #         return 0
    #     elif n == 0: # use equal denomination coin
    #         return 1
    #     elif not coins: # empty list
    #         return 0
    #     else:
    #         with_coin = count_partitions(n - coins[-1], coins)      
    #     '''
    #         注意！！！这中间不能使用coins.pop()，因为pop是instance method直接修改了coins，最后变成empty list 而后期有大量引用指向它 会报错
    #         而coins[:len(coins)-1] 是修改后，返回一个copy---empty list会被每个recursion自己创建
    #     ''' 
    #         without_coin = count_partitions(n, coins[:len(coins)-1])
            
    #         return  with_coin + without_coin        

    # return count_partitions(amount, get_coins(amount))

    
    # Official solution (which is apparently simpler)
    # min_coin增长，BOTTOM 2 TOP 的另类 recursion
    @trace
    def count_using(min_coin, amount):
        if amount < 0:
            return 0
        elif amount == 0:
            return 1
        elif min_coin > amount: # 面额不再继续*2了，recursion终止
            return 0
        else:
            with_min = count_using(min_coin, amount - min_coin)
            without_min = count_using(2*min_coin, amount) # 2*min_coin: 增大coin
            return with_min + without_min

    return count_using(1, amount)

    

###################
# Extra Questions #
###################

from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    return 'YOUR_EXPRESSION_HERE'
