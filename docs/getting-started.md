# Getting Started — AmharicScript

## Install
```bash
pip install amharicscript
# or
git clone https://github.com/bereket/amharicscript && cd amharicscript
```

## Your First Program
Create hello.amh:
```amharic
አሳይ('ሰላም ዓለም!')
```
Run it:
```bash
python translator.py hello.amh
# Output: ሰላም ዓለም!
```

## CLI Reference
| Command | Description |
|---------|-------------|
| python translator.py file.amh | Transpile and run |
| python translator.py file.amh --emit | Generate file.py only |
| python translator.py file.amh --check | Syntax check only |
| python translator.py file.amh --stats | Show keyword statistics |
| python translator.py --list-langs | List installed adapters |
| python translator.py --compare file.amh amharic oromo | Compare adapters |

## VS Code Extension
1. Install: search "AmharicScript" in Extensions panel
2. Open any .amh file — keywords highlight automatically
3. Type ስራ → Tab to expand function snippet
4. Click ▶ in editor title bar to run the file
5. Hover any keyword to see Python equivalent + meaning

## Next Steps
- [Keyword Reference](keywords.md) — all 37 keywords
- [Adding a Language](adding-language.md) — contribute a new adapter
- [Architecture](architecture.md) — how the transpiler works
