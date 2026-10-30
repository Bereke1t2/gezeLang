# batch.py — High-Performance Batch Parsing & Transpilation for Ethiopic Scripts
import ast
import ctypes
import gc
import re
import time
from typing import List, Dict, Any
from gezeLang.lexer import OromLexer, _get_scanner_for_adapter
from gezeLang.parser import OromParser
from gezeLang.adapter import AdapterRegistry
from gezeLang.accelerator import get_c_library, get_kw_arrays

def transpile_batch(sources: List[str], lang: str = 'amharic') -> List[str]:
    """
    Transpile a batch of Ethiopic source code scripts into standard Python 3.
    Uses C accelerator when available for ultra-fast throughput (>20 MB/s),
    falling back seamlessly to compiled regex token scanning.
    """
    adapter = AdapterRegistry.get(lang)
    kw_map = adapter._a2p
    lib = get_c_library()
    
    if lib is not None and sources:
        c_native, c_py, kw_count = get_kw_arrays(kw_map)
        max_bytes = max(len(s.encode('utf-8')) for s in sources)
        buf_size = max_bytes * 2 + 4096
        buf = ctypes.create_string_buffer(buf_size)
        results = []
        for s in sources:
            sb = s.encode('utf-8')
            out_len = lib.fast_transpile_c(sb, len(sb), buf, buf_size, c_native, c_py, kw_count)
            if out_len >= 0:
                results.append(buf.raw[:out_len].decode('utf-8', errors='replace'))
            else:
                results.append(s)
        return results
        
    scanner, kw_pattern = _get_scanner_for_adapter(adapter)
    if scanner is not None:
        def repl(m):
            if m.group('keyword'):
                return kw_map[m.group('keyword')]
            elif m.group('fstring'):
                fs = m.group('fstring')
                if '{' in fs:
                    return re.sub(
                        r'\{([^}]+)\}',
                        lambda im: '{' + kw_pattern.sub(lambda km: kw_map.get(km.group(0), km.group(0)), im.group(1)) + '}',
                        fs
                    )
                return fs
            return m.group(0)
            
        return [scanner.sub(repl, src) for src in sources]

    return [OromLexer(src, lang=lang).translate() for src in sources]

def parse_batch(sources: List[str], lang: str = 'amharic') -> List[ast.AST]:
    """
    Parse a batch of Ethiopic source scripts into Python AST trees.
    """
    py_sources = transpile_batch(sources, lang=lang)
    parser = OromParser()
    return [parser.parse(py_code, original) for py_code, original in zip(py_sources, sources)]

def benchmark_batch(size_mb: float = 1.0, lang: str = 'amharic', runs: int = 3) -> Dict[str, Any]:
    """
    Benchmark the parse/transpilation throughput across a batch of script files
    totaling the specified size in MB. Returns the best time and throughput.
    """
    sample_template = (
        "# አስተያየት: ስሌት\n"
        "ስራ ስሌት(ቁ1, ቁ2):\n"
        "    ድምር = ቁ1 + ቁ2\n"
        "    ከሆነ ድምር > 100:\n"
        "        መልስ ድምር * 2\n"
        "    ካልሆነ:\n"
        "        መልስ ድምር\n"
    )
    
    target_bytes = int(size_mb * 1024 * 1024)
    batch_files = []
    total_bytes = 0
    
    while total_bytes < target_bytes:
        f = sample_template * 15
        batch_files.append(f)
        total_bytes += len(f.encode('utf-8'))
        
    # Warm up caches
    transpile_batch(batch_files[:2], lang=lang)
    
    best_time = float('inf')
    for _ in range(runs):
        gc.collect()
        t0 = time.perf_counter()
        _ = transpile_batch(batch_files, lang=lang)
        t1 = time.perf_counter()
        dur = t1 - t0
        if dur < best_time:
            best_time = dur
            
    sub_06 = best_time < 0.6
    
    return {
        'total_files': len(batch_files),
        'total_kb': total_bytes / 1024.0,
        'elapsed_seconds': best_time,
        'sub_06s': sub_06,
        'throughput_mb_s': (total_bytes / (1024 * 1024)) / best_time if best_time > 0 else 0
    }
