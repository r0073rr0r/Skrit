from __future__ import annotations

import argparse

from satrovacki import (
    Satrovacki,
    _contains_cyrillic,
    _cyrillic_to_latin,
    _latin_to_cyrillic,
)


class Utrovacki(Satrovacki):
    def __init__(
        self,
        *,
        vowels: str = "aeiou",
        min_word_length: int = 3,
        exceptions: dict[str, str] | None = None,
        soft_tj_to_cyrillic: bool = False,
        plain_c_target: str = "ц",
        prefix: str = "u",
        infix: str = "za",
        suffix: str = "nje",
    ) -> None:
        super().__init__(
            vowels=vowels,
            min_word_length=min_word_length,
            exceptions=exceptions or {},
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
            plain_c_target=plain_c_target,
        )
        self.prefix = prefix.lower()
        self.infix = infix.lower()
        self.suffix = suffix.lower()

    def encode_word(self, word: str) -> str:
        if len(word) < self.min_word_length:
            return word

        output_script_is_cyrillic = _contains_cyrillic(word)
        normalized_latin = _cyrillic_to_latin(word) if output_script_is_cyrillic else word
        lower_word = normalized_latin.lower()
        split_index = self._find_split_index(lower_word)

        first_part = ""
        second_part = ""
        exception_value = self.exceptions.get(lower_word)

        if exception_value is not None:
            satro_word = exception_value.lower()
            if (
                0 < split_index < len(lower_word)
                and len(satro_word) == len(lower_word)
            ):
                second_len = len(lower_word) - split_index
                second_part = satro_word[:second_len]
                first_part = satro_word[second_len:]
            else:
                second_part = satro_word
        else:
            if split_index <= 0 or split_index >= len(lower_word):
                second_part = lower_word
            else:
                first_part = lower_word[:split_index]
                second_part = lower_word[split_index:]

        transformed = f"{self.prefix}{second_part}{self.infix}{first_part}{self.suffix}"

        if output_script_is_cyrillic:
            transformed = _latin_to_cyrillic(
                transformed,
                use_tj_for_c=self.soft_tj_to_cyrillic,
                plain_c_target=self.plain_c_target,
            )

        return self._apply_case(word, transformed)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Utrovacki encoder (Latin + Cyrillic support)."
    )
    parser.add_argument("text", nargs="+", help="Text to transform")
    args = parser.parse_args()

    encoder = Utrovacki()
    print(encoder.encode(" ".join(args.text)))


if __name__ == "__main__":
    main()
