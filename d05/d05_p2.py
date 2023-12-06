
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
        active_map[destination] = (val_range, source)
    if active_map:
        maps.append(active_map)
    return maps


def get_seed(location: int, maps) -> int:
    input_value = location
    for idx, mapping in enumerate(maps):
        for destination in mapping.keys():
            (val_range, source) = mapping[destination]
            if destination <= input_value <= (destination + val_range):
                input_value = source - destination + input_value
                break
    return input_value


def check_seed_presence(seed, seeds_list):
    for count in range(0, len(seeds_list), 2):
        seed_start, seed_range = seeds_list[count], seeds_list[count + 1]
        if seed_start <= seed < seed_start + seed_range:
            return True
    return False


def part_2(data_str: str, starting_location=0) -> int:
    seeds, *mapping = data_str.split('\n\n')
    seeds_list = list(map(int, seeds.split(': ')[1].strip().split(' ')))
    mapping_list = populate_maps('\n'.join(mapping))
    location = starting_location
    while True:
        seed_value = get_seed(location, mapping_list[::-1])
        print(seed_value, location)
        if check_seed_presence(seed_value, seeds_list):
            return location
        location += 1


with open('input.in') as f:
    data = f.read()
    # 72263011
    # TODO: Combine the files, and use overlapping range approach
    # https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    print(part_2(data, 72263010))

