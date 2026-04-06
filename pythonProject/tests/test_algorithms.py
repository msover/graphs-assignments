from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from src.domain.graph import Graph
from src.service.algorithms import (
    connected_components_bfs,
    connected_components_dfs,
    lowest_length_path_backward_bfs,
    lowest_length_path_forward_bfs,
)
from src.service.graph_io import read_graph


class AlgorithmsTest(unittest.TestCase):
    def test_forward_bfs_finds_a_shortest_path(self) -> None:
        graph = read_graph("data/manual/directed_manual_1.txt", directed=True)
        path, length = lowest_length_path_forward_bfs(graph, 0, 4)
        self.assertEqual([0, 1, 4], path)
        self.assertEqual(2, length)

    def test_backward_bfs_finds_a_shortest_path(self) -> None:
        graph = read_graph("data/manual/directed_manual_2.txt", directed=True)
        path, length = lowest_length_path_backward_bfs(graph, 3, 0)
        self.assertEqual([3, 1, 2, 0], path)
        self.assertEqual(3, length)

    def test_shortest_path_reports_missing_path(self) -> None:
        graph = Graph(3, directed=True)
        graph.add_edge(0, 1, 5)
        path, length = lowest_length_path_forward_bfs(graph, 1, 0)
        self.assertEqual([], path)
        self.assertEqual(-1, length)

    def test_connected_components_dfs(self) -> None:
        graph = read_graph("data/manual/undirected_components_1.txt", directed=False)
        components = connected_components_dfs(graph)
        component_vertices = [component.parse_vertices() for component in components]
        self.assertEqual([[0, 1, 2, 3], [4, 5, 6], [7]], component_vertices)

    def test_connected_components_bfs(self) -> None:
        graph = read_graph("data/manual/undirected_components_1.txt", directed=False)
        components = connected_components_bfs(graph)
        component_vertices = [component.parse_vertices() for component in components]
        self.assertEqual([[0, 1, 2, 3], [4, 5, 6], [7]], component_vertices)

    def test_zip_graph_input_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "graph.zip"
            with ZipFile(zip_path, "w") as archive:
                archive.write("data/manual/directed_manual_1.txt", arcname="graph.txt")

            graph = read_graph(str(zip_path), directed=True)
            self.assertEqual(5, graph.vertex_count())
            self.assertEqual(10, graph.edge_count())


if __name__ == "__main__":
    unittest.main()
