def day10():
    with open('../input/input10.txt', 'r') as f:
        data = f.read().splitlines()

    x = [1, 1]

    for instruction in data:
        if instruction[0] == 'n':
            x.append(x[-1])
        else:
            val = int(instruction.split(' ')[1])
            x.append(x[-1])
            x.append(val + x[-1])

    print('Part 1:', sum([x[i] * i for i in [20, 60, 100, 140, 180, 220]]))

    display = ''
    for row in range(6):
        display += '\n'
        pos = 0
        for cycle in range(40 * row + 1, 40*(row + 1) + 1):
            sprite = x[cycle]
            if sprite - 1 <= pos <= sprite + 1:
                display += '#'
            else:
                display += '.'
            pos += 1

    print('Part 2:', display)
