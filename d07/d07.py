
from collections import Counter

SAMPLE_INPUT = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

CHAR_MAPS = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}


class HANDS:
    FIVE_OF_KIND = 0
    FOUR_OF_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


def parse_input(input_list: list[str], part: int = 1) -> tuple[list[list[int]], list[int]]:
    cards, bids = [], []
    for line in input_list:
        card_str, bid = line.split(' ')
        card_list = [int(CHAR_MAPS[x]) if x in CHAR_MAPS else int(x) for x in card_str]
        if part == 2:
            card_list = [x if x != 11 else 1 for x in card_list]
        bid = int(bid)
        cards.append(card_list)
        bids.append(bid)
    return cards, bids


def determine_kind(card_list: list[int]) -> int:
    counter = Counter(card_list)
    counter_list = sorted(counter.values())
    if len(set(card_list)) == 1:
        return HANDS.FIVE_OF_KIND
    if counter_list == [1, 4]:
        return HANDS.FOUR_OF_KIND
    if counter_list == [2, 3]:
        return HANDS.FULL_HOUSE
    if counter_list == [1, 1, 3]:
        return HANDS.THREE_OF_KIND
    if counter_list == [1, 2, 2]:
        return HANDS.TWO_PAIR
    if counter_list == [1, 1, 1, 2]:
        return HANDS.ONE_PAIR
    return HANDS.HIGH_CARD


def determine_joker_based_kind(card_list: list[int]):
    counter = Counter(card_list)
    joker_count = counter.get(1, None)
    kind = determine_kind(card_list)

    if kind == HANDS.FOUR_OF_KIND and joker_count in [1, 4]:
        return HANDS.FIVE_OF_KIND
    if kind == HANDS.FULL_HOUSE and joker_count in [2, 3]:
        return HANDS.FIVE_OF_KIND
    if kind == HANDS.THREE_OF_KIND and joker_count in [1, 3]:
        return HANDS.FOUR_OF_KIND
    if kind == HANDS.TWO_PAIR:
        if joker_count == 1:
            return HANDS.FULL_HOUSE
        if joker_count == 2:
            return HANDS.FOUR_OF_KIND
    if kind == HANDS.ONE_PAIR and joker_count in [1, 2]:
        return HANDS.THREE_OF_KIND
    if kind == HANDS.HIGH_CARD and joker_count == 1:
        return HANDS.ONE_PAIR
    return kind


def get_same_kind_ranking_bid_output(
        card_rank_bid_list: list[tuple[int, int, list[int]]], active_rank: int
) -> tuple[int, int]:
    sum_value = 0
    active_list = sorted(card_rank_bid_list, key=lambda x: (x[2][0], x[2][1], x[2][2], x[2][3], x[2][4]), reverse=True)
    for item in active_list:
        sum_value += item[1] * active_rank
        active_rank -= 1
    return sum_value, active_rank


def process_hands(card_ranks_bids: list[tuple[int, int, list[int]]]) -> int:
    output = 0
    active_rank = len(card_ranks_bids)
    card_ranks_bids = sorted(card_ranks_bids, key=lambda x: x[0])
    active_list = []
    active_category = card_ranks_bids[0][0]
    for item in card_ranks_bids:
        if item[0] == active_category:
            active_list.append(item)
        else:
            sum_value, active_rank = get_same_kind_ranking_bid_output(active_list, active_rank)
            output += sum_value
            active_category = item[0]
            active_list = [item]

    if active_list:
        sum_value, active_rank = get_same_kind_ranking_bid_output(active_list, active_rank)
        output += sum_value
    return output


def part_1(input_str: str) -> int:
    input_data = input_str.split('\n')
    card_ranks_bids = []
    cards, bids = parse_input(input_data)

    for idx, card_list in enumerate(cards):
        hand_type = determine_kind(card_list)
        card_ranks_bids.append((hand_type, bids[idx], card_list))

    return process_hands(card_ranks_bids)


def part_2(input_str: str) -> int:
    input_data = input_str.split('\n')
    card_ranks_bids = []
    cards, bids = parse_input(input_data, part=2)
    for idx, card_list in enumerate(cards):
        hand_type = determine_joker_based_kind(card_list)
        card_ranks_bids.append((hand_type, bids[idx], card_list))

    return process_hands(card_ranks_bids)


with open('input.in') as f:
    data = f.read()
    # 250370104
    # 251735672

    # TODO: Improve the code, too many if-else
    print(part_1(data))
    print(part_2(data))
