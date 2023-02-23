from collections import namedtuple
from typing import Tuple

# External solver
from docplex.mp.model import Model

def solver(capacity: int, items: namedtuple) -> Tuple[int, list]:
    # Create model
    mdl = Model(name="knap_sack")
    
    # Binary variable
    x_values = {
        item.index: mdl.binary_var(name=f"item_{item.index}") for item in items
    }

    # Add constrain
    upper_b = mdl.add_constraint(
        sum(x_values[item.index] * item.weight for item in items) <= capacity
    )

    # Objective
    mdl.maximize(sum(x_values[item.index] * item.value for item in items))

    # Solve
    solve = mdl.solve()

    return solve.objective_value, [
        1 if i in solve.as_index_dict().keys() else 0 for i in range(len(items))
    ]