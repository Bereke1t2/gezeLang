import pytest, ast, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapter import AdapterRegistry
from lexer import OromLexer
from parser import OromParser
from codegen import CodeGen

AdapterRegistry.discover(Path(__file__).parent.parent / 'adapters')

def transpile(src):
    lexer = OromLexer(src, 'amharic')
    py_src = lexer.translate()
    tree = OromParser().parse(py_src)
    return CodeGen().generate(tree)

def test_hello_world():
    result = transpile("አሳይ('ሰላም ዓለም!')")
    assert "print" in result

def test_function():
    src = "ስራ ጨምር(ሀ, ለ):\n    መልስ ሀ + ለ"
    result = transpile(src)
    assert 'def' in result
    assert 'return' in result

def test_class():
    src = "ክፍለ ሰው:\n    ስራ __init__(እኔ, ስም):\n        እኔ.ስም = ስም"
    result = transpile(src)
    assert 'class' in result
    assert 'self' in result

def test_corpus():
    """Run all corpus pairs."""
    corpus = Path(__file__).parent / 'corpus'
    for amh_file in sorted(corpus.glob('*.amh')):
        py_file = amh_file.with_suffix('.py')
        if not py_file.exists():
            continue
        source = amh_file.read_text(encoding='utf-8')
        expected = py_file.read_text(encoding='utf-8').strip()
        result = transpile(source).strip()
        assert result == expected, f"Corpus mismatch: {amh_file.name}"
