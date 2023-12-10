
from collections import defaultdict


SAMPLE_1 = '''.....
.S-7.
.|.|.
.L-J.
.....'''

SAMPLE_2 = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''

DIRECTIONAL_COORDS = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

# Mapping of Pipe and the next direction based in incoming/input direction
PIPE_DIRECTION_MAPPING = {
    '|': {'D': 'D', 'U': 'U'},
    '-': {'R': 'R', 'L': 'L'},
    'L': {'D': 'R', 'L': 'U'},
    'J': {'D': 'L', 'R': 'U'},
    '7': {'R': 'D', 'U': 'L'},
    'F': {'L': 'D', 'U': 'R'}
}


def get_matrix_dimensions(input_lines: list[str]) -> tuple[int, int]:
    max_x, max_y = len(input_lines[0]), len(input_lines)
    return max_x, max_y


def get_starting_location_coordinates(input_matrix) -> tuple[int, int]:
    for y, line in enumerate(input_matrix):
        for x, character in enumerate(line):
            if character == 'S':
                return y, x


def is_move_possible(x, y, direction, max_x, max_y, input_matrix):
    if x >= max_x or x < 0 or y >= max_y or y < 0:
        return False
    current_character = input_matrix[y][x]
    if current_character == '.':
        return False
    if direction not in PIPE_DIRECTION_MAPPING[current_character]:
        return False
    return True


def navigate_matrix(
        input_matrix,  current_x, current_y, visited_coords: dict, current_steps, direction
):
    while True:
        if (current_y, current_x) in visited_coords and current_steps >= visited_coords[(current_y, current_x)]:
            return visited_coords
        current_character = input_matrix[current_y][current_x]
        if current_character == 'S':
            return visited_coords
        visited_coords[(current_y, current_x)] = current_steps

        direction = PIPE_DIRECTION_MAPPING[current_character][direction]
        current_steps += 1
        if direction == 'R':
            current_x = current_x + 1
        if direction == 'L':
            current_x = current_x - 1
        if direction == 'U':
            current_y = current_y - 1
        if direction == 'D':
            current_y = current_y + 1


def part_1(input_str):
    input_str = input_str.splitlines()
    max_x, max_y = get_matrix_dimensions(input_str)
    start_y, start_x = get_starting_location_coordinates(input_str)
    visited = defaultdict(int)
    output_dict = {}
    for direction in ['L', 'R', 'U', 'D']:
        diff_coords = DIRECTIONAL_COORDS[direction]
        if is_move_possible(start_x + diff_coords[0], start_y + diff_coords[1], direction, max_x, max_y, input_str):
            output = navigate_matrix(
                input_str, start_x + diff_coords[0], start_y + diff_coords[1], visited, 1, direction
            )
            for k, v in output.items():
                if k in output_dict:
                    output_dict[k] = min(output_dict[k], v)
                else:
                    output_dict[k] = v
    print(max(output_dict.values()))


with open('input.in') as f:
    data = f.read()
    # 6613
    # TODO: Part 2, it is confusing as heck for now
    part_1(data)
