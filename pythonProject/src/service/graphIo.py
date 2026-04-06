from __future__ import annotations

from io import TextIOWrapper
from pathlib import Path
from zipfile import ZipFile

from src.domain.graph import UndirectedGraph


def readGraph(fileName: str) -> UndirectedGraph:
    path = Path(fileName)
    lines = _readLines(path)
    if not lines:
        raise ValueError("The input file is empty")

    header = lines[0].split()
    if len(header) != 2:
        raise ValueError("The first line must contain the number of vertices and edges")

    vertices, edges = map(int, header)
    graph = UndirectedGraph(vertices)

    if len(lines) - 1 < edges:
        raise ValueError("The input file ended before all edges were read")

    for line in lines[1:edges + 1]:
        parts = line.split()
        if len(parts) != 3:
            raise ValueError("Each edge line must contain start, end and cost")

        u, v, cost = map(int, parts)
        graph.addEdge(u, v, cost)

    return graph


def writeGraph(fileName: str, graph: UndirectedGraph) -> None:
    path = Path(fileName)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        handle.write(f"{graph.vertexCount()} {graph.edgeCount()}\n")
        for (u, v), cost in graph.parseEdges():
            handle.write(f"{u} {v} {cost}\n")


def _readLines(path: Path) -> list[str]:
    if path.suffix == ".zip":
        return _readLinesFromZip(path)

    with path.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def _readLinesFromZip(path: Path) -> list[str]:
    with ZipFile(path, "r") as archive:
        members = [name for name in archive.namelist() if not name.endswith("/")]
        if not members:
            raise ValueError("The zip archive does not contain a graph file")

        memberName = sorted(members)[0]
        with archive.open(memberName, "r") as rawHandle:
            handle = TextIOWrapper(rawHandle, encoding="utf-8")
            return [line.strip() for line in handle if line.strip()]
