
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

P2_MAP = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}


def parse_input_p2(input_list):
    output_list = []
    for operation in input_list:
        _, _, op = operation.split(' ')
        op = op[2: -1]
        value, direction = int(op[:5], base=16), P2_MAP[op[-1]]
        output_list.append(f"{direction} {value} ")
    return output_list


def get_area_and_boundary_with_shoelace(input_list, previous_coords):
    """
    Use shoelace algorithm to get area of the figure. Boundary is calculated alongside by simple summation.

    # https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem
    """
    boundary = 0
    area = 0
    prev_y, prev_x = previous_coords
    for operation in input_list:
        direction, value, _ = operation.split(' ')
        value = int(value)
        dy, dx = DIRECTIONAL_DX_MAP[direction]
        new_y, new_x = prev_y + (dy * value), prev_x + (dx * value)
        area += (prev_x * new_y)
        area -= (prev_y * new_x)

        boundary += value
        prev_y, prev_x = new_y, new_x
    return boundary, area // 2


def solve(data_input, part=1):
    # This is using pick theorem and shoelace algo to solve this (Thanks reddit :sadpepe:)
    # both are used to calculate area of polygon.
    # Pick algo is A = i + (b/2) - 1 where A is area, i is number of points inside figure (what we need), and b is count
    # of boundary points.
    # A is provided from shoelace. b is boundary, i is calculated via re-arranging equation to i = A - b/2 + 1
    # Then, just do i + b to give the answer.
    data_input = data_input.splitlines()
    if part == 2:
        data_input = parse_input_p2(data_input)
    boundary, area = get_area_and_boundary_with_shoelace(data_input, (0, 0))
    inner_points = area - boundary/2 + 1
    return inner_points + boundary


with open('input.in') as f:
    data = f.read()
    # 56923.0
    # 66296566363189.0
    print(solve(data))
    print(solve(data, part=2))

