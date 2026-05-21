#!/usr/bin/env python3
# translator.py — AmharicScript CLI: python translator.py program.amh
"""
Usage:
  python translator.py program.amh              # transpile + run
  python translator.py program.amh --emit       # emit program.py, don't run
  python translator.py program.amh --lang oromo # use Oromo adapter
  python translator.py --check program.amh      # syntax check only
  python translator.py --list-langs             # list available adapters
"""
import argparse
import sys
import os
from pathlib import Path

# Allow running as script without installing as package
sys.path.insert(0, str(Path(__file__).parent))

from adapter import AdapterRegistry, AmharicScriptError
from lexer import OromLexer
from parser import OromParser
from codegen import CodeGen

ADAPTERS_DIR = Path(__file__).parent / 'adapters'

def main():
    parser = argparse.ArgumentParser(
        description='AmharicScript — አማርኛ ፕሮግራሚንግ ቋንቋ',
        epilog='ምሳሌ: python translator.py hello.amh'
    )
    parser.add_argument('file', nargs='?', help='የ .amh ፋይል ስም')
    parser.add_argument('--lang', default='amharic',
                        help='ቋንቋ adapter (default: amharic)')
    parser.add_argument('--emit', action='store_true',
                        help='Python ፋይል ብቻ ፍጠር፣ አታሂድ')
    parser.add_argument('--check', action='store_true',
                        help='አገባብ ብቻ ፈትሽ')
    parser.add_argument('--list-langs', action='store_true',
                        help='የሚገኙ ቋንቋዎችን አሳይ')
    args = parser.parse_args()

    # Discover all adapters
    AdapterRegistry.discover(ADAPTERS_DIR)

    # --list-langs
    if args.list_langs:
        langs = AdapterRegistry.list_langs()
        print("የሚገኙ ቋንቋዎች:")
        for lang in langs:
            print(f"  • {lang}")
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    source_path = Path(args.file)
    if not source_path.exists():
        print(f"ስህተት[E000] ፋይል አልተገኘም: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Read source with UTF-8 encoding (required for Amharic)
    source = source_path.read_text(encoding='utf-8')

    try:
        # Phase 1: Lex — translate Amharic keywords to Python keywords
        lexer = OromLexer(source, lang=args.lang)
        python_source = lexer.translate()

        # Phase 2: Parse — build AST
        ast_parser = OromParser()
        tree = ast_parser.parse(python_source)

        # --check only
        if args.check:
            print(f"✅ {args.file} — አገባቡ ትክክለኛ ነው")
            return

        # Phase 3: Code gen — emit Python source
        gen = CodeGen()
        output_source = gen.generate(tree)

        # --emit: write .py file only
        if args.emit:
            out_path = source_path.with_suffix('.py')
            out_path.write_text(output_source, encoding='utf-8')
            print(f"✅ ተፈጠረ: {out_path}")
            return

        # Default: execute the generated Python
        exec(compile(output_source, str(source_path), 'exec'), {'__name__': '__main__'})

    except AmharicScriptError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ስህተት[E005] ፕሮግራሙ ሲሄድ ስህተት ተፈጠረ: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
