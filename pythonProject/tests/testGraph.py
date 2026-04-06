from __future__ import annotations

import unittest

from src.domain.graph import UndirectedGraph


class GraphTest(unittest.TestCase):
    def testUndirectedEdgesAreAvailableInBothDirections(self) -> None:
        graph = UndirectedGraph(3)
        graph.addEdge(0, 2, 7)
        self.assertTrue(graph.isEdge(0, 2))
        self.assertTrue(graph.isEdge(2, 0))
        self.assertEqual(1, graph.edgeCount())

    def testSubgraphPreservesOriginalVertexIds(self) -> None:
        graph = UndirectedGraph(5)
        graph.addEdge(0, 1, 3)
        graph.addEdge(1, 4, 2)

        subGraph = graph.subGraph([0, 1, 4])
        self.assertEqual([0, 1, 4], subGraph.parseVertices())
        self.assertEqual(2, subGraph.edgeCount())

    def testRemoveVertexRemovesItsIncidentEdges(self) -> None:
        graph = UndirectedGraph(4)
        graph.addEdge(0, 1, 1)
        graph.addEdge(1, 2, 2)
        graph.addEdge(2, 3, 3)

        graph.removeVertex(1)

        self.assertEqual([0, 2, 3], graph.parseVertices())
        self.assertEqual(1, graph.edgeCount())


if __name__ == "__main__":
    unittest.main()
