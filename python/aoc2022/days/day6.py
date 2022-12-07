def day6():
    with open('../input/input6.txt', 'r') as f:
        data = f.read().split('\n')[0]

    print('Part 1: ', tune(data, 4))
    print('Part 2: ', tune(data, 14))


def tune(signal, length):
    for i in range(len(signal) - (length - 1)):
        d = signal[i:i + length]
        s = set([c for c in d])
        if len(s) == length:
            return i + length
    return None
