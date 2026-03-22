from src.domain.DirectedGraph import DirectedGraph


def readGraph(fileName: str) -> DirectedGraph:
    with open(fileName, "r") as file:
        firstLine = file.readline().strip()
        if not firstLine:
            raise ValueError("The input file is empty")

        vertices, edges = map(int, firstLine.split())
        graph = DirectedGraph(vertices)

        for _ in range(edges):
            line = file.readline().strip()
            if not line:
                raise ValueError("The input file ended before all edges were read")

            u, v, cost = map(int, line.split())
            graph.addEdge(u, v, cost)

    return graph


def writeGraph(fileName: str, graph: DirectedGraph) -> None:
    with open(fileName, "w") as file:
        file.write(f"{graph.getVertices()} {graph.getEdges()}\n")

        for (u, v), cost in sorted(graph.getCosts().items()):
            file.write(f"{u} {v} {cost}\n")
