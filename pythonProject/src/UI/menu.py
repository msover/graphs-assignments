from src.domain.DirectedGraph import DirectedGraph
from src.service.GraphIO import readGraph, writeGraph
from src.service.randomGraphMaker import makeRandomGraph


class ConsoleMenu:
    def __init__(self, graph: DirectedGraph | None = None):
        self._graph = graph if graph is not None else DirectedGraph()
        self._backup = None

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
        print("Directed Graph Console")
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
        }

        action = actions.get(option)
        if action is None:
            raise ValueError("Unknown menu option")

        action()

    def _loadGraph(self) -> None:
        fileName = input("File name: ").strip()
        self._graph = readGraph(fileName)
        print(f"Loaded graph from {fileName}.")

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
        print(f"Vertices: {self._graph.getVertices()}")
        print(f"Edges: {self._graph.getEdges()}")

    def _listVertices(self) -> None:
        vertices = self._graph.parseVertices()
        if not vertices:
            print("The graph has no vertices.")
            return

        print("Vertices:", " ".join(str(vertex) for vertex in vertices))

    def _inspectVertex(self) -> None:
        vertex = self._readInt("Vertex: ")
        inbound = self._graph.parseInboundNeighbors(vertex)
        outbound = self._graph.parseOutboundNeighbors(vertex)

        print(f"In-degree: {self._graph.getInDegree(vertex)}")
        print(f"Out-degree: {self._graph.getOutDegree(vertex)}")
        print("Inbound neighbors:", self._formatCollection(inbound))
        print("Outbound neighbors:", self._formatCollection(outbound))

    def _checkEdge(self) -> None:
        u, v = self._readEdge()
        exists = self._graph.isEdge(u, v)
        print(f"Edge {u} -> {v} exists: {'yes' if exists else 'no'}")

    def _showEdgeCost(self) -> None:
        u, v = self._readEdge()
        print(f"Cost of {u} -> {v}: {self._graph.getEdgeCost(u, v)}")

    def _updateEdgeCost(self) -> None:
        u, v = self._readEdge()
        cost = self._readInt("New cost: ")
        self._graph.setEdgeCost(u, v, cost)
        print("Edge cost updated.")

    def _addVertex(self) -> None:
        vertex = self._graph.addVertex()
        print(f"Added vertex {vertex}.")

    def _removeVertex(self) -> None:
        vertex = self._readInt("Vertex to remove: ")
        self._graph.removeVertex(vertex)
        print(f"Removed vertex {vertex}.")

    def _addEdge(self) -> None:
        u, v = self._readEdge()
        cost = self._readInt("Cost: ")
        self._graph.addEdge(u, v, cost)
        print(f"Added edge {u} -> {v}.")

    def _removeEdge(self) -> None:
        u, v = self._readEdge()
        self._graph.removeEdge(u, v)
        print(f"Removed edge {u} -> {v}.")

    def _backupGraph(self) -> None:
        self._backup = self._graph.copyGraph()
        print("Backup copy created.")

    def _restoreGraph(self) -> None:
        if self._backup is None:
            raise ValueError("No backup graph is available")

        self._graph = self._backup.copyGraph()
        print("Graph restored from backup.")

    def _printEdges(self) -> None:
        costs = self._graph.getCosts()
        if not costs:
            print("The graph has no edges.")
            return

        for (u, v), cost in sorted(costs.items()):
            print(f"{u} -> {v} (cost = {cost})")

    @staticmethod
    def _readInt(prompt: str) -> int:
        return int(input(prompt).strip())

    def _readEdge(self) -> tuple[int, int]:
        u = self._readInt("Start vertex: ")
        v = self._readInt("End vertex: ")
        return u, v

    @staticmethod
    def _formatCollection(values) -> str:
        if not values:
            return "none"
        return " ".join(str(value) for value in values)
