def day3():
    with open('../input/input3.txt', 'r') as f:
        data = f.read().split('\n')[:-1]
    bags = [[i for i in bag] for bag in data]

    score_item = 0
    score_badge = 0
    for bag in bags:
        # print(ord(intersection(bag[:len(bag)//2], bag[len(bag)//2:]))-ord('a')+1)
        item = intersection(bag[:len(bag) // 2], bag[len(bag) // 2:])
        score_item += score(item)

    for i in range(len(bags)//3):
        item = badge(bags[3*i],bags[3*i+1],bags[3*i+2])
        score_badge += score(item)

    print('Part 1: ', score_item)
    print('Part 2: ', score_badge)



def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3[0]


def badge(lst1, lst2, lst3):
    lst = [value for value in lst1 if value in lst2]
    lste = [value for value in lst if value in lst3]
    return lste[0]

def score(item):
    if 'a' <= item <= 'z':
        return(ord(item) - ord('a') + 1)
    else:
        return(ord(item) - ord('A') + 27)
