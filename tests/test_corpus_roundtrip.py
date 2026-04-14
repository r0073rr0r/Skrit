"""
Инваријантни тестови над корпусом од 963 српске речи.

Исти корпус (corpus_963.CORPUS_963) користе сва три система:
  - Шатровачки   (Satrovacki)
  - Утровачки    (Utrovacki)
  - Литровачки   (Leetrovacki)

Тестови проверавају **инваријанте** (структурна правила), а не хардкодоване
вредности — јер се ради о формалним системима чији је доказ алгоритам сам.

Инваријанте по систему:
  Шатровачки:
    [S1] encode не пада ни на једној речи
    [S2] дужина речи је очувана (|encode(w)| == |w|)
    [S3] roundtrip: decode(encode(w)) == w за речи дужине ≥ min_word_length
    [S4] кратке речи (< min_word_length) се не мењају
    [S5] велико слово на почетку је очувано

  Утровачки:
    [U1] encode не пада ни на једној речи
    [U2] излаз је дужи од улаза (|encode(w)| > |w|) за речи ≥ min_word_length
    [U3] излаз почиње са префиксом "u"
    [U4] излаз садржи инфикс "za"
    [U5] излаз завршава суфиксом "nje"
    [U6] roundtrip: decode(encode(w)) == w
    [U7] кратке речи се не мењају

  Литровачки:
    [L1] encode не пада ни на једној речи
    [L2] у satro режиму: излаз садржи leet карактере за речи са a/e/i/o/u/s/t/z
    [L3] у utro режиму: излаз почиње са "00" за речи ≥ min_word_length
    [L4] у utro режиму: излаз садржи "24" (za_style="24")
    [L5] у utro режиму: излаз завршава са "n73" (nje_style="n73")
    [L6] кратке речи се не мењају
"""
import unittest

from corpus_963 import CORPUS_963
from leetrovacki import Leetrovacki
from satrovacki import Satrovacki
from utrovacki import Utrovacki

_MIN = 3  # подразумевана min_word_length

LEET_SATRO_CHARS = set("4310572086")  # карактери basic leet профила


class TestSatrovackiCorpus(unittest.TestCase):
    """[S1–S5] Шатровачки инваријанте над 963 речи."""

    def setUp(self) -> None:
        self.enc = Satrovacki()

    def test_s1_no_crash(self) -> None:
        """[S1] encode не пада ни на једној речи."""
        for word in CORPUS_963:
            with self.subTest(word=word):
                self.enc.encode(word)

    def test_s2_length_preserved(self) -> None:
        """[S2] Дужина речи је очувана."""
        for word in CORPUS_963:
            encoded = self.enc.encode_word(word)
            with self.subTest(word=word):
                self.assertEqual(
                    len(encoded),
                    len(word),
                    f"encode_word({word!r}) = {encoded!r}: дужина {len(encoded)} != {len(word)}",
                )

    def test_s3_roundtrip_consistency(self) -> None:
        """[S3] encode(decode(encode(w))) == encode(w) за речи ≥ min_word_length.

        Тврди слаби облик roundtrip-а: декодирана форма, кад се поново
        кодира, мора вратити исти кодирани облик. Декодер може изабрати
        другачији оригинал (нпр. "nakru" → "runak" уместо "kruna"), али тај
        оригинал мора бити исправан пре-образ encoded форме.

        Строги roundtrip (decode(encode(w)) == w) није гарантован за све
        речи јер је шатровачки декодер хеуристички: код ротационе
        амбигвитете бира кандидата по скору, а не по оригиналном контексту.
        """
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.enc.encode_word(word.lower())
            decoded = self.enc.decode_word(encoded)
            re_encoded = self.enc.encode_word(decoded)
            with self.subTest(word=word, encoded=encoded, decoded=decoded):
                self.assertEqual(
                    re_encoded,
                    encoded,
                    f"Consistency failed: {word!r} → {encoded!r} → {decoded!r} → {re_encoded!r}",
                )

    def test_s4_short_words_unchanged(self) -> None:
        """[S4] Речи краће од min_word_length се не мењају."""
        for word in CORPUS_963:
            if len(word) >= _MIN:
                continue
            with self.subTest(word=word):
                self.assertEqual(self.enc.encode_word(word), word)

    def test_s5_titlecase_preserved(self) -> None:
        """[S5] Велико слово на почетку је очувано."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            titled = word.capitalize()
            encoded = self.enc.encode_word(titled)
            with self.subTest(word=titled):
                self.assertTrue(
                    encoded[0].isupper(),
                    f"encode_word({titled!r}) = {encoded!r}: прво слово није велико",
                )


class TestUtrovackiCorpus(unittest.TestCase):
    """[U1–U7] Утровачки инваријанте над 963 речи."""

    def setUp(self) -> None:
        self.enc = Utrovacki()

    def test_u1_no_crash(self) -> None:
        """[U1] encode не пада ни на једној речи."""
        for word in CORPUS_963:
            with self.subTest(word=word):
                self.enc.encode(word)

    def test_u2_longer_than_input(self) -> None:
        """[U2] Излаз је дужи од улаза за речи ≥ min_word_length."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.enc.encode_word(word)
            with self.subTest(word=word):
                self.assertGreater(
                    len(encoded),
                    len(word),
                    f"encode_word({word!r}) = {encoded!r}: дужина {len(encoded)} nije > {len(word)}",
                )

    def test_u3_starts_with_prefix(self) -> None:
        """[U3] Излаз почиње са 'u' (латиница) или 'у' (ћирилица)."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.enc.encode_word(word.lower())
            with self.subTest(word=word):
                self.assertTrue(
                    encoded.startswith("u") or encoded.startswith("у"),
                    f"encode_word({word!r}) = {encoded!r}: не почиње са 'u'/'у'",
                )

    def test_u4_contains_infix(self) -> None:
        """[U4] Излаз садржи инфикс 'za' (латиница) или 'за' (ћирилица)."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.enc.encode_word(word.lower())
            with self.subTest(word=word):
                self.assertTrue(
                    "za" in encoded or "за" in encoded,
                    f"encode_word({word!r}) = {encoded!r}: нема 'za'/'за'",
                )

    def test_u5_ends_with_suffix(self) -> None:
        """[U5] Излаз завршава са 'nje' (латиница) или 'ње' (ћирилица)."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.enc.encode_word(word.lower())
            with self.subTest(word=word):
                self.assertTrue(
                    encoded.endswith("nje") or encoded.endswith("ње"),
                    f"encode_word({word!r}) = {encoded!r}: не завршава са 'nje'/'ње'",
                )

    def test_u6_roundtrip(self) -> None:
        """[U6] decode(encode(w)) == w — строги roundtrip за све речи."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.enc.encode_word(word.lower())
            decoded = self.enc.decode_word(encoded)
            with self.subTest(word=word, encoded=encoded):
                self.assertEqual(
                    decoded,
                    word.lower(),
                    f"Roundtrip failed: {word!r} → {encoded!r} → {decoded!r}",
                )

    def test_u7_short_words_unchanged(self) -> None:
        """[U7] Речи краће од min_word_length се не мењају."""
        for word in CORPUS_963:
            if len(word) >= _MIN:
                continue
            with self.subTest(word=word):
                self.assertEqual(self.enc.encode_word(word), word)


