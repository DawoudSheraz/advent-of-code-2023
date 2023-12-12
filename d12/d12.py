
from functools import lru_cache


SAMPLE_INPUT = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''


def get_broken_pieces_length(data_str):
    output = []
    is_broken = False
    starting_index = 0
    for idx, character in enumerate(data_str):
        if character == '#' and not is_broken:
            is_broken = True
            starting_index = idx
        elif character == '.' and is_broken:
            is_broken = False
            output.append(idx - starting_index)
            starting_index = None
    if starting_index and is_broken:
        output.append(len(data_str) - starting_index)
    return output


def subset_generation(input_str, new_string, active_idx, subset_count, broken_pieces):
    if len(input_str) == len(new_string):
        if get_broken_pieces_length(new_string) == broken_pieces:
            subset_count.append(1)
        return
    else:
        current_character = input_str[active_idx]
        if current_character in ['#', '.']:
            new_string += current_character
            subset_generation(input_str, new_string, active_idx + 1, subset_count, broken_pieces)
        else:
            subset_generation(input_str, new_string + '.', active_idx + 1, subset_count, broken_pieces)
            subset_generation(input_str, new_string + '#', active_idx + 1, subset_count, broken_pieces)


def generate_possible_sequences(data_str, broken_pieces):
    subset_c = []
    subset_generation(data_str, "", 0, subset_c, broken_pieces)
    return len(subset_c)


def unfold_data_input(input_str, broken_pieces):
    input_str = '?'.join(input_str * 5)
    broken_pieces = ','.join(broken_pieces * 5)
    return input_str, broken_pieces


def part_1(input_str):
    out_sum = 0
    input_str = input_str.splitlines()
    for line in input_str:
        data_str, broken = line.split(' ')
        broken = list(map(int, broken.split(',')))
        out_sum += generate_possible_sequences(data_str, broken)
    return out_sum


def part_2(input_str):
    out_sum = 0
    input_str = input_str.splitlines()
    for line in input_str:
        data_str, broken = line.split(' ')
        data_str, broken = unfold_data_input([data_str], [broken])
        broken = list(map(int, broken.split(',')))
        print(data_str, broken, out_sum)
        out_sum += generate_possible_sequences(data_str, broken)
    return out_sum


with open('input.in') as f:
    data = f.read()
    # 7191

    # TODO: Part 2. Even part 1 takes a bit of time to complete
    # The subset generation can be made better I guess.
    # checking if the addition of # or . checks some parts of broken items and reduce input(?). Idk
    # a brain freeze about it for now.
    print(part_1(data))
