import cellMath

def runSSTA():
    return 0


#gotta edit this one to make some fuckin sense
def find_critical_path(output_wire):
    critical_path = []
    critical_path_cost = 0
    
    
    # Recursive function to traverse the circuit backward
    def traverse_circuit(wire):
        nonlocal critical_path, critical_path_cost
        
        # Find the gate connected to this wire
        gate = find_gate_by_output_wire(wire)
        
        # Add the gate to the critical path
        critical_path.insert(0,gate)
        critical_path_cost += gate.cost
        
        # Base case: If the gate has no inputs, return
        if not gate.inputs:
            return
        
        # Calculate the delay with each input gate and choose the max delay
        max_delay_wire = None
        max_delay = -float('inf')
        for input_gate in gate.inputs:
            delay_wire = cellMath.max_Obj(input_gate, gate)
            if delay_wire.a[0] > max_delay:
                max_delay = delay_wire.a[0]
                max_delay_wire = delay_wire
        
        # Recursively traverse the circuit with the input wire
        traverse_circuit(max_delay_wire)
    
    # Start traversing the circuit from the output wire
    traverse_circuit(output_wire)
    
    return critical_path, critical_path_cost
