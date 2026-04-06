from __future__ import annotations

import unittest

from src.domain.graph import Graph


class GraphTest(unittest.TestCase):
    def test_undirected_edges_are_available_in_both_directions(self) -> None:
        graph = Graph(3, directed=False)
        graph.add_edge(0, 2, 7)
        self.assertTrue(graph.is_edge(0, 2))
        self.assertTrue(graph.is_edge(2, 0))
        self.assertEqual(1, graph.edge_count())

    def test_subgraph_preserves_original_vertex_ids(self) -> None:
        graph = Graph(5, directed=True)
        graph.add_edge(0, 1, 3)
        graph.add_edge(1, 4, 2)
        graph.add_edge(2, 3, 9)

        subgraph = graph.subgraph([0, 1, 4])
        self.assertEqual([0, 1, 4], subgraph.parse_vertices())
        self.assertEqual(2, subgraph.edge_count())

    def test_remove_vertex_removes_its_incident_edges(self) -> None:
        graph = Graph(4, directed=False)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 3, 3)

        graph.remove_vertex(1)

        self.assertEqual([0, 2, 3], graph.parse_vertices())
        self.assertEqual(1, graph.edge_count())


if __name__ == "__main__":
    unittest.main()
