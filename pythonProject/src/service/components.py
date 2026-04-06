from __future__ import annotations

from collections import deque

from src.domain.graph import UndirectedGraph


def connectedComponentsBfs(graph: UndirectedGraph) -> list[UndirectedGraph]:
    visited: set[int] = set()
    components: list[UndirectedGraph] = []

    for vertex in graph.parseVertices():
        if vertex in visited:
            continue

        componentVertices = _collectComponentVertices(graph, vertex, visited)
        components.append(graph.subGraph(componentVertices))

    return components


def _collectComponentVertices(
    graph: UndirectedGraph,
    start: int,
    visited: set[int],
) -> list[int]:
    queue = deque([start])
    visited.add(start)
    component = [start]

    while queue:
        current = queue.popleft()
        for neighbor in graph.parseNeighbors(current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            component.append(neighbor)
            queue.append(neighbor)

    return component
