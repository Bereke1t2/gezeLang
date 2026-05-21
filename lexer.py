# lexer.py — Unicode tokenizer + Amharic→Python keyword translation
import tokenize
import io
from adapter import AdapterRegistry, AmharicScriptError

class AmharicLexError(AmharicScriptError):
    pass

class OromLexer:
    def __init__(self, source: str, lang: str = 'amharic'):
        self.source = source
        self.adapter = AdapterRegistry.get(lang)

    def translate(self) -> str:
        """
        Tokenize Amharic source, replace Amharic keywords with Python keywords,
        return reassembled Python-keyword source string.
        """
        try:
            tokens = list(tokenize.generate_tokens(
                io.StringIO(self.source).readline
            ))
        except tokenize.TokenError as e:
            raise AmharicLexError(
                f"ስህተት[E001] ቶከን ስህተት: {e}\n"
                f"ፋይልዎን ትክክለኛ UTF-8 ቅርጸት እንዲሆን ያረጋግጡ።"
            )

        translated = []
        for tok in tokens:
            translated.append(self._translate_token(tok))

        try:
            return tokenize.untokenize(translated)
        except Exception as e:
            raise AmharicLexError(
                f"ስህተት[E001] ኮድ ለማዋሃድ አልተቻለም: {e}"
            )

    def _translate_token(self, tok):
        """Replace Amharic NAME token with Python keyword if it matches."""
        import tokenize as tk
        if tok.type == tk.NAME:
            py_kw = self.adapter.to_python_keyword(tok.string)
            if py_kw:
                return tok._replace(string=py_kw)
        return tok
