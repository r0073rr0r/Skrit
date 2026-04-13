from __future__ import annotations

import argparse
import re
import sys
from typing import Literal

from leet import (
    DEFAULT_LEET_DENSITY,
    LEET_SIGNAL_CHARS,
    available_profiles,
    looks_like_leet,
)
from leetrovacki import Leetrovacki
from satrovacki import WORD_OR_OTHER_PATTERN, Satrovacki, _cyrillic_to_latin
from utrovacki import Utrovacki

SkritMode = Literal["auto", "satro", "utro", "leet"]


def _ensure_utf8_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except OSError:
            pass


def _looks_like_utro_word(word: str) -> bool:
    normalized = _cyrillic_to_latin(word).lower()
    return normalized.startswith("u") and "za" in normalized and normalized.endswith("nje")


def _looks_like_utro_leet(text: str) -> bool:
    lowered = text.lower()
    has_prefix = "00" in lowered
    has_middle = "24" in lowered or "z4" in lowered
    has_suffix = "n73" in lowered or "nj3" in lowered or "њ" in text
    return has_prefix and has_middle and has_suffix


def _looks_like_utrovacki(
    text: str,
    *,
    min_word_length: int = 3,
    plain_c_target: str = "ц",
    soft_tj_to_cyrillic: bool = False,
    utro_prefix: str = "u",
    utro_infix: str = "za",
    utro_suffix: str = "nje",
) -> bool:
    utro = Utrovacki(
        min_word_length=min_word_length,
        plain_c_target=plain_c_target,
        soft_tj_to_cyrillic=soft_tj_to_cyrillic,
        prefix=utro_prefix,
        infix=utro_infix,
        suffix=utro_suffix,
    )
    words = [part for part in WORD_OR_OTHER_PATTERN.findall(text) if part.isalpha()]
    words = [word for word in words if len(word) >= min_word_length]
    if not words:
        return False

    decodable_words = sum(1 for word in words if utro.can_decode_word(word))
    return decodable_words > 0 and (decodable_words / len(words)) >= 0.5


def _looks_like_leetrovacki(text: str) -> bool:
    if looks_like_leet(text) or _looks_like_utro_leet(text):
        return True

    tokens = [token for token in re.findall(r"\S+", text) if token]
    if not tokens:
        return False

    symbol_chars = LEET_SIGNAL_CHARS.difference(set("0123456789"))

    def _is_leet_token(token: str) -> bool:
        has_alpha = any(char.isalpha() for char in token)
        has_digit = any(char.isdigit() for char in token)
        has_symbol = any(char in symbol_chars or char in "`$" for char in token)
        return (has_digit and (has_alpha or has_symbol)) or (has_alpha and has_symbol)

    leet_tokens = sum(1 for token in tokens if _is_leet_token(token))
    return leet_tokens > 0 and (leet_tokens / len(tokens)) >= 0.5


def detect_leet_base(text: str) -> Literal["satro", "utro"]:
    if _looks_like_utro_leet(text):
        return "utro"

    words = [part for part in WORD_OR_OTHER_PATTERN.findall(text) if part.isalpha()]
    if not words:
        return "satro"

    utro_words = sum(1 for word in words if _looks_like_utro_word(word))
    if utro_words > 0 and (utro_words / len(words)) >= 0.5:
        return "utro"
    return "satro"


def detect_mode(
    text: str,
    *,
    min_word_length: int = 3,
    plain_c_target: str = "ц",
    soft_tj_to_cyrillic: bool = False,
    utro_prefix: str = "u",
    utro_infix: str = "za",
    utro_suffix: str = "nje",
) -> Literal["satro", "utro", "leet"]:
    if _looks_like_leetrovacki(text):
        return "leet"

    if _looks_like_utrovacki(
        text,
        min_word_length=min_word_length,
        plain_c_target=plain_c_target,
        soft_tj_to_cyrillic=soft_tj_to_cyrillic,
        utro_prefix=utro_prefix,
        utro_infix=utro_infix,
        utro_suffix=utro_suffix,
    ):
        return "utro"
    return "satro"


def _looks_like_satro_encoded(
    text: str,
    *,
    min_word_length: int = 3,
    plain_c_target: str = "ц",
    soft_tj_to_cyrillic: bool = False,
) -> bool:
    satro = Satrovacki(
        min_word_length=min_word_length,
        plain_c_target=plain_c_target,
        soft_tj_to_cyrillic=soft_tj_to_cyrillic,
    )
    words = [part for part in WORD_OR_OTHER_PATTERN.findall(text) if part.isalpha()]
    words = [word for word in words if len(word) >= min_word_length]
    if not words:
        return False

    decodable_words = sum(1 for word in words if satro.can_decode_word(word))
    return decodable_words > 0 and (decodable_words / len(words)) >= 0.5


