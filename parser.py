# parser.py — Builds Python AST from translated (Python-keyword) source
import ast
from adapter import AmharicScriptError

class AmharicParseError(AmharicScriptError):
    pass

class OromParser:
    def parse(self, python_source: str) -> ast.AST:
        """
        Parse the translated Python source into an AST.
        Maps SyntaxError back to Amharic error message.
        """
        try:
            tree = ast.parse(python_source)
            return tree
        except SyntaxError as e:
            raise AmharicParseError(
                f"ስህተት[E001] አገባብ ስህተት — ኮድዎ ትክክለኛ አይደለም\n"
                f"  መስመር {e.lineno}, ቦታ {e.offset}: {e.msg}\n"
                f"  힌트: ሁሉም ቁልፍ ቃላት አማርኛ መሆን አለባቸው፣ "
                f"መዋቅሩ ደግሞ ትክክለኛ ሊሆን ይገባዋል።"
            )
