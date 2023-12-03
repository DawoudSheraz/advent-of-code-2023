
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
) -> bool:

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
                return True
    return False


def part_1(input_lines: list[str]) -> int:
    max_x, max_y = get_matrix_dimensions(input_lines)
    value_sum = 0

    for current_y, line in enumerate(input_lines):
        start_x, end_x = None, None
        for current_x, character in enumerate(line.strip()):
            if character.isdigit():
                if start_x is None:
                    start_x = current_x
                end_x = current_x
            else:
                if start_x is not None and end_x is not None:
                    if is_number_included(start_x, end_x, current_y, max_x, max_y, input_lines):
                        value_sum += int(input_lines[current_y][start_x:end_x + 1])
                start_x, end_x = None, None
        if start_x is not None and end_x is not None:
            if is_number_included(start_x, end_x, current_y, max_x, max_y, input_lines):
                value_sum += int(input_lines[current_y][start_x:end_x + 1])

    return value_sum


with open('input.in') as f:
    data = f.readlines()
    # 527144
    print(part_1(data))
    # TODO: Combine both p1 and p2 in a single file. It can be done easily, just need to give a bit time
