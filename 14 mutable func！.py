def make_withdraw(balance):
    """Return a withdraw function with a starting balance."""
    def withdraw(amount):
        nonlocal balance 
        if amount > balance:
            return 'Insufficient funds'
        """当你不需要下面这一行的rebind时，
             nested function可以直接访问parent的变量balance!!"""
        balance = balance - amount 
        return balance
    return withdraw
    

def make_withdraw_list(balance):
    b = [balance]
    def withdraw(amount):
        if amount > b[0]:
            return 'Insufficient funds'
        b[0] = b[0] - amount
        return b[0]
    return withdraw

def f(x):
    x = 4
    def g(y):
        def h(z):
            nonlocal x
            x = x + 1
            return x + y + z
        return h
    return g
a = f(1)
b = a(2)
b(3) + b(4)