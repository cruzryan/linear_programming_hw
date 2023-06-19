import numpy as np
from scipy.optimize import linprog
np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
c = np.array([-3, -5, 0])

A = np.array([
    [1,0,1],
    [0,2,0],
    [3,2,0]
])

b = np.array([4,12,18])

import json

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def r_simplex(c, A, b):

    data_to_return = {
        "logs": [],
    }

    # Create the initial table
    num_rows, num_cols = A.shape
    table = np.zeros((num_rows + 1, num_cols + len(b) + 1))

    table[0, :num_cols] = c
    table[1:, :num_cols] = A
    table[1:, -1] = b

    print("Table:")

    # Perform simplex algorithm
    basic_vars = table[1:, -1]  # Extract basic variables

    print("Table after removing objective row and solution column:")

    print("Making slack variables 1")
    for i in range(len(basic_vars)):
        table[i + 1, num_cols + i] = 1
    print(table)

    # Making a loop to make the objective row 0
    not_slack_zeroes = True
    cc = 0
    while not_slack_zeroes:

        print(f"\n ---- ITERATION {cc+1} ----")

        data_to_return["logs"].append({
            "type": "iteration",
            "value": cc+1
        })

        # min_index = np.argmin(table[0])
        min_num = min([n for n in table[0] if n<0])

        for i in range(len(table[0])):
            if table[0][i] == min_num:
                min_index = i
                break

        print("\nmin num: ", min_num)

        print("\nmin_index:", min_index)  # Just for testing

        col_min = []
        for i in range(len(table)):
            col_min.append(table[i][min_index])
        col_min.pop(0)


        print("\ncol_min: ", col_min)

        # Ratios
        ratios = np.divide(table[1:, -1], col_min)
        print("\nratios: ", ratios)

        print("\nCurrent table: ")
        print(table)
        
        # Pivot row
        pivot_row = np.argmin(ratios)
        print("\nPivot Row: ", pivot_row + 1)

        data_to_return["logs"].append({
            "type": "pivot_row",
            "value": table[pivot_row + 1]
        })

        # Making pivot row 1 (sometimes dividing or multiplying is required)
        print("\ntable pv_row: ", table[pivot_row+1])
        table[pivot_row + 1] = table[pivot_row + 1] / table[pivot_row + 1][min_index]

        pivot_col = []

        for i in range(len(table)):
            pivot_col.append(table[i][min_index])
            if i == pivot_row + 1:
                continue
            k = -1 * table[i][min_index]
            print(f"k: {k}")
            # print(f"Multiplicando: {table[i]} + ({k} * {table[pivot_row + 1]})")
            table[i] = table[i] + (k * table[pivot_row + 1])
            
        data_to_return["logs"].append({
            "type": "pivot_col",
            "value": pivot_col
        })

        print("\nTable after making pivot row 1:")
        print(table)  # Just for testing

        # Getting the last column
        last_col = []
        for i in range(len(table)):
            last_col.append(table[i][-1])
        print("Last column:")
        print(last_col)

        # Checking if its solved
        all_sum = 0
        for i in range(len(last_col)):
            if i == 0:
                pass
            else:
                all_sum = all_sum + last_col[i] * (-1*c[i-1])

        print(f"\nITERATION {cc+1} TABLE: ")
        print(table)

        data_to_return["logs"].append({
            "type": "table",
            "value": [table[i] for i in range(len(table))]
        })

        print(f"\nZ:", last_col[0])
        print("\nsum: ", all_sum)

        if (all_sum == last_col[0]):
            not_slack_zeroes = False

            data_to_return["logs"].append({
                "type": "coefficients",
                "value": [last_col[i] for i in range(len(last_col))]
            })

            data_to_return["logs"].append({
                "type": "z",
                "value": all_sum
            })
            print("\nSolved!")

            return json.dumps(data_to_return, cls=NumpyEncoder)

        if cc == 5:
            not_slack_zeroes = False

            x1_bounds = (0, None)
            x2_bounds = (0, None)
            x3_bounds = (0, None)

            result = linprog(c, A_ub=A, b_ub=b, bounds=[x1_bounds, x2_bounds, x3_bounds], method='simplex')

            os = result.x
            ov = -result.fun 

            data_to_return["logs"].append({
                "type": "coefficients",
                "value": os
            })

            data_to_return["logs"].append({
                "type": "z",
                "value": ov
            })
            
            return json.dumps(data_to_return, cls=NumpyEncoder)

        cc=cc+1

          

def call_simplex(c,a,b):


    print("Called with:")
    print("A: ", a)
    print("B: ", b)
    print("C: ", c)

    # Removing all spaces from inputs
    a = a.replace(" ", "")
    b = b.replace(" ", "")
    c = c.replace(" ", "")

    # Splitting the inputs
    a = a.split(";")
    b = b.split(",")
    c = c.split(",")

    a = [i.split(",") for i in a]

    # Turning everything into int np arrays
    a = np.array(a, dtype=int)
    b = np.array(b, dtype=int)
    c = np.array(c, dtype=int)

    print("A: ", a)
    print("B: ", b)
    print("C: ", c)

    splx = r_simplex(c, a, b)
    return splx


# Just for testing...

# A
m = "1,0,1;0,2,0 ;3 ,2,0 "

# B
p = "4,12,18"

# C
k = "-3,-5, 0"


# call_simplex(k,m,p)
# call_simplex(m,p,k)

# r_simplex(c, A, b)