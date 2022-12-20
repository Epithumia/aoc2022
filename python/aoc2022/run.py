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
from aoc2022.days.day10 import day10
from aoc2022.days.day11 import day11
from aoc2022.days.day12 import day12
from aoc2022.days.day13 import day13
from aoc2022.days.day14 import day14
from aoc2022.days.day114 import day114
from aoc2022.days.day15 import day15
from aoc2022.days.day16 import day16
from aoc2022.days.day17 import day17
from aoc2022.days.day18 import day18
from aoc2022.days.day19 import day19
from aoc2022.days.day20 import day20


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
        day10()
    if int(args.day[0]) == 11:
        day11()
    if int(args.day[0]) == 12:
        day12()
    if int(args.day[0]) == 13:
        day13()
    if int(args.day[0]) == 14:
        day14()
    if int(args.day[0]) == 114:
        day114()
    if int(args.day[0]) == 15:
        day15()
    if int(args.day[0]) == 115:
        day15(True)
    if int(args.day[0]) == 16:
        day16()
    if int(args.day[0]) == 17:
        day17()
    if int(args.day[0]) == 18:
        day18()
    if int(args.day[0]) == 19:
        day19()
    if int(args.day[0]) == 20:
        day20()
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
