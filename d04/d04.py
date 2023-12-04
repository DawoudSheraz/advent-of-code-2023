from functools import reduce

SAMPLE_INPUT = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''


def calculate_intersection_card_numbers(card_string: str) -> list[int]:
    card, nums = card_string.split(': ')
    nums = nums.strip()
    winning, owned = nums.split(' | ')
    winning = [int(x.strip()) for x in winning.split(' ') if x]
    owned = [int(x.strip()) for x in owned.split(' ') if x]
    return list(set(winning).intersection(set(owned)))


def part_1(data_list: list[str]) -> int:
    value_sum = 0
    for line in data_list:
        output_list = calculate_intersection_card_numbers(line)
        if output_len := len(output_list):
            value_sum += pow(2, output_len - 1)
    return value_sum


def part_2(data_list: list[str]) -> int:
    card_count = {idx: 1 for idx, card in enumerate(data_list, start=1)}
    for idx, line in enumerate(data_list, start=1):
        output_list = calculate_intersection_card_numbers(line)
        for count in range(idx+1, idx + len(output_list) + 1):
            card_count[count] += card_count[idx]
    return reduce(lambda x, y: x + y, card_count.values())


with open('input.in') as f:
    data = f.readlines()
    # 32609
    # 14624680
    print(part_1(data))
    print(part_2(data))
