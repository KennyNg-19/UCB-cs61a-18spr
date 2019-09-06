# Trees

def tree(label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    # print("tree: ", [label] + list(branches))
    return [label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
	print(tree, "type(tree):", type(tree))
	if type(tree) != list or len(tree) < 1:
		return False
	for branch in branches(tree):
		if not is_tree(branch):
			return False
	return True

def is_leaf(tree):
    return not branches(tree)


### +++ === ABSTRACTION BARRIER === +++ ###

def fib_tree(n):
    """Construct a Fibonacci tree.

    >>> fib_tree(1)
    [1]
    >>> fib_tree(3)
    [2, [1], [1, [0], [1]]]
    >>> fib_tree(5)
    [5, [2, [1], [1, [0], [1]]], [3, [1, [0], [1]], [2, [1], [1, [0], [1]]]]]
    """
    if n == 0 or n == 1:
        return tree(n)
    else:
        left = fib_tree(n-2)
        right = fib_tree(n-1)
        fib_n = label(left) + label(right)
        return tree(fib_n, [left, right])

def count_leaves(t):
    """The number of leaves in tree.

    >>> count_leaves(fib_tree(5))
    8
    """
    if is_leaf(t):
        return 1
    else:
        return sum([count_leaves(b) for b in branches(t)])

def leaves(tree):
    """return a list containing the leaf label of tree"""
    if is_leaf(tree):
        print(label(tree))
        return [label(tree)] # 因为sum只能去掉一层[]
    else:
        return sum([leaves(b) for b in branches(tree)], []) # []很奇妙, 是做啥的？？


def increment_leaves(t):
    """Return a tree like t but with leaf values tripled.
    
    
    >>> print_tree(increment_leaves(fib_tree(4)))
    3
      1
        1
        2
      2
        2
        1
          1
          2
    """
    if is_leaf(t):
        return tree(label(t) + 1)
    else:
        bs = [increment_leaves(b) for b in branches(t)]
        return tree(label(t), bs)

def increment(t):
    """Return a tree like t but with all node values incremented.
    
    
    >>> print_tree(increment(fib_tree(4)))
    4
      2
        1
        2
      3
        2
        2
          1
          2
    """
    # 无需区分base case!!! 因为当b为leaf时，就剩下[]，所以压根没有call increment
    return tree(label(t) + 1, [increment(b) for b in branches(t)]) 

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the entry.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> print_tree(fib_tree(4))
    3
      1
        0
        1
      2
        1
        1
          0
          1
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
                    # indnent 自己递增，correspond to its depth
        print_tree(b, indent + 1)