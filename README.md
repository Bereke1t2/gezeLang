# AmharicScript — አማርኛስክሪፕት

Write Python in Amharic. Execute Anywhere.

## Installation
No installation needed — just Python 3.9+

## Usage
```bash
python translator.py hello.amh        # run
python translator.py hello.amh --emit # generate hello.py
python translator.py --list-langs     # see available languages
```

## Example
```amharic
# hello.amh
ስራ ሰላም(ስም):
    አሳይ(f'ሰላም፣ {ስም}!')

ሰላም('ቻሉ')
```

Generates:
```python
def ሰላም(ስም):
    print(f'ሰላም፣ {ስም}!')
ሰላም('ቻሉ')
```

## Adding a New Language
Create `adapters/<langname>/keywords.json` — zero code changes needed.

## License
MIT · Adama Science and Technology University · CSEg 4306
