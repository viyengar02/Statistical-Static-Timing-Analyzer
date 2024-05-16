import re
import pandas as pd
import time
import os
from op import *
from wire import *
from gate import *
from heuristics import *
from optHeuristics import *
        
def seek_cell_op(cell_library,op_name):
    current_op = []
    for cell in cell_library:
        if cell.op == op_name:
            current_op.append(cell)
    return current_op

def get_bench_file(filename,cell_library):
    with open(filename) as f:
        lines = [line.strip().split('\t') for line in f if not line.startswith('#') and line.strip()]

    primary_inputs = []
    primary_outputs = []
    gates = []
    
    for line in lines:
        line = line[0].replace(" ","")
        inputs = re.search('\((.*?)\)', line).group(1).split(",")
        current_op = None
        if line.startswith('INPUT'):
            primary_inputs.append(inputs[0])
            current_op = seek_cell_op(cell_library,"INPUT")
            gates.append(Gate(inputs[0],current_op[0],[]))
        elif line.startswith("OUTPUT"):
            primary_outputs.append(inputs[0])
        else:
            split_line = line.split('=')
            label = split_line[0]
            # Replace the text within parentheses (and the parentheses) with an empty string
            op_name = re.sub(r'\s*\(.*?\)', '', split_line[-1])
            current_op = seek_cell_op(cell_library,op_name)
            if current_op == None:
                current_op = seek_cell_op(cell_library,op_name)
            gates.append(Gate(label,current_op[0],inputs))
            
            for i in range(1,len(current_op)):
                exec(f"gates[-1].op{i+1} = current_op[{i}]")

    return primary_inputs, primary_outputs, gates


def get_time_file(filename):
    with open(filename) as f:
        lines = [line.strip().split('\t') for line in f if not line.startswith('#') and line.strip()]
    
    wires = []
    for line in lines:
        wire = Wire()
        wire.initialize(line)
        wires.append(wire)
    
    return wires

def get_cell_library(filename):
    # Create a list to hold the data for each gate
    gates_types = []

    # Open the file
    with open(filename, 'r') as file:
        # Initialize variables to hold data for the current gate
        current_gate = None
        current_op = None
        current_cost = None
        current_delay = None
        
        # Iterate through each line in the file
        for line in file:
            # Remove any leading or trailing whitespace
            line = line.strip()
            
            # Ignore comment lines starting with '#'
            if line.startswith('#') or line == '':
                continue
            
            # Check if the line contains gate data
            if line.startswith('GATE:'):
                # If there's a current gate data being processed, save it before starting a new gate
                if current_gate is not None:
                    gates_types.append(OP(current_gate,current_op,current_cost,current_delay))

                # Parse the gate name from the line
                current_gate = line.split(':')[1].strip()
                
            elif line.startswith('OP:'):
                # Parse the operation from the line
                current_op = line.split(':')[1].strip()
                
            elif line.startswith('COST:'):
                # Parse the cost from the line
                current_cost = float(line.split(':')[1].strip())
                
            elif line.startswith('DELAY:'):
                # Parse the delay from the line and convert it into a list of floats
                delay_values = line.split(':')[1].strip().split()
                current_delay = [float(value) for value in delay_values]

        # Append the last gate data being processed
        if current_gate is not None:
            gates_types.append(OP(current_gate,current_op,current_cost,current_delay))

        # Add DFF & Input gate
        gates_types.append(OP("DFF","DFF",0,[0,0,0,0]))
        gates_types.append(OP("INPUT","INPUT",0,[0,0,0,0]))

    return gates_types

def gather_files_by_extension(base_folder):
    # Lists to hold files with specific extensions
    time_files = []
    bench_files = []
    time_base_names = []

    # Iterate through the directory tree starting from the base folder
    for root, dirs, files in os.walk(base_folder):
        # Loop through each file in the current directory
        for file in files:
            # Construct the full file path
            file_path = os.path.join(root, file)
            
            # Check the file extension and add the file to the appropriate list
            if file.endswith('.time'):
                # Add the full file path to the time files list
                time_files.append(file_path)
                
                # Extract the base file name without extension or path and add to the list
                base_name = os.path.splitext(file)[0]
                time_base_names.append(base_name)
                
            elif file.endswith('.bench'):
                # Add the full file path to the bench files list
                bench_files.append(file_path)
    
    # Return the lists of time files, bench files, and time base names
    return time_files, bench_files, time_base_names

def run_ckt(ckt_name, primary_inputs, primary_outputs, gates, wires):
    start_time = time.perf_counter()
    g_copy = gates
    for gate in gates:
        input_wires = []
        output_wires = []
        for wire in wires:
            if wire.start_wire == gate.label:
                output_wires.append(wire)
            if wire.stop_wire == gate.label:
                input_wires.append(wire)
        gate.input_wires = input_wires
        gate.output_wires = output_wires

    ind = 0
    for gate in g_copy:
        if gate.label == primary_outputs[0]:
            ind = g_copy.index(gate)
            break

    initial_temperature = 1000
    cooling_rate = 0.95
    threshold = 0.001
    #critical_path, critical_path_cost, total_wire_delay = find_critical_path(gates[ind], gates)
    critical_path, critical_path_cost, total_wire_delay = simulated_annealing(gates[ind], gates, initial_temperature, cooling_rate, threshold)

    
    critical_path_string = ""
    for gate in critical_path:
        critical_path_string += gate.label + "->"
    critical_path_string = critical_path_string[0:-2]
    end_time = time.perf_counter()

    data = [ckt_name, critical_path_string, [total_wire_delay.a0,total_wire_delay.a1,total_wire_delay.a2,total_wire_delay.a3], critical_path_cost, (end_time-start_time)*1000]
    return data
""" 
if __name__ == "__main__":
    cell_library = get_cell_library("cell_library.time")
    data = []
    time_files, bench_files, ckt_names = gather_files_by_extension('BENCHMARKS')   
    wires = get_time_file("s27.time")
    primary_inputs, primary_outputs, gates = get_bench_file("s27.bench",cell_library)
    data.append(run_ckt("s27",primary_inputs,primary_outputs,gates, wires))
    df = pd.DataFrame(data, columns=["Benchmark", "Critical Path", "Critical Path Delay", "Cost", "Run Time (ms)"])
    df.to_csv('results.csv', index = False)
"""

if __name__ == "__main__":
    cell_library = get_cell_library("cell_library.time")

    time_files, bench_files, ckt_names = gather_files_by_extension('BENCHMARKS')   

    data = []

    i = 0
    
    for i in [9,11,12]:
        wires = get_time_file(time_files[i])
        primary_inputs, primary_outputs, gates = get_bench_file(bench_files[i],cell_library)
        data.append(run_ckt(ckt_names[i],primary_inputs,primary_outputs,gates,wires))

    df = pd.DataFrame(data, columns=["Benchmark", "Critical Path", "Critical Path Delay", "Cost", "Run Time (ms)"])
    df.to_csv('results.csv', index = False)  

    wires = get_time_file("s27.time")
    primary_inputs, primary_outputs, gates = get_bench_file("s27.bench",cell_library)
    data.append(run_ckt("s27",primary_inputs,primary_outputs,gates, wires))
    df = pd.DataFrame(data, columns=["Benchmark", "Critical Path", "Critical Path Delay", "Cost", "Run Time (ms)"])
    df.to_csv('results.csv', index = False) 





    