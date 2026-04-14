import unittest

from leetrovacki import Leetrovacki


class TestLeetrovacki(unittest.TestCase):
    def test_auto_detects_utro_pattern(self) -> None:
        encoder = Leetrovacki(leet_density=1.0)
        self.assertEqual(encoder.encode("učkazamanje"), "00čka24man73")
        self.assertEqual(encoder.encode("uzenzabanje"), "00zen24ban73")

    def test_default_density_is_86_percent(self) -> None:
        encoder = Leetrovacki(base_mode="satro")
        self.assertEqual(encoder.encode("prst"), "s7pr")

    def test_auto_falls_back_to_satro_leet(self) -> None:
        encoder = Leetrovacki(leet_density=1.0)
        self.assertEqual(encoder.encode("munze"), "m00n23")
        self.assertEqual(encoder.encode("мунзе"), "м00н23")
        self.assertEqual(encoder.encode("ushtoljzapinje"), "00shtolj24pin73")

    def test_explicit_utro_mode_from_plain(self) -> None:
        encoder = Leetrovacki(base_mode="utro", leet_density=1.0)
        self.assertEqual(encoder.encode("mačka"), "00čka24man73")
        self.assertEqual(encoder.encode("đavo"), "00vo24đan73")

    def test_explicit_satro_mode_from_plain(self) -> None:
        encoder = Leetrovacki(base_mode="satro", leet_density=1.0)
        self.assertEqual(encoder.encode("zemun"), "m00n23")
        self.assertEqual(encoder.encode("bazen"), "23n84")

    def test_all_satro_module_examples_in_satro_mode(self) -> None:
        encoder = Leetrovacki(base_mode="satro", leet_density=1.0)
        cases = {
            "Beograd": "6r4d830",
            "Zemun zakon matori": "M00n23 k0n24 70r1m4",
            "riba ribi grize rep": "84r1 81r1 236r1 pr3",
            "Земун закон матори": "М00н23 к0н24 70р1м4",
            "Zemun закон matori": "M00n23 к0н24 70r1m4",
            "brate BRATE Brate": "738r4 738R4 738r4",
            "123, ajde!": "123, d34j!",
            "prst": "57pr",
            "прст": "57пр",
        }
        for source, expected in cases.items():
            self.assertEqual(encoder.encode(source), expected)

        self.assertEqual(
            Leetrovacki(base_mode="satro", min_word_length=5, leet_density=1.0).encode(
                "riba rep"
            ),
            "riba rep",
        )

    def test_utro_styles(self) -> None:
        encoder = Leetrovacki(
            base_mode="utro", za_style="z4", nje_style="nj3", leet_density=1.0
        )
        self.assertEqual(encoder.encode("bazen"), "00zenz4banj3")

    def test_all_utro_module_examples_in_utro_mode(self) -> None:
        encoder = Leetrovacki(base_mode="utro", leet_density=1.0)
        cases = {
            "pishtolj": "00shtolj24pin73",
            "bazen": "00zen24ban73",
            "mačka": "00čka24man73",
            "značka": "00čka24znan73",
            "đavo": "00vo24đan73",
            "Pishtolj bazen MAČKA": "00shtolj24pin73 00zen24ban73 00ČKA24MAN73",
            "мачка значка ђаво": "00чка24ман73 00чка24знан73 00во24ђан73",
            "mačka значка đavo": "00čka24man73 00чка24знан73 00vo24đan73",
            "pas bazen": "00s24pan73 00zen24ban73",
        }
        for source, expected in cases.items():
            self.assertEqual(encoder.encode(source), expected)

        with_exceptions = Leetrovacki(
            base_mode="utro", exceptions={"brate": "tebra"}, leet_density=1.0
        )
        self.assertEqual(with_exceptions.encode("brate"), "00te24bran73")
        self.assertEqual(
            Leetrovacki(base_mode="utro", min_word_length=5, leet_density=1.0).encode(
                "pas bazen"
            ),
            "pas 00zen24ban73",
        )

    def test_nje_cyrillic_option(self) -> None:
        encoder = Leetrovacki(base_mode="utro", nje_style="њ", leet_density=1.0)
        self.assertEqual(encoder.encode("мачка"), "00чка24мањ")

    def test_tj_and_plain_c_options_propagate(self) -> None:
        encoder = Leetrovacki(
            base_mode="utro",
            soft_tj_to_cyrillic=True,
            plain_c_target="ћ",
            leet_density=1.0,
        )
        self.assertEqual(encoder.encode("атјб"), "00ћб24ан73")
        self.assertEqual(encoder.encode("ацб"), "00ћб24ан73")
        self.assertEqual(
            Leetrovacki(base_mode="utro", plain_c_target="ч", leet_density=1.0).encode(
                "ацб"
            ),
            "00чб24ан73",
        )

    def test_invalid_options_raise(self) -> None:
        with self.assertRaises(ValueError):
            Leetrovacki(base_mode="bad")
        with self.assertRaises(ValueError):
            Leetrovacki(za_style="bad")
        with self.assertRaises(ValueError):
            Leetrovacki(nje_style="bad")
        with self.assertRaises(ValueError):
            Leetrovacki(leet_complexity=-1)

    def test_full_profile_complexity_is_used(self) -> None:
        encoder = Leetrovacki(
            base_mode="satro",
            min_word_length=1,
            leet_profile="full",
            leet_complexity=1,
        )
        self.assertEqual(encoder.encode("a"), "/\\")


if __name__ == "__main__":
    unittest.main()
