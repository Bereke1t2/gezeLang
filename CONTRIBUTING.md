# Contributing to AmharicScript

Thank you for your interest! Contributions welcome from everyone.

## Ways to Contribute
- 🐛 Report bugs via GitHub Issues
- 📖 Improve documentation
- 🌍 Add a new language adapter (most impactful!)
- ✨ Add new keywords to the Amharic adapter
- 🧪 Add test corpus pairs

## Development Setup
```bash
git clone https://github.com/bereket/amharicscript
cd amharicscript
pip install pytest ruff
pytest tests/ -v
```

## Branch Naming
| Prefix | Use |
|--------|-----|
| feat/ | New feature |
| fix/ | Bug fix |
| lang/ | New language adapter |
| docs/ | Documentation |

## Adding a New Keyword
1. Add entry to adapters/amharic/keywords.json
2. Add at least one corpus test pair in tests/corpus/
3. Run pytest tests/ — must pass
4. Open a PR with a description

## Adding a New Language Adapter
See the full guide: docs/adding-language.md
Estimated time: 4–8 hours for a complete adapter.

## Commit Convention (Conventional Commits)
```
feat(lexer): support compound Amharic keywords
fix(adapter): correct ካልሆነ → else mapping
lang(tigrinya): add initial Tigrinya adapter
docs: update keyword reference table
```

## PR Checklist
- [ ] Tests pass: pytest tests/ -v
- [ ] Lint passes: ruff check .
- [ ] New keywords have corpus test pairs
- [ ] CHANGELOG.md updated under [Unreleased]
