import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gezeLang.adapter import AdapterRegistry
from gezeLang.reverse import reverse_transpile, verify_round_trip
import gezeLang

AdapterRegistry.discover(Path(__file__).parent.parent / 'gezeLang' / 'adapters')

def test_reverse_basic_function():
    py_code = "def add(a, b):\n    return a + b\n"
    amh_code = reverse_transpile(py_code, lang='amharic')
    assert 'ስራ add(a, b):' in amh_code
    assert 'መልስ a + b' in amh_code
    assert 'def' not in amh_code
    assert 'return' not in amh_code

def test_reverse_control_flow():
    py_code = (
        "if x > 10:\n"
        "    print('High')\n"
        "elif x > 5:\n"
        "    print('Medium')\n"
        "else:\n"
        "    print('Low')\n"
    )
    amh_code = reverse_transpile(py_code, lang='amharic')
    assert 'ከሆነ x > 10:' in amh_code
    assert 'ካልሆነከሆነ x > 5:' in amh_code
    assert 'ካልሆነ:' in amh_code
    assert 'አሳይ(' in amh_code

def test_reverse_classes():
    py_code = (
        "class Student:\n"
        "    def __init__(self, name):\n"
        "        self.name = name\n"
    )
    amh_code = reverse_transpile(py_code, lang='amharic')
    assert 'ክፍለ Student:' in amh_code
    assert 'ስራ __init__(እኔ, name):' in amh_code
    assert 'እኔ.name = name' in amh_code

def test_reverse_preserves_strings_and_comments():
    py_code = (
        "# This comment mentions def and class\n"
        "message = 'def and if inside a string should not change'\n"
        "def run():\n"
        "    return message\n"
    )
    amh_code = reverse_transpile(py_code, lang='amharic')
    # Comment preserved
    assert "# This comment mentions def and class" in amh_code
    # String literal preserved
    assert "'def and if inside a string should not change'" in amh_code
    # Keywords translated
    assert "ስራ run():" in amh_code
    assert "መልስ message" in amh_code

def test_reverse_preserves_identifiers_with_substrings():
    py_code = (
        "definition = 100\n"
        "importance = 200\n"
        "def compute(definition):\n"
        "    return definition + importance\n"
    )
    amh_code = reverse_transpile(py_code, lang='amharic')
    assert "definition = 100" in amh_code
    assert "importance = 200" in amh_code
    assert "ስራ compute(definition):" in amh_code
    assert "መልስ definition + importance" in amh_code

def test_reverse_fstrings():
    py_code = 'print(f"Total: {len(items)} items")'
    amh_code = reverse_transpile(py_code, lang='amharic')
    assert 'አሳይ(' in amh_code
    assert 'Total: {' in amh_code
    assert 'ርዝመት(items)' in amh_code

def test_reverse_multidialect():
    py_code = "def hello():\n    return True\n"
    
    # Classical Ge'ez
    geez_code = reverse_transpile(py_code, lang='geez')
    assert 'ግበር hello():' in geez_code
    assert 'አግብእ ጽድቅ' in geez_code

    # Tigrinya
    tig_code = reverse_transpile(py_code, lang='tigrinya')
    assert 'ስራ hello():' in tig_code
    assert 'መልስ ሓቂ' in tig_code

    # Gurage
    gurage_code = reverse_transpile(py_code, lang='gurage')
    assert 'ኤፐ hello():' in gurage_code
    assert 'አገፓ ኤውነት' in gurage_code

def test_round_trip_idempotency_corpus():
    """
    Test mathematical idempotency:
    AST(Forward(Reverse(PythonCode))) == AST(PythonCode)
    """
    test_scripts = [
        "def add(a, b):\n    return a + b\n",
        "total = 0\nfor i in range(10):\n    total += i\n",
        "if x > 0:\n    res = True\nelse:\n    res = False\n",
    ]
    for script in test_scripts:
        is_identical, orig_ast, recompiled_ast = verify_round_trip(script, lang='amharic')
        assert is_identical, (
            f"Round-trip AST mismatch!\nOriginal AST:\n{orig_ast}\nRecompiled AST:\n{recompiled_ast}"
        )
