from wire import *
from op import *

class Gate:
    cost = 0
    def __init__(self, label, op, inputs):
        self.label = label
        self.op = op
        self.inputs = inputs
        self.input_wires = []
        self.output_wires = []
        self.op2 = None
        self.op3 = None

def print_all_gates(gates):
    for gate in gates:
        print(f"{gate.label}: {gate.op}({gate.inputs})")

def print_gate(gate):
    print(f"GATE: {gate.label}")
    print(f"\t{gate.op.op}({gate.inputs})")
    print(f"\tINPUT WIRES: {len(gate.input_wires)}")
    print(f"\tOUTPUT WIRES: {len(gate.output_wires)}\n")

def create_empty_gate():
    return Gate('empty',OP('DFF','',0,[-0.01,-0.01,-0.01,-0.01]),[])