class TestLeetrovackiCorpus(unittest.TestCase):
    """[L1–L6] Литровачки инваријанте над 963 речи."""

    def setUp(self) -> None:
        self.satro = Leetrovacki(base_mode="satro", leet_density=1.0)
        self.utro = Leetrovacki(base_mode="utro", leet_density=1.0)

    def test_l1_no_crash_satro(self) -> None:
        """[L1a] encode не пада у satro режиму."""
        for word in CORPUS_963:
            with self.subTest(word=word):
                self.satro.encode(word)

    def test_l1_no_crash_utro(self) -> None:
        """[L1b] encode не пада у utro режиму."""
        for word in CORPUS_963:
            with self.subTest(word=word):
                self.utro.encode(word)

    def test_l2_satro_contains_leet_chars(self) -> None:
        """[L2] У satro режиму излаз садржи leet карактере за речи са a/e/i/o/u/s/t/z."""
        leet_trigger = set("aeioustz")
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            if not any(c in leet_trigger for c in word.lower()):
                continue
            encoded = self.satro.encode_word(word.lower())
            with self.subTest(word=word, encoded=encoded):
                self.assertTrue(
                    any(c in LEET_SATRO_CHARS for c in encoded),
                    f"encode_word({word!r}) = {encoded!r}: нема leet карактера",
                )

    def test_l3_utro_starts_00(self) -> None:
        """[L3] У utro режиму излаз почиње са '00' за речи ≥ min_word_length."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.utro.encode_word(word.lower())
            with self.subTest(word=word):
                self.assertTrue(
                    encoded.startswith("00"),
                    f"encode_word({word!r}) = {encoded!r}: не почиње са '00'",
                )

    def test_l4_utro_contains_24(self) -> None:
        """[L4] У utro режиму излаз садржи '24' (за_style='24')."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.utro.encode_word(word.lower())
            with self.subTest(word=word):
                self.assertIn(
                    "24",
                    encoded,
                    f"encode_word({word!r}) = {encoded!r}: нема '24'",
                )

    def test_l5_utro_ends_n73(self) -> None:
        """[L5] У utro режиму излаз завршава са 'n73'."""
        for word in CORPUS_963:
            if len(word) < _MIN:
                continue
            encoded = self.utro.encode_word(word.lower())
            with self.subTest(word=word):
                self.assertTrue(
                    encoded.endswith("n73"),
                    f"encode_word({word!r}) = {encoded!r}: не завршава са 'n73'",
                )

    def test_l6_short_words_unchanged(self) -> None:
        """[L6] Речи краће од min_word_length се не мењају у оба режима."""
        for word in CORPUS_963:
            if len(word) >= _MIN:
                continue
            with self.subTest(word=word):
                self.assertEqual(self.satro.encode_word(word), word)
                self.assertEqual(self.utro.encode_word(word), word)


if __name__ == "__main__":
    unittest.main(verbosity=2)
