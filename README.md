<div align="center">

# አማርኛስክሪፕት · AmharicScript

**Write Python in Amharic — Execute Anywhere**

*ፕሮግራሚንግ በእናታችን ቋንቋ — Programming in our mother tongue*

[![CI](https://github.com/bereket/amharicscript/actions/workflows/ci.yml/badge.svg)](https://github.com/bereket/amharicscript/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/amharicscript)](https://pypi.org/project/amharicscript/)
[![Python](https://img.shields.io/pypi/pyversions/amharicscript)](https://pypi.org/project/amharicscript/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![VS Code](https://img.shields.io/visual-studio-marketplace/v/amharicscript.amharicscript)](https://marketplace.visualstudio.com/items?itemName=amharicscript.amharicscript)

[🌐 Website](https://bereket.github.io/amharicscript) ·
[▶ Playground](https://bereket.github.io/amharicscript/playground.html) ·
[📖 Docs](https://bereket.github.io/amharicscript/docs/) ·
[🔌 VS Code Extension](https://marketplace.visualstudio.com/items?itemName=amharicscript.amharicscript)

</div>

---

## What is AmharicScript?

AmharicScript is an open-source **source-to-source transpiler** that lets developers
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
pip install amharicscript
```

Or clone:
```bash
git clone https://github.com/bereket/amharicscript.git
cd amharicscript
python translator.py examples/hello.amh
```

## VS Code Extension
Install from the marketplace: search **"AmharicScript"** or:
```bash
code --install-extension amharicscript.amharicscript
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

[→ Full 37-keyword reference](https://bereket.github.io/amharicscript/docs/keywords.html)

## Adding a New Language
AmharicScript's plugin architecture makes adding any Ethiopian language trivial:

```bash
# 1. Create adapter folder
mkdir adapters/tigrinya

# 2. Add keywords.json (map Tigrinya → Python)
echo '{"ስራ-tig": "def", ...}' > adapters/tigrinya/keywords.json

# 3. Use it — zero code changes
python translator.py program.tgr --lang tigrinya
```

[→ Full guide: Adding a Language](https://bereket.github.io/amharicscript/docs/adding-language.html)

## Architecture
```
.amh source → Lexer → Parser → Code Gen → .py output → CPython
                ↑
         adapters/amharic/keywords.json  (swappable per language)
```

## Project Structure
```
amharicscript/
├── amharicscript/    # pip-installable package
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
[Adding a Language guide](https://bereket.github.io/amharicscript/docs/adding-language.html).

## Built At
Adama Science and Technology University · SOEEC/CSE · CSEg 4306 · May 2026

## License
MIT — free to use, modify, and distribute.

---
*ለኢትዮጵያ ተማሪዎች ሁሉ — For all Ethiopian students*
