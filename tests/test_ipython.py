"""
tests/test_ipython.py — Tests for IPython / Google Colab gezeLang extension.
"""

import pytest
pytest.importorskip("IPython", reason="IPython is optional and not installed")
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from pathlib import Path


@pytest.fixture(scope="module")
def ipython_shell():
    """Create a persistent IPython interactive shell for testing."""
    shell = TerminalInteractiveShell.instance()
    # Load gezeLang extension
    shell.run_line_magic('load_ext', 'gezeLang')
    return shell


def test_ipython_load_extension(ipython_shell):
    """Verify that %load_ext gezeLang registers magics."""
    assert 'gezelang' in ipython_shell.magics_manager.magics['cell']
    assert 'gezelang' in ipython_shell.magics_manager.magics['line']
    assert 'gezelang_lang' in ipython_shell.magics_manager.magics['line']


def test_cell_magic_basic_execution(ipython_shell):
    """Verify standard Amharic script execution in cell magic."""
    cell = """
ስራ ደምር(ሀ, ለ):
    መልስ ሀ + ለ

ውጤት = ደምር(15, 27)
"""
    ipython_shell.run_cell_magic('gezelang', '', cell)
    assert ipython_shell.user_ns.get('ውጤት') == 42
    assert callable(ipython_shell.user_ns.get('ደምር'))


def test_python_and_gezelang_interoperability(ipython_shell):
    """Verify variables created in Python can be accessed in GezeLang and vice versa."""
    # Python sets a variable
    ipython_shell.run_cell("multiplier = 3")

    # GezeLang cell uses Python variable
    cell = """
ስራ እጥፍ(ቁጥር):
    መልስ ቁጥር * multiplier

የመጨረሻ = እጥፍ(10)
"""
    ipython_shell.run_cell_magic('gezelang', '', cell)
    assert ipython_shell.user_ns.get('የመጨረሻ') == 30

    # Python calls the function defined in GezeLang
    res = ipython_shell.run_cell("calc = እጥፍ(5)")
    assert ipython_shell.user_ns.get('calc') == 15


def test_cell_magic_multidialect(ipython_shell):
    """Verify dialect override via --lang flag."""
    # Tigrinya dialect
    tigrinya_cell = """
ስራ ተደምር(ሀ, ለ):
    መልስ ሀ + ለ

ውጽኢት = ተደምር(100, 50)
"""
    ipython_shell.run_cell_magic('gezelang', '--lang tigrinya', tigrinya_cell)
    assert ipython_shell.user_ns.get('ውጽኢት') == 150

    # Ge'ez dialect (ግዕዝ: def -> ግበር, return -> አግብእ)
    geez_cell = """
ግበር ተቀበል():
    አግብእ "ሰላም ለእከ"

ሰላምታ = ተቀበል()
"""
    ipython_shell.run_cell_magic('gezelang', '--lang geez', geez_cell)
    assert ipython_shell.user_ns.get('ሰላምታ') == "ሰላም ለእከ"


def test_line_magic_gezelang_lang(ipython_shell):
    """Verify %gezelang_lang changes sticky default dialect."""
    ipython_shell.run_line_magic('gezelang_lang', 'geez')
    # Cell without --lang now defaults to geez
    cell = """
ግበር ድምር(ሀ, ለ):
    አግብእ ሀ + ለ
ውጤት_ግዕዝ = ድምር(7, 3)
"""
    ipython_shell.run_cell_magic('gezelang', '', cell)
    assert ipython_shell.user_ns.get('ውጤት_ግዕዝ') == 10

    # Reset back to amharic
    ipython_shell.run_line_magic('gezelang_lang', 'amharic')


def test_cell_magic_flags(ipython_shell, capsys, tmp_path):
    """Verify --show-python, --no-exec, --emit, and --reverse flags."""
    # Test --show-python
    cell = """
x = 100
ከሆነ x > 50:
    y = 1
"""
    ipython_shell.run_cell_magic('gezelang', '--show-python', cell)
    captured = capsys.readouterr()
    assert "# [GezeLang → Python" in captured.out
    assert "if x > 50:" in captured.out

    # Test --emit
    emit_file = tmp_path / "emitted.py"
    ipython_shell.run_cell_magic('gezelang', f'--emit "{emit_file}"', cell)
    assert emit_file.exists()
    assert "if x > 50:" in emit_file.read_text(encoding='utf-8')

    # Test --reverse
    py_cell = """def calculate(a, b):
    return a + b
"""
    res = ipython_shell.run_cell_magic('gezelang', '--reverse', py_cell)
    captured = capsys.readouterr()
    assert "ስራ calculate(a, b):" in captured.out or "ስራ calculate(a, b):" in res


def test_cell_magic_error_diagnostics(ipython_shell, capsys):
    """Verify Amharic diagnostics on runtime error in notebook cell."""
    cell = """
x = 10 / 0
"""
    ipython_shell.run_cell_magic('gezelang', '', cell)
    captured = capsys.readouterr()
    assert "ስህተት[R001]" in captured.err or "በዜሮ ማካፈል" in captured.err or "ZeroDivisionError" in captured.err
