import ast
from amharicscript.adapter import AmharicScriptError
from amharicscript.explainer import explain_error

class AmharicParseError(AmharicScriptError):
    pass

class OromParser:
    def parse(self, python_source: str, original_source: str = "") -> ast.AST:
        """
        Parse the translated Python source into an AST.
        Maps SyntaxError back to Amharic error message.
        """
        try:
            tree = ast.parse(python_source)
            return tree
        except SyntaxError as e:
            source_lines = original_source.split('\n') if original_source else []
            explanation = explain_error(e.msg, e.lineno, e.offset, source_lines)
            raise AmharicParseError(explanation)