def _deleet_text_basic(text: str) -> str:
    multi = (
        ("n73", "nje"),
        ("nj3", "nje"),
        ("њ", "nje"),
        ("z4", "za"),
        ("24", "za"),
        ("00", "u"),
    )
    single = {
        "0": "o",
        "1": "i",
        "2": "z",
        "3": "e",
        "4": "a",
        "5": "s",
        "6": "g",
        "7": "t",
        "8": "b",
        "9": "p",
        "$": "s",
    }

    def _deleet_word(word: str) -> str:
        w = word.lower()
        for src, dst in multi:
            w = w.replace(src, dst)
        w = "".join(single.get(char, char) for char in w)
        if word.isupper():
            return w.upper()
        if word.istitle():
            return w.capitalize()
        return w

    parts = re.findall(r"\S+|\s+", text, re.UNICODE)
    transformed: list[str] = []
    for part in parts:
        if part.isspace():
            transformed.append(part)
        else:
            transformed.append(_deleet_word(part))
    return "".join(transformed)


def encode_text(
    text: str,
    *,
    mode: SkritMode = "auto",
    detect_from: str | None = None,
    min_word_length: int = 3,
    plain_c_target: str = "ц",
    soft_tj_to_cyrillic: bool = False,
    leet_base: Literal["auto", "satro", "utro"] = "auto",
    leet_profile: str = "basic",
    leet_complexity: int = 0,
    leet_density: float = DEFAULT_LEET_DENSITY,
    za_style: Literal["24", "z4"] = "24",
    nje_style: Literal["n73", "nj3", "њ"] = "n73",
    utro_prefix: str = "u",
    utro_infix: str = "za",
    utro_suffix: str = "nje",
) -> tuple[str, Literal["satro", "utro", "leet"]]:
    resolved_mode: Literal["satro", "utro", "leet"]
    reference_text = text
    if mode == "auto":
        reference_text = detect_from if detect_from is not None else text
        resolved_mode = detect_mode(
            reference_text,
            min_word_length=min_word_length,
            plain_c_target=plain_c_target,
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
            utro_prefix=utro_prefix,
            utro_infix=utro_infix,
            utro_suffix=utro_suffix,
        )
    else:
        resolved_mode = mode

    if resolved_mode == "satro":
        encoder = Satrovacki(
            min_word_length=min_word_length,
            plain_c_target=plain_c_target,
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
        )
        if mode == "auto" and detect_from is None and _looks_like_satro_encoded(
            reference_text,
            min_word_length=min_word_length,
            plain_c_target=plain_c_target,
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
        ):
            return encoder.decode(text), resolved_mode
        return encoder.encode(text), resolved_mode

    if resolved_mode == "utro":
        encoder = Utrovacki(
            min_word_length=min_word_length,
            plain_c_target=plain_c_target,
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
            prefix=utro_prefix,
            infix=utro_infix,
            suffix=utro_suffix,
        )
        if mode == "auto" and detect_from is None and _looks_like_utrovacki(
            reference_text,
            min_word_length=min_word_length,
            plain_c_target=plain_c_target,
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
            utro_prefix=utro_prefix,
            utro_infix=utro_infix,
            utro_suffix=utro_suffix,
        ):
            return encoder.decode(text), resolved_mode
        return encoder.encode(text), resolved_mode

    resolved_leet_base = leet_base
    if resolved_mode == "leet" and leet_base == "auto":
        resolved_leet_base = detect_leet_base(reference_text)

    if mode == "auto" and detect_from is None and _looks_like_leetrovacki(reference_text):
        deleeted = _deleet_text_basic(text)
        if resolved_leet_base == "utro":
            utro = Utrovacki(
                min_word_length=min_word_length,
                plain_c_target=plain_c_target,
                soft_tj_to_cyrillic=soft_tj_to_cyrillic,
                prefix=utro_prefix,
                infix=utro_infix,
                suffix=utro_suffix,
            )
            if _looks_like_utrovacki(
                deleeted,
                min_word_length=min_word_length,
                plain_c_target=plain_c_target,
                soft_tj_to_cyrillic=soft_tj_to_cyrillic,
                utro_prefix=utro_prefix,
                utro_infix=utro_infix,
                utro_suffix=utro_suffix,
            ):
                return utro.decode(deleeted), resolved_mode
        satro = Satrovacki(
            min_word_length=min_word_length,
            plain_c_target=plain_c_target,
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
        )
        if _looks_like_satro_encoded(
            deleeted,
            min_word_length=min_word_length,
            plain_c_target=plain_c_target,
            soft_tj_to_cyrillic=soft_tj_to_cyrillic,
        ):
            return satro.decode(deleeted), resolved_mode
        return deleeted, resolved_mode

    encoder = Leetrovacki(
        base_mode=resolved_leet_base,
        min_word_length=min_word_length,
        plain_c_target=plain_c_target,
        soft_tj_to_cyrillic=soft_tj_to_cyrillic,
        leet_profile=leet_profile,
        leet_complexity=leet_complexity,
        leet_density=leet_density,
        za_style=za_style,
        nje_style=nje_style,
    )
    return encoder.encode(text), resolved_mode


