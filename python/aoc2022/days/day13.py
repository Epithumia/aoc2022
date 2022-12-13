from ast import literal_eval
from functools import cmp_to_key

from aoc2022.days.day9 import sign


def day13():
    with open('../input/input13.txt', 'r') as f:
        data = f.read().split('\n\n')

    packets = []
    signal = ["[[2]]", "[[6]]"]
    score1 = 0
    i = 1
    for pair in data:
        packet = {'left': pair.splitlines()[0], 'right': pair.splitlines()[1]}
        packets.append(packet)
        signal.append(packet['left'])
        signal.append(packet['right'])
        if compare(packet['left'], packet['right']) == -1:
            score1 += i
        i += 1

    print('Part 1:', score1)

    decoded = sorted(signal, key=cmp_to_key(compare))

    score2 = 1
    for i in range(len(decoded)):
        if decoded[i] == "[[2]]" or decoded[i] == "[[6]]":
            score2 *= (i + 1)

    print('Part 2:', score2)


def compare(left, right):
    if isinstance(left, str):
        return compare(literal_eval(left), literal_eval(right))
    if isinstance(left, int) and isinstance(right, int):
        return sign(left - right)
    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    if isinstance(left, list) and isinstance(right, list):
        if len(left) == 0 and len(right) > 0:
            return -1
        if len(right) == 0 and len(left) > 0:
            return 1
        if len(left) == 0 and len(right) == 0:
            return 0
        result = compare(left[0], right[0])
        if result != 0:
            return result
        return compare(left[1:], right[1:])
    return 'X'
