from typing import Set, Dict, Tuple, Iterable
class DirectedGraph:
    """
    _out:  vertex -> outbound neighbors
    _in:   vertex -> inbound neighbors
    _cost: (u, v) -> edge cost
    """

    def __init__(self, vertices: int = 0):
        if vertices < 0:
            raise ValueError("vertices number must be positive")
        self.vertices = vertices
        self._out: Dict[int, Set[int]] = {}
        self._in: Dict[int, Set[int]] = {}
        self._cost: Dict[Tuple[int, int], int] = {}

        for v in range(vertices):
            self._out[v] = set()
            self._in[v] = set()

    def clone(self) -> DirectedGraph:
        graph = DirectedGraph()
        graph._out = {v: set(neighbour) for v, neighbour in self._out.items()}
        graph._in = {v: set(neighbour) for v, neighbour in self._in.items()}
        graph._cost = dict(self._cost)
        return graph

    def getVertexCount(self) -> int:
        return len(self._out)

    def getEdgesCount(self) -> int:
        return len(self._cost)

    def vertices(self) -> Iterable[int]:
        return self._out.keys()

    def hasVertex(self, vertex: int) -> bool:
        return vertex in self._out

    def hasEdge(self, edge: Tuple[int, int]) -> bool:
        return edge in self._cost