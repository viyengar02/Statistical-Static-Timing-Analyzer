class Gate:
    def __init__(self, label, op, inputs):
        self.label = label
        self.op = op
        self.inputs = inputs

def print_gates(gates):
    for gate in gates:
        print(f"{gate.label}: {gate.op}({gate.inputs})")