def main() -> None:
    _ensure_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="Unified encoder router for satrovacki, utrovacki and leetrovacki."
    )
    parser.add_argument("text", nargs="+", help="Text to transform")
    parser.add_argument(
        "--mode",
        choices=["auto", "satro", "utro", "leet"],
        default="auto",
        help="Auto-detect encryption style or force a specific module.",
    )
    parser.add_argument(
        "--show-mode",
        action="store_true",
        help="Print detected/selected module.",
    )
    parser.add_argument(
        "--detect-from",
        default=None,
        help="When --mode is auto, detect style from this reference text.",
    )
    parser.add_argument(
        "--min-word-length",
        type=int,
        default=3,
        help="Do not transform words shorter than this length.",
    )
    parser.add_argument(
        "--plain-c-target",
        choices=["ц", "ч", "ћ"],
        default="ц",
        help="How plain Latin 'c' is mapped in Cyrillic output.",
    )
    parser.add_argument(
        "--soft-tj",
        action="store_true",
        help="Enable optional 'tj -> ћ' handling in Cyrillic conversion.",
    )

    parser.add_argument(
        "--leet-base",
        choices=["auto", "satro", "utro"],
        default="auto",
        help="For leet mode: choose satro/utro base (or auto-detect).",
    )
    parser.add_argument(
        "--leet-profile",
        choices=list(available_profiles()),
        default="basic",
        help="Leet profile (basic/readable/full).",
    )
    parser.add_argument(
        "--leet-density",
        type=float,
        default=DEFAULT_LEET_DENSITY,
        help=f"Share of letters to transform in leet mode (0.0 to 1.0, default: {DEFAULT_LEET_DENSITY}).",
    )
    parser.add_argument(
        "--leet-complexity",
        type=int,
        default=0,
        help="Variant depth for full profile (0 = first variant).",
    )
    parser.add_argument(
        "--za-style",
        choices=["24", "z4"],
        default="24",
        help="Leet replacement for the 'za' block in utro-derived forms.",
    )
    parser.add_argument(
        "--nje-style",
        choices=["n73", "nj3", "њ"],
        default="n73",
        help="Leet replacement for the final 'nje' block.",
    )

    parser.add_argument(
        "--utro-prefix",
        default="u",
        help="Utro prefix (default: u).",
    )
    parser.add_argument(
        "--utro-infix",
        default="za",
        help="Utro infix inserted between swapped chunks (default: za).",
    )
    parser.add_argument(
        "--utro-suffix",
        default="nje",
        help="Utro suffix (default: nje).",
    )
    args = parser.parse_args()

    encoded, resolved_mode = encode_text(
        " ".join(args.text),
        mode=args.mode,
        detect_from=args.detect_from,
        min_word_length=args.min_word_length,
        plain_c_target=args.plain_c_target,
        soft_tj_to_cyrillic=args.soft_tj,
        leet_base=args.leet_base,
        leet_profile=args.leet_profile,
        leet_complexity=args.leet_complexity,
        leet_density=args.leet_density,
        za_style=args.za_style,
        nje_style=args.nje_style,
        utro_prefix=args.utro_prefix,
        utro_infix=args.utro_infix,
        utro_suffix=args.utro_suffix,
    )

    if args.show_mode:
        print(f"[mode={resolved_mode}]")
    print(encoded)


if __name__ == "__main__":
    main()
