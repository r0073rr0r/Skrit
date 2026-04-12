import unittest

from leet import (
    DEFAULT_LEET_DENSITY,
    LeetEncoder,
    LEET_TABLE,
    apply_leet,
    available_profiles,
    build_full_leet_profile,
    get_leet_profile,
    looks_like_leet,
)


class TestLeetModule(unittest.TestCase):
    def test_profiles_and_table(self) -> None:
        self.assertIn("basic", available_profiles())
        self.assertIn("readable", available_profiles())
        self.assertIn("full", available_profiles())
        self.assertEqual(len(LEET_TABLE), 26)
        self.assertEqual(DEFAULT_LEET_DENSITY, 0.86)

    def test_get_profile_validation(self) -> None:
        with self.assertRaises(ValueError):
            get_leet_profile("missing")

    def test_basic_and_full_encoding(self) -> None:
        basic = get_leet_profile("basic")
        full = get_leet_profile("full")

        self.assertEqual(
            apply_leet("Zemun zakon matori", basic, density=1.0),
            "23m00n 24k0n m470r1",
        )
        self.assertEqual(apply_leet("abcxyz", full), "4I3[><j2")

    def test_looks_like_leet(self) -> None:
        self.assertTrue(looks_like_leet("M00n23 k0n24 70r1m4"))
        self.assertFalse(looks_like_leet("Zemun zakon matori"))

    def test_encoder_class(self) -> None:
        self.assertEqual(LeetEncoder(profile="basic").encode("matori"), "m470r1")

    def test_density_control(self) -> None:
        mapping = get_leet_profile("basic")
        self.assertEqual(apply_leet("matori", mapping, density=0.0), "matori")
        self.assertEqual(apply_leet("matori", mapping, density=1.0), "m470r1")

    def test_custom_profile_and_uppercase_alpha_replacement(self) -> None:
        mapping = get_leet_profile(custom_map={"a": "x", "b": "yz"})
        self.assertEqual(apply_leet("AB", mapping), "XYZ")

    def test_invalid_density_raises(self) -> None:
        mapping = get_leet_profile("basic")
        with self.assertRaises(ValueError):
            apply_leet("abc", mapping, density=1.1)

    def test_full_profile_complexity(self) -> None:
        c0 = build_full_leet_profile(0)
        c1 = build_full_leet_profile(1)
        self.assertEqual(c0["a"], "4")
        self.assertEqual(c1["a"], "/\\")
        self.assertEqual(c0["r"], "ri2")
        self.assertEqual(c1["r"], "9")

    def test_invalid_complexity_raises(self) -> None:
        with self.assertRaises(ValueError):
            build_full_leet_profile(-1)

    def test_encoder_complexity(self) -> None:
        self.assertEqual(LeetEncoder(profile="full", complexity=1).encode("ab"), "/\\8")


if __name__ == "__main__":
    unittest.main()
