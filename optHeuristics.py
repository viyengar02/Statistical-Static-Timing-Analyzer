import random
import cellMath
from math import sqrt, exp

from wire import *
from gate import *
rec_counter = 0
def add_delays_wire_gate(w, g):
    w.a0 = w.a0 + g.op.a0
    w.a1 = w.a1 + g.op.a1
    w.a2 = w.a2 + g.op.a2
    w.a3 = sqrt((w.a3)**2 + (g.op.a3)**2)
    return w

def add_delay_w_w(w1, w2):
    w1.a0 = w1.a0 + w2.a0
    w1.a1 = w1.a1 + w2.a1
    w1.a2 = w1.a2 + w2.a2
    w1.a3 = sqrt((w1.a3)**2 + (w2.a3)**2)

def set_inputs(curr_gate, gates):
    gate_inp_lst = []
    for gate in gates:
        for st in curr_gate.inputs:
            if gate.label == st:
                gate_inp_lst.append(gate)
    return gate_inp_lst

def traverse_circuit(curr_gate, gates, critical_path, critical_path_cost, total_wire_delay):
    global rec_counter
    rec_counter +=1
    delay_wire = Wire()
    
    # Add the gate to the critical path
    critical_path.insert(0, curr_gate)
    critical_path_cost += curr_gate.op.cost
    
    # Base case: If the gate has no inputs, return
    if not curr_gate.inputs  or rec_counter>900:
        return critical_path_cost
    
    # Calculate the delay with each input gate and choose the max delay
    gate_inp_lst = set_inputs(curr_gate, gates)
    
    max_delay_gate = create_empty_gate()

    for input_gate in gate_inp_lst:
        if input_gate.op.op == "INPUT":
            if max_delay_gate in critical_path:
                critical_path_cost = 9999
                return
            else:
                max_delay_gate = input_gate
                break
        if input_gate.op.a[0] > max_delay_gate.op.a[0]:
            max_delay_gate = input_gate
                
        if len(max_delay_gate.input_wires) == 0:
            max_delay_gate.input_wires.append(Wire())
        if len(curr_gate.input_wires) == 0:
            curr_gate.input_wires.append(Wire())
        
        gate_inp_lst = set_inputs(max_delay_gate, gates)
        second_tier_delay_gate = create_empty_gate()
        for input in gate_inp_lst:
            if input.op.a[0] >= second_tier_delay_gate.op.a[0]:
                second_tier_delay_gate = input
        
        a = add_delays_wire_gate(second_tier_delay_gate.output_wires[0], max_delay_gate)
        b = add_delays_wire_gate(max_delay_gate.output_wires[0], curr_gate)
        
        delay_wire = cellMath.max_Obj(a, b)
        
    add_delay_w_w(total_wire_delay, delay_wire)
    return traverse_circuit(max_delay_gate, gates, critical_path, critical_path_cost, total_wire_delay)

def find_critical_path(output_gate, gates):
    critical_path = []
    critical_path_cost = 0
    total_wire_delay = Wire()
    critical_path_cost = traverse_circuit(output_gate, gates, critical_path, critical_path_cost, total_wire_delay)
    return critical_path, critical_path_cost, total_wire_delay

def acceptance_probability(delta_cost, temperature):
    return exp(-delta_cost / temperature)

def termination_condition(temperature, threshold):
    return temperature < threshold

def simulated_annealing(output_gate, gates, initial_temperature, cooling_rate, threshold):
    # Initialize the current state
    current_gate = output_gate
    current_path, current_path_cost, current_total_delay = find_critical_path(output_gate, gates)
    
    # Initialize the best state found so far
    best_path = current_path[:]
    best_path_cost = current_path_cost
    best_total_delay = current_total_delay
    
    temperature = initial_temperature
    while not termination_condition(temperature, threshold):
        random_gate = random.choice(gates)
        
        # Save the current operation
        current_op = random_gate.op
        
        # Flip to a different model
        if(random_gate.op2!=None and random_gate.op3!=None):
            random_gate.op = random.choice([random_gate.op, random_gate.op2, random_gate.op3])

        # Recalculate the critical path and cost
        new_path, new_path_cost, new_total_delay = find_critical_path(output_gate, gates)
        
        # Calculate the delta cost
        delta_cost = new_path_cost - current_path_cost
        
        # Update the current state if the new solution is accepted
        if delta_cost < 0 or random.random() < acceptance_probability(delta_cost, temperature):
            current_path = new_path
            current_path_cost = new_path_cost
            current_total_delay = new_total_delay
            
            # Check if this is the best path found so far
            if current_path_cost < best_path_cost:
                best_path = current_path[:]
                best_path_cost = current_path_cost
                best_total_delay = current_total_delay
        else:
            # Revert to the previous model
            random_gate.op = current_op
        
        # Cool down the temperature
        temperature *= cooling_rate

    return best_path, best_path_cost, best_total_delay