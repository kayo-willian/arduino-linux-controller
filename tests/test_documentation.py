"""Check local Markdown links and bilingual document structure."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [
    ("README.md", "README.pt-BR.md"),
    ("docs/hardware.md", "docs/hardware.pt-BR.md"),
    ("docs/installation.md", "docs/installation.pt-BR.md"),
    ("docs/development.md", "docs/development.pt-BR.md"),
    ("images/README.md", "images/README.pt-BR.md"),
]


class DocumentationTests(unittest.TestCase):
    def test_local_links_exist(self):
        for pair in PAIRS:
            for relative in pair:
                file = ROOT / relative
                for target in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                    if target.startswith(("https://", "http://", "#")):
                        continue
                    with self.subTest(file=relative, target=target):
                        self.assertTrue((file.parent / target.split("#")[0]).exists())
