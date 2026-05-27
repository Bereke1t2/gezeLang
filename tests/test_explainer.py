import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gezeLang.explainer import explain_error

def test_explain_missing_colon():
    msg = "expected ':'"
    explanation = explain_error(msg, 1, 10, ["ስራ ሰላም()"])
    assert '":" ይጎድላል' in explanation
    assert 'ስራ' in explanation

def test_explain_bad_indent():
    msg = "expected an indented block"
    explanation = explain_error(msg, 2, 0, ["  አሳይ('ሰላም')"])
    assert 'ምሳሪያ (Indentation) ስህተት' in explanation

def test_explain_fallback():
    msg = "some weird error"
    explanation = explain_error(msg, 1, 1, [""])
    assert 'አገባብ ስህተት' in explanation
