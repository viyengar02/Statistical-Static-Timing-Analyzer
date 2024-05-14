import cellMath
from math import sqrt, exp

from wire import *
from gate import *

import random

def add_delays_wire_gate(w, g):
    w.a0 = w.a0+g.op.a0
    w.a1 = w.a1+g.op.a1
    w.a2 = w.a2+g.op.a2
    w.a3 = sqrt((w.a3)**2+(g.op.a3)**2)
    return w
def add_delay_w_w(w1, w2):
    w1.a0 = w1.a0+w2.a0
    w1.a1 = w1.a1+w2.a1
    w1.a2 = w1.a2+w2.a2
    w1.a3 = sqrt((w1.a3)**2+(w2.a3)**2)

def acceptance_probability(delta_cost, temperature):
    return random.random() < exp(-delta_cost / temperature)

def termination_condition(temperature, threshold):
    return temperature < threshold

def traverse_circuit(output_gate):
    critical_path = []
    critical_path_cost = 0
    total_wire_delay = Wire()
    #edit line 36 so it calls gate.op instead of string.op. input_gate in curr_gate.inputs are strings
    def find_max_delay_gate(curr_gate):
        max_delay_gate = None
        max_delay = float('-inf')
        for input_gate in curr_gate.inputs:
            if input_gate.op.a[0] > max_delay:
                max_delay = input_gate.op.a[0]
                max_delay_gate = input_gate
        return max_delay_gate
    
    def calculate_delay_wire(input_gate, curr_gate):
        if not input_gate.input_wires:
            input_gate.input_wires.append(Wire())
        if not curr_gate.input_wires:
            curr_gate.input_wires.append(Wire())
        a = add_delays_wire_gate(input_gate.input_wires[0], input_gate)
        b = add_delays_wire_gate(curr_gate.input_wires[0], curr_gate)
        return cellMath.max_Obj(a, b)
    
    # Start traversing the circuit from the output gate
    current_gate = output_gate
    
    while current_gate is not None:
        # Add the gate to the critical path
        critical_path.append(current_gate)
        critical_path_cost += current_gate.op.cost
        
        # Base case: If the gate has no inputs, stop traversing
        if not current_gate.inputs:
            break
        
        # Find the gate with the maximum delay among inputs
        max_delay_gate = find_max_delay_gate(current_gate)
        
        # Calculate the delay wire between the input gate and the current gate
        delay_wire = calculate_delay_wire(max_delay_gate, current_gate)
        
        # Add the delay wire to the total wire delay
        add_delay_w_w(total_wire_delay, delay_wire)
        
        # Update the current gate for the next iteration
        current_gate = max_delay_gate
    
    return critical_path, critical_path_cost, total_wire_delay

def find_critical_path_opt(output_gate, gates, initial_temperature, cooling_rate, threshold):
    # Initialize the current state
    current_gate = output_gate
    current_path = [output_gate]
    current_path_cost = output_gate.op.cost
    
    # Initialize the best state found so far
    best_path = current_path[:]
    best_path_cost = current_path_cost
    
    # Start the simulated annealing loop
    temperature = initial_temperature
    while not termination_condition(temperature, threshold):
        # Pick a random gate
        random_gate = random.choice(gates)
        
        # Flip it to a different model
        random_gate.op = random.choice([random_gate.op1, random_gate.op2, random_gate.op3])
        
        # Recalculate the critical path and cost
        new_path, new_path_cost, _ = traverse_circuit(output_gate)
        
        # Calculate the delta cost
        delta_cost = new_path_cost - current_path_cost
        
        # Update the current state if the new solution is accepted
        if delta_cost < 0 or acceptance_probability(delta_cost, temperature):
            current_path = new_path
            current_path_cost = new_path_cost
            
            # Check if this is the best path found so far
            if current_path_cost < best_path_cost:
                best_path = current_path[:]
                best_path_cost = current_path_cost
        else:
            # Revert the gate to its previous model
            random_gate.op = current_gate.op
        
        # Cool down the temperature
        temperature *= cooling_rate
    
    return best_path, best_path_cost