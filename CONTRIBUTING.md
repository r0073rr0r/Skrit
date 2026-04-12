# Contributing to Skrit

Thanks for contributing.

## Development Setup

1. Use Python 3.10+.
2. Clone the repository.
3. Run tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Project Scope

Skrit contains multiple text transformation modules:

- `satrovacki.py`
- `utrovacki.py`
- `leet.py`
- `leetrovacki.py`
- `skrit.py` (main router/CLI)

If you add a new transformation mode, wire it through `skrit.py` and add tests.

## Coding Guidelines

- Keep code and comments in English.
- Preserve existing behavior unless your PR explicitly changes a rule.
- Add or update tests for every behavior change.
- Keep CLI examples in `README.md` aligned with real command output.

## Pull Requests

1. Open an issue first for non-trivial changes.
2. Create a focused branch and keep the PR small.
3. Include:
   - what changed
   - why it changed
   - test coverage details
4. Ensure all tests pass before requesting review.

## Commit Messages

Use clear, scoped commit messages. Example:

`feat(leet): add full-profile overrides for readability`
