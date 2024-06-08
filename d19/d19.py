
import math

SAMPLE_INPUT = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''


def parse_workflow_entry(input_str: str):
    start_idx = input_str.index('{')
    workflow_name = input_str[:start_idx]
    actions_list = []
    for action in input_str[start_idx + 1: -1].split(','):
        if ':' in action:
            condition, output = action.split(':')
            actions_list.append((condition[0], condition[1], int(condition[2:]), output))
        else:
            actions_list.append(action)

    return workflow_name, actions_list


def get_workflows(workflows_string: str) -> dict[str, list[tuple | str]]:
    workflows = {}
    for workflow in workflows_string.splitlines():
        name, actions = parse_workflow_entry(workflow)
        workflows[name] = actions
    return workflows


def transform_part(part_str: str) -> dict[str, int]:
    output_dict = {}
    for value in part_str[1:-1].split(','):
        part_type, val = value.split('=')
        output_dict[part_type] = int(val)
    return output_dict


def get_parts(part_str: str) -> list[dict]:
    output = []
    for part in part_str.splitlines():
        output.append(transform_part(part))
    return output


def get_part_status(part, workflow, workflows):
    for action in workflow:
        if isinstance(action, str):
            if action in 'AR':
                return action
            return get_part_status(part, workflows[action], workflows)
        else:
            threshold_variable, op, value, destination = action
            if (op == '>' and part[threshold_variable] > value) or (op == '<' and part[threshold_variable] < value):
                if destination in 'AR':
                    return destination
                return get_part_status(part, workflows[destination], workflows)


def calculate_allowed_ranges__part_2(action, part):
    if action == 'R':
        return 0
    return math.prod((high-low + 1) for low, high in part.values())


def get_part_status__part_2(part, workflow, workflows):
    output_value = 0
    active_part = part
    for action in workflow:
        if isinstance(action, str):
            if action in 'AR':
                output_value = output_value + calculate_allowed_ranges__part_2(action, active_part)
            else:
                output_value = output_value + get_part_status__part_2(active_part, workflows[action], workflows)
        else:
            threshold_variable, op, value, destination = action
            low, high = active_part[threshold_variable]
            next_workflow_part = active_part.copy()
            next_action_part = active_part.copy()
            # Made a big blunder here. Instead of taking low,high, I was setting low=1 and high=4000
            # After fixing this, we need to check if the new ranges are valid.
            if op == '>':
                next_workflow_part[threshold_variable] = (value + 1, high)
                next_action_part[threshold_variable] = (low, value)
            else:
                next_workflow_part[threshold_variable] = (low, value - 1)
                next_action_part[threshold_variable] = (value, high)
            if next_workflow_part[threshold_variable][0] <= next_workflow_part[threshold_variable][1]:
                if destination in 'AR':
                    output_value = output_value + calculate_allowed_ranges__part_2(destination, next_workflow_part)
                else:
                    output_value += get_part_status__part_2(next_workflow_part, workflows[destination], workflows)
            if next_action_part[threshold_variable][0] <= next_action_part[threshold_variable][1]:
                active_part = next_action_part
            else:
                break
    return output_value


def part_1(input_str):
    workflows, parts = input_str.split('\n\n')
    workflows = get_workflows(workflows)
    parts = get_parts(parts)
    output_sum = 0
    for part in parts:
        output = get_part_status(part, workflows['in'], workflows)
        if output == 'A':
            output_sum += sum(part.values())
    return output_sum


def part_2(input_str):
    workflows, parts = input_str.split('\n\n')
    workflows = get_workflows(workflows)
    initial_part = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    return get_part_status__part_2(initial_part, workflows['in'], workflows)


with open('input.in') as f:
    data = f.read()
    # 397134
    # 127517902575337
    print(part_1(data))
    print(part_2(data))
