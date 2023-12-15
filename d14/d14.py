
SAMPLE_INPUT = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''


def get_rolling_and_cube_rocks(input_matrix: list[str]) -> tuple[list, list]:

    rolling_rocks = []
    cube_rocks = []
    max_x, max_y = len(input_matrix[0]), len(input_matrix)
    for x_idx in range(max_x):
        for y_idx in range(max_y):
            character = input_matrix[y_idx][x_idx]
            if character == '#':
                cube_rocks.append((y_idx, x_idx))
            if character == 'O':
                rolling_rocks.append((y_idx, x_idx))
    return rolling_rocks, cube_rocks


def tilt_rocks__with_direction(
        rolling_rocks: list[tuple[int, int]],
        cube_rocks: list[tuple[int, int]],
        direction: str,
        max_y: int,
        max_x: int
):
    new_rocks = []
    rolling_rocks = set(rolling_rocks)
    x_diff = 0 if direction in 'NS' else 1
    y_diff = 0 if direction in 'WE' else 1
    op = '+' if direction in 'SE' else '-'
    rolling_rocks = sorted(
        rolling_rocks, key=lambda x: x[0] if direction in 'NS' else x[1],
        reverse=True if direction in 'SE' else False
    )
    for rock in rolling_rocks:
        rock_y, rock_x = rock
        active_y = rock_y
        active_x = rock_x
        while True:
            active_y = active_y + (y_diff * (-1 if op == '-' else 1))
            active_x = active_x + (x_diff * (-1 if op == '-' else 1))
            if active_y < 0 or active_x < 0 or active_y >= max_y or active_x >= max_x:
                break
            if (active_y, active_x) in new_rocks or (active_y, active_x) in cube_rocks:
                break
        # Here the 1 / -1 is reverse because the value has been added/subtracted in the loop and
        # needs to be reversed at here
        new_rocks.append(
            (active_y + (y_diff * (1 if op == '-' else -1)), active_x + (x_diff * (1 if op == '-' else -1)))
        )
    return new_rocks


def get_load(rocks: list[tuple[int, int]], max_y: int) -> int:
    output_sum = 0
    for rock in rocks:
        rock_y, rock_x = rock
        output_sum += (max_y - rock_y)
    return output_sum


def print_matrix(tilted, cube, max_x, max_y):
    for y in range(max_y):
        active_str = ""
        for x in range(max_x):
            if (y, x) in tilted:
                active_str += 'O'
            elif (y,x) in cube:
                active_str += '#'
            else:
                active_str += '.'
        print(active_str)
    print('\n')


def part_1(input_str: str) -> int:
    input_str = input_str.splitlines()
    max_y, max_x = len(input_str), len(input_str[0])
    rocks, cubes = get_rolling_and_cube_rocks(input_str)
    titled_rocks = tilt_rocks__with_direction(rocks, cubes, 'N', max_y, max_x)
    return get_load(titled_rocks, max_y)


def part_2(input_str: str, cycles: int) -> int:
    input_str = input_str.splitlines()
    max_y, max_x = len(input_str), len(input_str[0])
    rocks, cubes = get_rolling_and_cube_rocks(input_str)
    cache = {}
    load_cache = {}
    for count in range(cycles):
        rocks = tilt_rocks__with_direction(rocks, cubes, 'N', max_y, max_x)
        rocks = tilt_rocks__with_direction(rocks, cubes, 'W', max_y, max_x)
        rocks = tilt_rocks__with_direction(rocks, cubes, 'S', max_y, max_x)
        rocks = tilt_rocks__with_direction(rocks, cubes, 'E', max_y, max_x)
        if tuple(rocks) in cache:
            # This is same as AoC Day 17, 2022.
            # Find the index when repetition happens.
            # the total load is ((cycles - first_encountered_idx) % diff of current-first_idx) + first_encountered_idx
            # It is because the diff from first_idx to (prev_idx or 0) won't be same as current-first_idx.
            # So we need to factor that.
            # The -1 after cycles is needed because when we find the current_idx where the repeat happens, that point
            # is the start of new cycle, and we need to go back on idx for actual last point of cycle.
            previous_idx = cache[tuple(rocks)]
            diff = (cycles - 1 - previous_idx) % (count - previous_idx)
            return load_cache[diff + previous_idx]
        cache[tuple(rocks)] = count
        load_cache[count] = get_load(rocks, max_y)
        print("active cycle", count, load_cache[count])


with open('input.in') as f:
    data = f.read()
    # 107053
    # 88371
    # Part 2 takes some time to run even though there is no 2d array.
    print(part_1(data))
    print(part_2(data, 1000000000))
