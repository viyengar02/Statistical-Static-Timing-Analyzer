import re
import pandas as pd
import time
import os
from op import *
from wire import *
from gate import *
from heuristics import *

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
        elif line.startswith("OUTPUT"):
            primary_outputs.append(inputs[0])
        elif line.startswith('G'):
            split_line = line.split('=')
            label = split_line[0]
            # Replace the text within parentheses (and the parentheses) with an empty string
            op_name = re.sub(r'\s*\(.*?\)', '', split_line[-1])
            for cell in cell_library:
                if cell.op == op_name:
                    current_op = cell
                    break

            gates.append(Gate(label,current_op,inputs))

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
    gates = []

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
                    gates.append(OP(current_gate,current_op,current_cost,current_delay))

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
            gates.append(OP(current_gate,current_op,current_cost,current_delay))

        # Add DFF gate
        gates.append(OP("DFF","DFF",0,[0,0,0,0]))

    return gates

def gather_files_by_extension(base_folder):
    # Lists to hold files with specific extensions
    time_files = []
    bench_files = []

    # Iterate through the directory tree starting from the base folder
    for root, dirs, files in os.walk(base_folder):
        # Loop through each file in the current directory
        for file in files:
            # Construct the full file path
            file_path = os.path.join(root, file)
            
            # Check the file extension and add the file to the appropriate list
            if file.endswith('.time'):
                time_files.append(file_path)
            elif file.endswith('.bench'):
                bench_files.append(file_path)
    
    # Return the lists of time and bench files
    return time_files, bench_files

def run_ckt(primary_inputs, primary_outputs, gates):
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

    # print_gate(gates[75])
    ind = 0
    for gate in gates:
        if gate.label == primary_outputs[0]:
            ind = gates.index(gate)
            break
    start_time = time.time()
    critical_path, critical_path_cost, total_wire_delay = find_critical_path(gates[ind], gates)
    run_time = time.time() - start_time
    critical_path_string = "Input->"
    for gate in critical_path:
        if gate.label == "": continue
        critical_path_string += gate.label + "->"
    critical_path_string += "Output"

    data = ["Circuit", critical_path_string, [total_wire_delay.a0,total_wire_delay.a1,total_wire_delay.a2,total_wire_delay.a3], critical_path_cost, run_time]
    return data


if __name__ == "__main__":
    cell_library = get_cell_library("cell_library.time")

    time_files, bench_files = gather_files_by_extension('BENCHMARKS')   

    data = []
    
    for i in range(len(time_files)):
        wires = get_time_file(time_files[i])
        primary_inputs, primary_outputs, gates = get_bench_file(bench_files[i],cell_library)

    #wires = get_time_file("s27.time")
    #primary_inputs, primary_outputs, gates = get_bench_file("s27.bench",cell_library)
        data.append(run_ckt(primary_inputs,primary_outputs,gates))

    df = pd.DataFrame(data, columns=["Benchmark", "Critical Path", "Critical Path Delay", "Cost", "Run Time"])
    df.to_csv('results.csv', index = True) 
    