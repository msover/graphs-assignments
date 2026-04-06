from __future__ import annotations

from src.domain.graph import UndirectedGraph
from src.service.components import connectedComponentsBfs
from src.service.graphIo import readGraph, writeGraph
from src.service.randomGraph import makeRandomGraph


class ConsoleMenu:
    def __init__(self, graph: UndirectedGraph | None = None):
        self._graph = graph if graph is not None else UndirectedGraph()
        self._backup: UndirectedGraph | None = None

    def run(self) -> None:
        while True:
            self._printMenu()
            option = input("Choose an option: ").strip()

            if option == "0":
                print("Exiting application.")
                return

            try:
                self._handleOption(option)
            except ValueError as error:
                print(f"Error: {error}")
            except FileNotFoundError as error:
                print(f"File error: {error}")

            print()

    def _printMenu(self) -> None:
        print("Undirected Graph Console")
        print("1. Load graph from file")
        print("2. Save graph to file")
        print("3. Generate random graph")
        print("4. Show graph summary")
        print("5. List all vertices")
        print("6. Inspect a vertex")
        print("7. Check whether an edge exists")
        print("8. View an edge cost")
        print("9. Update an edge cost")
        print("10. Add a vertex")
        print("11. Remove a vertex")
        print("12. Add an edge")
        print("13. Remove an edge")
        print("14. Copy current graph to backup")
        print("15. Restore graph from backup copy")
        print("16. Print all edges")
        print("17. Connected components by BFS")
        print("0. Exit")

    def _handleOption(self, option: str) -> None:
        actions = {
            "1": self._loadGraph,
            "2": self._saveGraph,
            "3": self._generateRandomGraph,
            "4": self._showSummary,
            "5": self._listVertices,
            "6": self._inspectVertex,
            "7": self._checkEdge,
            "8": self._showEdgeCost,
            "9": self._updateEdgeCost,
            "10": self._addVertex,
            "11": self._removeVertex,
            "12": self._addEdge,
            "13": self._removeEdge,
            "14": self._backupGraph,
            "15": self._restoreGraph,
            "16": self._printEdges,
            "17": self._runComponentsBfs,
        }

        action = actions.get(option)
        if action is None:
            raise ValueError("Unknown menu option")

        action()

    def _loadGraph(self) -> None:
        fileName = input("File name: ").strip()
        self._graph = readGraph(fileName)
        print(f"Loaded undirected graph from {fileName}.")

    def _saveGraph(self) -> None:
        fileName = input("File name: ").strip()
        writeGraph(fileName, self._graph)
        print(f"Saved graph to {fileName}.")

    def _generateRandomGraph(self) -> None:
        vertices = self._readInt("Number of vertices: ")
        edges = self._readInt("Number of edges: ")
        minCost = self._readInt("Minimum edge cost: ")
        maxCost = self._readInt("Maximum edge cost: ")
        self._graph = makeRandomGraph(vertices, edges, minCost, maxCost)
        print("Random graph generated.")

    def _showSummary(self) -> None:
        print("Type: undirected")
        print(f"Vertices: {self._graph.vertexCount()}")
        print(f"Edges: {self._graph.edgeCount()}")

    def _listVertices(self) -> None:
        vertices = self._graph.parseVertices()
        if not vertices:
            print("The graph has no vertices.")
            return

        print("Vertices:", " ".join(str(vertex) for vertex in vertices))

    def _inspectVertex(self) -> None:
        vertex = self._readInt("Vertex: ")
        neighbors = self._graph.parseNeighbors(vertex)
        print(f"Degree: {self._graph.degree(vertex)}")
        print("Neighbors:", self._formatCollection(neighbors))

    def _checkEdge(self) -> None:
        u, v = self._readEdge()
        exists = self._graph.isEdge(u, v)
        print(f"Edge {u} -- {v} exists: {'yes' if exists else 'no'}")

    def _showEdgeCost(self) -> None:
        u, v = self._readEdge()
        print(f"Edge cost: {self._graph.getEdgeCost(u, v)}")

    def _updateEdgeCost(self) -> None:
        u, v = self._readEdge()
        cost = self._readInt("New cost: ")
        self._graph.setEdgeCost(u, v, cost)
        print("Edge cost updated.")

    def _addVertex(self) -> None:
        answer = input("Vertex id (leave empty for automatic): ").strip()
        vertex = self._graph.addVertex(None if answer == "" else int(answer))
        print(f"Added vertex {vertex}.")

    def _removeVertex(self) -> None:
        vertex = self._readInt("Vertex to remove: ")
        self._graph.removeVertex(vertex)
        print(f"Removed vertex {vertex}.")

    def _addEdge(self) -> None:
        u, v = self._readEdge()
        cost = self._readInt("Cost: ")
        self._graph.addEdge(u, v, cost)
        print("Edge added.")

    def _removeEdge(self) -> None:
        u, v = self._readEdge()
        self._graph.removeEdge(u, v)
        print("Edge removed.")

    def _backupGraph(self) -> None:
        self._backup = self._graph.copyGraph()
        print("Backup copy created.")

    def _restoreGraph(self) -> None:
        if self._backup is None:
            raise ValueError("No backup graph is available")

        self._graph = self._backup.copyGraph()
        print("Graph restored from backup.")

    def _printEdges(self) -> None:
        edges = self._graph.parseEdges()
        if not edges:
            print("The graph has no edges.")
            return

        for (u, v), cost in edges:
            print(f"{u} -- {v} (cost = {cost})")

    def _runComponentsBfs(self) -> None:
        self._printComponents(connectedComponentsBfs(self._graph), "BFS")

    @staticmethod
    def _readInt(prompt: str) -> int:
        return int(input(prompt).strip())

    def _readEdge(self) -> tuple[int, int]:
        u = self._readInt("Start vertex: ")
        v = self._readInt("End vertex: ")
        return u, v

    @staticmethod
    def _formatCollection(values: list[int]) -> str:
        if not values:
            return "none"
        return " ".join(str(value) for value in values)

    @staticmethod
    def _printComponents(components: list[UndirectedGraph], method: str) -> None:
        print(f"Connected components found by {method}: {len(components)}")
        for index, component in enumerate(components, start=1):
            print(
                f"{index}. vertices = {component.parseVertices()}, "
                f"edges = {component.edgeCount()}"
            )
