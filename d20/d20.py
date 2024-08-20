import math
from dataclasses import dataclass, field

SAMPLE_0 = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

SAMPLE_1 = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''


@dataclass
class Module:
    name: str
    type: str | None
    destination: list[str]
    current_pulse: bool = False  # for %
    low_pulse: int = 0
    high_pulse: int = 0
    states: dict[str, bool] = field(default_factory=dict)   # for &

    def __init__(self, input_str):
        name, destination = input_str.split('->')
        name = name.strip()
        destination = destination.strip()
        if name[0] in '&%' or 'broadcaster' in name:
            if 'broadcaster' in name:
                self.name = name
                self.type = 'broadcaster'
            else:
                self.name = name[1:]
                self.type = name[0]
        else:
            self.name = name
            self.type = None
        destination = destination.split(', ')
        self.destination = destination

    def add_input(self, value):
        self.states[value] = bool(0)

    def process_pulse(self, pulse, sender):
        if pulse:
            self.high_pulse += 1
        else:
            self.low_pulse += 1
        if self.type == '&':
            self.states[sender] = pulse
            if all(self.states.values()):
                return 0, self.name
            else:
                return 1, self.name
        elif self.type == '%':
            if pulse:
                return None, None
            self.current_pulse = not self.current_pulse
            if self.current_pulse:
                return 1, self.name
            else:
                return 0, self.name
        elif self.type == 'broadcaster':
            if pulse:
                return 1, self.name
            else:
                return 0, self.name
        else:
            return None, self.name


def process_input(data: str):
    module_dict = {}

    for input_str in data.splitlines():
        module = Module(input_str)
        module.states = {}
        module_dict[module.name] = module

    # Add modules who do not sent to any other module
    missing_modules = []
    for name, module in module_dict.items():
        for destination in module.destination:
            if destination not in module_dict:
                missing_modules.append(f"{destination} ->")
    for module_str in missing_modules:
        module = Module(module_str)
        module.states = {}
        module_dict[module.name] = module

    for name, module in module_dict.items():
        if name == 'broadcaster':
            continue
        for destination in module.destination:
            if destination in module_dict:
                module_dict[destination].add_input(name)
    return module_dict


def bfs(
        modules: dict[str, Module],
        start: str,
        pulse: bool,
        counter: int = 0,
        p2: bool = False,
        first_pulse_counter: list[int] = []
):
    queue = [(start, pulse, None)]

    while queue:
        current_module, pulse, sender = queue.pop(0)
        if current_module not in modules:
            continue
        current_module_obj = modules[current_module]
        sent_pulse, _ = current_module_obj.process_pulse(pulse, sender)
        if sent_pulse is None:
            continue
        if current_module in ['ln', 'dr', 'zx', 'vn'] and sent_pulse and p2:
            # ln, dr, zx, vn
            # 4 modules providing input to kj which then inputs to rx
            # kj is &, so it needs high from inputs to send low to rx
            # LCM of when the modules send high first time gets the answer
            # todo: make this automated
            first_pulse_counter.append(counter)

        for destination in current_module_obj.destination:
            queue.append((destination, sent_pulse, current_module))
    return modules


def part_1(data: str):
    low, high = 0, 0
    modules = process_input(data)
    for _ in range(1000):
        modules = bfs(modules, 'broadcaster', False)
    for module in modules.values():
        low += module.low_pulse
        high += module.high_pulse
    return low * high


def part_2(data: str):
    modules = process_input(data)
    counter = 0
    first_pulse_counter = []
    while True:
        counter += 1
        modules = bfs(modules, 'broadcaster', False, counter, True, first_pulse_counter)
        if counter >= 6000:
            break

    return math.lcm(*first_pulse_counter)


with open('input.in', 'r') as f:
    data = f.read()
    # 949764474
    # 243221023462303
    print(part_1(data))
    print(part_2(data))
