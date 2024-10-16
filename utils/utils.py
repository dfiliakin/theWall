from collections import defaultdict


def groups(data, func):
    """gives a subset of a matrix that represents:

    cols = groups(test, lambda x, y: x)

    rows = groups(test, lambda x, y: y)

    fdiag = groups(test, lambda x, y: x + y)

    bdiag = groups(test, lambda x, y: x - y)"""

    grouping = defaultdict(list)
    for y in range(len(data)):
        for x in range(len(data[y])):
            grouping[func(x, y)].append(data[y][x])
    return list(map(grouping.get, sorted(grouping)))
