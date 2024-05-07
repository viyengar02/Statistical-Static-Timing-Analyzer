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

def print_all_gates(gates):
    for gate in gates:
        print(f"{gate.label}: {gate.op}({gate.inputs})")

def print_gate(gate):
    print(f"{gate.label}: {gate.op}({gate.inputs})")
    print(f"{gate.op.op}")
    print("INPUT WIRES:")
    for wire in gate.input_wires:
        print_wire(wire)
    print("OUTPUT WIRES:")
    for wire in gate.output_wires:
        print_wire(wire)

def create_empty_gate():
    return Gate('',OP('','',0,[0,0,0,0]),[])