
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

SAMPLE_3 = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''

SAMPLE_4 = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''


SAMPLE_5 = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''


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


def looped_pipes_min_max(pipe_coords):
    min_x, min_y = pipe_coords[0][1], pipe_coords[0][0]
    max_x, max_y = 0, 0
    for count in range(1, len(pipe_coords)):
        y, x = pipe_coords[count]
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return min_x, min_y, max_x, max_y


def part_1(input_str):
    input_str = input_str.splitlines()
    max_x, max_y = get_matrix_dimensions(input_str)
    start_y, start_x = get_starting_location_coordinates(input_str)
    visited = defaultdict(int)
    starting_pipe_direction = ""
    output_dict = {(start_y, start_x): 0}
    for direction in ['L', 'R', 'U', 'D']:
        diff_coords = DIRECTIONAL_COORDS[direction]
        if is_move_possible(start_x + diff_coords[0], start_y + diff_coords[1], direction, max_x, max_y, input_str):
            output = navigate_matrix(
                input_str, start_x + diff_coords[0], start_y + diff_coords[1], visited, 1, direction
            )
            starting_pipe_direction += direction
            for k, v in output.items():
                if k in output_dict:
                    output_dict[k] = min(output_dict[k], v)
                else:
                    output_dict[k] = v

    return output_dict, starting_pipe_direction


def part_2(pipe_map, starting_pipe_directions, input_map):
    start_pipe_map = {  # to determine what sort of pipe S is based on its initial directions user went from it
        'U': '|',
        'D': '|',
        'R': '-',
        'L': '-',
        'LD': '7',
        'RD': 'F',
        'RU': 'L',
        'LU': 'J'

    }
    min_x, min_y, max_x, max_y = looped_pipes_min_max(list(pipe_map.keys()))
    included_count = 0
    for y in range(min_y, max_y+1):
        is_included = False
        active_curvy_pipe = None
        for x in range(min_x, max_x+1):
            current_character = input_map[y][x]
            if (y, x) in pipe_map:
                if current_character == 'S':
                    current_character = start_pipe_map[starting_pipe_directions]
                if current_character == '|' or (
                    current_character == 'J' and active_curvy_pipe == 'F'  # for cases F----J where pts after J are inside
                ) or (
                    current_character == '7' and active_curvy_pipe == 'L'  # for cases like L---7 where pts are 7 are inside
                ):
                    is_included = not is_included
                elif current_character in ['F', 'L']:
                    active_curvy_pipe = current_character
            elif current_character in '.F7JL-|' and is_included:
                included_count += 1
    return included_count


with open('input.in') as f:
    data = f.read()
    # 6613
    # 511
    navigated_pipe_map, starting_pipe_dirs = part_1(data)
    print(max(navigated_pipe_map.values()))
    print(part_2(navigated_pipe_map, starting_pipe_dirs, data.splitlines()))
