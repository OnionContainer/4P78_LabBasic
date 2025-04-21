from ColorfulGameOfLife.MyColorfulGameOfLife import MyColorfulGameOfLife
import numpy as np


class FitnessEvaluator:

    def __init__(self):
        pass

    def get_derivative_and_dverror(self, game_record:MyColorfulGameOfLife):
        try:
            difference_rate_history = game_record.get_difference_history()[100:500]
            derivative = np.diff(difference_rate_history)
            standard_error = np.std(derivative)
        except IndexError:
            derivative = 0.0
            standard_error = 0.0
        return derivative, standard_error

    def get_conceptual_fitness(self, game_record:MyColorfulGameOfLife):
        pass

    def get_overall_fitness(self, game_record:MyColorfulGameOfLife):
        pass

EVALUATOR = FitnessEvaluator()

if __name__ == "__main__":
    # Sample test cases for FitnessEvaluator.get_visual_fitness()

    class MockGameRecord:
        # Mocking MyColorfulGameOfLife for testing purposes
        def get_difference_history(self):
            return [0.0, 0.2, 0.5, 0.7, 0.6]

    # Initialize FitnessEvaluator
    evaluator = FitnessEvaluator()

    # Initialize mocked game record
    mock_record = MockGameRecord()

    # Test get_visual_fitness
    visual_fitness = evaluator.get_derivative_and_dverror(mock_record)
    print("Visual Fitness (Derivative):", visual_fitness)