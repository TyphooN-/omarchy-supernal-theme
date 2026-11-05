"""Characterize the recovered audit and regress its CLI failure handling.

Run: python3 -B -m unittest discover -s tests -v
Fixtures are synthetic RGB PNGs; they do not alter theme assets.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "palette_audit.py"
SPEC = importlib.util.spec_from_file_location("palette_audit", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class ColourMathTests(unittest.TestCase):
    def test_known_oklab_reference_values(self):
        vectors = {
            "#000000": (0.0, 0.0, 0.0),
            "#ffffff": (1.0, 0.0, 0.0),
            "#ff0000": (0.62795536, 0.22486306, 0.12584630),
            "#00ff00": (0.86643961, -0.23388757, 0.17949848),
            "#0000ff": (0.45201372, -0.03245698, -0.31152815),
        }
        for colour, expected in vectors.items():
            with self.subTest(colour=colour):
                np.testing.assert_allclose(audit.oklab(audit.hex_to_rgb(colour)), expected, atol=1e-7)

    def test_contrast_black_white_and_crimson(self):
        black, white = (audit.luminance(audit.hex_to_rgb(c)) for c in ("#000000", "#ffffff"))
        self.assertAlmostEqual(float(audit.contrast(black, white)), 21.0)
        red = audit.luminance(audit.hex_to_rgb("#DC143C"))
        self.assertGreater(float(audit.contrast(red, black)), 4.20)
        self.assertLess(float(audit.contrast(red, black)), 4.22)

    def test_hue_wrap_and_anchor_identity(self):
        self.assertEqual(float(audit.hue_diff(359, 1)), -2)
        self.assertEqual(float(audit.hue_diff(1, 359)), 2)
        np.testing.assert_array_equal(audit.hue_family(audit.ANCHOR_HUES), np.arange(len(audit.ANCHORS)))
        self.assertEqual(int(audit.hue_family(0)), int(audit.hue_family(360)))

    def test_hex_validation(self):
        for invalid in ("fff", "#fff", "#gg0000", "#1234567", "123456", None):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                audit.hex_to_rgb(invalid)
        self.assertEqual(audit.rgb_to_hex(audit.hex_to_rgb("#ABCDEF")), "#abcdef")

    def test_gap_requires_recurrence_and_area(self):
        self.assertEqual(audit.gap_verdict([0.02, 0.02, 0.02, 0]), "material recurring gap")
        self.assertEqual(audit.gap_verdict([0.10, 0, 0]), "image-specific")
        self.assertEqual(audit.gap_verdict([0, 0, 0]), "negligible")
        self.assertEqual(audit.gap_verdict([0.01, 0.01, 0.01, 0]), "recurring but small")


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.backgrounds = self.root / "backgrounds"
        self.backgrounds.mkdir()
        self.colors = self.root / "colors.toml"
        self.colors.write_text('background = "#000000"\nselection = "#ff0000"\nforeground = "#ffffff"\nred = "#ff0000"\nblue = "#0000ff"\n')
        Image.fromarray(np.array([[[0, 0, 0], [255, 255, 255], [255, 0, 0], [128, 128, 128]]], dtype=np.uint8)).save(self.backgrounds / "a.png")
        Image.new("RGB", (10, 10), "#0000ff").save(self.backgrounds / "b.png")

    def collection(self):
        return audit.load_collection(str(self.backgrounds), ["b.png"])

    def palette(self):
        return audit.load_palette(str(self.colors))

    def cli(self, *extra):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--colors", str(self.colors),
                               "--backgrounds", str(self.backgrounds), "--new", "b.png", *extra],
                              text=True, capture_output=True, timeout=20)

    def test_equal_image_weights_and_normalization(self):
        coll = self.collection()
        result = audit.analyse(coll, self.palette())
        np.testing.assert_array_equal(coll["N"], [4, 100])
        self.assertAlmostEqual(float(result["means"]["all"]["chromatic"]), 0.625)
        self.assertAlmostEqual(float(coll["weights"]["all"].sum()), 1.0)
        self.assertAlmostEqual(float(coll["weights"]["original"].sum()), 1.0)
        self.assertAlmostEqual(float(coll["weights"]["new"].sum()), 1.0)
        for row in result["per_image"]:
            self.assertAlmostEqual(row["dark"] + row["neutral"] + row["chromatic"], 1.0)
            self.assertAlmostEqual(float(row["family"].sum()), row["chromatic"])
            self.assertAlmostEqual(row["covered"] + row["uncovered"], row["chromatic"])
        self.assertAlmostEqual(result["per_image"][0]["dark"], 0.25)
        self.assertAlmostEqual(result["per_image"][0]["neutral"], 0.50)

    def test_representatives_are_real_member_pixels(self):
        coll = self.collection()
        result = audit.analyse(coll, self.palette())
        real = {audit.rgb_to_hex(rgb) for rgb in coll["rgb"]}
        for family in result["families"]:
            rep = family["representative"]
            if rep is not None:
                self.assertIn(rep["hex"], real)
                self.assertGreaterEqual(rep["images_with_exact_pixel"], 1)

    def test_surfaces_cannot_cover_foreground_gaps(self):
        self.colors.write_text('background = "#000000"\nselection = "#ff0000"\nforeground = "#ffffff"\n')
        palette = self.palette()
        self.assertFalse(next(t for t in palette["tokens"] if t["name"] == "selection")["usable"])
        result = audit.analyse(self.collection(), palette)
        self.assertEqual(result["roles"], ["foreground"])
        self.assertAlmostEqual(result["per_image"][0]["uncovered"], 0.25)

    def test_exact_probe_counts_and_equal_area_mean(self):
        probe = audit.probe(self.collection(), "#ff0000")
        self.assertEqual(probe["exact_pixels"], 1)
        self.assertEqual(probe["images_containing"], 1)
        self.assertAlmostEqual(probe["within_jnd_mean"], 0.125)
        self.assertEqual(audit.probe(self.collection(), "#010203")["exact_pixels"], 0)

    def test_unknown_new_image_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not in"):
            audit.load_collection(str(self.backgrounds), ["missing.png"])

    def test_empty_collection_is_rejected(self):
        empty = self.root / "empty"
        empty.mkdir()
        with self.assertRaisesRegex(ValueError, "no images"):
            audit.load_collection(str(empty))

    def test_transparent_and_corrupt_images_are_rejected(self):
        transparent = self.root / "alpha.png"
        Image.new("RGBA", (1, 1), (255, 0, 0, 0)).save(transparent)
        with self.assertRaisesRegex(ValueError, "transparent"):
            audit.read_image(str(transparent))
        corrupt = self.root / "bad.jpg"
        corrupt.write_bytes(b"not an image")
        with self.assertRaises(OSError):
            audit.read_image(str(corrupt))

    def test_palette_missing_background_is_rejected(self):
        self.colors.write_text('foreground = "#ffffff"\n')
        with self.assertRaisesRegex(ValueError, "no background"):
            self.palette()

    def test_cli_json_and_freshness_positive_and_stale(self):
        output = self.root / "audit.json"
        first = self.cli("--json", str(output))
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(len(json.loads(output.read_text())["result"]["per_image"]), 2)
        report = self.root / "report.md"
        report.write_text("# Synthetic audit\n\n" + first.stdout)
        match = self.cli("--check", str(report))
        self.assertEqual(match.returncode, 0, match.stderr)
        report.write_text(first.stdout.replace("Tokens (parsed", "Incorrect tokens (parsed"))
        stale = self.cli("--check", str(report))
        self.assertEqual(stale.returncode, 1)
        self.assertIn("stale", stale.stderr)

    def test_cli_invalid_new_image_is_controlled_error(self):
        failed = self.cli("--new", "absent.png")
        self.assertEqual(failed.returncode, 2)
        self.assertIn("not in", failed.stderr)
        self.assertNotIn("Traceback", failed.stderr)

    def test_cli_no_usable_roles_is_controlled_error(self):
        self.colors.write_text('background = "#000000"\nforeground = "#010101"\n')
        failed = self.cli()
        self.assertEqual(failed.returncode, 2, failed.stderr)
        self.assertIn("no usable foreground roles", failed.stderr)
        self.assertNotIn("Traceback", failed.stderr)


if __name__ == "__main__":
    unittest.main()
