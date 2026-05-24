import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from amharicscript.adapter import AdapterRegistry
from amharicscript.lexer import OromLexer

AdapterRegistry.discover(Path(__file__).parent.parent / 'amharicscript' / 'adapters')

def test_keyword_translation():
    src = "ስራ ሰላም():\n    አሳይ('ሰላም')"
    lexer = OromLexer(src, lang='amharic')
    result = lexer.translate()
    assert 'def' in result
    assert 'print' in result
    assert 'ስራ' not in result

def test_unicode_identifiers():
    src = "ቻሉ = 10\nአሳይ(ቻሉ)"
    lexer = OromLexer(src, lang='amharic')
    result = lexer.translate()
    assert 'ቻሉ' in result   # identifiers preserved
    assert 'print' in result

def test_all_keywords_translate():
    adapter = AdapterRegistry.get('amharic')
    for amharic, python in adapter._a2p.items():
        if amharic.startswith('$'):
            continue
        src = f"{amharic}"
        lexer = OromLexer(src, lang='amharic')
        result = lexer.translate()
        assert python in result, f"Failed to translate {amharic} → {python}"
