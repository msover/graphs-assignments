from __future__ import annotations

from pathlib import Path
from textwrap import wrap


PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT_MARGIN = 48
TOP_MARGIN = 790
LINE_HEIGHT = 14
MAX_TEXT_WIDTH = 90
LINES_PER_PAGE = 52


def build_pdf_from_text(source: Path, target: Path) -> None:
    text = source.read_text(encoding="utf-8")
    lines = _prepare_lines(text)
    pages = [lines[index:index + LINES_PER_PAGE] for index in range(0, len(lines), LINES_PER_PAGE)]
    pdf_bytes = _build_pdf_bytes(pages)
    target.write_bytes(pdf_bytes)


def _prepare_lines(text: str) -> list[str]:
    prepared_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.expandtabs(4)
        if not line:
            prepared_lines.append("")
            continue

        wrapped = wrap(line, width=MAX_TEXT_WIDTH, replace_whitespace=False, drop_whitespace=False)
        prepared_lines.extend(wrapped or [""])

    return prepared_lines or [""]


def _build_pdf_bytes(pages: list[list[str]]) -> bytes:
    objects: list[str] = []
    font_object_number = 3 + 2 * len(pages)
    page_object_numbers = [3 + 2 * index for index in range(len(pages))]
    content_object_numbers = [number + 1 for number in page_object_numbers]

    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{number} 0 R" for number in page_object_numbers)
    objects.append(f"<< /Type /Pages /Count {len(pages)} /Kids [{kids}] >>")

    for page_number, lines in zip(page_object_numbers, pages, strict=True):
        content_number = page_number + 1
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_object_number} 0 R >> >> /Contents {content_number} 0 R >>"
        )
        stream = _content_stream(lines)
        objects.append(f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream")

    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    result = ["%PDF-1.4\n"]
    offsets = [0]
    current_offset = len(result[0].encode("latin-1"))

    for index, obj in enumerate(objects, start=1):
        offsets.append(current_offset)
        serialized = f"{index} 0 obj\n{obj}\nendobj\n"
        result.append(serialized)
        current_offset += len(serialized.encode("latin-1"))

    xref_offset = current_offset
    xref = [f"xref\n0 {len(objects) + 1}\n", "0000000000 65535 f \n"]
    for offset in offsets[1:]:
        xref.append(f"{offset:010d} 00000 n \n")

    trailer = (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    )

    result.extend(xref)
    result.append(trailer)
    return "".join(result).encode("latin-1", errors="replace")


def _content_stream(lines: list[str]) -> str:
    content = ["BT", "/F1 10 Tf", f"{LEFT_MARGIN} {TOP_MARGIN} Td", f"{LINE_HEIGHT} TL"]
    for line in lines:
        content.append(f"({_escape_pdf_text(line)}) Tj")
        content.append("T*")
    content.append("ET")
    return "\n".join(content)


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    docs_dir = base_dir / "docs"

    targets = [
        "manual_execution_problem4",
    ]

    for name in targets:
        build_pdf_from_text(docs_dir / f"{name}.md", docs_dir / f"{name}.pdf")


if __name__ == "__main__":
    main()
