from __future__ import annotations

from io import TextIOWrapper
from pathlib import Path
from zipfile import ZipFile

from src.domain.graph import Graph


def read_graph(file_name: str, directed: bool = True) -> Graph:
    path = Path(file_name)
    lines = _read_lines(path)
    if not lines:
        raise ValueError("The input file is empty")

    header = lines[0].split()
    if len(header) != 2:
        raise ValueError("The first line must contain the number of vertices and edges")

    vertices, edges = map(int, header)
    graph = Graph(vertices, directed=directed)

    if len(lines) - 1 < edges:
        raise ValueError("The input file ended before all edges were read")

    for line in lines[1:edges + 1]:
        parts = line.split()
        if len(parts) != 3:
            raise ValueError("Each edge line must contain start, end and cost")

        u, v, cost = map(int, parts)
        graph.add_edge(u, v, cost)

    return graph


def write_graph(file_name: str, graph: Graph) -> None:
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        handle.write(f"{graph.vertex_count()} {graph.edge_count()}\n")
        for (u, v), cost in graph.parse_edges():
            handle.write(f"{u} {v} {cost}\n")


def _read_lines(path: Path) -> list[str]:
    if path.suffix == ".zip":
        return _read_lines_from_zip(path)

    with path.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def _read_lines_from_zip(path: Path) -> list[str]:
    with ZipFile(path, "r") as archive:
        members = [name for name in archive.namelist() if not name.endswith("/")]
        if not members:
            raise ValueError("The zip archive does not contain a graph file")

        member_name = sorted(members)[0]
        with archive.open(member_name, "r") as raw_handle:
            handle = TextIOWrapper(raw_handle, encoding="utf-8")
            return [line.strip() for line in handle if line.strip()]
