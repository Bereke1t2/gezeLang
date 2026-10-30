# lexer.py — Unicode tokenizer + Ethiopic→Python keyword translation
import re
import tokenize
import io
from gezeLang.adapter import AdapterRegistry, GezeLangError

class GezeLangLexError(GezeLangError):
    pass

_SCANNER_CACHE = {}

def _get_scanner_for_adapter(adapter):
    if adapter.lang in _SCANNER_CACHE:
        return _SCANNER_CACHE[adapter.lang]
    kw_map = adapter._a2p
    kw_keys = sorted(kw_map.keys(), key=len, reverse=True)
    if not kw_keys:
        return None, None
    kw_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, kw_keys)) + r')\b')
    scanner = re.compile(
        r'(?P<fstring>[fF](?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'))'
        r'|(?P<string>"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')'
        r'|(?P<comment>#[^\n]*)'
        r'|(?P<keyword>\b(?:' + '|'.join(map(re.escape, kw_keys)) + r')\b)'
    )
    _SCANNER_CACHE[adapter.lang] = (scanner, kw_pattern)
    return scanner, kw_pattern

class OromLexer:
    def __init__(self, source: str, lang: str = 'amharic'):
        self.source = source
        self.adapter = AdapterRegistry.get(lang)

    def translate(self, fast: bool = True) -> str:
        """
        Tokenize Ethiopic source, replace Ethiopic keywords with Python keywords,
        return reassembled Python-keyword source string.
        Achieves high-speed sub-millisecond translation per file.
        """
        if fast:
            scanner, kw_pattern = _get_scanner_for_adapter(self.adapter)
            if scanner is not None:
                kw_map = self.adapter._a2p
                def repl(m):
                    if m.group('keyword'):
                        return kw_map[m.group('keyword')]
                    elif m.group('fstring'):
                        fs = m.group('fstring')
                        if '{' in fs:
                            return re.sub(
                                r'\{([^}]+)\}',
                                lambda im: '{' + kw_pattern.sub(lambda km: kw_map.get(km.group(0), km.group(0)), im.group(1)) + '}',
                                fs
                            )
                        return fs
                    return m.group(0)
                return scanner.sub(repl, self.source)

        try:
            tokens = list(tokenize.generate_tokens(
                io.StringIO(self.source).readline
            ))
        except tokenize.TokenError as e:
            raise GezeLangLexError(
                f"ስህተት[E001] ቶከን ስህተት: {e}\n"
                f"ፋይልዎን ትክክለኛ UTF-8 ቅርጸት እንዲሆን ያረጋግጡ።"
            )

        translated = []
        for tok in tokens:
            translated.append(self._translate_token(tok))

        try:
            return tokenize.untokenize(translated)
        except Exception as e:
            raise GezeLangLexError(
                f"ስህተት[E001] ኮድ ለማዋሃድ አልተቻለም: {e}"
            )

    def _translate_token(self, tok):
        """Replace Ethiopic NAME token with Python keyword if it matches."""
        import tokenize as tk
        if tok.type == tk.NAME:
            py_kw = self.adapter.to_python_keyword(tok.string)
            if py_kw:
                return tok._replace(string=py_kw)
        return tok
