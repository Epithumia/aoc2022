from tqdm import tqdm


def day20():
    with open('../input/input20.txt', 'r') as f:
        data = f.read().splitlines()

    print('Part 1:', decrypt(data))

    print('Part 2:', decrypt(data, 10, 811589153))


def decrypt(data, rounds=1, key=1):
    length = len(data)
    crypted = []
    decrypted = {}
    for i in range(length):
        crypted.append(int(data[i]) * key)
        if (int(data[i]) * key, i) not in decrypted.keys():
            decrypted[(int(data[i]) * key, i)] = i
        else:
            decrypted[(int(data[i]) * key, i)][i] = i
    if rounds > 1:
        for _ in tqdm(range(rounds), position=0):
            do_round(crypted, decrypted, length, 1)
    else:
        do_round(crypted, decrypted, length)

    pos_zero = 0
    for val, pos in decrypted.items():
        if val[0] == 0:
            pos_zero = pos

    final = [x[0] for x in sorted(decrypted, key=lambda k: decrypted[k])]

    return final[(pos_zero + 1000) % length] + final[(pos_zero + 2000) % length] + final[(pos_zero + 3000) % length]


def do_round(crypted, decrypted, length, p=0):
    for di in tqdm(range(len(crypted)), position=p, leave=False):
        d = crypted[di]
        pos = decrypted[(d, di)]
        if d % length == 0:
            new_pos = pos
        else:
            new_pos = (pos + d) % (length - 1)
        decrypted[(d, di)] = new_pos
        for o in decrypted.keys():  # For all items
            if o != (d, di) and decrypted[o] > pos:
                decrypted[o] = (decrypted[o] - 1) % length
            if o != (d, di) and decrypted[o] >= new_pos:
                decrypted[o] = (decrypted[o] + 1) % length
