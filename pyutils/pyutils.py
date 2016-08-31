from collections import Counter, MutableMapping, defaultdict


def partition(predicate, iterable):
    t, f = [], []
    for item in iterable:
        if predicate(item):
            t.append(item)
        else:
            f.append(item)
    return t, f


def partition_mapping(predicate, mapping):
    mapping_type = type(mapping)
    a, b = partition(lambda pair: predicate(*pair), mapping.items())
    return mapping_type(a), mapping_type(b)


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


def duplicates(iterable):
    c = Counter(iterable)
    if len(c) == len(iterable):
        return set()
    else:
        return {k for (k, v) in Counter(iterable).items() if v > 1}


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


class InversibleDict(MutableMapping):
    '''A mutable mapping that keeps track of its inverse dynamically for fast
    lookup of the set of keys corresponding to a given value.
    '''
    def __init__(self, mapping=None):
        self._map = {}
        self._by_value = defaultdict(set)
        if mapping:
            self.update(mapping)

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self._map)

    def __setitem__(self, key, value):
        if key in self._map:
            self._by_value[self._map[key]].discard(key)
        self._map[key] = value
        self._by_value[value].add(key)

    def __getitem__(self, key):
        return self._map[key]

    def __delitem__(self, key):
        old_value = self._map.pop(key)
        keys = self._by_value[old_value]
        keys.remove(key)
        if not keys:
            del self._by_value[old_value]

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)

    def get_keys_for(self, value):
        # NB: we have to make a frozenset so that clients can't mess with our
        # internal reverse cache
        return frozenset(self._by_value.get(value, ()))

    def keys_for(self, value):
        if value not in self._by_value:
            raise KeyError(value)
        else:
            return self._by_value[value]

    def inverse(self):
        return {v: frozenset(ks) for v, ks in self._by_value.items()}
