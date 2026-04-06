from __future__ import annotations

from random import randint, sample

from src.domain.graph import UndirectedGraph


def make_random_graph(
    vertices: int,
    edges: int,
    min_cost: int,
    max_cost: int,
) -> UndirectedGraph:
    if vertices < 0:
        raise ValueError("The number of vertices must be non-negative")
    if edges < 0:
        raise ValueError("The number of edges must be non-negative")
    if min_cost > max_cost:
        raise ValueError("The minimum cost cannot be greater than the maximum cost")

    max_edges = vertices * (vertices - 1) // 2
    if edges > max_edges:
        raise ValueError("Too many edges for an undirected graph")

    graph = UndirectedGraph(vertices)
    all_edges = _all_possible_edges(vertices)

    for u, v in sample(all_edges, edges):
        graph.add_edge(u, v, randint(min_cost, max_cost))

    return graph


def _all_possible_edges(vertices: int) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for u in range(vertices):
        for v in range(u + 1, vertices):
            candidates.append((u, v))
    return candidates
