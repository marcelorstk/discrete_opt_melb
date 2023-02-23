import numpy as np

from collections import namedtuple
from typing import Tuple, List

def solver(capacity: int, items: namedtuple) -> Tuple[int, list]:
    # Sort by weight
    items = sorted(items, key=lambda x: x.weight, reverse=True)
    k_array = np.arange(0, capacity+1)

    # print(f"K: {capacity}")
    # print(f"N items: {len(items)}")

    v_matrix = _create_dynamic_table(items, k_array)    

    # Get objective
    objective = v_matrix[-1][-1]
    
    # Get items list
    x_values = _get_x_values(v_matrix, items)

    return objective, x_values

import time
def _create_dynamic_table(items: namedtuple, k_list: np.array) -> np.array:
    # items = sorted(items, key=lambda x: x.weight, reverse=False)
    v_matrix = np.zeros((len(items), len(k_list)), dtype=np.int32)
    start = time.time()
    for i, item in enumerate(items):
        # if i%100==0:
        #     print(f"Time to run 100: {time.time() - start}")
        #     start = time.time()
        
        old_row = v_matrix[i-1]
        if item.weight <= k_list[-1]:
            new_row = np.concatenate(
                [np.zeros(item.weight), v_matrix[i-1][:-item.weight] + item.value]
            )
        else:
            new_row = np.zeros(len(k_list))
        
        v_new = np.maximum(old_row, new_row)
        v_new = v_new.astype(np.int32)
        v_matrix[i] = v_new

    return v_matrix


def _get_x_values(v_matrix: List[list], items: namedtuple) -> list:
    items = items[::-1]
    selected_items = list()
    x_values = len(items)*[0]

    v_index = len(v_matrix[0]) - 1
    last_row, v_matrix = v_matrix[-1], v_matrix[:-1]
    last_val = last_row[v_index]
    item = items[0]
    for i in np.arange(1, len(items)):
        if i==0: continue

        row, v_matrix = v_matrix[-1], v_matrix[:-1]
        val = row[v_index]

        if val != last_val:
            x_values[item.index] = 1
            selected_items.append(item)
            v_index -= item.weight
            last_val = row[v_index]
        
        item = items[i]

    if last_val != 0:
        x_values[item.index] = 1

    return x_values