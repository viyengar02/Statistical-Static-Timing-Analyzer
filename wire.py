class Wire:
    def __init__(self, line):
        self.start_wire = line[0]
        self.stop_wire = line[1]
        self.a0 = line[2]
        self.a1 = line[3]
        self.a2 = line[4]
        self.a3 = line[5]

def print_wires(wires):
    for wire in wires:
        print(f"{wire.start_wire} {wire.stop_wire} {wire.a0} {wire.a1} {wire.a2} {wire.a3}")