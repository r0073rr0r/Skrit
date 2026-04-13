import unittest
from unittest.mock import patch

from skrit import (
    _deleet_text_basic,
    _looks_like_leetrovacki,
    _looks_like_satro_encoded,
    _looks_like_utrovacki,
    detect_mode,
    encode_text,
)


class TestSkriptRouter(unittest.TestCase):
    def test_detect_mode(self) -> None:
        self.assertEqual(detect_mode("Zemun zakon matori"), "satro")
        self.assertEqual(detect_mode("uzenzabanje"), "utro")
        self.assertEqual(detect_mode("M00n23 k0n24 70r1m4"), "leet")

    def test_auto_routes_to_satro(self) -> None:
        encoded, mode = encode_text("Zemun zakon matori", mode="auto")
        self.assertEqual(mode, "satro")
        self.assertEqual(encoded, "Munze konza torima")

    def test_auto_decodes_satro_input(self) -> None:
        decoded, mode = encode_text("munze konza", mode="auto")
        self.assertEqual(mode, "satro")
        self.assertEqual(decoded, "zemun zakon")

        decoded_torima, mode_torima = encode_text("munze konza torima", mode="auto")
        self.assertEqual(mode_torima, "satro")
        self.assertEqual(decoded_torima, "zemun zakon matori")

    def test_auto_encodes_ambiguous_plain_word(self) -> None:
        encoded, mode = encode_text("marija", mode="auto")
        self.assertEqual(mode, "satro")
        self.assertEqual(encoded, "rijama")

    def test_auto_decodes_utro_input(self) -> None:
        decoded, mode = encode_text("uzenzabanje", mode="auto")
        self.assertEqual(mode, "utro")
        self.assertEqual(decoded, "bazen")

    def test_auto_routes_to_leet(self) -> None:
        encoded, mode = encode_text("Zemun zakon matori", mode="auto", detect_from="M00n23")
        self.assertEqual(mode, "leet")
        self.assertEqual(encoded, "M00n23 k0n24 70r1m4")

    def test_auto_routes_to_utro(self) -> None:
        encoded, mode = encode_text("bazen", mode="auto", detect_from="uzenzabanje")
        self.assertEqual(mode, "utro")
        self.assertEqual(encoded, "uzenzabanje")

    def test_explicit_modes(self) -> None:
        satro, satro_mode = encode_text("bazen", mode="satro")
        utro, utro_mode = encode_text("bazen", mode="utro")
        leet, leet_mode = encode_text("bazen", mode="leet", leet_base="satro")

        self.assertEqual(satro_mode, "satro")
        self.assertEqual(utro_mode, "utro")
        self.assertEqual(leet_mode, "leet")
        self.assertEqual(satro, "zenba")
        self.assertEqual(utro, "uzenzabanje")
        self.assertEqual(leet, "23nb4")

    def test_leet_full_complexity_passthrough(self) -> None:
        encoded, mode = encode_text(
            "a",
            mode="leet",
            leet_base="satro",
            min_word_length=1,
            leet_profile="full",
            leet_complexity=1,
        )
        self.assertEqual(mode, "leet")
        self.assertEqual(encoded, "/\\")

    def test_satro_encoded_detector_with_no_words(self) -> None:
        self.assertFalse(_looks_like_satro_encoded("123 !!!"))
        self.assertFalse(_looks_like_satro_encoded("matori"))
        self.assertTrue(_looks_like_satro_encoded("munze torima"))

    def test_satro_encoded_detector_no_changed_pairs(self) -> None:
        class FakeSatro:
            def __init__(self, **_: object) -> None:
                pass

            def can_decode_word(self, _word: str) -> bool:
                return True

            def decode_word(self, word: str) -> str:
                return word

        with patch("skrit.Satrovacki", FakeSatro):
            self.assertFalse(_looks_like_satro_encoded("abc"))

    def test_utro_and_leet_detectors(self) -> None:
        self.assertTrue(_looks_like_utrovacki("uzenzabanje"))
        self.assertFalse(_looks_like_utrovacki("bazen"))
        self.assertTrue(_looks_like_leetrovacki("m00n23 k0n24"))
        self.assertTrue(_looks_like_leetrovacki("/\\/\\470ri21"))
        self.assertFalse(_looks_like_leetrovacki("zemun zakon"))
        self.assertFalse(_looks_like_leetrovacki(""))

    def test_auto_decodes_leet_inputs(self) -> None:
        decoded_satro, mode_satro = encode_text("m00n23 k0n24", mode="auto")
        self.assertEqual(mode_satro, "leet")
        self.assertEqual(decoded_satro, "zemun zakon")

        decoded_utro, mode_utro = encode_text("00zen24ban73", mode="auto")
        self.assertEqual(mode_utro, "leet")
        self.assertEqual(decoded_utro, "bazen")

    def test_deleet_basic_helper(self) -> None:
        self.assertEqual(_deleet_text_basic("m00n23"), "munze")
        self.assertEqual(_deleet_text_basic("00zen24ban73"), "uzenzabanje")
        self.assertEqual(_deleet_text_basic("M00N23"), "MUNZE")
        self.assertEqual(_deleet_text_basic("Nj3"), "Nje")

    def test_auto_leet_utro_fallback_returns_deleeted(self) -> None:
        decoded, mode = encode_text("00n73 24", mode="auto")
        self.assertEqual(mode, "leet")
        self.assertEqual(decoded, "unje za")


if __name__ == "__main__":
    unittest.main()
