from __future__ import annotations

from collections import deque

from src.domain.graph import Graph


def lowest_length_path_forward_bfs(graph: Graph, start: int, end: int) -> tuple[list[int], int]:
    _check_path_vertices(graph, start, end)
    parent = _bfs_parent_map(graph, start, end)
    return _reconstruct_path_from_parent(parent, start, end)


def lowest_length_path_backward_bfs(graph: Graph, start: int, end: int) -> tuple[list[int], int]:
    _check_path_vertices(graph, start, end)

    queue = deque([end])
    next_vertex: dict[int, int | None] = {end: None}

    while queue:
        current = queue.popleft()
        if current == start:
            break

        for neighbor in graph.parse_inbound_neighbors(current):
            if neighbor not in next_vertex:
                next_vertex[neighbor] = current
                queue.append(neighbor)

    if start not in next_vertex:
        return [], -1

    path = [start]
    current = start
    while next_vertex[current] is not None:
        current = next_vertex[current]
        path.append(current)

    return path, len(path) - 1


def connected_components_dfs(graph: Graph) -> list[Graph]:
    _check_undirected(graph)
    visited: set[int] = set()
    components: list[Graph] = []

    for vertex in graph.parse_vertices():
        if vertex in visited:
            continue

        component_vertices = _collect_component_dfs(graph, vertex, visited)
        components.append(graph.subgraph(component_vertices))

    return components


def connected_components_bfs(graph: Graph) -> list[Graph]:
    _check_undirected(graph)
    visited: set[int] = set()
    components: list[Graph] = []

    for vertex in graph.parse_vertices():
        if vertex in visited:
            continue

        component_vertices = _collect_component_bfs(graph, vertex, visited)
        components.append(graph.subgraph(component_vertices))

    return components


def format_path(path: list[int]) -> str:
    if not path:
        return "no path"
    return " -> ".join(str(vertex) for vertex in path)


def _bfs_parent_map(graph: Graph, start: int, end: int) -> dict[int, int | None]:
    queue = deque([start])
    parent: dict[int, int | None] = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for neighbor in graph.parse_outbound_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return parent


def _reconstruct_path_from_parent(
    parent: dict[int, int | None],
    start: int,
    end: int,
) -> tuple[list[int], int]:
    if end not in parent:
        return [], -1

    path: list[int] = []
    current: int | None = end
    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    if path[0] != start:
        return [], -1

    return path, len(path) - 1


def _collect_component_dfs(graph: Graph, start: int, visited: set[int]) -> list[int]:
    stack = [start]
    component: list[int] = []

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        component.append(current)

        for neighbor in reversed(graph.parse_outbound_neighbors(current)):
            if neighbor not in visited:
                stack.append(neighbor)

    return component


def _collect_component_bfs(graph: Graph, start: int, visited: set[int]) -> list[int]:
    queue = deque([start])
    visited.add(start)
    component = [start]

    while queue:
        current = queue.popleft()
        for neighbor in graph.parse_outbound_neighbors(current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            component.append(neighbor)
            queue.append(neighbor)

    return component


def _check_path_vertices(graph: Graph, start: int, end: int) -> None:
    if not graph.has_vertex(start):
        raise ValueError(f"Invalid start vertex: {start}")
    if not graph.has_vertex(end):
        raise ValueError(f"Invalid end vertex: {end}")


def _check_undirected(graph: Graph) -> None:
    if graph.is_directed():
        raise ValueError("Connected components require an undirected graph")
