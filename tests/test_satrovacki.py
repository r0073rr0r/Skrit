import unittest

from satrovacki import Satrovacki, _latin_to_cyrillic


class TestSatrovackiEncode(unittest.TestCase):
    def setUp(self) -> None:
        self.encoder = Satrovacki()

    def test_basic_examples_latin(self) -> None:
        self.assertEqual(self.encoder.encode("Beograd"), "Gradbeo")
        self.assertEqual(self.encoder.encode("Zemun zakon matori"), "Munze konza matori")
        self.assertEqual(self.encoder.encode("riba ribi grize rep"), "bari biri zegri pre")

    def test_basic_examples_cyrillic_and_mixed(self) -> None:
        self.assertEqual(self.encoder.encode("Земун закон матори"), "Мунзе конза матори")
        self.assertEqual(self.encoder.encode("Zemun закон matori"), "Munze конза matori")

    def test_case_and_exceptions(self) -> None:
        self.assertEqual(self.encoder.encode("brate BRATE Brate"), "tebra TEBRA Tebra")

    def test_punctuation_and_numbers(self) -> None:
        self.assertEqual(self.encoder.encode("123, ajde!"), "123, jdea!")

    def test_min_word_length(self) -> None:
        encoder = Satrovacki(min_word_length=5)
        self.assertEqual(encoder.encode("riba rep"), "riba rep")

    def test_no_vowel_fallback(self) -> None:
        self.assertEqual(self.encoder.encode("prst"), "stpr")
        self.assertEqual(self.encoder.encode("прст"), "стпр")


class TestCyrillicOptions(unittest.TestCase):
    def test_plain_c_target_variants(self) -> None:
        self.assertEqual(_latin_to_cyrillic("c C casa", plain_c_target="ц"), "ц Ц цаса")
        self.assertEqual(_latin_to_cyrillic("c C casa", plain_c_target="ч"), "ч Ч часа")
        self.assertEqual(_latin_to_cyrillic("c C casa", plain_c_target="ћ"), "ћ Ћ ћаса")

    def test_tj_default_and_soft_mode(self) -> None:
        self.assertEqual(_latin_to_cyrillic("tj Tj TJ"), "тј Тј ТЈ")
        self.assertEqual(
            _latin_to_cyrillic("tj Tj TJ", use_tj_for_c=True),
            "ћ Ћ Ћ",
        )

    def test_soft_tj_option_through_encoder(self) -> None:
        strict = Satrovacki(exceptions={"test": "tj"})
        soft = Satrovacki(exceptions={"test": "tj"}, soft_tj_to_cyrillic=True)

        self.assertEqual(strict.encode("тест"), "тј")
        self.assertEqual(soft.encode("тест"), "ћ")

    def test_invalid_plain_c_target_raises(self) -> None:
        with self.assertRaises(ValueError):
            Satrovacki(plain_c_target="x")


if __name__ == "__main__":
    unittest.main()
