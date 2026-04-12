import unittest

from utrovacki import Utrovacki


class TestUtrovackiEncode(unittest.TestCase):
    def setUp(self) -> None:
        self.encoder = Utrovacki()

    def test_user_examples_latin(self) -> None:
        self.assertEqual(self.encoder.encode("pishtolj"), "ushtoljzapinje")
        self.assertEqual(self.encoder.encode("bazen"), "uzenzabanje")
        self.assertEqual(self.encoder.encode("mačka"), "učkazamanje")
        self.assertEqual(self.encoder.encode("značka"), "učkazaznanje")
        self.assertEqual(self.encoder.encode("đavo"), "uvozađanje")

    def test_sentence_and_case(self) -> None:
        self.assertEqual(
            self.encoder.encode("Pishtolj bazen MAČKA"),
            "Ushtoljzapinje uzenzabanje UČKAZAMANJE",
        )

    def test_cyrillic_and_mixed(self) -> None:
        self.assertEqual(self.encoder.encode("мачка значка ђаво"), "учказамање учказазнање увозађање")
        self.assertEqual(self.encoder.encode("mačka значка đavo"), "učkazamanje учказазнање uvozađanje")

    def test_min_word_length(self) -> None:
        encoder = Utrovacki(min_word_length=5)
        self.assertEqual(encoder.encode("pas bazen"), "pas uzenzabanje")

    def test_soft_tj_and_plain_c_target(self) -> None:
        strict = Utrovacki()
        soft = Utrovacki(soft_tj_to_cyrillic=True)

        self.assertEqual(strict.encode("атјб"), "утјбзаање")
        self.assertEqual(soft.encode("атјб"), "ућбзаање")

        self.assertEqual(Utrovacki(plain_c_target="ц").encode("ацб"), "уцбзаање")
        self.assertEqual(Utrovacki(plain_c_target="ч").encode("ацб"), "учбзаање")
        self.assertEqual(Utrovacki(plain_c_target="ћ").encode("ацб"), "ућбзаање")

    def test_exceptions_are_supported(self) -> None:
        with_exceptions = Utrovacki(exceptions={"brate": "tebra"})
        self.assertEqual(with_exceptions.encode("brate"), "utezabranje")

    def test_custom_affixes(self) -> None:
        custom = Utrovacki(prefix="x", infix="yy", suffix="zz")
        self.assertEqual(custom.encode("bazen"), "xzenyybazz")


if __name__ == "__main__":
    unittest.main()
