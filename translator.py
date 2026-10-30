#!/usr/bin/env python3
"""
translator.py — Convenient root entrypoint for GezeLang CLI
Usage:
  python translator.py hello.amh
  python translator.py --bench
  python translator.py (starts interactive REPL)
"""
import sys
from pathlib import Path

# Add project root to path
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from gezeLang.cli import main

if __name__ == '__main__':
    main()
