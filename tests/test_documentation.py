"""Check local Markdown links and bilingual document structure."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [
    ("README.md", "docs/pt-BR/README.md"),
    ("docs/hardware.md", "docs/pt-BR/componentes-e-montagem.md"),
    ("docs/installation.md", "docs/pt-BR/instalacao.md"),
    ("docs/development.md", "docs/pt-BR/desenvolvimento.md"),
    ("images/README.md", "docs/pt-BR/registro-fotografico.md"),
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

    def test_bilingual_structure(self):
        for en, pt in PAIRS:
            a, b = [(ROOT / path).read_text() for path in (en, pt)]
            with self.subTest(pair=en):
                self.assertEqual(re.findall(r"^(#+) ", a, re.M), re.findall(r"^(#+) ", b, re.M))
                self.assertEqual(re.findall(r"```bash\n(.*?)```", a, re.S),
                                 re.findall(r"```bash\n(.*?)```", b, re.S))
                def photo_targets(path, content):
                    return [
                        ((ROOT / path).parent / target).resolve()
                        for target in re.findall(r"\]\(([^)]*arduino-\d+\.jpeg)\)", content)
                    ]

                self.assertEqual(photo_targets(en, a), photo_targets(pt, b))
