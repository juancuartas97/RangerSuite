#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIRECTORIES = (
    ROOT / "mockups" / "updated-pages",
    ROOT / "mockups" / "user-management-portal",
)
STYLESHEET_RE = re.compile(
    r'(?m)^(?P<indent>[ \t]*)<link rel="stylesheet" href="styles\.css"\s*/>\s*$'
)
HTML_REF_RE = re.compile(r'(["\'])([^"\']+\.html)(\1)')


def indent_block(text: str, indent: str) -> str:
    return "\n".join(f"{indent}  {line}" if line else "" for line in text.splitlines())


def inline_styles(html: str, css: str | None) -> str:
    if css is None:
        return html

    def replacer(match: re.Match[str]) -> str:
        indent = match.group("indent")
        block = indent_block(css.rstrip(), indent)
        return f"{indent}<style>\n{block}\n{indent}</style>"

    return STYLESHEET_RE.sub(replacer, html, count=1)


def rewrite_html_refs(html: str, source_names: set[str], generated_names: set[str]) -> str:
    def replacer(match: re.Match[str]) -> str:
        quote, target = match.group(1), match.group(2)
        normalized = target.removeprefix("./")

        if normalized.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            return match.group(0)

        if normalized.startswith("downloads/"):
            basename = Path(normalized).name
            if basename in generated_names:
                return f"{quote}{basename}{quote}"
            return match.group(0)

        if "/" in normalized:
            return match.group(0)

        if normalized in source_names:
            return f"{quote}{Path(normalized).stem}-download.html{quote}"

        return match.group(0)

    return HTML_REF_RE.sub(replacer, html)


def export_directory(source_dir: Path) -> list[Path]:
    output_dir = source_dir / "downloads"
    output_dir.mkdir(parents=True, exist_ok=True)

    for stale_path in output_dir.glob("*-download.html"):
        stale_path.unlink()

    html_files = sorted(path for path in source_dir.glob("*.html") if path.is_file())
    source_names = {path.name for path in html_files}
    generated_names = {f"{path.stem}-download.html" for path in html_files}

    css_path = source_dir / "styles.css"
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else None

    written: list[Path] = []
    for html_path in html_files:
        html = html_path.read_text(encoding="utf-8")
        html = inline_styles(html, css)
        html = rewrite_html_refs(html, source_names, generated_names)

        output_path = output_dir / f"{html_path.stem}-download.html"
        output_path.write_text(html, encoding="utf-8")
        written.append(output_path.relative_to(ROOT))

    return written


def main() -> int:
    written: list[Path] = []
    for source_dir in EXPORT_DIRECTORIES:
        written.extend(export_directory(source_dir))

    print("Exported download-ready HTML:")
    for path in written:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
