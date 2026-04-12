from __future__ import annotations

import contextlib
import io
import runpy
import unittest
from unittest.mock import patch

import skrit
from skrit import detect_leet_base, detect_mode, encode_text


class TestSkritDetectionCoverage(unittest.TestCase):
    def test_detect_leet_base_utro_and_ratio_and_fallback(self) -> None:
        self.assertEqual(detect_leet_base("00zen24ban73"), "utro")
        self.assertEqual(detect_leet_base("uzenzabanje plain"), "utro")
        self.assertEqual(detect_leet_base("Zemun zakon matori"), "satro")
        self.assertEqual(detect_leet_base("123 !!!"), "satro")

    def test_detect_mode_no_words_fallback(self) -> None:
        self.assertEqual(detect_mode("123 !!!"), "satro")

    def test_ensure_utf8_stdout_handles_oserror(self) -> None:
        class BrokenStdout:
            def reconfigure(self, **kwargs: object) -> None:
                raise OSError("cannot reconfigure")

        with patch.object(skrit.sys, "stdout", BrokenStdout()):
            skrit._ensure_utf8_stdout()

    def test_encode_text_auto_leet_base_detection(self) -> None:
        encoded, mode = encode_text(
            "Zemun zakon matori",
            mode="leet",
            leet_base="auto",
            detect_from="00zen24ban73",
        )
        self.assertEqual(mode, "leet")
        self.assertTrue(encoded)


class TestSkritCliCoverage(unittest.TestCase):
    def _run_cli(self, argv: list[str]) -> str:
        buffer = io.StringIO()
        with patch("sys.argv", argv), contextlib.redirect_stdout(buffer):
            runpy.run_module("skrit", run_name="__main__")
        return buffer.getvalue()

    def test_main_auto_show_mode(self) -> None:
        output = self._run_cli(
            ["skrit.py", "--mode", "auto", "--show-mode", "Zemun zakon matori"]
        )
        self.assertEqual(output, "[mode=satro]\nMunze konza matori\n")

    def test_main_leet_custom_flags(self) -> None:
        output = self._run_cli(
            [
                "skrit.py",
                "--mode",
                "leet",
                "--show-mode",
                "--leet-base",
                "utro",
                "--leet-profile",
                "basic",
                "--leet-density",
                "1.0",
                "--leet-complexity",
                "1",
                "--za-style",
                "z4",
                "--nje-style",
                "nj3",
                "--utro-prefix",
                "x",
                "--utro-infix",
                "yy",
                "--utro-suffix",
                "zz",
                "bazen",
            ]
        )
        self.assertEqual(output, "[mode=leet]\n00zenz4banj3\n")

    def test_main_auto_detect_from_reference_text(self) -> None:
        output = self._run_cli(
            [
                "skrit.py",
                "--mode",
                "auto",
                "--detect-from",
                "00zen24ban73",
                "Zemun zakon matori",
            ]
        )
        self.assertTrue(output.strip())


if __name__ == "__main__":
    unittest.main()
