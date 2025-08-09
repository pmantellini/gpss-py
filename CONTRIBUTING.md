# Contributing

Thanks for considering a contribution!

## Development Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Workflow
1. Fork & create a feature branch: `feature/<short-desc>`.
2. Keep commits small & focused; use imperative commit messages (e.g. `Add clock jump logic`).
3. Include or update tests for any new logic or bug fix.
4. Run all tests locally before opening a PR.
5. Open a PR with a summary describing motivation, changes, and any open questions.

## Testing Guidelines
- Add unit tests under `tests/` with filenames `test_*.py`.
- Cover at least one happy path and one edge case.
- Prefer small deterministic tests.

## Style
- Aim for PEP8 & snake_case (legacy camelCase will be refactored gradually).
- Keep functions small and cohesive.
- Add docstrings for public classes/methods when behavior is non-trivial.

## Roadmap Alignment
Before larger features (new block types, statistics framework), open an issue referencing the relevant `ROADMAP.md` item or propose a new one.

## Reporting Issues
Provide:
- Expected vs actual behavior
- Minimal reproducible example (code snippet)
- Environment details (Python version, OS)

## Security
No known security-sensitive operations now. If you still believe you've found a vulnerability, contact maintainers privately (see CODEOWNERS).

## License
By contributing, you agree your contributions will be licensed under the MIT License.
