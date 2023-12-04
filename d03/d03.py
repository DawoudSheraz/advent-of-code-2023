
from collections import defaultdict


SAMPLE_INPUT = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''


def get_matrix_dimensions(input_lines: list[str]) -> tuple[int, int]:
    max_x, max_y = len(input_lines[0]), len(input_lines)
    return max_x, max_y


def is_number_included(
        start_x: int,
        end_x: int,
        number_y: int,
        max_x: int,
        max_y: int,
        input_lines: list[str]
) -> tuple[int, int, bool, bool]:  # x, y, included, True if gear

    def check_symbol_presence(x, y):
        if x + 1 >= max_x or x < 0 or y + 1 >= max_y or y < 0:
            return False
        current_character = input_lines[y][x]
        if current_character.isdigit() or current_character == '.':
            return False
        return True

    for x_diff in range(start_x-1, end_x + 2):
        for y_diff in [-1, 0, 1]:
            if (start_x <= x_diff <= end_x) and y_diff == 0:
                continue
            if check_symbol_presence(x_diff, y_diff + number_y):
                return x_diff, y_diff + number_y, True, True if input_lines[y_diff + number_y][x_diff] == '*' else False
    return end_x, number_y, False, False


def solve(input_lines: list[str]) -> tuple[int, int]:
    max_x, max_y = get_matrix_dimensions(input_lines)
    gears = defaultdict(list)
    value_sum = 0
    gear_sum = 0

    for current_y, line in enumerate(input_lines):
        start_x, end_x = None, None
        for current_x, character in enumerate(line):
            if character.isdigit():
                if start_x is None:
                    start_x = current_x
                end_x = current_x
                # Small optimization-ish to loop ahead if the current index is not at end.
                # The idea is that if the index is at last element and that element is digit,
                # perform the inclusion and gears check. This tail-end optimization removes the need to perform these
                # checks after 2nd loop.
                if current_x + 1 != max_x:
                    continue
            if start_x is not None and end_x is not None:
                gear_x, gear_y, is_included, is_gear = is_number_included(
                    start_x, end_x, current_y, max_x, max_y, input_lines
                )
                if is_gear:
                    gears[(gear_y, gear_x)].append(int(input_lines[current_y][start_x:end_x + 1]))
                if is_included:
                    value_sum += int(input_lines[current_y][start_x:end_x + 1])
            start_x, end_x = None, None

    for gear, values_list in gears.items():
        if len(values_list) == 2:
            gear_sum += values_list[0] * values_list[-1]

    return value_sum, gear_sum


with open('input.in') as f:
    data = f.readlines()
    p1, p2 = solve(data)
    # 527144
    # 81463996
    print(p1)
    print(p2)
