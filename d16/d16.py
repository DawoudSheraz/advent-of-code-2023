
SAMPLE_INPUT = '''.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''


MIRROR_DIRECTION_MAP = {
    '/': {'R': 'U', 'L': 'D', 'U': 'R', 'D': 'L'},
    '\\': {'R': 'D', 'L': 'U', 'U': 'L', 'D': 'R'}
}

DIRECTIONAL_DX_MAP = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}


def get_mirrors(sample_input):
    mirrors = {}
    for y_idx, line in enumerate(sample_input):
        for x_idx, character in enumerate(line):
            if character != '.':
                mirrors[(y_idx, x_idx)] = character
    return mirrors


def beams_blaze(beams, mirrors, max_x, max_y):
    energized = set()
    energy_list = []
    while True:
        temp_beams = []
        for beam in beams:
            # if beam == ((0, 3), 'L'):
            #     breakpoint()
            beam_coords, beam_direction = beam
            beam_y, beam_x = beam_coords
            if beam_y >= max_y or beam_y < 0 or beam_x < 0 or beam_x >= max_x:
                continue
            energized.add(beam_coords)
            if beam_coords in mirrors:
                mirror = mirrors[beam_coords]
                if mirror == '|':
                    if beam_direction in 'UD':
                        dy, dx = DIRECTIONAL_DX_MAP[beam_direction]
                        temp_beams.extend([((beam_y + dy, beam_x + dx), beam_direction)])
                    else:
                        temp_beams.extend([((beam_y + 1, beam_x), 'D'), ((beam_y - 1, beam_x), 'U')])
                elif mirror == '-':
                    if beam_direction in 'LR':
                        dy, dx = DIRECTIONAL_DX_MAP[beam_direction]
                        temp_beams.extend([((beam_y + dy, beam_x + dx), beam_direction)])
                    else:
                        temp_beams.extend(
                            [((beam_y, beam_x - 1), 'L'), ((beam_y, beam_x + 1), 'R')]
                        )
                else:
                    new_direction = MIRROR_DIRECTION_MAP[mirror][beam_direction]
                    dy, dx = DIRECTIONAL_DX_MAP[new_direction]
                    bny, bnx = beam_y + dy, beam_x + dx
                    temp_beams.extend([((bny, bnx), new_direction)])
            else:
                dy, dx = DIRECTIONAL_DX_MAP[beam_direction]
                by, bx = beam_coords[0] + dy, beam_coords[1] + dx
                temp_beams.append(((by, bx), beam_direction))

        if not temp_beams:
            break
        temp_beams = list(set(temp_beams))
        beams = temp_beams

        # This is a weird hack and relates to bug in code (can't locate where at this point)
        # What's happening is that beams for some reason are not ending(?). So, This hack maintains
        # a list of last 10 energized values and if they are all same, that means the value is the actual
        # energy value. 10 is just a random, optimum value. We can pick (max_x + max_y) for better checks.
        # This is a TODO, if I understand what I did wrong :sweat-smile:
        if len(energy_list) == 10:
            if len(set(energy_list)) == 1:
                break
            else:
                energy_list = []
        energy_list.append(len(energized))
    return len(energized)


def print_matrix(energized, max_x, max_y):
    for y in range(max_y):
        active_str = ""
        for x in range(max_x):
            if (y, x) in energized:
                active_str += '#'
            else:
                active_str += '.'
        print(active_str)
    print('\n')


def part_1(input_str):
    input_data = input_str.splitlines()
    max_x, max_y = len(input_data[0]), len(input_data)
    mirrors = get_mirrors(input_data)
    return beams_blaze([((0, 0), 'R')], mirrors, max_x, max_y)


def part_2(input_str):
    beams_energy = []
    input_data = input_str.splitlines()
    max_x, max_y = len(input_data[0]), len(input_data)
    mirrors = get_mirrors(input_data)

    for x in range(max_x):
        beams_energy.append(beams_blaze(
            [((0, x), 'D')], mirrors, max_x, max_y)
        )
        beams_energy.append(beams_blaze(
            [((max_y - 1, x), 'U')], mirrors, max_x, max_y)
        )
        if x == 0:
            beams_energy.append(beams_blaze(
                [((0, x), 'R')], mirrors, max_x, max_y)
            )
            beams_energy.append(beams_blaze(
                [((max_y - 1, x), 'R')], mirrors, max_x, max_y)
            )

        if x == (max_x - 1):
            if x == 0:
                beams_energy.append(beams_blaze(
                    [((0, x), 'L')], mirrors, max_x, max_y)
                )
                beams_energy.append(beams_blaze(
                    [((max_y - 1, x), 'L')], mirrors, max_x, max_y)
                )

    for y in range(max_y):
        beams_energy.append(beams_blaze(
            [((y, 0), 'R')], mirrors, max_x, max_y)
        )
        beams_energy.append(beams_blaze(
            [((y, max_x - 1), 'L')], mirrors, max_x, max_y)
        )
        if y == 0:
            beams_energy.append(beams_blaze(
                [((y, 0), 'D')], mirrors, max_x, max_y)
            )
            beams_energy.append(beams_blaze(
                [((y, max_x - 1), 'D')], mirrors, max_x, max_y)
            )

        if y == (max_y - 1):
            beams_energy.append(beams_blaze(
                [((y, 0), 'U')], mirrors, max_x, max_y)
            )
            beams_energy.append(beams_blaze(
                [((y, max_x - 1), 'U')], mirrors, max_x, max_y)
            )

    return max(beams_energy)


with open('input.in') as f:
    data = f.read()
    # 7951
    # 8148
    print(part_1(data))
    print(part_2(data))
