def partition(predicate, iterable):
    t, f = [], []
    for item in iterable:
        if predicate(item):
            t.append(item)
        else:
            f.append(item)
    return t, f


def strict_zip(*iterables):
    if iterables:
        iterables = tuple(map(tuple, iterables))
        lens = tuple(map(len, iterables))
        first = lens[0]
        if not all(l == first for l in lens):
            e = ValueError('Iterables are different lengths')
            e.lens = lens
            raise e
    return zip(*iterables)


def bound(value, _min, _max):
    if _min is None:
        if _max is None:
            return value
        else:
            return min(value, _max)
    else:
        if _max is None:
            return max(_min, value)
        else:
            return sorted((_min, value, _max))[1]
