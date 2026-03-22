class DirectedGraph:
    def __init__(self, vertices: int = 0):
        self._vertices = vertices
        self._edges = 0
        self._outbound = {i: set() for i in range(vertices)}
        self._inbound = {i: set() for i in range(vertices)}
        self._costs = {}

    def _checkVertex(self, vertex: int) -> None:
        if vertex not in self._outbound:
            raise ValueError(f"Invalid vertex: {vertex}")

    def _checkEdge(self, u: int, v: int) -> None:
        self._checkVertex(u)
        self._checkVertex(v)
        if v not in self._outbound[u]:
            raise ValueError(f"Edge {u} -> {v} does not exist")

    def isEdge(self, u: int, v: int) -> bool:
        self._checkVertex(u)
        self._checkVertex(v)
        return v in self._outbound[u]

    def addEdge(self, u: int, v: int, cost: int) -> None:
        self._checkVertex(u)
        self._checkVertex(v)
        if v in self._outbound[u]:
            raise ValueError(f"Edge {u} -> {v} already exists")
        self._outbound[u].add(v)
        self._inbound[v].add(u)
        self._costs[(u, v)] = cost
        self._edges += 1

    def removeEdge(self, u: int, v: int) -> None:
        self._checkEdge(u, v)

        self._outbound[u].remove(v)
        self._inbound[v].remove(u)
        del self._costs[(u, v)]
        self._edges -= 1

    def addVertex(self) -> int:
        newVertex = 0 if not self._outbound else max(self._outbound) + 1
        self._outbound[newVertex] = set()
        self._inbound[newVertex] = set()
        self._vertices += 1
        return newVertex

    def removeVertex(self, vertex: int) -> None:
        self._checkVertex(vertex)

        outboundNeighbors = list(self._outbound[vertex])
        inboundNeighbors = list(self._inbound[vertex])

        for neighbor in outboundNeighbors:
            self.removeEdge(vertex, neighbor)

        for neighbor in inboundNeighbors:
            if neighbor in self._outbound and vertex in self._outbound[neighbor]:
                self.removeEdge(neighbor, vertex)

        del self._outbound[vertex]
        del self._inbound[vertex]
        self._vertices -= 1

    def setEdgeCost(self, u: int, v: int, cost: int) -> None:
        self._checkEdge(u, v)
        self._costs[(u, v)] = cost

    def getEdgeCost(self, u: int, v: int) -> int:
        self._checkEdge(u, v)
        return self._costs[(u, v)]

    def copyGraph(self):
        newGraph = DirectedGraph(0)
        newGraph._vertices = self._vertices
        newGraph._edges = self._edges
        newGraph._outbound = {
            vertex: neighbors.copy()
            for vertex, neighbors in self._outbound.items()
        }
        newGraph._inbound = {
            vertex: neighbors.copy()
            for vertex, neighbors in self._inbound.items()
        }
        newGraph._costs = self._costs.copy()
        return newGraph

    def getVertices(self) -> int:
        return self._vertices

    def getEdges(self) -> int:
        return self._edges

    def getCosts(self) -> {}:
        return self._costs

    def parseVertices(self):
        return sorted(self._outbound.keys())

    def parseOutboundNeighbors(self, vertex: int):
        self._checkVertex(vertex)
        return sorted(self._outbound[vertex])

    def parseInboundNeighbors(self, vertex: int):
        self._checkVertex(vertex)
        return sorted(self._inbound[vertex])

    def getOutDegree(self, vertex: int) -> int:
        self._checkVertex(vertex)
        return len(self._outbound[vertex])

    def getInDegree(self, vertex: int) -> int:
        self._checkVertex(vertex)
        return len(self._inbound[vertex])
