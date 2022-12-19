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

    for blueprint in tqdm(blueprints[0:min(3, len(blueprints))]):  # min needed for test case
        s = build(blueprint, 32)
        score *= s

    print('Part 2:', score)


def init_array(name, duration, var_type):
    arr = [None]
    for m in range(1, duration + 1):
        arr.append(LpVariable(name.format(m=m), 0, None, var_type))
    return arr


def build(blueprint, duration):
    prob = LpProblem("Tuning", LpMaximize)
    ore_robots = init_array("ore_robot_{m}", duration, LpBinary)
    clay_robots = init_array("clay_robot_{m}", duration, LpBinary)
    obs_robots = init_array("obs_robot_{m}", duration, LpBinary)
    geo_robots = init_array("geo_robot_{m}", duration, LpBinary)
    nb_ore_day_start = init_array("nb_ore_start_{m}", duration, LpInteger)
    nb_clay_day_start = init_array("nb_clay_start_{m}", duration, LpInteger)
    nb_obs_day_start = init_array("nb_obs_start_{m}", duration, LpInteger)
    nb_geo_day_start = init_array("nb_geo_start_{m}", duration, LpInteger)
    nb_ore_day_end = init_array("nb_ore_end_{m}", duration, LpInteger)
    nb_clay_day_end = init_array("nb_clay_end_{m}", duration, LpInteger)
    nb_obs_day_end = init_array("nb_obs_end_{m}", duration, LpInteger)
    nb_geo_day_end = init_array("nb_geo_end_{m}", duration, LpInteger)

    prob += nb_geo_day_end[duration]
    for m in range(1, duration + 1):
        # build at most one robot
        prob += ore_robots[m] + clay_robots[m] + obs_robots[m] + geo_robots[m] <= 1

        if m > 1:
            # Number of ore on start of day m = nb day before - build cost, must stay >= 0
            prob += nb_ore_day_start[m] == nb_ore_day_end[m - 1] - ore_robots[m] * blueprint['ore_robot_ore_cost'] \
                    - clay_robots[m] * blueprint['clay_robot_ore_cost'] - obs_robots[m] * blueprint[
                        'obs_robot_ore_cost'] - geo_robots[m] * blueprint['geo_robot_ore_cost']
            prob += nb_ore_day_start[m] >= 0
            # End of the day = start + production
            prob += nb_ore_day_end[m] == nb_ore_day_start[m] + sum([ore_robots[k] for k in range(1, m)])
            # Number of clay
            # Start
            prob += nb_clay_day_start[m] == nb_clay_day_end[m - 1] - obs_robots[m] * blueprint[
                'obs_robot_clay_cost']
            prob += nb_clay_day_start[m] >= 0
            # End
            prob += nb_clay_day_end[m] == nb_clay_day_start[m] + sum([clay_robots[k] for k in range(1, m)])
            # Number of obsidian
            # Start
            prob += nb_obs_day_start[m] == nb_obs_day_end[m - 1] - geo_robots[m] * blueprint[
                'geo_robot_obs_cost']
            prob += nb_obs_day_start[m] >= 0
            # End
            prob += nb_obs_day_end[m] == nb_obs_day_start[m] + sum([obs_robots[k] for k in range(1, m)])
            # Number of geode
            # Start
            prob += nb_geo_day_start[m] == nb_geo_day_end[m - 1]
            prob += nb_geo_day_start[m] >= 0
            # End
            prob += nb_geo_day_end[m] == nb_geo_day_start[m] + sum([geo_robots[k] for k in range(1, m)])

    # First robot is an ore robot
    prob += ore_robots[1] == 1

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
