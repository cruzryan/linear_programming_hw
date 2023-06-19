from abc import ABC

from approximation_method import ApproximationMethod
import numpy as np
import os 
import time 

def call_vogel(file_str):
    # Saving string as file.txt
    file = open("file.txt", "w")
    file.write(file_str)
    file.close()

    fs = open("file_solucion.txt", "w").close()

    # Syscall
    os.system("python ./transporte.py 2 file.txt")

    time.sleep(1.5)

    print("Reading file...")
    file = open("file_solucion.txt", "r")
    file_str = file.read()

    print("File readed: ", file_str)
    return {"result": file_str}


class VogelMethod(ApproximationMethod, ABC):

    def __init__(self, file):
        super().__init__(file=file)
        self.__add_diff_column()
        self.__add_diff_row()

    def solve(self) -> None:
        """
        Finds the minimum value based on the greatest diff in the supply
        column and the demand row
        """

        while super().has_rows_and_columns_left():
            self.__update_diff_row()
            self.__update_diff_column()
            self.choose_cost()
        self.writer.write_initial_solution(self.assign_table,
                                           demand=self.cost_table[self.demand_row, :-1],
                                           supply=self.cost_table[:-1, self.supply_column])
        self.writer.write_initial_cost(self.total_cost())
        self.improve()

    def __add_diff_column(self) -> None:
        """
        Adds a column filled with zeros for the lowest diff in each row
        """

        dfi_column = np.zeros((self.rows, 1))
        self.cost_table = np.append(self.cost_table, values=dfi_column, axis=1)

    def __add_diff_row(self) -> None:
        """
        Adds a row filled with zeros for the lowest diff in each column
        """

        dcj_row = np.zeros((1, self.columns + 1))
        self.cost_table = np.append(self.cost_table, values=dcj_row, axis=0)

    def __update_diff_column(self) -> None:
        """
        Calculates the lowest difference in each row based on the
        cost table & updates the biggest difference of them with its column
        """

        biggest_diff, biggest_col = -np.inf, -1
        consumers = np.transpose(self.cost_table[:self.demand_row, :self.supply_column])
        # for each column find the lowest difference in terms of cost
        for col, costs in enumerate(consumers):
            # flag deleted columns
            if col in self.deleted_cols:
                self.cost_table[self.rows][col] = -np.inf
                continue
            diff = self.minimum_diff(costs, omit=self.deleted_rows)
            if diff > biggest_diff:
                biggest_diff = diff
                biggest_col = col
            self.cost_table[self.rows][col] = diff
        # set the biggest diff and it's index in corner
        self.cost_table[self.rows][self.supply_column] = (biggest_diff, biggest_col)

    def __update_diff_row(self) -> None:
        """
        Calculates the lowest difference in each column based on the
        cost table & updates the biggest difference of them with its row
        """
        biggest_diff, biggest_row = -np.inf, -1
        suppliers = self.cost_table[:self.demand_row, :self.supply_column]
        # for each row find the lowest difference in terms of cost
        for row, costs in enumerate(suppliers):
            # flag deleted rows
            if row in self.deleted_rows:
                self.cost_table[row][self.columns] = -np.inf
                continue
            diff = self.minimum_diff(costs, omit=self.deleted_cols)
            if diff > biggest_diff:
                biggest_diff = diff
                biggest_row = row
            self.cost_table[row][self.columns] = diff
        # set the biggest diff and it's index in corner
        self.cost_table[self.demand_row][self.columns] = (biggest_diff, biggest_row)

    @staticmethod
    def minimum_diff(costs: np.ndarray, omit: set) -> int:
        """
        Given a np.ndarray of values, calculate
        second lowest - lowest (minimum difference)

        :param costs: values to calculate difference
        :param omit: indices of deleted rows or columns
        :return: integer the lowest difference number
        """

        # find diff between two lowest elements
        lowest, second_lowest = np.inf, np.inf
        for i, c in enumerate(costs):
            # don't use omitted rows or columns
            if i in omit:
                continue
            elif c < lowest:
                second_lowest = lowest
                lowest = c
            elif c < second_lowest:
                second_lowest = c
            else:
                continue
        # case in which there was only 1 element left
        if second_lowest == np.inf:
            return lowest
        else:
            return second_lowest - lowest

    def choose_cost(self) -> None:
        """
        Assigns a value depending on the demand or supply difference
        by finding which one of them it's the lowest
        """

        maximum_supply_diff, i = self.cost_table[self.demand_row][self.columns]
        maximum_demand_diff, j = self.cost_table[self.rows][self.supply_column]
        if maximum_supply_diff >= maximum_demand_diff:
            j = self.__minimum_index_in_row(i)
            self.assign(*self.best_value_at(i, j))
        else:
            i = self.__minimum_index_in_column(j)
            self.assign(*self.best_value_at(i, j))

    def __minimum_index_in_row(self, i: int) -> int:
        """
        Return the column index of the lowest
        cost available in a row
        :param i: row to find lowest cost
        :return: index of the column with lowest value
        """

        costs = self.cost_table[i][:self.supply_column]
        costs_left = np.delete(costs, list(self.deleted_cols))
        lowest_cost = np.min(costs_left)
        j = list(set(np.where(costs == lowest_cost)[0]) - self.deleted_cols)[0]
        return j

    def __minimum_index_in_column(self, j: int) -> int:
        """
        Return the row index of the lowest
        cost available in a column
        :param j: column to find lowest cost
        :return: index of the row with lowest value
        """

        costs = self.cost_table[:, j][:self.demand_row]
        costs_left = np.delete(costs, list(self.deleted_rows))
        lowest_cost = np.min(costs_left)
        i = list(set(np.where(costs == lowest_cost)[0]) - self.deleted_rows)[0]
        return i
