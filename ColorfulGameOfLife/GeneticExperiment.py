"""
GeneticExperiment is a class that operates the experiment of genetic algorithm on MyColorfulGameOfLife

it provides the following services:

1.Set up a population of game(a game also contains its gene)
2.Evaluate the fitness of all current population
    evaluation process will not keep the process blocked.
    there is a limit of evaluation time.
    when the time is over, the evaluation process will pause, and return the progress of evaluation process.
    next time it will continue.
3.Generate the next population based on the current population
4.Save/Load experiment record using pandas
"""
import time
import random
import pandas as pd
from typing import List, Tuple, Any, Dict

from PyQt5.QtCore.QProcess import program

from ColorfulGameOfLife.AbstractColorfulGameOfLife import RuleSet, CellType
from ColorfulGameOfLife.MyColorfulGameOfLife import MyColorfulGameOfLife
from ColorfulGameOfLife.FitnessEvaluator import EVALUATOR
from Logger.Logger import hot


# TO-DO: from your_game_module import MyColorfulGameOfLife, Gene
# TO-DO: from evaluator_module import FitnessEvaluator

class GeneticExperiment:
    """
    用于执行 MyColorfulGameOfLife 上的遗传算法实验。
    提供初始化种群、评估、生成下一代、保存与加载记录等功能。
    """
    def __init__(self):
        self._setup_generation_size = int(hot("genetic_setup_generation_size", "100"))
        self._setup_gene_test_steps = int(hot("genetic_setup_gene_test_steps", "500"))
        self._setup_frame_size = int(hot("genetic_setup_frame_size", "100"))
        self._setup_discard_init_frames = int(hot("genetic_setup_discard_init_frames", "30"))
        self._setup_time_limit_s = float(hot("genetic_setup_time_limit_ms", "1.00"))

        # 当前种群（每个个体包含 game 和 gene）
        self.population: List[MyColorfulGameOfLife] = []

        # 每个个体的适应度得分
        self.fitness_scores: Dict[MyColorfulGameOfLife, float] = {}

        # 实验历史记录
        self.history: pd.DataFrame = pd.DataFrame()

    def initialize_population(self):
        """
        初始化种群：
        1. 生成 size 个随机个体（game + gene）
        2. 清空历史记录与得分
        """
        self.population = []
        self.fitness_scores = {}
        for _ in range(self._setup_generation_size):
            game = MyColorfulGameOfLife(
                self._setup_frame_size,
                self._setup_frame_size
            )
            ruleset = RuleSet()
            ruleset.add_cell_type(CellType.conway())
            game.setup_rule_set(ruleset)
            self.population.append(game)
        pass

    def evaluate_all(self) -> float:
        """
        非阻塞评估当前种群：
        1. 从 evaluation_progress 开始
        2. 评估每个个体（调用 evaluator.evaluate）
        3. 超过时间限制则暂停并返回进度（0-1 之间）
        """
        # time_start = time.time()
        # progress_count = len(self.fitness_scores)
        # while time.time() - time_start < self._setup_time_limit_s:
        #
        # return 1.

        pass

    def get_normalized_fitness(self, weights=None) -> List[float]:
        """
        对 raw 分数做归一化处理（可加权）
        1. 若有 weights 则先做加权
        2. 使用 min-max 或 softmax 归一化
        """
        pass

    def generate_next_population(self):
        """
        基于当前种群生成下一代：
        1. 选择（轮盘赌/锦标赛）
        2. 交叉生成新基因
        3. 突变操作
        4. 生成新个体并替代旧种群
        """
        pass

    def save_to_csv(self, path: str):
        """
        将当前实验状态保存为 CSV 文件：
        1. 包括 generation、gene、fitness 等字段
        2. 使用 pandas 结构化保存
        """
        pass

    def load_from_csv(self, path: str):
        """
        从 CSV 文件中加载实验状态：
        1. 恢复 population、fitness、generation 等状态
        2. 构造 game + gene 对象（需要反序列化）
        """
        pass

    def record_generation(self):
        """
        记录当前代的统计数据：
        1. 最佳个体得分与基因
        2. 平均适应度
        3. 存入 self.history
        """
        pass



