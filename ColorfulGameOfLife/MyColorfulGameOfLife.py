from abc import ABC, abstractmethod
from typing import List, Set, Iterable
import numpy as np
from numpy.typing import NDArray
from numpy import int32
from scipy import signal
from sympy.physics.units import energy
import time

from ColorfulGameOfLife.AbstractColorfulGameOfLife import AbstractColorfulGameOfLife, RuleSet, CellType
from Logger.Logger import Logger, hot
from GUI.MyQt.MyQtTextColBoxLayout import say

def check_mapping_facts(prev: np.ndarray, anergy: np.ndarray, after: np.ndarray, rule_set: RuleSet = None):
    text = {}
    for x in range(prev.shape[0]):
        for y in range(prev.shape[1]):
            p = prev[x, y]
            a = anergy[x, y]
            a_after = after[x, y]


            t = f"cell {p}({a}) -> {a_after}"
            if t not in text:
                text[t] = 1
            else:
                text[t] += 1
    for key, value in text.items():
        print(f"{key}({value})")


class MyColorfulGameOfLife:

    def setup_rule_set(self, rule_set: RuleSet):
        self._rule_set = rule_set
        self._history_key_matrix: List[NDArray[int32]] = []

        pass

    #implement next frame calculation with conditions
    def energy_matrix_to_next_frame_vanilla(self, prev: np.ndarray, energy_matrix:np.ndarray)->np.ndarray:
        new_index_matrix = np.zeros(prev.shape, dtype=int32)

        # Iterate over each cell to determine its new state based on energy and ruleset conditions.
        for x in range(prev.shape[0]):
            for y in range(prev.shape[1]):
                original = prev[x, y]
                anergy = energy_matrix[x, y]
                new_cell_condition = original


                if original == 0:
                    for i in range(1, self._rule_set.get_cell_types_length() + 1):
                        # print(f"checking cell type:{i}")
                        cell = self._rule_set.get_cell_type(i)
                        if anergy in cell.get_generate_condition():
                            new_cell_condition = i
                            #spawn report:
                            # print(f"spawn at {x},{y}: {original}({anergy})->{i}")
                            break

                if original != 0:
                    cell = self._rule_set.get_cell_type(int(original))
                    if anergy in cell.get_death_condition():
                        new_cell_condition = 0

                new_index_matrix[x, y] = new_cell_condition

        return new_index_matrix

    #implement next frame calculation with np.take
    def energy_matrix_to_next_frame_chocolate(self, prev:np.ndarray, energy_matrix:np.ndarray)->np.ndarray:

        spaced_energy_matrix = energy_matrix * (
                self._rule_set.get_cell_types_length()+1
        )
        spaced_energy_matrix += prev
        return np.take(self._rule_set._energy_last_frame2key_mapping_rules, spaced_energy_matrix)

    def iterate(self, iterations: int = 1):
        while True:
            if iterations == 0:
                break
            iterations -= 1

            # Initialize the first random key matrix if there is no prior history available.
            if len(self._history_key_matrix) == 0:
                self._history_key_matrix.append(
                    np.random.randint(
                        0,
                        self._rule_set.get_cell_types_length() + 1,
                        size=(
                            self._game_size[0],
                            self._game_size[1]
                        ),
                        dtype=int32)
                )
                continue

            prev = self.get_recent_history_key_matrix()
            # Map each cell's current state to a contribution value using the ruleset.
            contribution_matrix = np.take(
                self._rule_set._key2energy_mapping_rules,
                prev,
            )




            # Calculate the energy matrix by convolving the contribution matrix with the convolution kernel.
            # This represents the sum of contributions from neighboring cells for game state updates.
            energy_matrix:NDArray[int32] = signal.convolve2d(
                contribution_matrix,
                self._convolution_kernel,
                mode='same',
                boundary='wrap'
            )


            start_time_vanilla = time.time()
            next_frame = self.energy_matrix_to_next_frame_vanilla(prev, energy_matrix)
            end_time_vanilla = time.time()
            msg1 = f"Runtime for energy_matrix_to_next_frame_vanilla: {end_time_vanilla - start_time_vanilla:.6f} seconds"

            start_time_chocolate = time.time()
            compare_index_matrix = self.energy_matrix_to_next_frame_chocolate(prev, energy_matrix)
            end_time_chocolate = time.time()
            msg2 = f"Runtime for energy_matrix_to_next_frame_chocolate: {end_time_chocolate - start_time_chocolate:.6f} seconds"

            say("vanilla", msg1)
            say("chocolate", msg2)
            # next_frame = self.energy_matrix_to_next_frame_chocolate(prev, energy_matrix)
            # comp = self.energy_matrix_to_next_frame_vanilla(prev, energy_matrix)
            # say("Error of the new iterating method", f"difference: {np.sum(comp != next_frame)}")

            # check_mapping_facts(prev, energy_matrix, next_frame)

            # print("Top left 5x5 of prev:")
            # print(prev[:5, :5])
            # print("Top left 5x5 of next_frame(chocolate):")
            # print(next_frame[:5, :5])
            # print("Top left 5x5 of comp(vanilla):")
            # print(comp[:5, :5])
            
            


            
            


            self._history_key_matrix.append(next_frame)
            

            
            # Compute the number of differing cells
            # Compute the number of differing cells and track the proportion of changes between iterations.
            differing_cells = np.sum(prev != next_frame)
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

    def get_game_size(self):
        return self._game_size

    def get_difference_history(self):
        return self._difference_history

    def __init__(self):
        super().__init__()
        self._history_key_matrix: List[NDArray[int32]] = []
        self._rule_set: RuleSet | None = None
        self._convolution_kernel = np.ones((3, 3), dtype=int)
        self._convolution_kernel[1, 1] = 0
        self._game_size = (
            int(hot("game_width", 50)),
            int(hot("game_height", 60))
        )
        self._difference_history:List[float] = []


# r = RuleSet()
# r.add_cell_type(CellType(
#     generate_condition={83},
#     death_condition={80,81,84,85,86,87,88},
#     contribution=11
# ))
#
# # print(r.get_cell_types_length())
#
# g = MyColorfulGameOfLife()
# g.setup_rule_set(r)
# g.iterate(200)
# print("what is happening here?")
# print(g.get_recent_history_key_matrix())