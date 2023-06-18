import numpy as np
np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
c = np.array([-3, -5, 0])

A = np.array([
    [1,0,1],
    [0,2,0],
    [3,2,0]
])

b = np.array([4,12,18])

def run_simplex(a,b,c):

    pass

def r_simplex(c, A, b):

    # Create the initial table
    num_rows, num_cols = A.shape
    table = np.zeros((num_rows + 1, num_cols + len(b) + 1))

    table[0, :num_cols] = c
    table[1:, :num_cols] = A
    table[1:, -1] = b

    print("Table:")
    print(table)  # Just for testing

    # Perform simplex algorithm
    basic_vars = table[1:, -1]  # Extract basic variables

    # print("Basic variables:")
    # print(basic_vars)  # Just for testing

    print("Table after removing objective row and solution column:")
    # print(table)  # Just for testing

    # Making slack variables 1
    print("Making slack variables 1")
    for i in range(len(basic_vars)):
        table[i + 1, num_cols + i] = 1
    print(table)

    # Making a loop to make the objective row 0
    not_slack_zeroes = True
    cc = 0
    while not_slack_zeroes:

        print(f"\n ---- ITERATION {cc+1} ----")

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

        # Making pivot row 1 (sometimes dividing or multiplying is required)
        print("\ntable pv_row: ", table[pivot_row+1])
        table[pivot_row + 1] = table[pivot_row + 1] / table[pivot_row + 1][min_index]

        

        for i in range(len(table)):
            if i == pivot_row + 1:
                continue
            k = -1 * table[i][min_index]
            print(f"k: {k}")
            # print(f"Multiplicando: {table[i]} + ({k} * {table[pivot_row + 1]})")
            table[i] = table[i] + (k * table[pivot_row + 1])

            # print("\nResultado: ", table[i])
            
        print("\nTable after making pivot row 1:")
        print(table)  # Just for testing

        # Getting the last column
        last_col = []
        for i in range(len(table)):
            last_col.append(table[i][-1])
        # print("Last column:")
        # print(last_col)

        # Checking if its solved
        all_sum = 0
        for i in range(len(last_col)):
            if i == 0:
                pass
            else:
                all_sum = all_sum + last_col[i] * (-1*c[i-1])

        print(f"\nITERATION {cc+1} TABLE: ")
        print(table)
        print(f"\nZ:", last_col[0])
        print("\nsum: ", all_sum)

        if (all_sum == last_col[0]):
            not_slack_zeroes = False


r_simplex(c, A, b)