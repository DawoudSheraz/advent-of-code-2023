from collections import defaultdict

SAMPLE_INPUT = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''


def get_hash_value(input_str: str) -> int:
    value = 0
    for character in input_str:
        value = ((value + ord(character)) * 17) % 256
    return value


def part_1(input_str: str) -> int:
    output = 0
    for string in input_str.split(','):
        output += get_hash_value(string)
    return output


def is_label_present(box: list[tuple[str, int]], label: int) -> int | None:
    for idx, entry in enumerate(box):
        if entry[0] == label:
            return idx
    return None


def part_2(input_str: str) -> int:
    lenses_focal_values = defaultdict(int)
    boxes = [[] for _ in range(256)]
    for string in input_str.split(','):
        is_removal = string[-1] == '-'
        is_addition = string[-2] == '='
        if is_removal:
            label = string[:-1]
            label_hash = get_hash_value(label)
            is_existing_label = is_label_present(boxes[label_hash], label)
            if is_existing_label is not None:
                boxes[label_hash].pop(is_existing_label)
        elif is_addition:
            label = string[:-2]
            label_hash = get_hash_value(label)
            focal_length = int(string[-1])
            is_existing_label = is_label_present(boxes[label_hash], label)
            if is_existing_label is not None:
                boxes[label_hash][is_existing_label] = (label, focal_length)
            else:
                boxes[label_hash].append((label, focal_length))

    for box_idx, box in enumerate(boxes):
        for placement_idx, lens in enumerate(box):
            lenses_focal_values[lens[0]] += (box_idx + 1) * (placement_idx + 1) * lens[1]
    return sum(lenses_focal_values.values())


with open('input.in') as f:
    data = f.read()
    # 515495
    # 229349
    print(part_1(data))
    print(part_2(data))
