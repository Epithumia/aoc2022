def day1():
    with open('../input/input1.txt', 'r') as f:
        data = f.read()
        data = data.split('\n')
        data.append('')
    acc = 0
    calories = []
    for item in data:
        if item != '':
            acc += int(item)
        else:
            calories.append(acc)
            acc = 0
    calories.sort(reverse=True)
    print('Max calories: ', calories[0])
    print('Top 3 calories: ', calories[0] + calories[1] + calories[2])
