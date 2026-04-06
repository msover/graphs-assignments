from __future__ import annotations

from collections.abc import Iterable


class UndirectedGraph:
    def __init__(self, vertices: int = 0):
        if vertices < 0:
            raise ValueError("The number of vertices must be non-negative")

        self._neighbors: dict[int, dict[int, int]] = {index: {} for index in range(vertices)}
        self._costs: dict[tuple[int, int], int] = {}
        self._edgeCount = 0

    def hasVertex(self, vertex: int) -> bool:
        return vertex in self._neighbors

    def vertexCount(self) -> int:
        return len(self._neighbors)

    def edgeCount(self) -> int:
        return self._edgeCount

    def parseVertices(self) -> list[int]:
        return sorted(self._neighbors)

    def parseNeighbors(self, vertex: int) -> list[int]:
        self._checkVertex(vertex)
        return sorted(self._neighbors[vertex])

    def degree(self, vertex: int) -> int:
        self._checkVertex(vertex)
        return len(self._neighbors[vertex])

    def addVertex(self, vertex: int | None = None) -> int:
        if vertex is None:
            vertex = 0 if not self._neighbors else max(self._neighbors) + 1

        if self.hasVertex(vertex):
            raise ValueError(f"Vertex {vertex} already exists")

        self._neighbors[vertex] = {}
        return vertex

    def removeVertex(self, vertex: int) -> None:
        self._checkVertex(vertex)

        for neighbor in list(self._neighbors[vertex]):
            self.removeEdge(vertex, neighbor)

        del self._neighbors[vertex]

    def isEdge(self, u: int, v: int) -> bool:
        self._checkVertex(u)
        self._checkVertex(v)
        return v in self._neighbors[u]

    def addEdge(self, u: int, v: int, cost: int = 0) -> None:
        self._checkVertex(u)
        self._checkVertex(v)
        if u == v:
            raise ValueError("Loops are not allowed")

        edgeKey = self._edgeKey(u, v)
        if edgeKey in self._costs:
            raise ValueError(f"Edge {u} -- {v} already exists")

        self._neighbors[u][v] = cost
        self._neighbors[v][u] = cost
        self._costs[edgeKey] = cost
        self._edgeCount += 1

    def removeEdge(self, u: int, v: int) -> None:
        self._checkEdge(u, v)
        del self._neighbors[u][v]
        del self._neighbors[v][u]
        del self._costs[self._edgeKey(u, v)]
        self._edgeCount -= 1

    def getEdgeCost(self, u: int, v: int) -> int:
        self._checkEdge(u, v)
        return self._costs[self._edgeKey(u, v)]

    def setEdgeCost(self, u: int, v: int, cost: int) -> None:
        self._checkEdge(u, v)
        self._neighbors[u][v] = cost
        self._neighbors[v][u] = cost
        self._costs[self._edgeKey(u, v)] = cost

    def parseEdges(self) -> list[tuple[tuple[int, int], int]]:
        return sorted(self._costs.items())

    def copyGraph(self) -> UndirectedGraph:
        graphCopy = UndirectedGraph(0)
        for vertex in self.parseVertices():
            graphCopy.addVertex(vertex)
        for (u, v), cost in self.parseEdges():
            graphCopy.addEdge(u, v, cost)
        return graphCopy

    def subGraph(self, vertices: Iterable[int]) -> UndirectedGraph:
        selectedVertices = set(vertices)
        newGraph = UndirectedGraph(0)

        for vertex in sorted(selectedVertices):
            self._checkVertex(vertex)
            newGraph.addVertex(vertex)

        for (u, v), cost in self.parseEdges():
            if u in selectedVertices and v in selectedVertices:
                newGraph.addEdge(u, v, cost)

        return newGraph

    def _checkVertex(self, vertex: int) -> None:
        if not self.hasVertex(vertex):
            raise ValueError(f"Invalid vertex: {vertex}")

    def _checkEdge(self, u: int, v: int) -> None:
        if not self.isEdge(u, v):
            raise ValueError(f"Edge {u} -- {v} does not exist")

    @staticmethod
    def _edgeKey(u: int, v: int) -> tuple[int, int]:
        return (u, v) if u <= v else (v, u)
