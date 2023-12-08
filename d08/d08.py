
from math import lcm

SAMPLE_1 = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''

SAMPLE_2 = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''


SAMPLE_3 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''


def parse_input(input_str: str) -> tuple[str, dict]:
    output_dict = {}
    instruction, _, *maps = input_str.split('\n')
    for map_line in maps:
        parent, children = map_line.split(' = ')
        left, right = children.split(', ')
        left, right = left[1:], right[:-1]
        output_dict[parent] = {'left': left, 'right': right}
    return instruction, output_dict


def navigate_count(instructions, input_map, start, destination=None, part=1):
    count = 0
    steps = 0
    active_node = start
    while True:
        active_node = input_map[active_node]
        if count == len(instructions):
            count = 0
        instruction = instructions[count]
        if instruction == 'L':
            active_node = active_node['left']
        else:
            active_node = active_node['right']
        steps += 1
        if (active_node == destination and part == 1) or (active_node[-1] == 'Z' and part == 2):
            return steps
        count += 1


def get_all_starting_notes(input_map):
    starting_nodes = []
    for key in input_map.keys():
        if key[-1] == 'A':
            starting_nodes.append(key)
    return starting_nodes


def part_1(input_str):
    instruction, input_map = parse_input(input_str)
    return navigate_count(instruction, input_map, 'AAA', 'ZZZ')


def part_2(input_str):
    steps = []
    instruction, input_map = parse_input(input_str)
    starting_nodes = (get_all_starting_notes(input_map))
    for starting_node in starting_nodes:
        output = navigate_count(instruction, input_map, starting_node, part=2)
        steps.append(output)
    # The initial example made it seems like product was approach, but lcm turned out to be the correct one.
    # Why LCM? Because the steps will be repeated until all the starting nodes are at destination.
    # the movement for all nodes is done simultaneously and the product / multiplication does not take that
    # into account. That's LCM takes all the steps and provides the first common multiple of all steps individually.
    return lcm(*steps)


with open('input.in') as f:
    data = f.read()
    # 19241
    # 9606140307013
    print(part_1(data))
    print(part_2(data))
