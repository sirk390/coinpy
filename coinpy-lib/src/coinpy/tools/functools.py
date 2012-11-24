import itertools

''' Enhanced version of itertools.groupby that sorts and returns a dictionary '''
def xgroupby(data, keyfunc):
    data = sorted(data, key=keyfunc)
    return dict((grp, list(elemens)) for grp, elemens in itertools.groupby(data, keyfunc))


''' Return the first element in "iterable" for which "func" returns true'''
def first(iterable, func):
    for elm in iterable:
        if func(elm):
            return elm
    return None

if (__name__ == '__main__'):
    print xgroupby(range(10), lambda x: x%5)
