from __future__ import annotations

from collections import deque

from src.domain.graph import UndirectedGraph


def connected_components_bfs(graph: UndirectedGraph) -> list[UndirectedGraph]:
    visited: set[int] = set()
    components: list[UndirectedGraph] = []

    for vertex in graph.parse_vertices():
        if vertex in visited:
            continue

        component_vertices = _collect_component_vertices(graph, vertex, visited)
        components.append(graph.subgraph(component_vertices))

    return components


def _collect_component_vertices(
    graph: UndirectedGraph,
    start: int,
    visited: set[int],
) -> list[int]:
    queue = deque([start])
    visited.add(start)
    component = [start]

    while queue:
        current = queue.popleft()
        for neighbor in graph.parse_neighbors(current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            component.append(neighbor)
            queue.append(neighbor)

    return component
