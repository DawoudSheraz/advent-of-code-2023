
import itertools
import operator

SAMPLE_INPUT = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

DIRECTIONAL_DX_MAP = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}


def dig_outer(input_list):
    mapped_points = {(0, 0)}
    y, x = 0, 0

    for operation in input_list:
        direction, value, _ = operation.split(' ')
        value = int(value)
        dy, dx = DIRECTIONAL_DX_MAP[direction]

        for _ in range(value):
            x += dx
            y += dy
            mapped_points.add((y, x))
    return mapped_points


def get_dimensions(mapped_points):
    min_x, min_y, max_x, max_y = 9999999999999, 9999999999, 0, 0
    for point in mapped_points:
        y, x = point
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    return min_x, min_y, max_x, max_y



def dig_inner(outer_mapped_points, min_x, min_y, max_x, max_y):
    new_points = set()
    outer_mapped_points = sorted(list(outer_mapped_points), key=lambda x: (x[0], x[1]))
    for y in range(min_y, max_y + 1):
        is_included = False
        x = min_x
        while True:
            if x > max_x + 1:
                break
            if (y, x) in outer_mapped_points:
                while (y, x) in outer_mapped_points:
                    x += 1
                is_included = not is_included
            if is_included and min_x <= x <= max_x:
                new_points.add((y, x))
            x += 1
    return new_points


def get_group_inner_count(row_group):
    inner_count = set()
    for idx in range(len(row_group) - 1):
        current, nxt = row_group[idx], row_group[idx + 1]
        if (diff := nxt[1] - current[1]) != 1:
            for count in range(1, diff + 1):
                inner_count.add((current[0], current[1] + count))
    return inner_count


def part_1(data_input):
    data_input = data_input.splitlines()
    mapped_points = dig_outer(data_input)
    mapped_points = sorted(list(mapped_points), key=lambda x: (x[0], x[1]))
    inner_pts = []
    for key, group in itertools.groupby(mapped_points, operator.itemgetter(0)):
        group = list(group)
        diff_count = get_group_inner_count(group)
        inner_pts.extend(list(diff_count))
        inner_pts = list(set(inner_pts))
    print(len(inner_pts), len(mapped_points))


with open('input.in') as f:
    data = f.read()
    # NOTE: Does not work
    print(part_1(data))

