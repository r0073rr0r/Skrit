import unittest

from skrit import detect_mode, encode_text


class TestSkriptRouter(unittest.TestCase):
    def test_detect_mode(self) -> None:
        self.assertEqual(detect_mode("Zemun zakon matori"), "satro")
        self.assertEqual(detect_mode("uzenzabanje"), "utro")
        self.assertEqual(detect_mode("M00n23 k0n24 70r1m4"), "leet")

    def test_auto_routes_to_satro(self) -> None:
        encoded, mode = encode_text("Zemun zakon matori", mode="auto")
        self.assertEqual(mode, "satro")
        self.assertEqual(encoded, "Munze konza matori")

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


if __name__ == "__main__":
    unittest.main()
