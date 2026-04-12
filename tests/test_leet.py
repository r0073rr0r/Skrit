import unittest

from leet import (
    LeetEncoder,
    LEET_TABLE,
    apply_leet,
    available_profiles,
    get_leet_profile,
    looks_like_leet,
)


class TestLeetModule(unittest.TestCase):
    def test_profiles_and_table(self) -> None:
        self.assertIn("basic", available_profiles())
        self.assertIn("full", available_profiles())
        self.assertEqual(len(LEET_TABLE), 26)

    def test_get_profile_validation(self) -> None:
        with self.assertRaises(ValueError):
            get_leet_profile("missing")

    def test_basic_and_full_encoding(self) -> None:
        basic = get_leet_profile("basic")
        full = get_leet_profile("full")

        self.assertEqual(apply_leet("Zemun zakon matori", basic), "23m00n 24k0n m470r1")
        self.assertEqual(apply_leet("abcxyz", full), "4I3[><j2")

    def test_looks_like_leet(self) -> None:
        self.assertTrue(looks_like_leet("M00n23 k0n24 70r1m4"))
        self.assertFalse(looks_like_leet("Zemun zakon matori"))

    def test_encoder_class(self) -> None:
        self.assertEqual(LeetEncoder(profile="basic").encode("matori"), "m470r1")


if __name__ == "__main__":
    unittest.main()
