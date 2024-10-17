
SAMPLE = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''


def get_maze_with_coords(input_str: str) -> tuple[int, int, list[[str]]]:
    maze = []
    for line in input_str.splitlines():
        maze.append(list(line))
    return len(maze), len(maze[0]), maze


def print_maze(maze: list[list[str]], visited_points: set[int, int], max_x: int, max_y: int) -> None:

    for y in range(max_y):
        active = ''
        for x in range(max_x):
            if (y, x) in visited_points:
                active += 'o'
            else:
                active += maze[y][x]
        print(active)


def get_start_position(maze: list[list[str]]) -> tuple[int, int]:

    for y, row in enumerate(maze):
        for x, value in enumerate(row):
            if value == 'S':
                return y, x

def traverse(
        maze: list[list[str]],
        max_y: int,
        max_x: int,
        y: int,
        x: int,
        visited: set,
        current_steps: int,
        allowed_steps: int,
        memo: set[tuple[int, int, int]],
) -> int:
    if x < 0 or y < 0 or y >= max_y or x >= max_x or maze[y][x] == '#':
        return len(visited)

    if current_steps == allowed_steps:
        visited.add((y, x))
        return len(visited)

    if (current_steps, y, x) in memo:
        return len(visited)
    memo.add((current_steps, y, x))

    for y_step, x_step in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        new_y = y + y_step
        new_x = x + x_step
        if new_x < 0 or new_y < 0 or new_y >= max_y or new_x >= max_x or maze[new_y][new_x] == '#':
            new_y -= y_step
            new_x -= x_step
            # visited.add((new_y, new_x))
            continue
        else:
            traverse(maze, max_y, max_x, new_y, new_x, visited, current_steps + 1, allowed_steps, memo)


def part_1(input_str: str) -> int:
    max_y, max_x, maze = get_maze_with_coords(input_str)
    start_y, start_x = get_start_position(maze)
    endpoints = set()
    traverse(maze, max_y, max_x, start_y, start_x, endpoints, 0, 64, set())
    return len(endpoints)


with open('input.in') as input_file:
    data = input_file.read()
    # 3542
    print(part_1(data))
