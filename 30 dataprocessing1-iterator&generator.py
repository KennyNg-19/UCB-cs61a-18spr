# 查找a有没有b的所有char(按照顺序)
def contains_not_sidebyside(a, b):
    ai = iter(a) # 遍历a
    for x in b: # 巧妙：b的元素得全部match——得完成for循环！ 才返回true
        try: 
            while next(ai) != x: # 巧妙：这个while很妙，b的x没有match, 就不执行for ——x就不动              
                pass                    
        except StopIteration:
            return False # run out of letters in a, for还没结束...
    return True

# generator
def evens(start, end):
    # 巧妙(math): 先找出>=start的even number
    even = start + start%2 # 最初使用一次，
    while even <= end:
        yield even
        even += 2

# ============= Generator & iterator: yield from ============

# 在混合recursive, 使用yield
def prefixes(s):
    """Yield all prefixes of s.

    >>> list(prefixes('both'))
    ['b', 'bo', 'bot', 'both']
    """
    if s:
        yield from prefixes(s[:-1])
        yield s

# substring: sum all prefixes of all prefixes of s(onwards 一个方向产生) 
def substrings(s):
    """Yield all substrings of s.

    >>> list(substrings('tops'))
    ['t', 'to', 'top', 'tops', 'o', 'op', 'ops', 'p', 'ps', 's']
    """
    if s:
        yield from prefixes(s) # 获得当前s的所有prefix
        yield from substrings(s[1:])


