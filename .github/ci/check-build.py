#!/usr/bin/env python3
"""Check the final LaTeX logs and both PDFs after latexmk has converged."""

import argparse
from pathlib import Path
import re
import sys


# Do not reject every warning: unicode-math, empty optional bibliographies,
# and overfull/underfull boxes need not indicate a broken document.
ERRORS = re.compile(
    r"^![^\n]*"
    r"|(?:LaTeX|Package [\w-]+|Class [\w-]+) Error:[^\n]*"
    r"|(?:Fatal error|Emergency stop|Undefined control sequence|Missing character:)[^\n]*"
    r"|(?:LaTeX|Package [\w-]+) Warning:\s*(?:Reference|Citation)\b"
    r"(?:(?!\n\s*\n).)*?\bundefined\b[^\n]*"
    r"|LaTeX Warning: There were undefined (?:references|citations)[^\n]*",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
DUPLICATE = re.compile(r"LaTeX Warning: Label `([^']+)'\s+multiply\s+defined\.")
DUPLICATE_SUMMARY = re.compile(r"LaTeX Warning: There were multiply-defined labels\.")
# xr-hyper imports dissertation.aux into synopsis. biblatex and totpages also
# create these exact bookkeeping labels locally; user labels are never exempt.
IMPORTED_LABEL = re.compile(r"(?:TotPages|refsection:\d+(?:@cref)?)")


def check_log(log, allow_imported_labels=False):
    matches = list(ERRORS.finditer(log))
    duplicates = list(DUPLICATE.finditer(log))
    matches.extend(match for match in duplicates
                   if not (allow_imported_labels and IMPORTED_LABEL.fullmatch(match.group(1))))
    # An unexplained summary still fails: do not silently ignore an unfamiliar
    # duplicate-warning format when no individual labels could be parsed.
    if not duplicates:
        matches.extend(DUPLICATE_SUMMARY.finditer(log))
    return [(log.count("\n", 0, match.start()) + 1, " ".join(match.group().split()))
            for match in sorted(matches, key=lambda match: match.start())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir", type=Path, help="directory containing final PDFs and logs")
    directory = parser.parse_args().build_dir
    problems = []
    for name in ("dissertation", "synopsis"):
        for extension in ("pdf", "log"):
            path = directory / f"{name}.{extension}"
            if not path.is_file() or path.stat().st_size == 0:
                problems.append(f"{path}: missing or empty file")
                continue
            if extension == "log":
                log = path.read_text(encoding="utf-8", errors="replace")
                for line, message in check_log(log, allow_imported_labels=name == "synopsis"):
                    problems.append(f"{path}:{line}: {message}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"Both PDFs and final LaTeX logs passed checks in {directory}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
