import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import List, Set, Tuple, Dict

influence_map_for_shape:Dict[Tuple[int,int], Dict[Tuple[int, int], Set[Tuple[int,int]]]] = {}

def _new_shape_influence_map(shape: Tuple[int, int]):
    influence_map_for_shape[shape] = {}
    for x in range(shape[0]):
        for y in range(shape[1]):
            key = (x, y)
            val = set()
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    tox = (x + dx) % shape[0]
                    toy = (y + dy) % shape[1]
                    val.add((tox, toy))
                    # if key == (0,0):
                        # print((tox, toy))
            influence_map_for_shape[shape][key] = val
    # print(influence_map_for_shape[shape][(0,0)])
    pass

def get_neighbour_mapping_for_shape(shape:Tuple[int, int]) -> dict:

    try:
        return influence_map_for_shape[shape]
    except KeyError:
        _new_shape_influence_map(shape)
        return influence_map_for_shape[shape]

def island_detection(frame: np.ndarray) -> List[Set[Tuple[int, int]]]:
    """
    Detect all islands in a frame of the Game of Life.

    An island is a group of live cells where each cell is related to another
    if their maximum x or y distance is less than or equal to 2.

    :param frame: 2D numpy array representing the life frame (0 or 1 values)
    :return: A list of islands, where each island is a set of (x, y) coordinates
    """
    islands = []
    # width, height = frame.shape
    alive_cells = set(map(tuple, np.argwhere(frame != 0)))  # live cells as (x, y)
    neighbour_mapping = get_neighbour_mapping_for_shape(frame.shape)

    while alive_cells:
        cell = alive_cells.pop()
        island = {cell}
        queue = [cell]

        while queue:
            cx, cy = queue.pop()
            for neighbour in neighbour_mapping[(cx,cy)]:
                if neighbour in alive_cells:
                    island.add(neighbour)
                    queue.append(neighbour)
                    alive_cells.remove(neighbour)
            # for dx in range(-2, 3):
            #     for dy in range(-2, 3):
            #         if dx == 0 and dy == 0:
            #             continue
            #         nx_, ny_ = cx + dx, cy + dy
            #         nx_ = nx_ % width
            #         ny_ = ny_ % height
            #         neighbor = (nx_, ny_)
            #         if neighbor in alive_cells:
            #             island.add(neighbor)
            #             queue.append(neighbor)
            #             alive_cells.remove(neighbor)
        islands.append(island)
    return islands


def get_influence_area(island: Set[Tuple[int, int]], shape: Tuple[int, int]) -> Set[Tuple[int, int]]:
    width, height = shape
    influence = set()
    neighbour_mapping = get_neighbour_mapping_for_shape(shape)
    for x, y in island:
        for neighbour in neighbour_mapping[(x, y)]:
            influence.add(neighbour)
        # for dx in range(-2, 3):
        #     for dy in range(-2, 3):
        #         nnx = (x + dx) % height
        #         nny = (y + dy) % width
        #         influence.add((nnx, nny))
    return influence



def find_related_island_pairs(islands1: List[Set[Tuple[int, int]]], islands2: List[Set[Tuple[int, int]]], shape:Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Find pairs of islands from two consecutive frames that are spatially related.

    :param shape:
    :param islands1: List of islands from frame t
    :param islands2: List of islands from frame t+1
    :return: List of index pairs (i, j) where islands1[i] and islands2[j] are related
    """
    related_pairs = []
    influences1 = [get_influence_area(island, shape) for island in islands1]
    influences2 = [get_influence_area(island, shape) for island in islands2]

    for i, inf1 in enumerate(influences1):
        for j, inf2 in enumerate(influences2):
            if inf1 & inf2:
                related_pairs.append((i, j))
    return related_pairs


def build_island_graph(frames: List[np.ndarray]) -> nx.Graph:
    """
    Build a graph representing island evolution across Game of Life frames.

    :param frames: List of 2D numpy arrays representing life game frames
    :return: A NetworkX graph where nodes are (frame_index, island_index)
             and edges connect spatially related islands between frames
    """
    G = nx.Graph()
    all_islands = []
    shape = frames[0].shape

    for t, frame in enumerate(frames):
        islands = island_detection(frame)
        for i, island in enumerate(islands):
            G.add_node((t, i), cells=island)
        all_islands.append(islands)

    for t in range(len(frames) - 1):
        pairs = find_related_island_pairs(all_islands[t], all_islands[t + 1], shape)
        for i1, i2 in pairs:
            G.add_edge((t, i1), (t + 1, i2))

    return G


def generate_random_graph(n_nodes: int = 10, edge_prob: float = 0.2, seed: int = None) -> nx.Graph:
    """
    Generate a random undirected graph using the Erdős–Rényi model G(n, p).

    :param n_nodes: Number of nodes in the graph
    :param edge_prob: Probability of edge creation between any pair of nodes
    :param seed: Optional seed for reproducibility
    :return: A NetworkX graph with random edges and random 'value' attributes on nodes
    """
    G = nx.gnp_random_graph(n=n_nodes, p=edge_prob, seed=seed)

    for node in G.nodes:
        G.nodes[node]['value'] = random.randint(1, 10)
    return G

def draw_life_frame(array: np.ndarray, title: str = "Life Frame", islands: List[Set[Tuple[int, int]]] = None):
    """
    Display a 2D Life Game frame using a heatmap, and optionally overlay detected islands.

    :param array: The 2D numpy array representing the life frame
    :param title: Title of the plot
    :param islands: Optional list of sets of (x, y) coordinates representing islands
    """
    array = array.T
    plt.figure(figsize=(6, 6))
    plt.imshow(array, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.title(title)
    plt.axis('off')

    if islands:
        colors_cycle = [
            'red',
            'blue',
            'green',
            'orange',
            'magenta',
            'cyan',
            'yellow',
            'brown',
            'purple',
            'deepskyblue'
        ]
        for idx, island in enumerate(islands):
            color = colors_cycle[idx % len(colors_cycle)]
            for x, y in island:
                # Note: swap x/y because array is transposed
                plt.plot(x, y, 'o', color=color, markersize=6, markeredgewidth=0.9, markeredgecolor='white', alpha=0.5)

    plt.tight_layout()
    plt.show()

def draw_graph_matplotlib(G: nx.Graph, title: str = "Random Graph") -> None:
    """
    Visualize a graph using matplotlib with spring layout.

    :param G: A NetworkX graph to draw
    :param title: Title of the plot
    """
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)
    node_colors = [G.nodes[n].get('value', 1) for n in G.nodes]

    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        cmap=plt.cm.get_cmap('viridis'),
        node_size=500,
        edge_color='gray',
        font_size=10
    )

    plt.title(title)
    plt.show()


def test_random_graph_visualization() -> None:
    """
    Generate a random graph and visualize it to test functionality.
    """
    G = generate_random_graph(n_nodes=30, edge_prob=0.1, seed=44)
    draw_graph_matplotlib(G, title="Test Random Graph")


# Run test
if __name__ == "__main__":
    test_random_graph_visualization()

