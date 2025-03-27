"""
A ColorfulGameOfLife object can take a rule set and compute its iterations.
"""
from abc import ABC, abstractmethod
from typing import List, Set, Iterable
import numpy as np
from numpy.typing import NDArray
from numpy import int32


class CellType:
    def __init__(self, generate_condition:Set[int], death_condition:Set[int], contribution:int):
        """
        :param generate_condition: if surrounding energy is in this list, cell will be generated from empty grid
        :param death_condition: if surrounding energy is in this list, cell will die
        :param contribution: how much energy this cell contribute to the surrounding cells
        """
        self._generate_condition = generate_condition
        self._death_condition = death_condition
        self._contribution = contribution

    def get_generate_condition(self)->Iterable:
        return tuple(self._generate_condition)

    def get_death_condition(self)->Iterable:
        return tuple(self._death_condition)

    def get_contribution(self)->int:
        return self._contribution

class RuleSet:

    def __init__(self):
        # self.outer_readonly_energy2key_mapping_rules = None
        self.outer_readonly_key2contribution_mapping_rules = None
        # self._direct_iteration_mapping_rules = None
        self._convolution_kernel = np.ones((3, 3), dtype=int)
        self._convolution_kernel[1,1] = 0
        self._size = (100,100)#hot argument
        self._cell_type_collection:List[CellType] = []

        # self.add_cell_type(CellType(
        #     generate_condition=set(),
        #     death_condition={1,4,5,6,7,8},
        #     contribution=10
        # ))
        pass


    def add_cell_type(self, cell_type:CellType):
        self._cell_type_collection.append(cell_type)
        self.reset_mapping_rules()
        pass

    def reset_mapping_rules(self):
        self.outer_readonly_key2contribution_mapping_rules = np.full(self.get_cell_types_length() + 1, 10, dtype=int)
        
        for i in range(1, self.get_cell_types_length() + 1):
            self.outer_readonly_key2contribution_mapping_rules[i] = self.get_cell_type(i).get_contribution()

    def get_cell_type(self, index:int):
        return self._cell_type_collection[index - 1]

    def get_cell_types_length(self):
        return len(self._cell_type_collection)


class AbstractColorfulGameOfLife(ABC):
    def __init__(self):
        self._history_key_matrix:List[NDArray[int32]] = []
        self._rule_set:RuleSet|None = None
        self._convolution_kernel = np.ones((3, 3), dtype=int)
        self._convolution_kernel[1,1] = 0

    @abstractmethod
    def setup_rule_set(self, rule_set:RuleSet):
        """
        reset rule set. Notice: this action will remove all previous record of this game object
        :param rule_set: The new rule set for this game object
        :return:
        """
        pass

    @abstractmethod
    def iterate(self, iterations:int=1):
        """
        iterate using the current rule set
        if there is no history frame, this will automatically generate a randomized initial state
        :param iterations: how many iterations to perform
        :return:
        """
        pass