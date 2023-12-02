
from functools import reduce


SAMPLE_INPUT = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''


CUBE_LIMIT = {'red': 12, 'green': 13, 'blue': 14}


def is_game_possible(cube_string: str) -> bool:
    for game_set in cube_string.split(';'):
        for cubes in game_set.split(','):
            cube_count, cube_color = cubes.strip().split(' ')
            if int(cube_count) > CUBE_LIMIT[cube_color]:
                return False
    return True


def get_cube_power(cube_string: str) -> int:
    cube_count = {'red': 0, 'green': 0, 'blue': 0}
    for game_set in cube_string.split(';'):
        for cubes in game_set.split(','):
            value, cube_color = cubes.strip().split(' ')
            cube_count[cube_color] = max(cube_count[cube_color], int(value))
    return reduce(lambda x, y: x * y, cube_count.values())


def part_1(input_lines: list[str]) -> int:
    id_sum = 0
    for input_line in input_lines:
        game, cubes = input_line.split(': ')
        if is_game_possible(cubes):
            id_sum += int(game.split(' ')[-1])
    return id_sum


def part_2(input_lines: list[str]) -> int:
    power_sum = 0
    for input_line in input_lines:
        _, cubes = input_line.split(': ')
        power_sum += get_cube_power(cubes)
    return power_sum


with open('input.in') as f:
    data = f.readlines()
    # 1734
    # 70387
    print(part_1(data))
    print(part_2(data))
