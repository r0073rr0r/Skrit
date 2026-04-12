from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import Literal

from leet import (
    DEFAULT_LEET_DENSITY,
    apply_leet,
    available_profiles,
    get_leet_profile,
)
from satrovacki import (
    WORD_OR_OTHER_PATTERN,
    _contains_cyrillic,
    _cyrillic_to_latin,
    _latin_to_cyrillic,
)
from utrovacki import Utrovacki
from satrovacki import Satrovacki

BaseMode = Literal["auto", "utro", "satro"]
ZaStyle = Literal["24", "z4"]
NjeStyle = Literal["n73", "nj3", "њ"]


def _ensure_utf8_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except OSError:
            pass


@dataclass(slots=True)
class Leetrovacki:
    base_mode: BaseMode = "auto"
    za_style: ZaStyle = "24"
    nje_style: NjeStyle = "n73"
    prefix_style: str = "00"
    leet_profile: str = "basic"
    leet_complexity: int = 0
    leet_density: float = DEFAULT_LEET_DENSITY
    vowels: str = "aeiou"
    min_word_length: int = 3
    exceptions: dict[str, str] = field(default_factory=dict)
    soft_tj_to_cyrillic: bool = False
    plain_c_target: str = "ц"
    leet_map: dict[str, str] | None = None
    _satro: Satrovacki = field(init=False, repr=False)
    _utro: Utrovacki = field(init=False, repr=False)
    _leet_map: dict[str, str] = field(init=False, repr=False)
    _full_letter_leet: bool = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.base_mode not in {"auto", "utro", "satro"}:
            raise ValueError("base_mode must be one of: 'auto', 'utro', 'satro'")
        if self.za_style not in {"24", "z4"}:
            raise ValueError("za_style must be one of: '24', 'z4'")
        if self.nje_style not in {"n73", "nj3", "њ"}:
            raise ValueError("nje_style must be one of: 'n73', 'nj3', 'њ'")
        if self.plain_c_target not in {"ц", "ч", "ћ"}:
            raise ValueError("plain_c_target must be one of: 'ц', 'ч', 'ћ'")
        if self.leet_map is None and self.leet_profile not in available_profiles():
            valid = ", ".join(available_profiles())
            raise ValueError(f"leet_profile must be one of: {valid}")
        if not isinstance(self.leet_complexity, int) or self.leet_complexity < 0:
            raise ValueError("leet_complexity must be a non-negative integer")
        if not 0.0 <= self.leet_density <= 1.0:
            raise ValueError("leet_density must be between 0.0 and 1.0")

        self._satro = Satrovacki(
            vowels=self.vowels,
            min_word_length=self.min_word_length,
            exceptions=dict(self.exceptions),
            soft_tj_to_cyrillic=self.soft_tj_to_cyrillic,
            plain_c_target=self.plain_c_target,
        )
        self._leet_map = get_leet_profile(
            self.leet_profile,
            self.leet_map,
            complexity=self.leet_complexity,
        )
        self._full_letter_leet = self.leet_map is not None or self.leet_profile in {
            "readable",
            "full",
        }
        self._utro = Utrovacki(
            vowels=self.vowels,
            min_word_length=self.min_word_length,
            exceptions=dict(self.exceptions),
            soft_tj_to_cyrillic=self.soft_tj_to_cyrillic,
            plain_c_target=self.plain_c_target,
        )

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

        variant, base_word = self._resolve_base_word(lower_word)
        if variant == "utro":
            transformed_latin = self._leetify_utro(base_word, output_script_is_cyrillic)
        else:
            transformed_latin = self._leetify_satro(base_word)

        if output_script_is_cyrillic:
            transformed = _latin_to_cyrillic(
                transformed_latin,
                use_tj_for_c=self.soft_tj_to_cyrillic,
                plain_c_target=self.plain_c_target,
            )
        else:
            transformed = transformed_latin

        return self._apply_case(word, transformed)

    def _resolve_base_word(self, lower_word: str) -> tuple[str, str]:
        if self.base_mode == "utro":
            return "utro", self._utro.encode_word(lower_word)
        if self.base_mode == "satro":
            return "satro", self._satro.encode_word(lower_word)

        if self._looks_like_utro(lower_word):
            return "utro", lower_word
        return "satro", lower_word

    def _looks_like_utro(self, word: str) -> bool:
        return word.startswith("u") and "za" in word and word.endswith("nje")

    def _leetify_utro(self, word: str, output_script_is_cyrillic: bool) -> str:
        transformed = word

        if transformed.startswith("u"):
            transformed = f"{self.prefix_style}{transformed[1:]}"

        za_index = transformed.find("za")
        if za_index != -1:
            left = transformed[:za_index]
            right = transformed[za_index + 2 :]
            if self._full_letter_leet:
                left = apply_leet(left, self._leet_map, density=self.leet_density)
                right = apply_leet(right, self._leet_map, density=self.leet_density)
            transformed = f"{left}{self.za_style}{right}"
        elif self._full_letter_leet:
            transformed = apply_leet(transformed, self._leet_map, density=self.leet_density)

        if transformed.endswith("nje"):
            suffix = self._nje_replacement(output_script_is_cyrillic)
            transformed = f"{transformed[:-3]}{suffix}"

        return transformed

    def _nje_replacement(self, output_script_is_cyrillic: bool) -> str:
        if self.nje_style == "њ":
            if output_script_is_cyrillic:
                return "nj"
            return "nj"
        return self.nje_style

    def _leetify_satro(self, word: str) -> str:
        return apply_leet(word, self._leet_map, density=self.leet_density)

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
        description="Leetrovacki encoder (leet over satrovacki/utrovacki)."
    )
    parser.add_argument("text", nargs="+", help="Text to transform")
    parser.add_argument(
        "--mode",
        choices=["auto", "utro", "satro"],
        default="auto",
        help="Auto mode detects utro by u...za...nje pattern, otherwise satro.",
    )
    parser.add_argument(
        "--za-style",
        choices=["24", "z4"],
        default="24",
        help="Leet replacement for 'za' in utro mode.",
    )
    parser.add_argument(
        "--nje-style",
        choices=["n73", "nj3", "њ"],
        default="n73",
        help="Leet replacement for the 'nje' ending in utro mode.",
    )
    parser.add_argument(
        "--leet-profile",
        choices=list(available_profiles()),
        default="basic",
        help="Leet letter replacement profile (basic/readable/full).",
    )
    parser.add_argument(
        "--leet-density",
        type=float,
        default=DEFAULT_LEET_DENSITY,
        help=f"Share of letters to transform (0.0 to 1.0, default: {DEFAULT_LEET_DENSITY}).",
    )
    parser.add_argument(
        "--leet-complexity",
        type=int,
        default=0,
        help="Variant depth for full profile (0 = first variant).",
    )
    args = parser.parse_args()

    encoder = Leetrovacki(
        base_mode=args.mode,
        za_style=args.za_style,
        nje_style=args.nje_style,
        leet_profile=args.leet_profile,
        leet_complexity=args.leet_complexity,
        leet_density=args.leet_density,
    )
    print(encoder.encode(" ".join(args.text)))


if __name__ == "__main__":
    main()
