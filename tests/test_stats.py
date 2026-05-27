import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gezeLang.stats import analyze

def test_analyze_empty():
    res = analyze("")
    assert res['total_lines'] == 1
    assert res['total_keywords'] == 0

def test_analyze_basic():
    source = "ስራ ሰላም():\n    አሳይ('hi')\n"
    res = analyze(source)
    assert res['total_lines'] == 3
    assert res['total_keywords'] == 2  # def, print
    assert 'ስራ' in res['keyword_uses']
    assert 'አሳይ' in res['keyword_uses']

def test_analyze_amharic_ratio():
    source = "ስራ ሒሳብ(ሀ, ለ):\n    መልስ ሀ + ለ\n"
    res = analyze(source)
    # ሒሳብ, ሀ, ለ are Amharic identifiers
    assert res['amharic_identifier_ratio'] > 0
