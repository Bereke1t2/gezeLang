"""
conftest.py — automatically add project root to sys.path so tests
can import adapter, lexer, parser, codegen without installing package.
"""
import sys
from pathlib import Path

# Ensure repo root is on the path when pytest is run from any directory
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
