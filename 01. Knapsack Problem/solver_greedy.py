from collections import namedtuple
from typing import Tuple

def solver(capacity: int, items: namedtuple) -> Tuple[int, list]:
    # Get x_values
    x_values = len(items)*[0]

    # Sort by density
    items = sorted(items, key=lambda x: x.density)

    # Iterate over density until capacity
    remain_capacity = capacity
    objective = 0
    for item in items:
        # New remain capacity
        _remain_capacity = remain_capacity - item.weight
        
        # Choose if we have capacity
        if _remain_capacity >= 0:
            x_values[item.index] = 1
            remain_capacity = _remain_capacity
            objective += item.value
        else:
            continue
 

    return objective, x_values