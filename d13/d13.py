
SAMPLE_INPUT = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''


def locate_reflection(input_matrix, previous_reflection_idx=None):
    max_y = len(input_matrix)
    for mirror_line in range(max_y):
        diff_counter = 0
        mirror_found = True  # consider mirror to be there, break if any anomaly is found

        while (mirror_line - diff_counter >= 0) and ((mirror_line + diff_counter + 1) < max_y) and mirror_found:
            previous_value = input_matrix[mirror_line - diff_counter]
            # Since we are on the row itself, we need to check the next value and not row itself :facepalm:
            next_value = input_matrix[mirror_line + diff_counter + 1]
            if next_value != previous_value:
                mirror_found = False
                break
            diff_counter += 1
        if mirror_found and previous_reflection_idx != (mirror_line + 1):
            # Previous_reflect_idx is only meant for P2. This one was weird enough for me. I was doing this
            # check in matrix_reflection_part_2 where I was checking the new calculated value with old one, and it
            # was not yielding expected results. Some digging around reddit and other solutions, it seems this
            # check was needed here :confused:
            if mirror_line == max_y - 1:
                return 0
            return mirror_line + 1
    return 0


def matrix_transpose(input_matrix):
    return [''.join([input_matrix[j][i] for j in range(len(input_matrix))]) for i in range(len(input_matrix[0]))]


def matrix_reflection(input_matrix, previous_row=None, previous_column=None):
    horizontal_reflection = locate_reflection(input_matrix, previous_row)
    vertical_reflection = locate_reflection(matrix_transpose(input_matrix), previous_column)
    if horizontal_reflection:
        return horizontal_reflection, 0
    elif vertical_reflection:
        return 0, vertical_reflection


def matrix_reflection_part_2(input_matrix):
    previous_reflect = matrix_reflection(input_matrix, 0, 0)
    for y_idx in range(len(input_matrix)):
        for x_idx in range(len(input_matrix[0])):
            previous_value = input_matrix[y_idx][x_idx]
            new_value = '#' if previous_value == '.' else '.'
            input_matrix[y_idx] = f"{input_matrix[y_idx][:x_idx]}{new_value}{input_matrix[y_idx][x_idx+1:]}"
            reflection = matrix_reflection(input_matrix, previous_reflect[0], previous_reflect[1])
            if reflection and previous_reflect != reflection:
                return reflection
            input_matrix[y_idx] = f"{input_matrix[y_idx][:x_idx]}{previous_value}{input_matrix[y_idx][x_idx + 1:]}"


def part_1(input_str):
    output_sum = 0
    input_matrices = input_str.split('\n\n')
    for idx, mtrx in enumerate(input_matrices):
        mtrx = mtrx.splitlines()
        output = matrix_reflection(mtrx)
        output_sum += (output[0] * 100) + (output[1])
    return output_sum


def part_2(input_str):
    output_sum = 0
    input_matrices = input_str.split('\n\n')
    for idx, mtrx in enumerate(input_matrices):
        mtrx = mtrx.splitlines()
        output = matrix_reflection_part_2(mtrx)
        output_sum += (output[0] * 100) + (output[1])
    return output_sum


with open('input.in') as f:
    data = f.read()
    # 36448
    # 35799
    print(part_1(data))
    print(part_2(data))
