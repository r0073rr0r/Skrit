from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field


CYR_TO_LAT: dict[str, str] = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "ђ": "đ",
    "е": "e",
    "ж": "ž",
    "з": "z",
    "и": "i",
    "ј": "j",
    "к": "k",
    "л": "l",
    "љ": "lj",
    "м": "m",
    "н": "n",
    "њ": "nj",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "ћ": "ć",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "c",
    "ч": "č",
    "џ": "dž",
    "ш": "š",
    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "G",
    "Д": "D",
    "Ђ": "Đ",
    "Е": "E",
    "Ж": "Ž",
    "З": "Z",
    "И": "I",
    "Ј": "J",
    "К": "K",
    "Л": "L",
    "Љ": "Lj",
    "М": "M",
    "Н": "N",
    "Њ": "Nj",
    "О": "O",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "Ћ": "Ć",
    "У": "U",
    "Ф": "F",
    "Х": "H",
    "Ц": "C",
    "Ч": "Č",
    "Џ": "Dž",
    "Ш": "Š",
}

LAT_TO_CYR_DIGRAPHS: dict[str, str] = {
    "dž": "џ",
    "Dž": "Џ",
    "DŽ": "Џ",
    "lj": "љ",
    "Lj": "Љ",
    "LJ": "Љ",
    "nj": "њ",
    "Nj": "Њ",
    "NJ": "Њ",
}

LAT_TO_CYR_SINGLE: dict[str, str] = {
    "a": "а",
    "b": "б",
    "v": "в",
    "g": "г",
    "d": "д",
    "đ": "ђ",
    "e": "е",
    "ž": "ж",
    "z": "з",
    "i": "и",
    "j": "ј",
    "k": "к",
    "l": "л",
    "m": "м",
    "n": "н",
    "o": "о",
    "p": "п",
    "r": "р",
    "s": "с",
    "t": "т",
    "ć": "ћ",
    "u": "у",
    "f": "ф",
    "h": "х",
    "c": "ц",
    "č": "ч",
    "š": "ш",
    "A": "А",
    "B": "Б",
    "V": "В",
    "G": "Г",
    "D": "Д",
    "Đ": "Ђ",
    "E": "Е",
    "Ž": "Ж",
    "Z": "З",
    "I": "И",
    "J": "Ј",
    "K": "К",
    "L": "Л",
    "M": "М",
    "N": "Н",
    "O": "О",
    "P": "П",
    "R": "Р",
    "S": "С",
    "T": "Т",
    "Ć": "Ћ",
    "U": "У",
    "F": "Ф",
    "H": "Х",
    "C": "Ц",
    "Č": "Ч",
    "Š": "Ш",
}

WORD_OR_OTHER_PATTERN = re.compile(r"[^\W\d_]+|\d+|\s+|.", re.UNICODE)

OPTIONAL_TJ_TO_CYR: dict[str, str] = {
    "tj": "ћ",
    "Tj": "Ћ",
    "TJ": "Ћ",
}


def _ensure_utf8_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except OSError:
            pass


def _is_cyrillic_char(char: str) -> bool:
    return ("\u0400" <= char <= "\u04FF") or ("\u0500" <= char <= "\u052F")


def _contains_cyrillic(word: str) -> bool:
    return any(_is_cyrillic_char(char) for char in word)


def _cyrillic_to_latin(text: str) -> str:
    return "".join(CYR_TO_LAT.get(char, char) for char in text)


def _latin_to_cyrillic(
    text: str, *, use_tj_for_c: bool = False, plain_c_target: str = "ц"
) -> str:
    converted: list[str] = []
    index = 0
    length = len(text)
    lower_c_map = {"ц": "ц", "ч": "ч", "ћ": "ћ"}
    upper_c_map = {"ц": "Ц", "ч": "Ч", "ћ": "Ћ"}
    mapped_c_lower = lower_c_map.get(plain_c_target, "ц")
    mapped_c_upper = upper_c_map.get(plain_c_target, "Ц")

    while index < length:
        two_chars = text[index : index + 2]
        if use_tj_for_c:
            mapped_optional = OPTIONAL_TJ_TO_CYR.get(two_chars)
            if mapped_optional is not None:
                converted.append(mapped_optional)
                index += 2
                continue

        mapped_digraph = LAT_TO_CYR_DIGRAPHS.get(two_chars)
        if mapped_digraph is not None:
            converted.append(mapped_digraph)
            index += 2
            continue

        current_char = text[index]
        if current_char == "c":
            converted.append(mapped_c_lower)
        elif current_char == "C":
            converted.append(mapped_c_upper)
        else:
            converted.append(LAT_TO_CYR_SINGLE.get(current_char, current_char))
        index += 1

    return "".join(converted)


