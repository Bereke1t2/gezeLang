"""
gezeLang IPython & Google Colab Extension
Enables %%gezelang cell magic and %gezelang line magic for interactive Ethiopic script programming.

Usage in Google Colab / Jupyter Notebooks:
    !pip install gezeLang
    %load_ext gezelang
    
    %%gezelang
    ስራ ደምር(ሀ, ለ):
        መልስ ሀ + ለ
    አሳይ(ደምር(5, 7))

Multi-dialect support:
    %%gezelang --lang tigrinya
    %%gezelang --lang geez
    %gezelang_lang gurage
"""

import argparse
import shlex
import sys
import textwrap
from pathlib import Path
from gezeLang.lexer import OromLexer
from gezeLang.parser import OromParser
from gezeLang.codegen import CodeGen
from gezeLang.explainer import explain_runtime_exception
from gezeLang.reverse import reverse_transpile
from gezeLang.adapter import AdapterRegistry

_ADAPTERS_DIR = Path(__file__).parent / 'adapters'

try:
    from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
except ImportError:
    Magics = object
    def magics_class(cls): return cls
    def line_magic(f): return f
    def cell_magic(f): return f


@magics_class
class GezeLangMagics(Magics):
    """IPython Magics for GezeLang Ethiopic Programming Language."""

    def __init__(self, shell):
        super().__init__(shell)
        AdapterRegistry.discover(_ADAPTERS_DIR)
        self.default_lang = 'amharic'

    @line_magic
    def gezelang_lang(self, line):
        """Set or inspect default dialect for GezeLang cells.
        Usage:
            %gezelang_lang tigrinya
            %gezelang_lang
        """
        lang = line.strip().lower()
        if not lang:
            print(f"Current GezeLang dialect: {self.default_lang}")
            return self.default_lang

        available = AdapterRegistry.list_langs()
        if lang in available:
            self.default_lang = lang
            print(f"✅ GezeLang default dialect set to: {self.default_lang}")
            return self.default_lang
        else:
            print(f"⚠️ Unknown dialect '{lang}'. Available dialects: {', '.join(sorted(available))}")
            return None

    @line_magic
    def gezelang(self, line):
        """Execute a single line of GezeLang Ethiopic code.
        Usage:
            %gezelang አሳይ('ሰላም ዓለም')
        """
        return self._execute_code(line, lang=self.default_lang)

    @cell_magic
    def gezelang(self, line, cell):
        """Execute a cell of GezeLang Ethiopic code inside Jupyter/Colab.
        Options:
            --lang LANG       Specify Ethiopic dialect (e.g. amharic, tigrinya, geez, gurage)
            -p, --show-python Display transpiled Python code before execution
            -a, --show-ast    Display AST representation
            --emit FILE       Save generated Python code to given file
            --reverse         Reverse transpile Python code in cell to GezeLang
            --no-exec         Transpile only without executing
        """
        parser = argparse.ArgumentParser(prog='%%gezelang', add_help=False)
        parser.add_argument('--lang', default=None, help='Ethiopic dialect')
        parser.add_argument('-p', '--show-python', action='store_true', help='Show generated Python code')
        parser.add_argument('-a', '--show-ast', action='store_true', help='Show AST tree')
        parser.add_argument('--emit', default=None, help='Save transpiled code to file')
        parser.add_argument('--reverse', action='store_true', help='Reverse transpile Python to GezeLang')
        parser.add_argument('--no-exec', action='store_true', help='Transpile without executing')

        try:
            args = parser.parse_args(shlex.split(line))
        except SystemExit:
            return

        lang = (args.lang.lower() if args.lang else self.default_lang)
        cleaned_cell = textwrap.dedent(cell).strip()

        if args.reverse:
            ethiopic_code = reverse_transpile(cleaned_cell, lang=lang)
            print(ethiopic_code)
            if args.emit:
                Path(args.emit).write_text(ethiopic_code, encoding='utf-8')
                print(f"✅ Saved Ethiopic source to: {args.emit}")
            return ethiopic_code

        return self._execute_code(
            cleaned_cell,
            lang=lang,
            show_python=args.show_python,
            show_ast=args.show_ast,
            emit_file=args.emit,
            no_exec=args.no_exec
        )

    def _execute_code(self, source, lang='amharic', show_python=False, show_ast=False, emit_file=None, no_exec=False):
        try:
            source = textwrap.dedent(source).strip()
            lexer = OromLexer(source, lang=lang)
            python_source = lexer.translate()

            parser = OromParser()
            tree = parser.parse(python_source, original_source=source)

            codegen = CodeGen()
            emitted = codegen.generate(tree)

            if emit_file:
                Path(emit_file).write_text(emitted, encoding='utf-8')
                print(f"✅ Generated Python saved to: {emit_file}")

            if show_python:
                print(f"# [GezeLang → Python ({lang})]")
                print(emitted)
                print("-" * 40)

            if show_ast:
                from gezeLang.cli import print_ast
                print_ast(tree)

            if no_exec:
                return emitted

            if self.shell is not None:
                res = self.shell.run_cell(emitted, store_history=True, silent=False)
                if not res.success and res.error_in_exec:
                    diag = explain_runtime_exception(res.error_in_exec, '<cell>', source.splitlines())
                    print(diag, file=sys.stderr)
                return res.result
            else:
                compiled = compile(emitted, '<cell>', 'exec')
                exec(compiled, globals())
                return None

        except Exception as e:
            diag = explain_runtime_exception(e, '<cell>', source.splitlines())
            print(diag, file=sys.stderr)
            return None


def load_ipython_extension(ipython):
    """Standard entry point for `%load_ext gezelang` or `%load_ext gezeLang`."""
    ipython.register_magics(GezeLangMagics(ipython))
    print("✨ GezeLang IPython/Colab Extension loaded! Use %%gezelang to run Ethiopic code.")


def unload_ipython_extension(ipython):
    """Entry point for `%unload_ext gezelang`."""
    pass
