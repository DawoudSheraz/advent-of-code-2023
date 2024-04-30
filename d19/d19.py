
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


with open('input.in') as f:
    data = f.read()
    # 397134
    print(part_1(data))