@dataclass(slots=True)
class Satrovacki:
    vowels: str = "aeiou"
    min_word_length: int = 3
    exceptions: dict[str, str] = field(
        default_factory=lambda: {
            "brate": "tebra",
            "matori": "matori",
        }
    )
    soft_tj_to_cyrillic: bool = False
    plain_c_target: str = "ц"

    def __post_init__(self) -> None:
        if self.plain_c_target not in {"ц", "ч", "ћ"}:
            raise ValueError("plain_c_target must be one of: 'ц', 'ч', 'ћ'")

    def encode(self, text: str) -> str:
        parts = WORD_OR_OTHER_PATTERN.findall(text)
        encoded_parts: list[str] = []

        for part in parts:
            if part.isalpha():
                encoded_parts.append(self.encode_word(part))
            else:
                encoded_parts.append(part)

        return "".join(encoded_parts)

    def encode_word(self, word: str) -> str:
        if len(word) < self.min_word_length:
            return word

        output_script_is_cyrillic = _contains_cyrillic(word)
        normalized_latin = _cyrillic_to_latin(word) if output_script_is_cyrillic else word
        lower_word = normalized_latin.lower()

        replaced = self.exceptions.get(lower_word)
        if replaced is None:
            split_index = self._find_split_index(lower_word)
            if split_index <= 0 or split_index >= len(lower_word):
                replaced = lower_word
            else:
                replaced = lower_word[split_index:] + lower_word[:split_index]

        if output_script_is_cyrillic:
            replaced = _latin_to_cyrillic(
                replaced,
                use_tj_for_c=self.soft_tj_to_cyrillic,
                plain_c_target=self.plain_c_target,
            )

        return self._apply_case(word, replaced)

    def decode(self, text: str) -> str:
        parts = WORD_OR_OTHER_PATTERN.findall(text)
        decoded_parts: list[str] = []

        for part in parts:
            if part.isalpha():
                decoded_parts.append(self.decode_word(part))
            else:
                decoded_parts.append(part)

        return "".join(decoded_parts)

    def decode_word(self, word: str) -> str:
        if len(word) < self.min_word_length:
            return word

        output_script_is_cyrillic = _contains_cyrillic(word)
        normalized_latin = _cyrillic_to_latin(word) if output_script_is_cyrillic else word
        lower_word = normalized_latin.lower()

        reverse_exceptions = {value: key for key, value in self.exceptions.items()}
        replaced = reverse_exceptions.get(lower_word)

        if replaced is None:
            candidates = self._decode_candidates(lower_word)
            if candidates:
                replaced = self._pick_best_decode_candidate(candidates)
            else:
                replaced = lower_word

        if output_script_is_cyrillic:
            replaced = _latin_to_cyrillic(
                replaced,
                use_tj_for_c=self.soft_tj_to_cyrillic,
                plain_c_target=self.plain_c_target,
            )

        return self._apply_case(word, replaced)

    def can_decode_word(self, word: str) -> bool:
        if len(word) < self.min_word_length:
            return False

        normalized_latin = _cyrillic_to_latin(word) if _contains_cyrillic(word) else word
        lower_word = normalized_latin.lower()
        reverse_exceptions = {value: key for key, value in self.exceptions.items()}
        if lower_word in reverse_exceptions:
            return True
        return bool(self._decode_candidates(lower_word))

    def _encode_latin_word(self, lower_word: str) -> str:
        replaced = self.exceptions.get(lower_word)
        if replaced is not None:
            return replaced

        return self._encode_latin_word_plain(lower_word)

    def _encode_latin_word_plain(self, lower_word: str) -> str:
        split_index = self._find_split_index(lower_word)
        if split_index <= 0 or split_index >= len(lower_word):
            return lower_word
        return lower_word[split_index:] + lower_word[:split_index]

    def _decode_candidates(self, lower_word: str) -> list[tuple[int, str]]:
        candidates: list[tuple[int, str]] = []
        for split_index in range(1, len(lower_word)):
            candidate = lower_word[-split_index:] + lower_word[:-split_index]
            encoded_with_exceptions = self._encode_latin_word(candidate)
            encoded_plain = self._encode_latin_word_plain(candidate)
            if encoded_with_exceptions == lower_word or encoded_plain == lower_word:
                candidates.append((split_index, candidate))
        return candidates

    def _pick_best_decode_candidate(
        self, candidates: list[tuple[int, str]]
    ) -> str:
        half = len(candidates[0][1]) / 2.0
        vowels = self.vowels.lower()

        def score(item: tuple[int, str]) -> tuple[float, int, int, int]:
            split_index, candidate = item
            second_is_vowel = int(len(candidate) > 1 and candidate[1] in vowels)
            starts_with_consonant = int(candidate and candidate[0] not in vowels)
            return (
                abs(split_index - half),
                -second_is_vowel,
                -starts_with_consonant,
                split_index,
            )

        return min(candidates, key=score)[1]

    def _find_split_index(self, word: str) -> int:
        vowels = self.vowels.lower()

        for index, char in enumerate(word):
            if char in vowels:
                split_index = index + 1
                while split_index < len(word) and word[split_index] in vowels:
                    split_index += 1
                return split_index

        return len(word) // 2

    def _apply_case(self, original: str, transformed: str) -> str:
        if original.isupper():
            return transformed.upper()
        if original.istitle():
            return transformed.capitalize()
        if original.islower():
            return transformed.lower()
        return transformed


def main() -> None:
    _ensure_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="Satrovacki encoder (Latin + Cyrillic support)."
    )
    parser.add_argument("text", nargs="+", help="Text to transform")
    args = parser.parse_args()

    encoder = Satrovacki()
    print(encoder.encode(" ".join(args.text)))


if __name__ == "__main__":
    main()
