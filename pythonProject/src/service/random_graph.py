from __future__ import annotations

from random import randint, sample

from src.domain.graph import Graph


def make_random_graph(
    vertices: int,
    edges: int,
    min_cost: int,
    max_cost: int,
    directed: bool = True,
) -> Graph:
    if vertices < 0:
        raise ValueError("The number of vertices must be non-negative")
    if edges < 0:
        raise ValueError("The number of edges must be non-negative")
    if min_cost > max_cost:
        raise ValueError("The minimum cost cannot be greater than the maximum cost")

    max_edges = vertices * (vertices - 1)
    if not directed:
        max_edges //= 2

    if edges > max_edges:
        raise ValueError("Too many edges for the selected graph type")

    graph = Graph(vertices, directed=directed)
    all_edges = _all_possible_edges(vertices, directed)

    for u, v in sample(all_edges, edges):
        graph.add_edge(u, v, randint(min_cost, max_cost))

    return graph


def _all_possible_edges(vertices: int, directed: bool) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for u in range(vertices):
        for v in range(vertices):
            if u == v:
                continue
            if directed or u < v:
                candidates.append((u, v))
    return candidates
