#!/usr/bin/env python3
# cli.py — GezeLang CLI & Interactive Ethiopic REPL
"""
Usage:
  gezeLang                             # launch interactive Ethiopic REPL
  gezeLang program.amh                 # transpile + execute with runtime diagnostics
  gezeLang program.amh --ast           # display Abstract Syntax Tree (AST)
  gezeLang program.amh --tokens        # inspect token stream
  gezeLang program.amh --emit          # emit program.py without executing
  gezeLang program.amh --lang tigrinya # choose from 10+ Ethiopic dialects
  gezeLang --bench                     # run 1MB batch throughput benchmark
  gezeLang --list-langs                # list all 15 supported language adapters
"""
import argparse
import ast
import io
import sys
import tokenize
from pathlib import Path

# Allow running as script without installing as package
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from gezeLang.adapter import AdapterRegistry, GezeLangError
from gezeLang.lexer import OromLexer
from gezeLang.parser import OromParser
from gezeLang.codegen import CodeGen
from gezeLang.batch import benchmark_batch
from gezeLang.explainer import explain_runtime_exception
from gezeLang.reverse import reverse_transpile, verify_round_trip

ADAPTERS_DIR = Path(__file__).parent / 'adapters'

def run_bench(lang='amharic'):
    print(f"\n{'━'*64}")
    print(" ⚡ GezeLang High-Throughput Batch Telemetry (Sub-0.6s Engine)")
    print(f"{'━'*64}")
    res = benchmark_batch(size_mb=1.0, lang=lang, runs=3)
    
    status_icon = "✅ PASSED (Sub-0.6s Verified)" if res['sub_06s'] else "❌ FAILED"
    
    print(f"  • Batch Corpus Size:     {res['total_kb']:.2f} KB ({res['total_files']} files)")
    print(f"  • Evaluated Dialect:     {lang}")
    print(f"  • Parse & Transpile Time:{res['elapsed_seconds']:.4f}s")
    print(f"  • Engine Throughput:     {res['throughput_mb_s']:.2f} MB/s")
    print(f"  • Latency SLA Target:    < 0.6000s")
    print(f"  • Performance Status:    {status_icon}")
    print(f"{'━'*64}\n")

def print_ast(tree: ast.AST):
    print(f"\n{'━'*50}")
    print(" 🌳 GezeLang Abstract Syntax Tree (AST)")
    print(f"{'━'*50}")
    try:
        print(ast.dump(tree, indent=2))
    except TypeError:
        # Fallback for Python versions without indent parameter
        print(ast.dump(tree))
    print(f"{'━'*50}\n")

def print_tokens(source: str, lang: str):
    print(f"\n{'━'*50}")
    print(f" ⚡ GezeLang Token Stream [Dialect: {lang}]")
    print(f"{'━'*50}")
    adapter = AdapterRegistry.get(lang)
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    for tok in tokens:
        if tok.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
            continue
        tok_name = tokenize.tok_name.get(tok.type, str(tok.type))
        py_kw = adapter.to_python_keyword(tok.string) if tok.type == tokenize.NAME else None
        mapping_str = f" → {py_kw}" if py_kw else ""
        print(f"  [{tok.start[0]}:{tok.start[1]:<2}] {tok_name:<10} '{tok.string}'{mapping_str}")
    print(f"{'━'*50}\n")

