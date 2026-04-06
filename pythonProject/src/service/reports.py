from __future__ import annotations

from pathlib import Path

from src.service.algorithms import (
    format_path,
    lowest_length_path_backward_bfs,
    lowest_length_path_forward_bfs,
)
from src.service.graph_io import read_graph


def generate_large_graph_report(input_dir: str, output_file: str) -> Path:
    input_path = Path(input_dir)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report_lines = [
        "# Large Graph Path Results",
        "",
        "Queries: 1 -> 100 and 100 -> 1.",
        "",
    ]

    datasets = {
        "graph1k": ["graph1k.txt", "graph1k.zip"],
        "graph10k": ["graph10k.txt", "graph10k.zip"],
        "graph100k": ["graph100k.zip", "graph100k.txt"],
    }

    for label, candidates in datasets.items():
        source = _find_dataset_file(input_path, candidates)
        report_lines.append(f"## {label}")
        report_lines.append("")

        if source is None:
            report_lines.append("Dataset not found.")
            report_lines.append("")
            continue

        graph = read_graph(str(source), directed=True)
        report_lines.extend(_path_section(graph, "Forward BFS", lowest_length_path_forward_bfs))
        report_lines.extend(_path_section(graph, "Backward BFS", lowest_length_path_backward_bfs))
        report_lines.append(f"Source file: `{source.name}`")
        report_lines.append("")

    output_path.write_text("\n".join(report_lines), encoding="utf-8")
    return output_path


def _find_dataset_file(base_dir: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = base_dir / candidate
        if path.exists():
            return path
    return None


def _path_section(graph, title: str, algorithm) -> list[str]:
    lines = [f"### {title}", ""]
    for start, end in ((1, 100), (100, 1)):
        path, length = algorithm(graph, start, end)
        lines.append(f"- {start} -> {end}: length = {length}; path = {format_path(path)}")
    lines.append("")
    return lines
