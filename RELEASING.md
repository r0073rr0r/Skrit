# Releasing (Local PyPI Upload)

## 1) Bump version

Edit `pyproject.toml`:

- `[project].version = "X.Y.Z"`

Use a new version every release (PyPI does not allow overwriting files).

## 2) Run quality checks

```bash
py -m flake8 .
py -m unittest discover -s tests -p "test_*.py"
py -m coverage run -m unittest discover -s tests -p "test_*.py"
py -m coverage report
```

Expected: 100% coverage gate passes.

## 3) Build distributions

```bash
py -m pip install --upgrade build twine
py -m build
py -m twine check dist/skrit-*.tar.gz dist/skrit-*-py3-none-any.whl
```

## 4) Configure PyPI credentials

Preferred location: `%USERPROFILE%\\.pypirc`

Example:

```ini
[pypi]
username = __token__
password = pypi-<your-token>
```

Never commit `.pypirc` to git.

## 5) Upload to PyPI

If `%USERPROFILE%\\.pypirc` exists:

```bash
py -m twine upload dist/skrit-*.tar.gz dist/skrit-*-py3-none-any.whl
```

If you want to force a repo-local config file:

```bash
py -m twine upload --config-file .pypirc dist/skrit-*.tar.gz dist/skrit-*-py3-none-any.whl
```

## 6) Verify

Open:

- `https://pypi.org/project/skrit/`
