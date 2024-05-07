class Wire:
    start_wire = ''
    stop_wire = ''
    a0 = 0
    a1 = 0
    a2 = 0
    a3 = 0

    def __init__(self):
        pass

    def initialize(self, line):
        self.start_wire = line[0]
        self.stop_wire = line[1]
        self.a0 = float(line[2])
        self.a1 = float(line[3])
        self.a2 = float(line[4])
        self.a3 = float(line[5])

def print_all_wires(wires):
    for wire in wires:
        print_wire(wire)

def print_wire(wire):
    print(f"{wire.start_wire} {wire.stop_wire} {wire.a0} {wire.a1} {wire.a2} {wire.a3}")

def get_output_gate(wire, gates):
    for gate in gates:
        if gate.label == wire.stop_wire:
            return gate
        
def get_input_gate(wire, gates):
    for gate in gates:
        if gate.label == wire.start_wire:
            return gate