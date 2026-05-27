# Changelog

All notable changes to GezeLang are documented here.
Format: [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [1.1.0] — 2026-05-27
### Added
- Added full Tigrinya (ትግርኛ) language mapping to the language plugins
- Added a `--version` flag to the cli.py to show GezeLang version
- Added `architecture.md` to properly document the source-to-source system
- Built unit tests targeting error explainer and language stats modules
- Built `lists_and_dicts.amh` sample file showcasing array manipulations

### Changed
- Refactored all internal error classes cleanly from `Amharic*` to `GezeLang*` prefix formatting
- Resolved CLI name breaking during CI deployment pipelines
- Fixed inappropriate hardcoded terms residing in the `hello.amh` guide code
- Patched completely remaining legacy references inside `amharicscript` core to dynamically use `gezeLang`

## [1.0.0] — 2026-05-24
### Added
- Full Amharic → Python 3 transpiler (37 keywords)
- Plugin architecture: add languages via keywords.json
- CLI: translator.py with run, emit, check, stats, list-langs, compare
- Afan Oromo adapter (adapters/oromo/)
- VS Code extension: syntax highlighting, snippets, hover docs, run button
- Public website: landing page, live playground, full docs
- GitHub Actions CI/CD: test matrix, PyPI publish, GitHub Pages deploy
- Contextual Amharic error explainer
- Language statistics dashboard (--stats)
- Multi-language comparison mode (--compare)
- pytest suite with corpus tests (3 programs × amharic)
