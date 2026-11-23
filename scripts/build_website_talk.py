#!/usr/bin/env python3
"""Render the Osaka talk into an existing website checkout."""

import argparse
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit


class ResourceParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if not value or value.startswith("data:"):
                continue
            if key in {"src", "data-src", "poster"} or (tag == "link" and key == "href"):
                url = urlsplit(value)
                if url.scheme or url.netloc or url.path:
                    raise RuntimeError(f"Resource is not embedded: {value}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--website-dir", required=True, type=Path,
                        help="Existing checkout of the website branch")
    parser.add_argument("--destination", default="talks/osaka_talk_2026",
                        help="Directory relative to the website root")
    args = parser.parse_args()

    site = args.website_dir.resolve()
    relative = PurePosixPath(args.destination)
    if relative.is_absolute() or not relative.parts or any(
        part.startswith(".") for part in relative.parts
    ):
        parser.error("destination must be a non-hidden subdirectory within the website")
    destination = site.joinpath(*relative.parts)
    if not site.is_dir() or not (site / ".git").exists():
        parser.error("website-dir must be a Git checkout")
    if destination.resolve() != destination:
        parser.error("destination must not traverse symbolic links")

    source = Path(__file__).resolve().parents[1]
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        parser.error("destination must be separate from the talk source")

    # Build with the same project settings as a local render, without using local output.
    with tempfile.TemporaryDirectory(prefix="osaka-talk-") as temporary:
        build = Path(temporary)
        for name in ("_quarto.yml", "talk.qmd", "theme.scss", "styles.css"):
            shutil.copy2(source / name, build / name)
        shutil.copytree(source / "assets", build / "assets")
        subprocess.run(["quarto", "render"], cwd=build, check=True)

        rendered = build / "_output" / "index.html"
        ResourceParser().feed(rendered.read_text(encoding="utf-8"))
        destination.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".build-", dir=destination) as staging:
            staged = Path(staging) / "index.html"
            shutil.copyfile(rendered, staged)
            staged.replace(destination / "index.html")

    print(f"Compiled talk written to {destination / 'index.html'}")


if __name__ == "__main__":
    main()
