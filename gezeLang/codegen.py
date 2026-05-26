# codegen.py — Emits valid Python source from AST via ast.unparse()
import ast
from amharicscript.adapter import AmharicScriptError

class AmharicCodeGenError(AmharicScriptError):
    pass

class CodeGen:
    def generate(self, tree: ast.AST) -> str:
        """
        Convert AST to Python source string.
        Output is byte-for-byte equivalent to hand-written Python.
        Zero runtime overhead — CPython compiles it identically.
        """
        try:
            return ast.unparse(tree)
        except Exception as e:
            raise AmharicCodeGenError(
                f"ስህተት[E005] ኮድ ለማመንጨት አልተቻለም: {e}"
            )
