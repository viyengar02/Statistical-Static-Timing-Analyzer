class Wire:
    def __init__(self, line):
        self.start_wire = line[0]
        self.stop_wire = line[1]
        self.a0 = line[2]
        self.a1 = line[3]
        self.a2 = line[4]
        self.a3 = line[5]


def get_bench_file():
    pass

def get_time_file(filename):
    with open(filename) as f:
        lines = [line.strip().split(" ") for line in f if not line.startswith('#')]
    
    wires = []
    for line in lines:
        wires.append(Wire(line))
    
    return wires

if __name__ == "__main__":
    get_time_file()