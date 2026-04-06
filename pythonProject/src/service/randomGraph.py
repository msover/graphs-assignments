from __future__ import annotations

from random import randint, sample

from src.domain.graph import UndirectedGraph


def makeRandomGraph(
    vertices: int,
    edges: int,
    minCost: int,
    maxCost: int,
) -> UndirectedGraph:
    if vertices < 0:
        raise ValueError("The number of vertices must be non-negative")
    if edges < 0:
        raise ValueError("The number of edges must be non-negative")
    if minCost > maxCost:
        raise ValueError("The minimum cost cannot be greater than the maximum cost")

    max_edges = vertices * (vertices - 1) // 2
    if edges > max_edges:
        raise ValueError("Too many edges for an undirected graph")

    graph = UndirectedGraph(vertices)
    allEdges = _allPossibleEdges(vertices)

    for u, v in sample(allEdges, edges):
        graph.addEdge(u, v, randint(minCost, maxCost))

    return graph


def _allPossibleEdges(vertices: int) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for u in range(vertices):
        for v in range(u + 1, vertices):
            candidates.append((u, v))
    return candidates
