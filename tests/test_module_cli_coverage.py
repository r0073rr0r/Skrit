from __future__ import annotations

import io
import runpy
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from leetrovacki import Leetrovacki, _ensure_utf8_stdout as leetrovacki_ensure
from satrovacki import Satrovacki, _ensure_utf8_stdout as satrovacki_ensure
from utrovacki import Utrovacki, _ensure_utf8_stdout as utrovacki_ensure


class _RecordingStdout:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def reconfigure(self, **kwargs: str) -> None:
        self.calls.append(kwargs)


class _RaisingStdout:
    def reconfigure(self, **kwargs: str) -> None:
        raise OSError("stdout reconfigure failed")


def _run_module_main(module_name: str, argv: list[str]) -> str:
    buf = io.StringIO()
    with patch.object(sys, "argv", argv), redirect_stdout(buf):
        runpy.run_module(module_name, run_name="__main__")
    return buf.getvalue().strip()


class TestUtf8Helpers(unittest.TestCase):
    def test_helpers_reconfigure_and_ignore_oserror(self) -> None:
        for helper in (satrovacki_ensure, utrovacki_ensure, leetrovacki_ensure):
            with self.subTest(helper=helper.__module__):
                stdout = _RecordingStdout()
                with patch.object(sys, "stdout", stdout):
                    helper()
                self.assertEqual(stdout.calls, [{"encoding": "utf-8"}])

                with patch.object(sys, "stdout", _RaisingStdout()):
                    helper()


class TestLeetrovackiCoverage(unittest.TestCase):
    def test_validation_branches(self) -> None:
        with self.assertRaises(ValueError):
            Leetrovacki(plain_c_target="x")
        with self.assertRaises(ValueError):
            Leetrovacki(leet_profile="missing")
        with self.assertRaises(ValueError):
            Leetrovacki(leet_density=1.1)

    def test_full_letter_leet_branches(self) -> None:
        encoder = Leetrovacki(base_mode="utro", leet_profile="full", leet_density=1.0)

        present = encoder._leetify_utro("uzenzabanje", False)
        absent = encoder._leetify_utro("matori", False)
        plain = Leetrovacki(base_mode="utro")._leetify_utro("matori", False)

        self.assertEqual(present, "0023^/24I34^/,_|3")
        self.assertEqual(absent, "/\\/\\470ri21")
        self.assertEqual(plain, "matori")

    def test_nje_replacement_and_fallback_case(self) -> None:
        encoder = Leetrovacki(nje_style="њ")
        self.assertEqual(encoder._nje_replacement(False), "nj")
        self.assertEqual(encoder._apply_case("mIxEd", "changed"), "changed")

    def test_main(self) -> None:
        output = _run_module_main(
            "leetrovacki",
            [
                "leetrovacki.py",
                "--mode",
                "utro",
                "--leet-profile",
                "full",
                "--leet-density",
                "1.0",
                "bazen",
            ],
        )
        self.assertEqual(output, "0023^/24i34^/,_|3")


class TestSatrovackiCoverage(unittest.TestCase):
    def test_mixed_case_fallback(self) -> None:
        encoder = Satrovacki()
        self.assertEqual(encoder._apply_case("mIxEd", "changed"), "changed")

    def test_main(self) -> None:
        output = _run_module_main(
            "satrovacki",
            ["satrovacki.py", "Zemun", "zakon"],
        )
        self.assertEqual(output, "Munze konza")


class TestUtrovackiCoverage(unittest.TestCase):
    def test_exception_length_mismatch_and_split_fallback(self) -> None:
        mismatch = Utrovacki(exceptions={"brate": "tb"})
        self.assertEqual(mismatch.encode_word("brate"), "utbzanje")

        fallback = Utrovacki()
        with patch.object(fallback, "_find_split_index", return_value=0):
            self.assertEqual(fallback.encode_word("bazen"), "ubazenzanje")

    def test_main(self) -> None:
        output = _run_module_main("utrovacki", ["utrovacki.py", "bazen"])
        self.assertEqual(output, "uzenzabanje")


if __name__ == "__main__":
    unittest.main()
