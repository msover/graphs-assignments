import random

from src.domain.DirectedGraph import DirectedGraph


def makeRandomGraph(vertices: int, edges: int, minCost: int = 0, maxCost: int = 100) -> DirectedGraph:
    if vertices < 0:
        raise ValueError("The number of vertices cannot be negative")
    if edges < 0:
        raise ValueError("The number of edges cannot be negative")
    if minCost > maxCost:
        raise ValueError("Invalid cost interval")

    maxEdges = vertices * vertices
    if edges > maxEdges:
        raise ValueError("Too many edges for the given number of vertices")

    graph = DirectedGraph(vertices)

    while graph._edges < edges:
        u = random.randrange(vertices)
        v = random.randrange(vertices)

        if graph.isEdge(u, v):
            continue

        cost = random.randint(minCost, maxCost)
        graph.addEdge(u, v, cost)

    return graph
