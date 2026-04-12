# Skrit

Skrit is a Python toolkit for Serbian slang-style text transforms:

- `satrovacki` (base split/swap transform)
- `utrovacki` (derived from satro: `u + second + za + first + nje`)
- `leetrovacki` (leet layer over satro/utro logic)

The main entry point is `skrit.py` (router + CLI).

## Project Story

Skrit is a recreation of an older idea.

The original concept existed much earlier, around 2000, as a personal
experiment written in the mIRC scripting language (mIRC script/basic style).
It was my first and only attempt to turn street talk and slang patterns into a
kind of playful "encryption" system.

That early script was likely published on a paste site that no longer exists,
so the original implementation was lost.

This repository brings that same core idea back, now rebuilt in Python after a
long time.

Future direction may include:

- a TypeScript module version
- and later, a possible integration into the AndroidIRCx app

## Requirements

- Python 3.10+

## Quick Start

```bash
py skrit.py --mode auto "Zemun zakon matori"
```

Output:

```text
Munze konza matori
```

## Modes

- `--mode auto` - detect and choose module automatically (`satro`, `utro`, or `leet`)
- `--mode satro` - force satrovacki
- `--mode utro` - force utrovacki
- `--mode leet` - force leetrovacki

## Examples (with output)

### Auto

```bash
py skrit.py --mode auto "Zemun zakon matori"
```

```text
Munze konza matori
```

### Satro

```bash
py skrit.py --mode satro "Zemun zakon matori"
```

```text
Munze konza matori
```

### Utro

```bash
py skrit.py --mode utro "Zemun zakon matori"
```

```text
Umunzazenje ukonzazanje utorizamanje
```

```bash
py skrit.py --mode utro "Zemun Pistolj Bazen"
```

```text
Umunzazenje Ustoljzapinje Uzenzabanje
```

### Leet (default leet base = auto)

```bash
py skrit.py --mode leet "Zemun zakon matori"
```

```text
M00n23 k0n24 70r1m4
```

### Leet over Utro base

```bash
py skrit.py --mode leet --leet-base utro "Zemun zakon matori"
```

```text
00mun24zen73 00kon24zan73 00tori24man73
```

### Keep the same encryption style as reference text

```bash
py skrit.py --mode auto --detect-from "M00n23 k0n24 70r1m4" "Zemun zakon matori"
```

```text
M00n23 k0n24 70r1m4
```

### Show detected mode

```bash
py skrit.py --mode auto --show-mode "Zemun zakon matori"
```

```text
[mode=satro]
Munze konza matori
```

### Full leet profile

```bash
py skrit.py --mode leet --leet-profile full "Zemun zakon matori"
```

```text
/\/\(_)^/23 >|0^/24 70ri21/\/\4
```

`full` uses the full per-letter variant table from `leet.py` (`LEET_TABLE`).
You can choose deeper variants with `--leet-complexity`.

```bash
py skrit.py --mode leet --leet-profile full --leet-complexity 2 "Zemun zakon matori"
```

