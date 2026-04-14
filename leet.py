from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Mapping

DEFAULT_LEET_DENSITY = 0.86


LEET_TABLE: dict[str, tuple[str, ...]] = {
    "a": ("4", "/\\", "@", "^", "(L", "/-\\"),
    "b": ("I3", "8", "13", "|3", "!3", "(3", "/3", ")3", "|-]", "j3"),
    "c": ("[", "<", "(", "{"),
    "d": (")", "|)", "(|", "[)", "I>", "|>", "T)", "I7", "cl", "|}", "|]", "l)", "I)"),
    "e": ("3", "&", "[-", "|=-"),
    "f": ("|=", "|#", "ph", "/=", "v"),
    "g": ("6", "&", "(_+", "9", "C-", "gee", "(?,", "[,", "{,", "<-", "(."),
    "h": ("#", "/-/", "\\-\\", "[-]", "]-[", ")-(", "(-)", ":-:", "|~|", "|-|", "]~[", "}{", "!-!", "1-1", "\\-/", "I+I"),
    "i": ("1", "|", "][", "!", "eye", "3y3"),
    "j": (",_|", "_|", "._|", "._]", "_]", ",_]", "]"),
    "k": (">|", "|<", "1<", "|c", "|("),
    "l": ("1", "7", "2", "|_", "|"),
    "m": ("/\\/\\", "/V\\", "[V]", "|\\/|", "^^", "<\\/>", "{V}", "(v)", "(V)", "|\\|\\", "]\\/[", "nn", "11"),
    "n": ("^/", "|\\|", "/\\/", "[\\]", "<\\>", "{\\}", "/V", "^", "|V"),
    "o": ("0", "()", "oh", "[]", "<>"),
    "p": ("|*", "|o", "|^", "|>", "|\"", "9", "[]D", "|7", "|0"),
    "q": ("(_,)", "()_", "2", "0_", "<|", "&", "9", "0|"),
    "r": ("I2", "9", "|`", "|~", "|?", "/2", "|^", "lz", "l2", "7", "2", "12", "[z", "|-", "|2"),
    "s": ("5", "$", "z", "ehs", "es", "2"),
    "t": ("7", "+", "-|-", "']['", "~|~"),
    "u": ("(_)", "|_|", "v", "L|"),
    "v": ("\\/", "|/", "\\|"),
    "w": ("\\/\\/", "|/\\|", "vv", "\\N", "'//", "\\\\'", "\\^/", "(n)", "\\V/", "\\X/", "\\|/", "\\_|_/", "\\_:_/", "uu", "2u", "\\\\//\\\\//"),
    "x": ("><", "}{", "ecks", ")(", "]["),
    "y": ("j", "`/", "\\|/", "\\//", "'/"),
    "z": ("2", "7_", "-/_", "%"),
}

# Stable profile used in previous outputs (digit-oriented "readable leet").
BASIC_LEET_PROFILE: dict[str, str] = {
    "a": "4",
    "b": "8",
    "e": "3",
    "g": "6",
    "i": "1",
    "o": "0",
    "s": "5",
    "t": "7",
    "u": "00",
    "z": "2",
}

def build_full_leet_profile(complexity: int = 0) -> dict[str, str]:
    if not isinstance(complexity, int) or complexity < 0:
        raise ValueError("complexity must be a non-negative integer")

    profile: dict[str, str] = {}
    for letter, variants in LEET_TABLE.items():
        index = min(complexity, len(variants) - 1)
        profile[letter] = variants[index]

    # Backward-compatible default expected by existing examples.
    if complexity == 0:
        profile["r"] = "ri2"

    return profile


FULL_LEET_PROFILE: dict[str, str] = build_full_leet_profile()

# Readable full profile: one replacement for every letter, but kept practical.
# Values are selected from common/well-known leet variants.
READABLE_FULL_PROFILE: dict[str, str] = {
    "a": "4",
    "b": "8",
    "c": "(",
    "d": "|)",
    "e": "3",
    "f": "ph",
    "g": "6",
    "h": "#",
    "i": "1",
    "j": "_|",
    "k": "|<",
    "l": "1",
    "m": "^^",
    "n": "^/",
    "o": "0",
    "p": "9",
    "q": "0_",
    "r": "ri2",
    "s": "5",
    "t": "7",
    "u": "00",
    "v": "\\/",
    "w": "vv",
    "x": "><",
    "y": "`/",
    "z": "2",
}

LEET_PROFILES: dict[str, dict[str, str]] = {
    "basic": BASIC_LEET_PROFILE,
    "readable": READABLE_FULL_PROFILE,
    "full": FULL_LEET_PROFILE,
}

LEET_SIGNAL_CHARS = set("0123456789@$!+|\\/()[]{}<>^_-*#%")
TOKEN_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


def available_profiles() -> tuple[str, ...]:
    return tuple(sorted(LEET_PROFILES.keys()))


def get_leet_profile(
    name: str = "basic",
    custom_map: Mapping[str, str] | None = None,
    complexity: int = 0,
) -> dict[str, str]:
    if custom_map is not None:
        return {key.lower(): value for key, value in custom_map.items()}

    if name.lower() == "full":
        return build_full_leet_profile(complexity=complexity)

    profile = LEET_PROFILES.get(name.lower())
    if profile is None:
        valid = ", ".join(available_profiles())
        raise ValueError(f"Unknown leet profile '{name}'. Valid profiles: {valid}")
    return dict(profile)


def apply_leet(
    text: str,
    mapping: Mapping[str, str],
    density: float = DEFAULT_LEET_DENSITY,
) -> str:
    if not 0.0 <= density <= 1.0:
        raise ValueError("density must be between 0.0 and 1.0")

    transformed: list[str] = []
    mapped_position = 0
    for char in text:
        replacement = mapping.get(char.lower())
        if replacement is None:
            transformed.append(char)
            continue

        if density < 1.0:
            mapped_position += 1
            score = ((mapped_position * 131) + (ord(char.lower()) * 17)) % 100
            if score >= int(density * 100):
                transformed.append(char)
                continue

        if char.isupper() and replacement.isalpha():
            transformed.append(replacement.upper())
        elif char.islower() and replacement.isalpha():
            transformed.append(replacement.lower())
        else:
            transformed.append(replacement)
    return "".join(transformed)


def looks_like_leet(text: str) -> bool:
    for token in TOKEN_PATTERN.findall(text):
        has_letter = any(char.isalpha() for char in token)
        has_signal = any(char.isdigit() or char in LEET_SIGNAL_CHARS for char in token)
        if has_letter and has_signal:
            return True

    lowered = text.lower()
    return "n73" in lowered or "nj3" in lowered or "00" in lowered or "z4" in lowered


@dataclass(slots=True)
class LeetEncoder:
    profile: str = "basic"
    custom_map: Mapping[str, str] | None = None
    complexity: int = 0
    density: float = DEFAULT_LEET_DENSITY
    _mapping: dict[str, str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._mapping = get_leet_profile(
            self.profile,
            self.custom_map,
            complexity=self.complexity,
        )

    def encode(self, text: str) -> str:
        return apply_leet(text, self._mapping, density=self.density)
