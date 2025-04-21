
"""
an island is a group of cells in a frame of the life game that are related to each other.
define "related": two cells are related if the maximum distance of them in x-axis and y-axis is less than or equal to 2.
range is like this
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 0 0
0 0 0 0 0

here is several things to do with one frame in a life game:

1.for each frame, detect all islands in it.
2.for each neighbour frames, find all pairs of islands that are in different frames but spatially related(there is an overlay of their effected area)
3.build a graph for the whole game history(collection of all frames), let vertices be islands and edges be pairs of islands that are related in neighbour frames.
ok，那应该也不用优化了
我说一下目前的思路
第一个函数：将一个frame转换为island list（顺便一提frame是np.ndarray）
步骤：
遍历frame中所有位置，如果有细胞就加入细胞位置集
从细胞位置集中取出细胞执行以下步骤，直到没有细胞可取（像之前所说，细胞包含的数据仅为一个坐标）：
    求所有与当前细胞位置相关的位置（一共5*5-1 24个点）
    如果这个位置在原frame中存在活细胞，加入同一岛，并从原frame中移除这个点
    直到无法再加点，这个岛的生成完成
最后返回岛集

"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import random
def island_detection(frame):
    islands = []
    alive_cells = set(map(tuple, np.argwhere(frame == 1)))  # 活细胞坐标集 {(x, y)}

    while alive_cells:
        cell = alive_cells.pop()
        island = {cell}
        queue = [cell]

        while queue:
            cx, cy = queue.pop()
            # 搜索 5x5 区域内其他活细胞
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = cx + dx, cy + dy
                    neighbor = (nx, ny)
                    if neighbor in alive_cells:
                        island.add(neighbor)
                        queue.append(neighbor)
                        alive_cells.remove(neighbor)
        islands.append(island)
    return islands

def get_influence_area(island):
    influence = set()
    for x, y in island:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                influence.add((x + dx, y + dy))
    return influence

def find_related_island_pairs(islands1, islands2):
    related_pairs = []
    influences1 = [get_influence_area(island) for island in islands1]
    influences2 = [get_influence_area(island) for island in islands2]

    for i, inf1 in enumerate(influences1):
        for j, inf2 in enumerate(influences2):
            if inf1 & inf2:  # 非空交集
                related_pairs.append((i, j))
    return related_pairs



def build_island_graph(frames):
    G = nx.Graph()
    all_islands = []  # [(frame_index, island_index, island_set)]

    # 1. 处理每帧岛屿
    for t, frame in enumerate(frames):
        islands = island_detection(frame)
        for i, island in enumerate(islands):
            G.add_node((t, i), cells=island)
        all_islands.append(islands)

    # 2. 加边：相邻帧相关岛屿之间连边
    for t in range(len(frames) - 1):
        pairs = find_related_island_pairs(all_islands[t], all_islands[t + 1])
        for i1, i2 in pairs:
            G.add_edge((t, i1), (t + 1, i2))

    return G




def generate_random_graph(n_nodes=10, edge_prob=0.2, seed=None):
    """
    生成一个随机无向图，使用 G(n, p) 模型。
    :param n_nodes: 节点数量
    :param edge_prob: 任意两点之间连边的概率
    :param seed: 随机种子
    :return: networkx.Graph 对象
    """
    G = nx.gnp_random_graph(n=n_nodes, p=edge_prob, seed=seed)

    # 给每个节点添加一个可视化属性，例如颜色或值
    for node in G.nodes:
        G.nodes[node]['value'] = random.randint(1, 10)
    return G


def draw_graph_matplotlib(G, title="Random Graph"):
    """
    使用 matplotlib 画出 networkx 图。
    :param G: networkx 图
    :param title: 图标题
    """
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)  # 布局算法

    # 节点颜色映射
    node_colors = [G.nodes[n].get('value', 1) for n in G.nodes]

    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        cmap=plt.cm.viridis,
        node_size=500,
        edge_color='gray',
        font_size=10
    )

    plt.title(title)
    plt.show()


def test_random_graph_visualization():
    G = generate_random_graph(n_nodes=15, edge_prob=0.3, seed=42)
    draw_graph_matplotlib(G, title="Test Random Graph")

test_random_graph_visualization()