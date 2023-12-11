
SAMPLE_1 = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''


def get_matrix_dimensions(input_lines: list[str]) -> tuple[int, int]:
    max_x, max_y = len(input_lines[0]), len(input_lines)
    return max_x, max_y


def get_galaxy_less_rows(input_matrix: list[str]) -> list[int]:
    rows = []
    for idx, line in enumerate(input_matrix):
        if line.count('.') == len(line):
            rows.append(idx)
    return rows


def get_galaxy_less_columns(input_matrix: list[str]) -> list[int]:
    max_x, max_y = get_matrix_dimensions(input_matrix)
    columns_to_expand = []
    for x in range(max_x):
        is_galaxy_missing = True
        for y in range(max_y):
            if input_matrix[y][x] == '#':
                is_galaxy_missing = False
                break
        if is_galaxy_missing:
            columns_to_expand.append(x)
    return columns_to_expand


def get_coordinates_difference(
        pair_1: tuple[int, int],
        pair_2: tuple[int, int],
        galaxy_less_rows: list[int],
        galaxy_less_columns: list[int],
        galaxy_upscale: int = 2
):
    x1, x2 = pair_1[1], pair_2[1]
    y1, y2 = pair_1[0], pair_2[0]
    x_range = list(range(min(x1, x2), max(x1, x2) + 1))
    y_range = list(range(min(y1, y2), max(y1, y2) + 1))

    x_diff = list(set(x_range).intersection(set(galaxy_less_columns)))
    y_diff = list(set(y_range).intersection(set(galaxy_less_rows)))
    return abs(x2 - x1) + abs(y2 - y1) + (len(x_diff) * galaxy_upscale) + (len(y_diff) * galaxy_upscale)


def get_galaxy_pairs(input_data: list[str]) -> list[tuple[int, int]]:
    galaxy_pairs = []
    for y, line in enumerate(input_data):
        for x, character in enumerate(line):
            if character == '#':
                galaxy_pairs.append((y, x))
    return galaxy_pairs


def solve(input_str: str, galaxy_upscale: int = 2) -> int:
    output_sum = 0
    input_str = input_str.splitlines()
    galaxies = get_galaxy_pairs(input_str)
    galaxy_less_rows = get_galaxy_less_rows(input_str)
    galaxy_less_columns = get_galaxy_less_columns(input_str)
    for outer_counter in range(0, len(galaxies) - 1):
        for inner_counter in range(outer_counter + 1, len(galaxies)):
            p1, p2 = galaxies[outer_counter], galaxies[inner_counter]
            output_sum += get_coordinates_difference(
                p1, p2,
                galaxy_less_rows, galaxy_less_columns,
                galaxy_upscale-1  # do -1 to exclude the initial row or column itself.
            )
    return output_sum


with open('input.in') as f:
    data = f.read()
    # 9647174
    # 377318892554
    print(solve(data))
    print(solve(data, 1000000))
