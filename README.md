<div align="center">

# ጌዜ ቋንቋ · GezeLang

**Write Python in Amharic — Execute Anywhere**

*ፕሮግራሚንግ በእናታችን ቋንቋ — Programming in our mother tongue*

[![CI](https://github.com/Bereke1t2/gezeLang/actions/workflows/ci.yml/badge.svg)](https://github.com/Bereke1t2/gezeLang/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/gezeLang)](https://pypi.org/project/gezeLang/)
[![Python](https://img.shields.io/pypi/pyversions/gezeLang)](https://pypi.org/project/gezeLang/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![VS Code](https://img.shields.io/visual-studio-marketplace/v/gezeLang.gezeLang)](https://marketplace.visualstudio.com/items?itemName=gezeLang.gezeLang)

[🌐 Website](https://Bereke1t2.github.io/gezeLang) ·
[▶ Playground](https://Bereke1t2.github.io/gezeLang/playground.html) ·
[📖 Docs](https://Bereke1t2.github.io/gezeLang/docs/) ·
[🔌 VS Code Extension](https://marketplace.visualstudio.com/items?itemName=gezeLang.gezeLang)

</div>

---

## What is GezeLang?

GezeLang is an open-source **source-to-source transpiler** that lets developers
write Python programs using **Amharic (አማርኛ)** keywords and identifiers.

Source files (`.amh`) are parsed into a language-agnostic AST, then compiled to
standard Python 3 — with **zero runtime overhead**.

```amharic
# hello.amh
ስራ ሰላም(ስም):
    አሳይ(f'ሰላም፣ {ስም}!')

ሰላም('ቻሉ')
```
↓ Generates:
```python
def ሰላም(ስም):
    print(f'ሰላም፣ {ስም}!')

ሰላም('ቻሉ')
```

## Installation

```bash
pip install gezeLang
```

Or clone:
```bash
git clone https://github.com/Bereke1t2/gezeLang.git
cd gezeLang
python translator.py examples/hello.amh
```

## VS Code Extension
Install from the marketplace: search **"GezeLang"** or:
```bash
code --install-extension gezeLang.gezeLang
```
Features: syntax highlighting · code snippets · hover docs · ▶ run button

## Usage
```bash
python translator.py program.amh           # transpile + run
python translator.py program.amh --emit    # emit program.py
python translator.py program.amh --stats   # show language statistics
python translator.py --list-langs          # show available language adapters
```

## Keyword Sample
| Amharic | Python | Meaning |
|---------|--------|---------|
| ስራ | def | Define function |
| ከሆነ | if | If condition |
| እስከሆነ | while | While loop |
| አሳይ | print | Print output |
| ክፍለ | class | Define class |
| እኔ | self | Instance self |

[→ Full 37-keyword reference](https://Bereke1t2.github.io/gezeLang/docs/keywords.html)

## Adding a New Language
GezeLang's plugin architecture makes adding any Ethiopian language trivial:

```bash
# 1. Create adapter folder
mkdir adapters/tigrinya

# 2. Add keywords.json (map Tigrinya → Python)
echo '{"ስራ-tig": "def", ...}' > adapters/tigrinya/keywords.json

# 3. Use it — zero code changes
python translator.py program.tgr --lang tigrinya
```

[→ Full guide: Adding a Language](https://Bereke1t2.github.io/gezeLang/docs/adding-language.html)

## Architecture
```
.amh source → Lexer → Parser → Code Gen → .py output → CPython
                ↑
         adapters/amharic/keywords.json  (swappable per language)
```

## Project Structure
```
gezeLang/
├── gezeLang/         # pip-installable package
├── translator.py     # CLI entry point
├── vscode-extension/ # VS Code extension
├── website/          # Static documentation site
├── tests/            # pytest suite + corpus
└── adapters/         # Language plugins (amharic, oromo, ...)
```

## Contributing
We welcome contributions of all kinds — new keywords, new language adapters,
bug fixes, documentation improvements.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

New language adapters are especially welcome! If you speak an Ethiopian language,
you can add support in 4–8 hours by following our
[Adding a Language guide](https://Bereke1t2.github.io/gezeLang/docs/adding-language.html).

## Built At
Adama Science and Technology University · SOEEC/CSE · May 2026

## License
MIT — free to use, modify, and distribute.

---
*ለኢትዮጵያ ተማሪዎች ሁሉ — For all Ethiopian students*
