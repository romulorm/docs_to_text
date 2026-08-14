"""Headless tests for the converter's file and format rules."""

import tempfile
import unittest
from pathlib import Path

from main import (
    AUTO_DETECT,
    build_output_path,
    detect_input_type,
    input_type_matches,
)
from translations import LANGUAGES, TRANSLATIONS


class ConverterRulesTest(unittest.TestCase):
    def test_pt_br_is_the_default_language_option(self) -> None:
        self.assertEqual(LANGUAGES[0], "pt-BR")
        self.assertIn("Converta", TRANSLATIONS["pt-BR"]["tagline"])
        self.assertEqual(
            TRANSLATIONS["English"]["output_text"],
            "Text",
        )

    def test_detects_supported_extensions_case_insensitively(self) -> None:
        self.assertEqual(detect_input_type("report.PDF"), "PDF")
        self.assertEqual(detect_input_type("scan.jpeg"), "JPEG")
        self.assertEqual(detect_input_type("voice.WAV"), "WAV")

    def test_unknown_extension_is_auto_detect(self) -> None:
        self.assertEqual(detect_input_type("archive.zip"), AUTO_DETECT)
        self.assertFalse(input_type_matches("archive.zip", AUTO_DETECT))

    def test_auto_detect_and_explicit_type_validation(self) -> None:
        self.assertTrue(input_type_matches("slides.pptx", AUTO_DETECT))
        self.assertTrue(input_type_matches("slides.pptx", "PPTX"))
        self.assertFalse(input_type_matches("slides.pptx", "PDF"))

    def test_builds_output_path_from_source_stem(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_output_path(
                Path(directory) / "meeting notes.PDF",
                directory,
                "Markdown",
            )
        self.assertEqual(output.name, "meeting notes.md")


if __name__ == "__main__":
    unittest.main()
