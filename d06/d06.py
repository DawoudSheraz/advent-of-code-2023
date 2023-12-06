
SAMPLE_INPUT = '''Time:      7  15   30
Distance:  9  40  200'''


def get_time_distances(input_str: str) -> tuple[list[int], list[int]]:
    time, distance = input_str.split('\n')
    time = time.split(':')[1].strip().split(' ')
    distance = distance.split(':')[1].strip().split(' ')
    time = [int(x) for x in time if x]
    distance = [int(x) for x in distance if x]
    return time, distance


def total_ways_to_win(time: int, record_distance: int) -> int:
    ways = 0
    for hold_time in range(1, time+1):
        distance_travelled = hold_time * (time - hold_time)
        if distance_travelled > record_distance:
            ways += 1
    return ways


def part_1(input_str: str) -> int:
    output_sum = 1
    time, distance = get_time_distances(input_str)
    for count in range(len(time)):
        output_sum *= total_ways_to_win(time[count], distance[count])
    return output_sum


def part_2(input_str) -> int:
    time, distance = get_time_distances(input_str)
    time = list(map(str, time))
    distance = list(map(str, distance))
    time = int(''.join(time))
    distance = int(''.join(distance))
    return total_ways_to_win(time, distance)


with open('input.in') as f:
    data = f.read()
    # 140220
    # 39570185  (p2 takes about 10 seconds, ok for now)
    print(part_1(data))
    print(part_2(data))
