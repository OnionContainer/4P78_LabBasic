from abc import ABC, abstractmethod
from typing import List, Set, Iterable
import numpy as np
from numpy.typing import NDArray
from numpy import int32
from scipy import signal
from sympy.physics.units import energy

from ColorfulGameOfLife.AbstractColorfulGameOfLife import AbstractColorfulGameOfLife, RuleSet, CellType
from Logger.Logger import Logger

class MyColorfulGameOfLife(AbstractColorfulGameOfLife):

    def setup_rule_set(self, rule_set: RuleSet):
        self._rule_set = rule_set
        self._history_key_matrix: List[NDArray[int32]] = []

        pass

    def iterate(self, iterations: int = 1):


        while True:
            if iterations == 0:
                break
            iterations -= 1

            if len(self._history_key_matrix) == 0:
                self._history_key_matrix.append(
                    np.random.randint(
                        0,
                        self._rule_set.get_cell_types_length() + 1,
                        size=(
                            int(Logger.i().read_hot_argument("game_width", 50)),
                            int(Logger.i().read_hot_argument("game_height", 60))
                        ),
                        dtype=int32)
                )
                continue

            # print(self._rule_set.outer_readonly_key2contribution_mapping_rules)
            prev = self.get_recent_history_key_matrix()
            contribution_matrix = np.take(
                self._rule_set.outer_readonly_key2contribution_mapping_rules,
                prev,
            )

            # print(contribution_matrix)



            energy_matrix:NDArray[int32] = signal.convolve2d(
                contribution_matrix,
                self._convolution_kernel,
                mode='same',
                boundary='wrap'
            )

            # print(energy_matrix)

            new_index_matrix = np.zeros(prev.shape, dtype=int32)

            for x in range(prev.shape[0]):
                for y in range(prev.shape[1]):
                    original = prev[x,y]
                    # print(type(self.get_recent_history_key_matrix()))
                    # print(type(energy_matrix))
                    # print(energy_matrix[x,y])
                    anergy = energy_matrix[x,y]
                    new_cell_condition = original

                    if original == 0:
                        for i in range(1, self._rule_set.get_cell_types_length() + 1):
                            cell_type = self._rule_set.get_cell_type(i)
                            if anergy in cell_type.get_generate_condition():
                                new_cell_condition = i

                    if original != 0:
                        cell_type = self._rule_set.get_cell_type(int(original))
                        if anergy in cell_type.get_death_condition():
                            new_cell_condition = 0

                    new_index_matrix[x,y] = new_cell_condition
                    # print(f"{x},{y}:{original}")

            self._history_key_matrix.append(new_index_matrix)
            
            
            
            # print(new_index_matrix)
            
            # Compute the number of differing cells
            differing_cells = np.sum(prev != new_index_matrix)
            portion_difference = differing_cells / (prev.shape[0] * prev.shape[1])
            self._difference_history.append(portion_difference)
            # print(f"Number of differing cells: {differing_cells}")


        pass

    def get_history_length(self):
        return len(self._history_key_matrix)

    def get_recent_history_key_matrix(self):
        return self._history_key_matrix[-1]

    def get_recent_difference(self):
        if len(self._difference_history) == 0:
            return 0
        return self._difference_history[-1]

    def get_difference_history(self):
        return self._difference_history

    def __init__(self):
        super().__init__()
        self._difference_history:List[float] = []

r = RuleSet()
r.add_cell_type(CellType(
    generate_condition={83},
    death_condition={80,81,84,85,86,87,88},
    contribution=11
))

# print(r.get_cell_types_length())

g = MyColorfulGameOfLife()
g.setup_rule_set(r)
g.iterate(200)
# print(g.get_recent_history_key_matrix())