# reverse.py — High-Performance Reverse Transpiler (Python 3 → Ethiopic Script)
import ast
import re
from typing import Optional, Tuple
from gezeLang.adapter import AdapterRegistry, GezeLangError

class GezeLangReverseError(GezeLangError):
    """Raised when reverse transpilation fails."""
    pass

_REVERSE_SCANNER_CACHE = {}

def _get_reverse_scanner_for_adapter(adapter):
    """
    Build and cache compiled regex scanner that translates Python keywords
    into the target Ethiopic dialect while strictly preserving string literals,
    comments, and non-keyword identifiers.
    """
    if adapter.lang in _REVERSE_SCANNER_CACHE:
        return _REVERSE_SCANNER_CACHE[adapter.lang]

    p2a = adapter._p2a
    # Sort by length descending to match longer keywords first (e.g. 'elif' before 'if')
    py_kws = sorted(p2a.keys(), key=len, reverse=True)
    if not py_kws:
        return None, None

    kw_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, py_kws)) + r')\b')
    scanner = re.compile(
        r'(?P<fstring>[fF](?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'))'
        r'|(?P<string>"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^\"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')'
        r'|(?P<comment>#[^\n]*)'
        r'|(?P<keyword>\b(?:' + '|'.join(map(re.escape, py_kws)) + r')\b)'
    )
    _REVERSE_SCANNER_CACHE[adapter.lang] = (scanner, kw_pattern)
    return scanner, kw_pattern

class ReverseLexer:
    """
    Translates standard Python 3 source into Ethiopic-script source code
    according to the chosen language adapter.
    """
    def __init__(self, python_source: str, lang: str = 'amharic'):
        self.source = python_source
        self.lang = lang
        self.adapter = AdapterRegistry.get(lang)

    def translate(self) -> str:
        scanner, kw_pattern = _get_reverse_scanner_for_adapter(self.adapter)
        if scanner is None:
            return self.source

        p2a = self.adapter._p2a

        def repl(m):
            if m.group('keyword'):
                return p2a.get(m.group('keyword'), m.group('keyword'))
            elif m.group('fstring'):
                fs = m.group('fstring')
                if '{' in fs:
                    # Translate expressions inside { ... } while keeping string formatting intact
                    return re.sub(
                        r'\{([^}]+)\}',
                        lambda im: '{' + kw_pattern.sub(lambda km: p2a.get(km.group(0), km.group(0)), im.group(1)) + '}',
                        fs
                    )
                return fs
            return m.group(0)

        return scanner.sub(repl, self.source)

def reverse_transpile(python_source: str, lang: str = 'amharic') -> str:
    """
    Convert a Python 3 source code string into an Ethiopic-script source code string.
    Example:
      reverse_transpile("def add(a, b): return a + b", lang='amharic')
      -> "ስራ add(a, b): መልስ a + b"
    """
    lexer = ReverseLexer(python_source, lang=lang)
    return lexer.translate()

def verify_round_trip(python_source: str, lang: str = 'amharic') -> Tuple[bool, str, str]:
    """
    Verify bidirectional compiler idempotency:
      AST(Forward(Reverse(PythonCode))) == AST(PythonCode)
    Returns (is_idempotent, original_ast_dump, roundtrip_ast_dump).
    """
    from gezeLang.lexer import OromLexer
    from gezeLang.parser import OromParser
    from gezeLang.codegen import CodeGen

    # 1. Parse original Python AST
    orig_tree = ast.parse(python_source)
    orig_ast_str = ast.dump(orig_tree)

    # 2. Reverse transpile: Python -> Ethiopic
    ethiopic_code = reverse_transpile(python_source, lang=lang)

    # 3. Forward transpile: Ethiopic -> Python
    fwd_lexer = OromLexer(ethiopic_code, lang=lang)
    recompiled_py = fwd_lexer.translate()
    recompiled_tree = OromParser().parse(recompiled_py, original_source=ethiopic_code)
    recompiled_ast_str = ast.dump(recompiled_tree)

    is_identical = (orig_ast_str == recompiled_ast_str)
    return is_identical, orig_ast_str, recompiled_ast_str
