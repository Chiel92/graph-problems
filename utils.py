Infinity = float('inf')

def argmax(items, key):
    maxvalue = -Infinity
    for arg in items:
        if key(arg) > maxvalue:
            maxvalue = key(arg)
            maxarg = arg
    try:
        return maxarg
    except UnboundLocalError:
        raise ValueError('Argument items is empty')
