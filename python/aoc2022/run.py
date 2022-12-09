import argparse
from aoc2022.days.day1 import day1
from aoc2022.days.day2 import day2
from aoc2022.days.day3 import day3
from aoc2022.days.day4 import day4
from aoc2022.days.day5 import day5
from aoc2022.days.day6 import day6
from aoc2022.days.day7 import day7
from aoc2022.days.day8 import day8
from aoc2022.days.day9 import day9


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('day', metavar='day', type=int, nargs=1,
                        help='an integer for the accumulator')

    args = parser.parse_args()

    if int(args.day[0]) == 1:
        day1()
    if int(args.day[0]) == 2:
        day2()
    if int(args.day[0]) == 3:
        day3()
    if int(args.day[0]) == 4:
        day4()
    if int(args.day[0]) == 5:
        day5()
    if int(args.day[0]) == 6:
        day6()
    if int(args.day[0]) == 7:
        day7()
    if int(args.day[0]) == 8:
        day8()
    if int(args.day[0]) == 9:
        day9()
    if int(args.day[0]) == 10:
        pass
    if int(args.day[0]) == 11:
        pass
    if int(args.day[0]) == 12:
        pass
    if int(args.day[0]) == 13:
        pass
    if int(args.day[0]) == 14:
        pass
    if int(args.day[0]) == 15:
        pass
    if int(args.day[0]) == 16:
        pass
    if int(args.day[0]) == 17:
        pass
    if int(args.day[0]) == 18:
        pass
    if int(args.day[0]) == 19:
        pass
    if int(args.day[0]) == 20:
        pass
    if int(args.day[0]) == 21:
        pass
    if int(args.day[0]) == 22:
        pass
    if int(args.day[0]) == 23:
        pass
    if int(args.day[0]) == 24:
        pass
    if int(args.day[0]) == 25:
        pass


if __name__ == "__main__":
    main()
