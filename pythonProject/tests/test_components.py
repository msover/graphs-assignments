from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from src.domain.graph import UndirectedGraph
from src.service.components import connected_components_bfs
from src.service.graph_io import read_graph


class ComponentsTest(unittest.TestCase):
    def test_connected_components_bfs_finds_three_components(self) -> None:
        graph = read_graph("data/manual/undirected_components_1.txt")
        components = connected_components_bfs(graph)
        component_vertices = [component.parse_vertices() for component in components]
        self.assertEqual([[0, 1, 2, 3], [4, 5, 6], [7]], component_vertices)

    def test_connected_components_bfs_finds_one_component(self) -> None:
        graph = read_graph("data/manual/undirected_components_2.txt")
        components = connected_components_bfs(graph)
        component_vertices = [component.parse_vertices() for component in components]
        self.assertEqual([[0, 1, 2, 3, 4, 5]], component_vertices)

    def test_isolated_vertices_become_single_vertex_components(self) -> None:
        graph = UndirectedGraph(3)
        components = connected_components_bfs(graph)
        component_vertices = [component.parse_vertices() for component in components]
        self.assertEqual([[0], [1], [2]], component_vertices)

    def test_zip_graph_input_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "graph.zip"
            with ZipFile(zip_path, "w") as archive:
                archive.write("data/manual/undirected_components_1.txt", arcname="graph.txt")

            graph = read_graph(str(zip_path))
            self.assertEqual(8, graph.vertex_count())
            self.assertEqual(8, graph.edge_count())


if __name__ == "__main__":
    unittest.main()
