def day25():
    with open('../input/input25.txt', 'r') as f:
        data = f.read().splitlines()

    print('Part 1:', dec_to_bquint(sum([bquint_to_dec(d) for d in data])))


def bquint_to_dec(value):
    c = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
    return sum([(c[value[-(i + 1)]] * (5 ** i)) for i in range(len(value))])


def dec_to_bquint(value):
    base_num = []
    c = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-', 5: '0'}
    # Convert to base 5
    while value > 0:
        dig = int(value % 5)
        base_num.append(dig)
        value //= 5
    # carry forward
    carry = 0
    balanced_base_num = ""
    for d in base_num:
        k = d + carry
        balanced_base_num += c[k]
        carry = 1
        if k <= 2:
            carry = 0
    if carry == 1:
        balanced_base_num += "1"
    return balanced_base_num[::-1]
