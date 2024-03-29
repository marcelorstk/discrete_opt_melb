#!/usr/bin/python
# -*- coding: utf-8 -*-

from solver_external import solver as solver_ext

def _data_collector(input_data: str) -> tuple:
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    
    return edges, edge_count, node_count
    

def solve_it(input_data, kind_solver="external"):
    # Read data
    edges, edge_count, node_count = _data_collector(input_data)

    # Resolve problem
    if kind_solver=="external":
        colors = solver_ext(edges, node_count)

    # prepare the solution in the specified output format
    output_data = str(max(colors)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, colors))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

