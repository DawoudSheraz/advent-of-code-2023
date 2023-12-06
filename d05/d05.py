
SAMPLE_INPUT = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''


def populate_maps(input_str: str) -> list:
    maps = []
    active_map = {}
    for line in input_str.splitlines():
        if 'map:' in line:
            if active_map:
                maps.append(active_map)
            active_map = {}
            continue
        destination, source, val_range = list(map(int, line.split(' ')))
        active_map[source] = (val_range, destination)
    if active_map:
        maps.append(active_map)
    return maps


def get_location(seed: int, maps) -> int:
    input_value = seed
    for mapping in maps:
        for source in mapping.keys():
            (val_range, destination) = mapping[source]
            if source <= input_value <= (source + val_range):
                input_value = destination - source + input_value
                break
    return input_value


def part_1(data_str: str) -> int:
    min_value = None
    seeds, *mapping = data_str.split('\n\n')
    seeds_list = list(map(int, seeds.split(': ')[1].strip().split(' ')))
    maps = populate_maps('\n'.join(mapping))
    for seed in seeds_list:
        value = get_location(seed, maps)
        if min_value is None:
            min_value = value
        else:
            min_value = min(value, min_value)

    return min_value


with open('input.in') as f:
    data = f.read()
    # 251346198
    print(part_1(data))
