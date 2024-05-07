import cellMath
from math import sqrt
from wire import *
from gate import *
def runSSTA():
    return 0

def add_delays_wire_gate(w, g):
    w.a[0] = w.a[0]+g.op.a[0]
    w.a[1] = w.a[1]+g.op.a[1]
    w.a[2] = w.a[2]+g.op.a[2]
    w.a[3] = sqrt((w.a[3])^2+(g.op.a[3])^2)
    return w
def add_delay_w_w(w1, w2):
    w1.a[0] = w1.a[0]+w2.a[0]
    w1.a[1] = w1.a[1]+w2.a[1]
    w1.a[2] = w1.a[2]+w2.a[2]
    w1.a[3] = sqrt((w1.a[3])^2+(w2.a[3])^2)


#gotta edit this one to make some fuckin sense
def find_critical_path(output_gate, gates):
    critical_path = []
    critical_path_cost = 0
    #init a blank wire obj
    total_wire_delay = Wire()
    
    # Recursive function to traverse the circuit backward
    def traverse_circuit(curr_gate):
        nonlocal critical_path, critical_path_cost
        
        # Find the gate connected to this wire
        
        # Add the gate to the critical path
        critical_path.insert(0,curr_gate)
        critical_path_cost += curr_gate.cost
        
        # Base case: If the gate has no inputs, return
        if not curr_gate.inputs:
            return
        
        # Calculate the delay with each input gate and choose the max delay
        max_delay_wire = None
        max_delay = -float('inf')
        gate_inp_lst = []
        #init a blank gate object 
        max_delay_gate = create_empty_gate()
        for gate in gates:
            for st in curr_gate.inputs:
                if gate.label == st:
                    gate_inp_lst.append(gate)
        for input_gate in gate_inp_lst:
            if input_gate.op.a[0] > max_delay_gate.op.a[0]:
                max_delay_gate = input_gate

            a = add_delays_wire_gate(input_gate.input_wires, input_gate)
            b = add_delays_wire_gate(curr_gate.input_wires, curr_gate)
            delay_wire = cellMath.max_Obj(a, b)
            
        
        # Recursively traverse the circuit with the input wire
        add_delay_w_w(total_wire_delay, delay_wire)
        traverse_circuit(max_delay_wire)
    
    # Start traversing the circuit from the output gate
    traverse_circuit(output_gate)
    
    return critical_path, critical_path_cost, total_wire_delay
