
import re


SAMPLE_INPUT = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''

SAMPLE_INPUT_P2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''

WORDS_TO_NUM = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0',
}


def get_calibration(data_string: str) -> int:
    matched_numbers = list(map(int, re.findall('\\d', data_string)))
    return matched_numbers[0] * 10 + matched_numbers[-1]


def get_calibration_part_2(data_string: str) -> int:
    matched_numbers = []
    for idx in range(len(data_string)):
        if data_string[idx].isdigit():
            matched_numbers.append(int(data_string[idx]))
        for word, num in WORDS_TO_NUM.items():
            if data_string[idx: idx + len(word)] == word:
                matched_numbers.append(int(num))

    return matched_numbers[0] * 10 + matched_numbers[-1]


def part_1(data: list[str]) -> int:
    calibration_sum = 0
    for row in data:
        calibration_sum += get_calibration(row)
    return calibration_sum


def part_2(data: list[str]) -> int:
    calibration_sum = 0
    for row in data:
        calibration_sum += get_calibration_part_2(row)
    return calibration_sum


with open('input.in') as f:
    input_lines = f.readlines()
    # Part 1: 54916
    # Part 2: 54728
    print(f"Part 1: {part_1(input_lines)}")
    print(f"Part 2: {part_2(input_lines)}")
