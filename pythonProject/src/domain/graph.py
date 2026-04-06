from __future__ import annotations

from collections.abc import Iterable


class UndirectedGraph:
    def __init__(self, vertices: int = 0):
        if vertices < 0:
            raise ValueError("The number of vertices must be non-negative")

        self._neighbors: dict[int, dict[int, int]] = {index: {} for index in range(vertices)}
        self._costs: dict[tuple[int, int], int] = {}
        self._edge_count = 0

    def has_vertex(self, vertex: int) -> bool:
        return vertex in self._neighbors

    def vertex_count(self) -> int:
        return len(self._neighbors)

    def edge_count(self) -> int:
        return self._edge_count

    def parse_vertices(self) -> list[int]:
        return sorted(self._neighbors)

    def parse_neighbors(self, vertex: int) -> list[int]:
        self._check_vertex(vertex)
        return sorted(self._neighbors[vertex])

    def degree(self, vertex: int) -> int:
        self._check_vertex(vertex)
        return len(self._neighbors[vertex])

    def add_vertex(self, vertex: int | None = None) -> int:
        if vertex is None:
            vertex = 0 if not self._neighbors else max(self._neighbors) + 1

        if self.has_vertex(vertex):
            raise ValueError(f"Vertex {vertex} already exists")

        self._neighbors[vertex] = {}
        return vertex

    def remove_vertex(self, vertex: int) -> None:
        self._check_vertex(vertex)

        for neighbor in list(self._neighbors[vertex]):
            self.remove_edge(vertex, neighbor)

        del self._neighbors[vertex]

    def is_edge(self, u: int, v: int) -> bool:
        self._check_vertex(u)
        self._check_vertex(v)
        return v in self._neighbors[u]

    def add_edge(self, u: int, v: int, cost: int = 0) -> None:
        self._check_vertex(u)
        self._check_vertex(v)
        if u == v:
            raise ValueError("Loops are not allowed")

        edge_key = self._edge_key(u, v)
        if edge_key in self._costs:
            raise ValueError(f"Edge {u} -- {v} already exists")

        self._neighbors[u][v] = cost
        self._neighbors[v][u] = cost
        self._costs[edge_key] = cost
        self._edge_count += 1

    def remove_edge(self, u: int, v: int) -> None:
        self._check_edge(u, v)
        del self._neighbors[u][v]
        del self._neighbors[v][u]
        del self._costs[self._edge_key(u, v)]
        self._edge_count -= 1

    def get_edge_cost(self, u: int, v: int) -> int:
        self._check_edge(u, v)
        return self._costs[self._edge_key(u, v)]

    def set_edge_cost(self, u: int, v: int, cost: int) -> None:
        self._check_edge(u, v)
        self._neighbors[u][v] = cost
        self._neighbors[v][u] = cost
        self._costs[self._edge_key(u, v)] = cost

    def parse_edges(self) -> list[tuple[tuple[int, int], int]]:
        return sorted(self._costs.items())

    def copy_graph(self) -> UndirectedGraph:
        graph_copy = UndirectedGraph(0)
        for vertex in self.parse_vertices():
            graph_copy.add_vertex(vertex)
        for (u, v), cost in self.parse_edges():
            graph_copy.add_edge(u, v, cost)
        return graph_copy

    def subgraph(self, vertices: Iterable[int]) -> UndirectedGraph:
        selected_vertices = set(vertices)
        new_graph = UndirectedGraph(0)

        for vertex in sorted(selected_vertices):
            self._check_vertex(vertex)
            new_graph.add_vertex(vertex)

        for (u, v), cost in self.parse_edges():
            if u in selected_vertices and v in selected_vertices:
                new_graph.add_edge(u, v, cost)

        return new_graph

    def _check_vertex(self, vertex: int) -> None:
        if not self.has_vertex(vertex):
            raise ValueError(f"Invalid vertex: {vertex}")

    def _check_edge(self, u: int, v: int) -> None:
        if not self.is_edge(u, v):
            raise ValueError(f"Edge {u} -- {v} does not exist")

    @staticmethod
    def _edge_key(u: int, v: int) -> tuple[int, int]:
        return (u, v) if u <= v else (v, u)
