#!/usr/bin/env python3
"""Exercise the real Makefile's release contract without installing TeX."""

import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tarfile
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
DATE = "2001-02-03"
check_log = runpy.run_path(str(REPO / ".github/ci/check-build.py"))["check_log"]
LATEXMK = r'''#!/usr/bin/env python3
from pathlib import Path
import sys
import time

output = Path(next((arg.split("=", 1)[1] for arg in sys.argv[1:]
                    if arg.startswith("-outdir=")), "."))
name = Path(sys.argv[-1]).stem
output.mkdir(parents=True, exist_ok=True)
with Path("build-order.txt").open("a") as events:
    events.write(name + ":start\n")
if name == "dissertation":
    # Expose a missing make dependency even when make runs both jobs in parallel.
    time.sleep(0.1)
    (output / "thesis-stats.tex").write_text("fresh statistics\n")
elif name == "synopsis":
    if not (output / "dissertation.pdf").is_file():
        sys.exit("synopsis started before dissertation finished")
    if Path("thesis-stats.tex").read_text() != "fresh statistics\n":
        sys.exit("synopsis did not receive fresh dissertation statistics")
else:
    sys.exit("unexpected latexmk input: " + name)
(output / (name + ".pdf")).write_text("fixture PDF: " + name + "\n")
with Path("build-order.txt").open("a") as events:
    events.write(name + ":done\n")
'''


