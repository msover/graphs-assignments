from __future__ import annotations

from src.domain.graph import UndirectedGraph
from src.service.components import connected_components_bfs
from src.service.graph_io import read_graph, write_graph
from src.service.random_graph import make_random_graph


class ConsoleMenu:
    def __init__(self, graph: UndirectedGraph | None = None):
        self._graph = graph if graph is not None else UndirectedGraph()
        self._backup: UndirectedGraph | None = None

    def run(self) -> None:
        while True:
            self._print_menu()
            option = input("Choose an option: ").strip()

            if option == "0":
                print("Exiting application.")
                return

            try:
                self._handle_option(option)
            except ValueError as error:
                print(f"Error: {error}")
            except FileNotFoundError as error:
                print(f"File error: {error}")

            print()

    def _print_menu(self) -> None:
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

    def _handle_option(self, option: str) -> None:
        actions = {
            "1": self._load_graph,
            "2": self._save_graph,
            "3": self._generate_random_graph,
            "4": self._show_summary,
            "5": self._list_vertices,
            "6": self._inspect_vertex,
            "7": self._check_edge,
            "8": self._show_edge_cost,
            "9": self._update_edge_cost,
            "10": self._add_vertex,
            "11": self._remove_vertex,
            "12": self._add_edge,
            "13": self._remove_edge,
            "14": self._backup_graph,
            "15": self._restore_graph,
            "16": self._print_edges,
            "17": self._run_components_bfs,
        }

        action = actions.get(option)
        if action is None:
            raise ValueError("Unknown menu option")

        action()

    def _load_graph(self) -> None:
        file_name = input("File name: ").strip()
        self._graph = read_graph(file_name)
        print(f"Loaded undirected graph from {file_name}.")

    def _save_graph(self) -> None:
        file_name = input("File name: ").strip()
        write_graph(file_name, self._graph)
        print(f"Saved graph to {file_name}.")

    def _generate_random_graph(self) -> None:
        vertices = self._read_int("Number of vertices: ")
        edges = self._read_int("Number of edges: ")
        min_cost = self._read_int("Minimum edge cost: ")
        max_cost = self._read_int("Maximum edge cost: ")
        self._graph = make_random_graph(vertices, edges, min_cost, max_cost)
        print("Random graph generated.")

    def _show_summary(self) -> None:
        print("Type: undirected")
        print(f"Vertices: {self._graph.vertex_count()}")
        print(f"Edges: {self._graph.edge_count()}")

    def _list_vertices(self) -> None:
        vertices = self._graph.parse_vertices()
        if not vertices:
            print("The graph has no vertices.")
            return

        print("Vertices:", " ".join(str(vertex) for vertex in vertices))

    def _inspect_vertex(self) -> None:
        vertex = self._read_int("Vertex: ")
        neighbors = self._graph.parse_neighbors(vertex)
        print(f"Degree: {self._graph.degree(vertex)}")
        print("Neighbors:", self._format_collection(neighbors))

    def _check_edge(self) -> None:
        u, v = self._read_edge()
        exists = self._graph.is_edge(u, v)
        print(f"Edge {u} -- {v} exists: {'yes' if exists else 'no'}")

    def _show_edge_cost(self) -> None:
        u, v = self._read_edge()
        print(f"Edge cost: {self._graph.get_edge_cost(u, v)}")

    def _update_edge_cost(self) -> None:
        u, v = self._read_edge()
        cost = self._read_int("New cost: ")
        self._graph.set_edge_cost(u, v, cost)
        print("Edge cost updated.")

    def _add_vertex(self) -> None:
        answer = input("Vertex id (leave empty for automatic): ").strip()
        vertex = self._graph.add_vertex(None if answer == "" else int(answer))
        print(f"Added vertex {vertex}.")

    def _remove_vertex(self) -> None:
        vertex = self._read_int("Vertex to remove: ")
        self._graph.remove_vertex(vertex)
        print(f"Removed vertex {vertex}.")

    def _add_edge(self) -> None:
        u, v = self._read_edge()
        cost = self._read_int("Cost: ")
        self._graph.add_edge(u, v, cost)
        print("Edge added.")

    def _remove_edge(self) -> None:
        u, v = self._read_edge()
        self._graph.remove_edge(u, v)
        print("Edge removed.")

    def _backup_graph(self) -> None:
        self._backup = self._graph.copy_graph()
        print("Backup copy created.")

    def _restore_graph(self) -> None:
        if self._backup is None:
            raise ValueError("No backup graph is available")

        self._graph = self._backup.copy_graph()
        print("Graph restored from backup.")

    def _print_edges(self) -> None:
        edges = self._graph.parse_edges()
        if not edges:
            print("The graph has no edges.")
            return

        for (u, v), cost in edges:
            print(f"{u} -- {v} (cost = {cost})")

    def _run_components_bfs(self) -> None:
        self._print_components(connected_components_bfs(self._graph), "BFS")

    @staticmethod
    def _read_int(prompt: str) -> int:
        return int(input(prompt).strip())

    def _read_edge(self) -> tuple[int, int]:
        u = self._read_int("Start vertex: ")
        v = self._read_int("End vertex: ")
        return u, v

    @staticmethod
    def _format_collection(values: list[int]) -> str:
        if not values:
            return "none"
        return " ".join(str(value) for value in values)

    @staticmethod
    def _print_components(components: list[UndirectedGraph], method: str) -> None:
        print(f"Connected components found by {method}: {len(components)}")
        for index, component in enumerate(components, start=1):
            print(
                f"{index}. vertices = {component.parse_vertices()}, "
                f"edges = {component.edge_count()}"
            )
