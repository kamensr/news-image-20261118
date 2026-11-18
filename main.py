#!/usr/bin/env python3
"""news-image-20261118: copy the entry image to the output directory.

The entry image (entry.png, in this repository) is a news poster summing up
the world news of Wednesday 18 November 2026. The grader runs this program
twice with no network; both runs must write the same bytes, so this is a
plain copy of a fixed file.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main():
    if not SOURCE.is_file():
        raise SystemExit(f"entry image missing: {SOURCE}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, out_dir / "entry.png")


if __name__ == "__main__":
    main()
