#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import time

from solver_external import solver as solver_ext
from solver_greedy import solver as solver_gre
from solver_dynamic import solver as solver_dyn

Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def _data_collector(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(
            Item(
                i-1, # Index
                int(parts[0]), # Value  
                int(parts[1]), # Weight
                int(parts[0])/int(parts[1]), # Density
            )
        )


    return capacity, items


def _anwser_formater(obj: int, x_values: list) -> str:
    output_data = str(int(obj)) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, x_values))
    return output_data

def solve_it(input_data: str, kind_solver: str = "dynamic") -> str:
    start = time.time()
    # Read data
    capacity, items = _data_collector(input_data)
    
    # Resolve problem
    if kind_solver=="greedy":
        obj, x_values = solver_gre(capacity, items)
    if kind_solver=="dynamic":
        obj, x_values = solver_dyn(capacity, items)
    if kind_solver=="external":
        obj, x_values = solver_ext(capacity, items)

    # Format anwser
    anwser =  _anwser_formater(obj, x_values)
    end = time.time()
    # print(f"Time cto find solution: {end-start}s")
    return anwser


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        
        # Solve by greedy
        print("Greedy", solve_it(input_data, kind_solver='greedy'))

        # Solve by External solver
        print("External", solve_it(input_data, kind_solver='external'))

        # Solve by Dynamic programming
        print("Dynamic", solve_it(input_data, kind_solver='dynamic'))
        # print(solve_it(input_data, kind_solver='dynamic'))



    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

