# __init__.py — AmharicScript library API
from amharicscript.adapter import AdapterRegistry
from amharicscript.lexer import OromLexer
from amharicscript.parser import OromParser
from .codegen import CodeGen
from pathlib import Path

_ADAPTERS_DIR = Path(__file__).parent / 'adapters'
AdapterRegistry.discover(_ADAPTERS_DIR)

def transpile(source: str, lang: str = 'amharic') -> str:
    """Transpile Amharic source string to Python source string."""
    lexer = OromLexer(source, lang=lang)
    python_source = lexer.translate()
    parser = OromParser()
    tree = parser.parse(python_source)
    gen = CodeGen()
    return gen.generate(tree)

def execute(source: str, lang: str = 'amharic') -> None:
    """Transpile and execute Amharic source string."""
    py_source = transpile(source, lang=lang)
    exec(compile(py_source, '<amharicscript>', 'exec'), {'__name__': '__main__'})
