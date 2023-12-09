
SAMPLE_INPUT = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''


def get_next_history_value(value_list: list[int]) -> int:
    active_list = value_list
    end_value_stack = [value_list[-1]]
    while True:
        temp_list = []
        for counter in range(len(active_list) - 1):
            difference = active_list[counter+1] - active_list[counter]
            temp_list.append(difference)
        end_value_stack.append(temp_list[-1])
        active_list = temp_list
        if active_list.count(0) == len(active_list):
            break
    return sum(end_value_stack)


def solve(input_str: str) -> tuple[int, int]:
    p1, p2 = 0, 0
    for line in input_str.splitlines():
        line = list(map(int, line.split(' ')))
        # Just reverse the list and it is essentially part 1
        line_reversed = line[::-1]
        history = get_next_history_value(line)
        history_part_2 = get_next_history_value(line_reversed)
        p1 += history
        p2 += history_part_2
    return p1, p2


with open('input.in') as f:
    data = f.read()
    part_1, part_2 = solve(data)
    # 1938731307
    # 948
    print(part_1)
    print(part_2)
