from __future__ import annotations

import argparse
import sys

from satrovacki import (
    WORD_OR_OTHER_PATTERN,
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

        parsed = self._split_encoded_parts(lower_word)
        if parsed is None:
            transformed = lower_word
        else:
            first_part, second_part = parsed
            transformed = first_part + second_part

        if output_script_is_cyrillic:
            transformed = _latin_to_cyrillic(
                transformed,
                use_tj_for_c=self.soft_tj_to_cyrillic,
                plain_c_target=self.plain_c_target,
            )

        return self._apply_case(word, transformed)

    def can_decode_word(self, word: str) -> bool:
        if len(word) < self.min_word_length:
            return False
        normalized_latin = _cyrillic_to_latin(word) if _contains_cyrillic(word) else word
        return self._split_encoded_parts(normalized_latin.lower()) is not None

    def _split_encoded_parts(self, lower_word: str) -> tuple[str, str] | None:
        if not lower_word.startswith(self.prefix):
            return None
        if self.suffix and not lower_word.endswith(self.suffix):
            return None

        end = len(lower_word) - len(self.suffix) if self.suffix else len(lower_word)
        if end <= len(self.prefix):
            return None

        core = lower_word[len(self.prefix) : end]

        split_at = core.rfind(self.infix)
        if split_at < 0:
            return None

        second_part = core[:split_at]
        first_part = core[split_at + len(self.infix) :]

        if not second_part and not first_part:
            return None
        return first_part, second_part


def _ensure_utf8_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except OSError:
            pass


def main() -> None:
    _ensure_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="Utrovacki encoder (Latin + Cyrillic support)."
    )
    parser.add_argument("text", nargs="+", help="Text to transform")
    args = parser.parse_args()

    encoder = Utrovacki()
    print(encoder.encode(" ".join(args.text)))


if __name__ == "__main__":
    main()
