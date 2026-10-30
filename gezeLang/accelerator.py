# accelerator.py — Optional C Accelerator Engine for High-Throughput Batch Transpilation
import ctypes
import os
from pathlib import Path
from typing import Dict, Optional

_LIB: Optional[ctypes.CDLL] = None
_LIB_TRIED = False

def get_c_library() -> Optional[ctypes.CDLL]:
    global _LIB, _LIB_TRIED
    if _LIB_TRIED:
        return _LIB
    _LIB_TRIED = True
    
    so_path = Path(__file__).parent / '_fast_lexer.so'
    if so_path.exists():
        try:
            lib = ctypes.CDLL(str(so_path))
            lib.fast_transpile_c.argtypes = [
                ctypes.c_char_p, ctypes.c_int,
                ctypes.c_char_p, ctypes.c_int,
                ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_char_p), ctypes.c_int
            ]
            lib.fast_transpile_c.restype = ctypes.c_int
            _LIB = lib
        except Exception:
            _LIB = None
    return _LIB

_KW_CACHE: Dict[str, tuple] = {}

def get_kw_arrays(kw_map: dict):
    key = id(kw_map)
    if key in _KW_CACHE:
        return _KW_CACHE[key]
    
    kws_native = list(kw_map.keys())
    kws_py = [kw_map[k] for k in kws_native]
    
    c_native = (ctypes.c_char_p * len(kws_native))(*[k.encode('utf-8') for k in kws_native])
    c_py = (ctypes.c_char_p * len(kws_py))(*[k.encode('utf-8') for k in kws_py])
    
    _KW_CACHE[key] = (c_native, c_py, len(kws_native))
    return _KW_CACHE[key]

def transpile_c_accelerated(source: str, kw_map: dict) -> Optional[str]:
    lib = get_c_library()
    if lib is None:
        return None
    
    src_bytes = source.encode('utf-8')
    src_len = len(src_bytes)
    # Output buffer with safety margin
    buf_size = src_len * 2 + 1024
    dst_buf = ctypes.create_string_buffer(buf_size)
    
    c_native, c_py, kw_count = get_kw_arrays(kw_map)
    
    out_len = lib.fast_transpile_c(src_bytes, src_len, dst_buf, buf_size, c_native, c_py, kw_count)
    if out_len >= 0:
        return dst_buf.raw[:out_len].decode('utf-8', errors='replace')
    return None
