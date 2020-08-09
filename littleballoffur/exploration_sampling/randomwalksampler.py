import random
import networkx as nx
import networkit as nk
from typing import Union
from littleballoffur.sampler import Sampler


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class RandomWalkSampler(Sampler):
    r"""An implementation of node sampling by random walks. A simple random walker
    which created an induced subgraph by walking around. `"For details about the
    algorithm see this paper." <https://ieeexplore.ieee.org/document/5462078>`_

    Args:
        number_of_nodes (int): Number of nodes. Default is 100.
        seed (int): Random seed. Default is 42.
    """
    def __init__(self, number_of_nodes: int=100, seed: int=42):
        self.number_of_nodes = number_of_nodes
        self.seed = seed
        self._set_seed()

    def _create_initial_node_set(self, graph):
        """
        Choosing an initial node.
        """
        self._current_node = random.choice(range(self.backend.get_number_of_nodes(graph)))
        self._sampled_nodes = set([self._current_node])

    def _do_a_step(self, graph):
        """
        Doing a single random walk step.
        """
        neighbors = self.backend.get_neighbors(graph, self._current_node)
        self._current_node = random.choice(neighbors)
        self._sampled_nodes.add(self._current_node)

    def sample(self, graph: Union[NXGraph, NKGraph]) -> Union[NXGraph, NKGraph]:
        """
        Sampling nodes with a single random walk.

        Arg types:
            * **graph** *(NetworkX or NetworKit graph)* - The graph to be sampled from.

        Return types:
            * **new_graph** *(NetworkX or NetworKit graph)* - The graph of sampled nodes.
        """
        self._deploy_backend(graph)
        self._check_number_of_nodes(graph)
        self._create_initial_node_set(graph)
        while len(self._sampled_nodes) < self.number_of_nodes:
            self._do_a_step(graph)
        new_graph = self.backend.get_subgraph(graph, self._sampled_nodes)
        return new_graph
