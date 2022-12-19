import parse
from pulp import LpProblem, LpMaximize, LpVariable, LpInteger, LpBinary, value, PULP_CBC_CMD
from tqdm import tqdm
from parse import parse


def day19():
    with open('../input/input19.txt', 'r') as f:
        data = f.read().splitlines()

    format_string = 'Blueprint {:d}: Each ore robot costs {:d} ore.' \
                    + ' Each clay robot costs {:d} ore.' \
                    + ' Each obsidian robot costs {:d} ore and {:d} clay.' \
                    + ' Each geode robot costs {:d} ore and {:d} obsidian.'
    blueprints = []
    for row in data:
        blueprint_data = parse(format_string, row)
        blueprint = {
            'number': blueprint_data[0],
            'ore_robot_ore_cost': blueprint_data[1],
            'clay_robot_ore_cost': blueprint_data[2],
            'obs_robot_ore_cost': blueprint_data[3],
            'obs_robot_clay_cost': blueprint_data[4],
            'geo_robot_ore_cost': blueprint_data[5],
            'geo_robot_obs_cost': blueprint_data[6]
        }
        blueprints.append(blueprint)

    score = 0

    for blueprint in tqdm(blueprints):
        s = build(blueprint, 24)
        score += s * blueprint['number']

    print('Part 1:', score)

    score = 1

    for blueprint in tqdm(blueprints[0:3]):
        s = build(blueprint, 32)
        score *= s

    print('Part 2:', score)


def build(blueprint, duration):
    prob = LpProblem("Tuning", LpMaximize)
    nb_ore_robots = [None]
    nb_clay_robots = [None]
    nb_obs_robots = [None]
    nb_geo_robots = [None]
    nb_ore_day_start = [None]
    nb_clay_day_start = [None]
    nb_obs_day_start = [None]
    nb_geo_day_start = [None]
    nb_ore_day_end = [None]
    nb_clay_day_end = [None]
    nb_obs_day_end = [None]
    nb_geo_day_end = [None]
    for m in range(1, duration + 1):
        nb_ore_robot = LpVariable(f"ore_robot_{m}", 0, None, LpBinary)
        nb_ore_robots.append(nb_ore_robot)
        nb_clay_robot = LpVariable(f"nb_clay_robot_{m}", 0, None, LpBinary)
        nb_clay_robots.append(nb_clay_robot)
        nb_obs_robot = LpVariable(f"nb_obs_robot_{m}", 0, None, LpBinary)
        nb_obs_robots.append(nb_obs_robot)
        nb_geo_robot = LpVariable(f"nb_geo_robot_{m}", 0, None, LpBinary)
        nb_geo_robots.append(nb_geo_robot)
        nb_ore_start = LpVariable(f"nb_ore_start_{m}", 0, None, LpInteger)
        nb_ore_day_start.append(nb_ore_start)
        nb_clay_start = LpVariable(f"nb_clay_start_{m}", 0, None, LpInteger)
        nb_clay_day_start.append(nb_clay_start)
        nb_obs_start = LpVariable(f"nb_obs_start_{m}", 0, None, LpInteger)
        nb_obs_day_start.append(nb_obs_start)
        nb_geo_start = LpVariable(f"nb_geo_start_{m}", 0, None, LpInteger)
        nb_geo_day_start.append(nb_geo_start)
        nb_ore_end = LpVariable(f"nb_ore_end_{m}", 0, None, LpInteger)
        nb_ore_day_end.append(nb_ore_end)
        nb_clay_end = LpVariable(f"nb_clay_end_{m}", 0, None, LpInteger)
        nb_clay_day_end.append(nb_clay_end)
        nb_obs_end = LpVariable(f"nb_obs_end_{m}", 0, None, LpInteger)
        nb_obs_day_end.append(nb_obs_end)
        nb_geo_end = LpVariable(f"nb_geo_end_{m}", 0, None, LpInteger)
        nb_geo_day_end.append(nb_geo_end)

    prob += nb_geo_day_end[duration]
    for m in range(1, duration + 1):
        # build at most one robot
        prob += nb_ore_robots[m] + nb_clay_robots[m] + nb_obs_robots[m] + nb_geo_robots[m] <= 1

        if m > 1:
            # Number of ore on start of day m = nb day before - build cost
            prob += nb_ore_day_start[m] == nb_ore_day_end[m - 1] - nb_ore_robots[m] * blueprint['ore_robot_ore_cost'] \
                    - nb_clay_robots[m] * blueprint['clay_robot_ore_cost'] - nb_obs_robots[m] * blueprint[
                        'obs_robot_ore_cost'] - nb_geo_robots[m] * blueprint['geo_robot_ore_cost']
            prob += nb_ore_day_start[m] >= 0
            # End of the day = start + production
            prob += nb_ore_day_end[m] == nb_ore_day_start[m] + sum([nb_ore_robots[k] for k in range(1, m)])
            # Number of clay
            prob += nb_clay_day_start[m] == nb_clay_day_end[m - 1] - nb_obs_robots[m] * blueprint[
                'obs_robot_clay_cost']
            prob += nb_clay_day_start[m] >= 0
            prob += nb_clay_day_end[m] == nb_clay_day_start[m] + sum([nb_clay_robots[k] for k in range(1, m)])
            # Number of obsidian
            prob += nb_obs_day_start[m] == nb_obs_day_end[m - 1] - nb_geo_robots[m] * blueprint[
                'geo_robot_obs_cost']
            prob += nb_obs_day_start[m] >= 0
            prob += nb_obs_day_end[m] == nb_obs_day_start[m] + sum([nb_obs_robots[k] for k in range(1, m)])
            # Number of geode
            prob += nb_geo_day_start[m] == nb_geo_day_end[m - 1]
            prob += nb_geo_day_start[m] >= 0
            prob += nb_geo_day_end[m] == nb_geo_day_start[m] + sum([nb_geo_robots[k] for k in range(1, m)])

    # First robot is an ore robot
    prob += nb_ore_robots[1] == 1

    # First day
    prob += nb_ore_day_start[1] == 0
    prob += nb_ore_day_end[1] == 1
    prob += nb_clay_day_start[1] == 0
    prob += nb_clay_day_end[1] == 0
    prob += nb_obs_day_start[1] == 0
    prob += nb_obs_day_end[1] == 0
    prob += nb_geo_day_start[1] == 0
    prob += nb_geo_day_end[1] == 0

    prob.solve(PULP_CBC_CMD(msg=False))

    return int(value(prob.objective))