class BuildLogTests(unittest.TestCase):
    # Excerpts from the project's final synopsis.log, including its harmless
    # unicode-math warning and imported bookkeeping labels.
    LOG = r"""Package unicode-math Warning: I'm going to overwrite the following commands
(unicode-math)                from the `mathtools' package:

LaTeX Warning: Label `refsection:1' multiply defined.
LaTeX Warning: Label `refsection:1@cref' multiply defined.
LaTeX Warning: Label `refsection:2' multiply defined.
LaTeX Warning: Label `refsection:2@cref' multiply defined.
LaTeX Warning: Label `TotPages' multiply defined.
LaTeX Warning: There were multiply-defined labels.
Overfull \hbox (1.0pt too wide) in paragraph at lines 1--2
"""

    def test_only_imported_bookkeeping_labels_are_ignored(self):
        self.assertEqual(check_log(self.LOG, allow_imported_labels=True), [])
        for label in ("th:example", "eq:example", "TotPagesExtra", "refsection:x"):
            with self.subTest(label=label):
                issues = check_log(self.LOG.replace("`TotPages'", f"`{label}'"),
                                   allow_imported_labels=True)
                self.assertEqual(len(issues), 1)
                self.assertIn(label, issues[0][1])

    def test_dissertation_bookkeeping_duplicates_fail(self):
        issues = check_log(self.LOG)
        self.assertEqual(len(issues), 5)
        self.assertTrue(any("TotPages" in message for _, message in issues))
        self.assertTrue(any("refsection:1@cref" in message for _, message in issues))

    def test_unexplained_duplicate_summary_fails(self):
        self.assertTrue(check_log("LaTeX Warning: There were multiply-defined labels."))

    def test_document_errors_fail(self):
        for warning in (
            "LaTeX Warning: Reference `th:missing' on page 1 undefined on input line 2.",
            "LaTeX Warning: Citation `missing' on page 1\nundefined on input line 2.",
            "LaTeX Warning: There were undefined references.",
            "./source.tex:2: LaTeX Error: Something's wrong.",
            "!  ==> Fatal error occurred, no output PDF file produced!",
            "Missing character: There is no Ж (U+0416) in font Example!",
        ):
            with self.subTest(warning=warning):
                self.assertTrue(check_log(self.LOG + "\n" + warning, allow_imported_labels=True))


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="khod-release-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copyfile(REPO / "Makefile", self.root / "Makefile")
        self.sources = {
            "Makefile", "latexmkrc", "dissertation.tex", "synopsis.tex", "common/shared.tex"
        }
        for name in self.sources - {"Makefile"}:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"fixture source: {name}\n")
        for name in ("tracked.pdf", "fig/illustration.pdf"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"tracked PDF to exclude from the source archive")
        (self.root / "thesis-stats.tex").write_text("stale statistics\n")
        binaries = self.root / "test-bin"
        binaries.mkdir()
        for name, content in {
            "latexmk": LATEXMK,
            "date": f"#!/bin/sh\nprintf '%s\\n' '{DATE}'\n",
        }.items():
            path = binaries / name
            path.write_text(content)
            path.chmod(0o755)
        self.env = os.environ.copy()
        for name in ("BUILD_DIR", "MAKEFLAGS", "MFLAGS", "MAKELEVEL",
                     "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            self.env.pop(name, None)
        self.env["PATH"] = str(binaries) + os.pathsep + self.env["PATH"]
        self.run_command("git", "init", "--quiet")
        self.run_command("git", "add", "--", *sorted(self.sources),
                         "tracked.pdf", "fig/illustration.pdf")

    def run_command(self, *arguments):
        result = subprocess.run(arguments, cwd=self.root, env=self.env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout)
        return result.stdout

    def release(self, build_dir=None):
        arguments = ["make", "-j4", "release"]
        if build_dir:
            arguments.append(f"BUILD_DIR={build_dir}")
        self.run_command(*arguments)

    def assert_pair(self, suffix="", build_dir="."):
        for document, prefix in (("dissertation", "khod-disser"), ("synopsis", "khod-synopsis")):
            product = self.root / build_dir / f"{document}.pdf"
            released = self.root / "releases" / f"{prefix}-{DATE}{suffix}.pdf"
            self.assertEqual(product.read_text(), f"fixture PDF: {document}\n")
            self.assertEqual(released.read_bytes(), product.read_bytes())

    def assert_build_order(self):
        self.assertEqual((self.root / "build-order.txt").read_text().splitlines(), [
            "dissertation:start", "dissertation:done", "synopsis:start", "synopsis:done",
        ])

    def assert_source_archive(self, suffix=""):
        path = self.root / "releases" / f"archive-{DATE}{suffix}.tar.gz"
        with tarfile.open(path, "r:gz") as archive:
            names = set(archive.getnames())
            self.assertTrue(self.sources.issubset(names))
            self.assertFalse(any(name.endswith(".pdf") for name in names))
            for name in self.sources:
                self.assertEqual(archive.extractfile(name).read(), (self.root / name).read_bytes())

    def snapshot_releases(self):
        return {path.name: path.read_bytes() for path in (self.root / "releases").iterdir()}

    def assert_preserved(self, snapshot):
        for name, content in snapshot.items():
            self.assertEqual((self.root / "releases" / name).read_bytes(), content, name)

    def test_release_in_root(self):
        self.release()
        self.assert_pair()
        self.assert_build_order()
        self.assert_source_archive()

    def test_release_in_build_directory(self):
        self.release("build")
        self.assert_pair(build_dir="build")
        self.assert_build_order()
        self.assert_source_archive()
        for document in ("dissertation", "synopsis"):
            self.assertFalse((self.root / f"{document}.pdf").exists())

    def test_release_pdfs_does_not_archive_sources(self):
        self.run_command("make", "-j4", "release-pdfs", "BUILD_DIR=build")
        self.assert_pair(build_dir="build")
        self.assert_build_order()
        self.assertEqual(list(self.root.rglob("*.tar.gz")), [])

    def test_repeat_preserves_previous_release(self):
        self.release()
        previous = self.snapshot_releases()
        self.release()
        self.assert_preserved(previous)
        self.assert_pair("-1")
        self.assert_source_archive("-1")
        self.assert_build_order()  # Up-to-date PDFs must not be rebuilt.

    def release_with_failure(self, command):
        stub = self.root / "test-bin" / command
        message = f"simulated {command} failure"
        stub.write_text(f"#!/bin/sh\nprintf '%s\\n' '{message}' >&2\nexit 17\n")
        stub.chmod(0o755)
        # Without BUILD_DIR, cp is used only by release, not by statistics export.
        result = subprocess.run(["make", "-j4", "release"], cwd=self.root, env=self.env,
                                text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=30)
        self.assertIn(message, result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result.stdout

    def test_copy_failure_stops_before_archive(self):
        tar = self.root / "test-bin" / "tar"
        tar.write_text("#!/bin/sh\n: > tar-called\nexit 0\n")
        tar.chmod(0o755)
        output = self.release_with_failure("cp")
        self.assertNotIn("Released PDF as", output)
        self.assertNotIn("Released archive as", output)
        self.assertFalse((self.root / "tar-called").exists())

    def test_archive_failure_does_not_report_success(self):
        output = self.release_with_failure("tar")
        self.assertNotIn("Released archive as", output)

    def check_occupied_numbers(self, first, second):
        releases = self.root / "releases"
        releases.mkdir()
        for name in (f"{first}-{DATE}.pdf", f"{first}-{DATE}-1.pdf",
                     f"{second}-{DATE}-2.pdf", f"archive-{DATE}.tar.gz",
                     f"archive-{DATE}-1.tar.gz"):
            (releases / name).write_text(f"existing release: {name}\n")
        previous = self.snapshot_releases()
        self.release("build")
        self.assert_preserved(previous)
        self.assert_pair("-3", build_dir="build")
        self.assert_source_archive("-2")
        expected = set(previous) | {
            f"khod-disser-{DATE}-3.pdf", f"khod-synopsis-{DATE}-3.pdf",
            f"archive-{DATE}-2.tar.gz",
        }
        self.assertEqual(set(self.snapshot_releases()), expected)

    def test_dissertation_name_alone_reserves_pair(self):
        self.check_occupied_numbers("khod-disser", "khod-synopsis")

    def test_synopsis_name_alone_reserves_pair(self):
        self.check_occupied_numbers("khod-synopsis", "khod-disser")


if __name__ == "__main__":
    unittest.main(verbosity=2)
