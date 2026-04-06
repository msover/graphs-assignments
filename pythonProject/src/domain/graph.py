from __future__ import annotations

from collections.abc import Iterable


class Graph:
    def __init__(self, vertices: int = 0, directed: bool = True):
        if vertices < 0:
            raise ValueError("The number of vertices must be non-negative")

        self._directed = directed
        self._outbound: dict[int, dict[int, int]] = {index: {} for index in range(vertices)}
        self._inbound: dict[int, dict[int, int]] = {index: {} for index in range(vertices)}
        self._costs: dict[tuple[int, int], int] = {}
        self._edge_count = 0

    def is_directed(self) -> bool:
        return self._directed

    def has_vertex(self, vertex: int) -> bool:
        return vertex in self._outbound

    def vertex_count(self) -> int:
        return len(self._outbound)

    def edge_count(self) -> int:
        return self._edge_count

    def parse_vertices(self) -> list[int]:
        return sorted(self._outbound)

    def parse_outbound_neighbors(self, vertex: int) -> list[int]:
        self._check_vertex(vertex)
        return sorted(self._outbound[vertex])

    def parse_inbound_neighbors(self, vertex: int) -> list[int]:
        self._check_vertex(vertex)
        return sorted(self._inbound[vertex])

    def get_out_degree(self, vertex: int) -> int:
        self._check_vertex(vertex)
        return len(self._outbound[vertex])

    def get_in_degree(self, vertex: int) -> int:
        self._check_vertex(vertex)
        return len(self._inbound[vertex])

    def add_vertex(self, vertex: int | None = None) -> int:
        if vertex is None:
            vertex = 0 if not self._outbound else max(self._outbound) + 1

        if self.has_vertex(vertex):
            raise ValueError(f"Vertex {vertex} already exists")

        self._outbound[vertex] = {}
        self._inbound[vertex] = {}
        return vertex

    def remove_vertex(self, vertex: int) -> None:
        self._check_vertex(vertex)

        incident_edges = {(vertex, neighbor) for neighbor in self._outbound[vertex]}
        incident_edges.update((neighbor, vertex) for neighbor in self._inbound[vertex])

        for u, v in list(incident_edges):
            if self.is_edge(u, v):
                self.remove_edge(u, v)

        del self._outbound[vertex]
        del self._inbound[vertex]

    def is_edge(self, u: int, v: int) -> bool:
        self._check_vertex(u)
        self._check_vertex(v)
        return v in self._outbound[u]

    def add_edge(self, u: int, v: int, cost: int = 0) -> None:
        self._check_vertex(u)
        self._check_vertex(v)

        edge_key = self._edge_key(u, v)
        if edge_key in self._costs:
            connector = "->" if self._directed else "--"
            raise ValueError(f"Edge {u} {connector} {v} already exists")

        self._outbound[u][v] = cost
        self._inbound[v][u] = cost

        if not self._directed:
            self._outbound[v][u] = cost
            self._inbound[u][v] = cost

        self._costs[edge_key] = cost
        self._edge_count += 1

    def remove_edge(self, u: int, v: int) -> None:
        self._check_edge(u, v)

        del self._outbound[u][v]
        del self._inbound[v][u]

        if not self._directed:
            del self._outbound[v][u]
            del self._inbound[u][v]

        del self._costs[self._edge_key(u, v)]
        self._edge_count -= 1

    def get_edge_cost(self, u: int, v: int) -> int:
        self._check_edge(u, v)
        return self._costs[self._edge_key(u, v)]

    def set_edge_cost(self, u: int, v: int, cost: int) -> None:
        self._check_edge(u, v)

        self._outbound[u][v] = cost
        self._inbound[v][u] = cost

        if not self._directed:
            self._outbound[v][u] = cost
            self._inbound[u][v] = cost

        self._costs[self._edge_key(u, v)] = cost

    def parse_edges(self) -> list[tuple[tuple[int, int], int]]:
        return sorted(self._costs.items())

    def copy_graph(self) -> Graph:
        graph_copy = Graph(0, directed=self._directed)
        for vertex in self.parse_vertices():
            graph_copy.add_vertex(vertex)
        for (u, v), cost in self.parse_edges():
            graph_copy.add_edge(u, v, cost)
        return graph_copy

    def subgraph(self, vertices: Iterable[int]) -> Graph:
        selected_vertices = set(vertices)
        new_graph = Graph(0, directed=self._directed)

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
            connector = "->" if self._directed else "--"
            raise ValueError(f"Edge {u} {connector} {v} does not exist")

    def _edge_key(self, u: int, v: int) -> tuple[int, int]:
        if self._directed:
            return u, v
        return (u, v) if u <= v else (v, u)
