def partition(predicate, iterable):
    t, f = [], []
    for item in iterable:
        if predicate(item):
            t.append(item)
        else:
            f.append(item)
    return t, f
