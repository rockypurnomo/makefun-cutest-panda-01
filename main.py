"""make.fun cutest-picture-01 entry: the baby panda picture.

This entry is a single bundled picture, so the program has exactly
one job: carry the bytes of that picture to the judging output
location, completely untouched, and prove the copy arrived whole.
"""

import os
import shutil
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
FALLBACK_OUTPUT_DIR = "/output"


def picture_source() -> Path:
    # The picture travels beside this file inside the repository
    # snapshot, so resolve it from this file's own location and
    # never from whatever directory the process happens to sit in.
    return Path(__file__).resolve().parent / PICTURE_NAME


def chosen_output_dir() -> Path:
    configured = os.environ.get(OUTPUT_ENV_VAR, "").strip()
    if configured:
        return Path(configured)
    return Path(FALLBACK_OUTPUT_DIR)


def deliver_picture() -> Path:
    source = picture_source()
    target = chosen_output_dir() / PICTURE_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target


def verify_delivery(target: Path) -> None:
    # Compare content, not just length: the grading runs must agree
    # byte for byte, so a same-sized but altered copy is as much a
    # failure as a truncated one, and both abort before judging.
    bundled_bytes = picture_source().read_bytes()
    written_bytes = target.read_bytes()
    if written_bytes != bundled_bytes:
        raise SystemExit(
            f"incomplete copy: {target} holds {len(written_bytes)} bytes "
            f"that differ from the bundled picture's {len(bundled_bytes)}"
        )


def main() -> int:
    written = deliver_picture()
    verify_delivery(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
