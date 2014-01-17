import itertools


def only(lst, exception=Exception):
    """ Returns the only element in an array or raises an Exception
        inspired by ruby facets / only
    """
    l = len(lst)
    if l != 1:
        raise exception("Expected one element but found :%d " %(l))
    return lst[0]

def xgroupby(data, keyfunc):
    ''' Enhanced version of itertools.groupby that sorts and returns a dictionary '''
    data = sorted(data, key=keyfunc)
    return dict((grp, list(elemens)) for grp, elemens in itertools.groupby(data, keyfunc))


def first(iterable, func):
    ''' Return the first element in "iterable" for which "func" returns true'''
    for elm in iterable:
        if func(elm):
            return elm
    return None


def lindex(lst, func):
    ''' Return the first index in "iterable" for which "func" returns true'''
    for i in range(len(lst)):
        if func(lst[i]):
            return i
    return None

def rindex(lst, func):
    ''' Return the last index in "iterable" for which "func" returns true'''
    for i in range(len(lst)-1, -1, -1):
        if func(lst[i]):
            return i
    return None

def nth(gen, n):
    ''' Return the nth element in a generator '''
    try:
        res = gen.next()
        for _ in range(n):
            res = gen.next()
        return res
    except StopIteration:
        raise IndexError("No such element in generator: %d" % n)

def invert_dict(d):
    return {v:k for k,v in d.iteritems()}

def invert_dict_multi(d):
    """Invert a dictionary that can have the same value for different keys by returning a dictionary of lists.
       
       >>> invert_dict_multi({"A" : 5, "B" : 5, "C" : 9})
       {9: ['C'], 5: ['A', 'B']}
    """
    items_by_value = xgroupby(d.iteritems(), lambda (k, v): v)
    return {k: [a for (a,b) in v] for k, v in items_by_value.iteritems()}

def count_leading_chars(str, c):
    n = 0
    while str[n] == c:
        n += 1
    return n

if (__name__ == '__main__'):
    print xgroupby(range(10), lambda x: x%5)
    print invert_dict_multi({"A" : 5, "B" : 5, "C" : 9})