def start_repl(initial_lang: str = 'amharic'):
    current_lang = initial_lang
    AdapterRegistry.discover(ADAPTERS_DIR)
    
    print(f"""
 ╔═══════════════════════════════════════════════════════════════╗
 ║ ጌዜ ቋንቋ · GezeLang v1.2.0 Interactive REPL                   ║
 ║ Ethiopic-Script Shell · WebAssembly Core · 15 Dialects Ready  ║
 ║ Commands: :help, :lang <name>, :ast, :tokens, :bench, :quit   ║
 ╚═══════════════════════════════════════════════════════════════╝
""")
    
    env_globals = {'__name__': '__main__'}
    
    while True:
        try:
            prompt = f"[{current_lang}] >>> "
            line = input(prompt)
            stripped = line.strip()
            
            if not stripped:
                continue
                
            # REPL Commands
            if stripped in (':quit', ':exit', 'quit()', 'exit()'):
                print("ደህና ሁኑ! (Goodbye!)")
                break
            elif stripped == ':help':
                print("""
REPL Commands:
  :lang <name>   Switch dialect (e.g. :lang geez, :lang tigrinya)
  :list          List all 15 supported dialects
  :reverse <py>  Reverse transpile Python code to Ethiopic script
  :roundtrip <py>Verify mathematical AST round-trip idempotency
  :ast <code>    Print AST tree of code
  :tokens <code> Print token breakdown of code
  :bench         Run live 1MB batch throughput benchmark
  :quit          Exit REPL
""")
                continue
            elif stripped == ':list':
                for l in sorted(AdapterRegistry.list_langs()):
                    print(f"  • {l}")
                continue
            elif stripped.startswith(':lang'):
                parts = stripped.split()
                if len(parts) > 1 and parts[1] in AdapterRegistry.list_langs():
                    current_lang = parts[1]
                    print(f"✅ Dialect switched to: {current_lang}")
                else:
                    print(f"⚠️ Unknown dialect. Use :list to see available dialects.")
                continue
            elif stripped.startswith(':reverse'):
                py_code = stripped[8:].strip()
                res = reverse_transpile(py_code, lang=current_lang)
                print(f"\n{res}\n")
                continue
            elif stripped.startswith(':roundtrip'):
                py_code = stripped[10:].strip()
                try:
                    is_identical, orig_ast, recompiled_ast = verify_round_trip(py_code, lang=current_lang)
                    if is_identical:
                        print("✅ Round-trip AST Idempotency Verified! (AST(Forward(Reverse(code))) == AST(code))")
                    else:
                        print("❌ AST Mismatch detected during round-trip.")
                except Exception as err:
                    print(f"❌ Round-trip validation error: {err}")
                continue
            elif stripped.startswith(':ast'):
                code_to_inspect = stripped[4:].strip()
                py_src = OromLexer(code_to_inspect, lang=current_lang).translate()
                tree = OromParser().parse(py_src, original_source=code_to_inspect)
                print_ast(tree)
                continue
            elif stripped.startswith(':tokens'):
                code_to_inspect = stripped[7:].strip()
                print_tokens(code_to_inspect, lang=current_lang)
                continue
            elif stripped == ':bench':
                run_bench(lang=current_lang)
                continue
                
            # Multi-line block collection if line ends with ':'
            code_lines = [line]
            if stripped.endswith(':'):
                while True:
                    sub_line = input(f"[{current_lang}] ... ")
                    code_lines.append(sub_line)
                    if not sub_line.strip():
                        break
                        
            full_code = '\n'.join(code_lines)
            lexer = OromLexer(full_code, lang=current_lang)
            py_code = lexer.translate()
            parser = OromParser()
            tree = parser.parse(py_code, original_source=full_code)
            gen = CodeGen()
            emitted = gen.generate(tree)
            
            # Try eval for single expressions first to print output
            try:
                expr_code = compile(emitted, '<repl>', 'eval')
                val = eval(expr_code, env_globals)
                if val is not None:
                    print(repr(val))
            except Exception:
                # Execute as statement
                stmt_code = compile(emitted, '<repl>', 'exec')
                exec(stmt_code, env_globals)
                
        except (KeyboardInterrupt, EOFError):
            print("\nደህና ሁኑ! (Goodbye!)")
            break
        except GezeLangError as ge:
            print(str(ge), file=sys.stderr)
        except Exception as err:
            diag = explain_runtime_exception(err, '<repl>', code_lines if 'code_lines' in locals() else [])
            print(diag, file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description='GezeLang — አማርኛ እና የኢትዮጵያ ቋንቋዎች ፕሮግራሚንግ',
        epilog='ምሳሌ: gezeLang hello.amh  |  gezeLang --bench  |  gezeLang (interactive REPL)'
    )
    parser.add_argument('file', nargs='?', help='የ .amh ፋይል ስም (ባዶ ከሆነ REPL ይጀምራል)')
    parser.add_argument('--lang', default='amharic',
                        help='ቋንቋ adapter (default: amharic, e.g. tigrinya, geez, gurage)')
    parser.add_argument('--emit', action='store_true',
                        help='Python ፋይል ብቻ ፍጠር፣ አታሂድ')
    parser.add_argument('--ast', action='store_true',
                        help='የ Abstract Syntax Tree (AST) መዋቅር አሳይ')
    parser.add_argument('--tokens', action='store_true',
                        help='የ Token ፍሰት አሳይ')
    parser.add_argument('--bench', action='store_true',
                        help='የ 1MB batch script ፍጥነት ፈትሽ (Sub-0.6s Engine)')
    parser.add_argument('--check', action='store_true',
                        help='አገባብ ብቻ ፈትሽ')
    parser.add_argument('--list-langs', action='store_true',
                        help='የሚገኙ 10+ ቋንቋዎችን አሳይ')
    parser.add_argument('--stats', action='store_true',
                        help='Show language statistics')
    parser.add_argument('--reverse', action='store_true',
                        help='Python ኮድን ወደ Ethiopic script ቀይር (Reverse transpile Python to GezeLang)')
    parser.add_argument('--round-trip', action='store_true',
                        help='Verify mathematical AST round-trip idempotency')
    parser.add_argument('--sourcemap', action='store_true',
                        help='Generate V3 Source Map (.py.map) for browser debugging and runtime line mapping')
    parser.add_argument('--lsp', action='store_true',
                        help='Start Language Server Protocol (LSP) daemon on stdio')
    parser.add_argument('--compare', nargs='+', metavar='LANG',
                        help='Compare adapters against a program')
    parser.add_argument('--version', action='store_true',
                        help='Show GezeLang version')
    args = parser.parse_args()

    # Discover all adapters
    AdapterRegistry.discover(ADAPTERS_DIR)

    if args.lsp:
        from gezeLang.lsp import run_server
        run_server()
        return

    if args.version:
        print("GezeLang v1.2.0 (WebAssembly Core + 15 Ethiopic Dialects)")
        return

    # --bench
    if args.bench:
        run_bench(lang=args.lang)
        return

    # --list-langs
    if args.list_langs:
        langs = sorted(AdapterRegistry.list_langs())
        print(f"\nየሚገኙ ቋንቋዎች ({len(langs)} adapters available):")
        for lang in langs:
            print(f"  • {lang}")
        print()
        return

    # Launch REPL if no file provided
    if not args.file:
        start_repl(initial_lang=args.lang)
        return

    source_path = Path(args.file)
    if not source_path.exists():
        print(f"ስህተት[E000] ፋይል አልተገኘም: {args.file}", file=sys.stderr)
        sys.exit(1)

    source = source_path.read_text(encoding='utf-8')

    if args.reverse:
        ethiopic_source = reverse_transpile(source, lang=args.lang)
        if args.emit:
            ext = '.amh' if args.lang == 'amharic' else f'.{args.lang}'
            out_path = source_path.with_suffix(ext)
            out_path.write_text(ethiopic_source, encoding='utf-8')
            print(f"✅ ተፈጠረ: {out_path}")
        else:
            print(ethiopic_source)
        return

    if args.round_trip:
        try:
            is_identical, orig_ast, recompiled_ast = verify_round_trip(source, lang=args.lang)
            if is_identical:
                print("✅ Round-trip AST Idempotency Verified! (AST(Forward(Reverse(code))) == AST(code))")
                return
            else:
                print("❌ AST Mismatch detected during round-trip:", file=sys.stderr)
                print(f"--- Original AST ---\n{orig_ast}\n--- Recompiled AST ---\n{recompiled_ast}", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"❌ Round-trip validation error: {e}", file=sys.stderr)
            sys.exit(1)

    if args.compare:
        langs = args.compare
        results = {}
        for lang in langs:
            try:
                lexer = OromLexer(source, lang=lang)
                py_src = lexer.translate()
                tree = OromParser().parse(py_src, original_source=source)
                results[lang] = CodeGen().generate(tree)
            except Exception as e:
                results[lang] = f'ስህተት: {e}'
        
        print(f"{'━'*40}")
        print("GezeLang — የቋንቋ ንጽጽር (Language Comparison)")
        print(f"{'━'*40}")
        print(f"ፋይል: {source_path.name}\n")
        for lang, r in results.items():
            print(f"[{lang}] → Generated Python:")
            for line in r.splitlines():
                print(f"  {line}")
            print()
        print("ንጽጽር ተጠናቋል ✅")
        print(f"{'━'*40}")
        return

    if args.stats:
        from gezeLang.stats import print_stats
        print_stats(source, source_path.name)
        return

    if args.tokens:
        print_tokens(source, args.lang)
        return

    try:
        # Phase 1: Lex — translate Ethiopic keywords to Python keywords
        lexer = OromLexer(source, lang=args.lang)
        python_source = lexer.translate()

        # Phase 2: Parse — build AST
        ast_parser = OromParser()
        tree = ast_parser.parse(python_source, original_source=source)

        if args.ast:
            print_ast(tree)
            return

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
            if args.sourcemap:
                from gezeLang.sourcemap import SourceMapGenerator
                generator = SourceMapGenerator(file=out_path.name, source_file=source_path.name)
                _, smap = generator.generate(source, lang=args.lang)
                map_path = source_path.with_suffix('.py.map')
                map_path.write_text(smap.to_json(indent=2), encoding='utf-8')
                output_source += smap.get_source_mapping_comment(inline=False, map_file=map_path.name)
                print(f"🗺️  V3 Source Map ተፈጠረ: {map_path}")
            out_path.write_text(output_source, encoding='utf-8')
            print(f"✅ ተፈጠረ: {out_path}")
            return

        # Execute the generated Python with runtime error source mapping
        try:
            compiled = compile(output_source, str(source_path), 'exec')
            exec(compiled, {'__name__': '__main__'})
        except Exception as runtime_err:
            diag = explain_runtime_exception(runtime_err, str(source_path), source.splitlines())
            print(diag, file=sys.stderr)
            sys.exit(1)

    except GezeLangError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