```text
[v]v/\/-/_[- 1<oh/\/-/_@ -|-oh|`][[v]@
```

### Readable full leet with density control

```bash
py skrit.py --mode leet --leet-profile readable --leet-density 0.5 "Zemun zakon matori"
```

```text
Munze k0nz4 70ri21^^4
```

### Cyrillic option examples

```bash
py skrit.py --mode utro --plain-c-target "ч" "ацб"
```

```text
учбзаање
```

```bash
py skrit.py --mode utro --soft-tj "атјб"
```

```text
ућбзаање
```

### Longer Cyrillic sentence examples

```bash
py skrit.py --mode auto "Земун закон матори пиштољ базен значка ђаво"
```

```text
Мунзе конза матори штољпи зенба чказна вођа
```

```bash
py skrit.py --mode utro "Земун закон матори пиштољ базен значка ђаво"
```

```text
Умунзазење уконзазање уторизамање уштољзапиње узензабање учказазнање увозађање
```

```bash
py skrit.py --mode leet --leet-base utro "Земун закон матори пиштољ базен значка ђаво"
```

```text
00мун24зен73 00кон24зан73 00тори24ман73 00штољ24пин73 00зен24бан73 00чка24знан73 00во24ђан73
```

## CLI Help

```bash
py skrit.py --help
```

The CLI supports:

- `--mode {auto,satro,utro,leet}`
- `--show-mode`
- `--detect-from`
- `--min-word-length`
- `--plain-c-target {ц,ч,ћ}`
- `--soft-tj`
- `--leet-base {auto,satro,utro}`
- `--leet-profile {basic,readable,full}`
- `--leet-complexity`
- `--leet-density` (default: `0.86`)
- `--za-style {24,z4}`
- `--nje-style {n73,nj3,њ}`
- `--utro-prefix`
- `--utro-infix`
- `--utro-suffix`

## Command Examples For All Flags

### `--show-mode`

```bash
py skrit.py --mode auto --show-mode "M00n23 k0n24"
```

```text
[mode=leet]
M00n23 k0n24
```

### `--detect-from`

```bash
py skrit.py --mode auto --detect-from "M00n23 k0n24 70r1m4" "Zemun zakon matori"
```

```text
M00n23 k0n24 70r1m4
```

### `--min-word-length`

```bash
py skrit.py --mode satro --min-word-length 5 "riba rep"
```

```text
riba rep
```

### `--plain-c-target`

```bash
py skrit.py --mode utro --plain-c-target "ч" "ацб"
```

```text
учбзаање
```

### `--soft-tj`

```bash
py skrit.py --mode utro --soft-tj "атјб"
```

```text
ућбзаање
```

### `--leet-base`

```bash
py skrit.py --mode leet --leet-base utro "Zemun zakon matori"
```

```text
00mun24zen73 00kon24zan73 00tori24man73
```

### `--leet-profile`

```bash
py skrit.py --mode leet --leet-profile full "Zemun zakon matori"
```

```text
/\/\(_)^/23 >|0^/24 70ri21/\/\4
```

### `--leet-complexity`

```bash
py skrit.py --mode leet --leet-profile full --leet-complexity 2 "Zemun zakon matori"
```

```text
[v]v/\/-/_[- 1<oh/\/-/_@ -|-oh|`][[v]@
```

### `--leet-density`

```bash
py skrit.py --mode leet --leet-profile readable --leet-density 0.5 "Zemun zakon matori"
```

```text
Munze k0nz4 70ri21^^4
```

### `--za-style`

```bash
py skrit.py --mode leet --leet-base utro --za-style z4 "Zemun zakon matori"
```

```text
00munz4zen73 00konz4zan73 00toriz4man73
```

### `--nje-style`

```bash
py skrit.py --mode leet --leet-base utro --nje-style nj3 "Zemun zakon matori"
```

```text
00mun24zenj3 00kon24zanj3 00tori24manj3
```

### `--utro-prefix --utro-infix --utro-suffix`

```bash
py skrit.py --mode utro --utro-prefix x --utro-infix yy --utro-suffix zz "bazen"
```

```text
xzenyybazz
```

## Project Modules

- `skrit.py` - unified router/CLI
- `satrovacki.py` - satro transformer
- `utrovacki.py` - utro transformer
- `leet.py` - leet table + profiles + helper API
- `leetrovacki.py` - leet transformer on top of satro/utro

## Community Standards

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `SUPPORT.md`
- `.github/ISSUE_TEMPLATE/*`
- `.github/PULL_REQUEST_TEMPLATE.md`

## License

This project is licensed under the GNU General Public License v3.0.
See `LICENSE` for the full text.

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Local Commit Gate (Coverage 100%)

Enable repo hooks:

```bash
git config core.hooksPath .githooks
```

With this enabled, `pre-commit` runs tests under coverage and blocks commit unless coverage stays at 100% (from `.coveragerc`).
