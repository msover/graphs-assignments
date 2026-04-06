from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from src.domain.graph import UndirectedGraph
from src.service.components import connectedComponentsBfs
from src.service.graphIo import readGraph


class ComponentsTest(unittest.TestCase):
    def testConnectedComponentsBfsFindsThreeComponents(self) -> None:
        graph = readGraph("data/manual/undirectedComponents1.txt")
        components = connectedComponentsBfs(graph)
        componentVertices = [component.parseVertices() for component in components]
        self.assertEqual([[0, 1, 2, 3], [4, 5, 6], [7]], componentVertices)

    def testConnectedComponentsBfsFindsOneComponent(self) -> None:
        graph = readGraph("data/manual/undirectedComponents2.txt")
        components = connectedComponentsBfs(graph)
        componentVertices = [component.parseVertices() for component in components]
        self.assertEqual([[0, 1, 2, 3, 4, 5]], componentVertices)

    def testIsolatedVerticesBecomeSingleVertexComponents(self) -> None:
        graph = UndirectedGraph(3)
        components = connectedComponentsBfs(graph)
        componentVertices = [component.parseVertices() for component in components]
        self.assertEqual([[0], [1], [2]], componentVertices)

    def testZipGraphInputIsSupported(self) -> None:
        with tempfile.TemporaryDirectory() as tempDir:
            zipPath = Path(tempDir) / "graph.zip"
            with ZipFile(zipPath, "w") as archive:
                archive.write("data/manual/undirectedComponents1.txt", arcname="graph.txt")

            graph = readGraph(str(zipPath))
            self.assertEqual(8, graph.vertexCount())
            self.assertEqual(8, graph.edgeCount())


if __name__ == "__main__":
    unittest.main()
