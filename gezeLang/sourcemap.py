"""
sourcemap.py — Production V3 Source Map Generator and Consumer for GezeLang.
Complies with the Source Map Revision 3 Proposal standard (Base64 VLQ encoding).
Enables zero-friction browser/DevTools debugging and precise Python runtime error sourcemapping.
"""

import base64
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

from gezeLang.adapter import AdapterRegistry
from gezeLang.lexer import _get_scanner_for_adapter

BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
BASE64_MAP = {c: i for i, c in enumerate(BASE64_CHARS)}


def encode_vlq(value: int) -> str:
    """Encode an integer into a Base64 Variable-Length Quantity (VLQ) string."""
    vlq = (-value << 1) | 1 if value < 0 else value << 1
    chars = []
    while True:
        digit = vlq & 0x1F
        vlq >>= 5
        if vlq > 0:
            digit |= 0x20
        chars.append(BASE64_CHARS[digit])
        if vlq == 0:
            break
    return "".join(chars)


def decode_vlq_stream(s: str) -> List[int]:
    """Decode a Base64 VLQ string into a list of integers."""
    values = []
    shift = 0
    value = 0
    for char in s:
        if char not in BASE64_MAP:
            continue
        integer = BASE64_MAP[char]
        has_continuation = (integer & 0x20) != 0
        digit = integer & 0x1F
        value += digit << shift
        if has_continuation:
            shift += 5
        else:
            is_negative = (value & 1) == 1
            shifted = value >> 1
            values.append(-shifted if is_negative else shifted)
            value = 0
            shift = 0
    return values


@dataclass
class SourceMap:
    """V3 Source Map data container compliant with the RFC spec."""
    file: str
    sources: List[str]
    mappings: str
    sourcesContent: List[str] = field(default_factory=list)
    names: List[str] = field(default_factory=list)
    sourceRoot: str = ""
    version: int = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert to standard JSON-compatible dictionary."""
        d = {
            "version": self.version,
            "file": self.file,
            "sourceRoot": self.sourceRoot,
            "sources": self.sources,
            "names": self.names,
            "mappings": self.mappings,
        }
        if self.sourcesContent:
            d["sourcesContent"] = self.sourcesContent
        return d

    def to_json(self, indent: Optional[int] = None) -> str:
        """Serialize source map to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_data_url(self) -> str:
        """Return base64-encoded data URL for inline source map embedding."""
        b64 = base64.b64encode(self.to_json().encode('utf-8')).decode('ascii')
        return f"data:application/json;charset=utf-8;base64,{b64}"

    def get_source_mapping_comment(self, inline: bool = False, map_file: Optional[str] = None) -> str:
        """Return comment to append to generated file."""
        if inline:
            return f"\n//# sourceMappingURL={self.to_data_url()}\n"
        target = map_file or f"{self.file}.map"
        return f"\n//# sourceMappingURL={target}\n"


class SourceMapGenerator:
    """Generates V3 source maps during Ethiopic-to-Python transpilation."""

    def __init__(self, file: str = "output.py", source_file: str = "source.amh"):
        self.file = file
        self.source_file = source_file

    def generate(self, source: str, lang: str = 'amharic') -> Tuple[str, SourceMap]:
        """
        Transpiles Ethiopic source code while building high-precision V3 SourceMap mappings.
        Returns (transpiled_python_source, source_map_instance).
        """
        adapter = AdapterRegistry.get(lang)
        scanner, kw_pattern = _get_scanner_for_adapter(adapter)
        kw_map = adapter._a2p

        orig_lines = source.splitlines()
        gen_lines = []
        raw_mappings = []

        last_src_idx = 0
        last_orig_line = 0
        last_orig_col = 0

        for line_idx, orig_line in enumerate(orig_lines):
            # Scan tokens and substitute keywords while tracking columns
            gen_col = 0
            orig_idx = 0
            line_segments = []
            gen_line_parts = []

            for m in scanner.finditer(orig_line):
                start, end = m.span()
                # Text preceding match
                if start > orig_idx:
                    chunk = orig_line[orig_idx:start]
                    line_segments.append((gen_col, 0, line_idx, orig_idx))
                    gen_line_parts.append(chunk)
                    gen_col += len(chunk)
                    orig_idx = start

                if m.group('keyword'):
                    kw = m.group('keyword')
                    py_kw = kw_map.get(kw, kw)
                    line_segments.append((gen_col, 0, line_idx, start))
                    gen_line_parts.append(py_kw)
                    gen_col += len(py_kw)
                    orig_idx = end
                elif m.group('fstring'):
                    fs = m.group('fstring')
                    if '{' in fs:
                        # Substitute keywords inside f-string expressions
                        subbed = re.sub(
                            r'\{([^}]+)\}',
                            lambda im: '{' + kw_pattern.sub(lambda km: kw_map.get(km.group(0), km.group(0)), im.group(1)) + '}',
                            fs
                        )
                        line_segments.append((gen_col, 0, line_idx, start))
                        gen_line_parts.append(subbed)
                        gen_col += len(subbed)
                    else:
                        line_segments.append((gen_col, 0, line_idx, start))
                        gen_line_parts.append(fs)
                        gen_col += len(fs)
                    orig_idx = end
                else:
                    # String or comment
                    chunk = m.group(0)
                    line_segments.append((gen_col, 0, line_idx, start))
                    gen_line_parts.append(chunk)
                    gen_col += len(chunk)
                    orig_idx = end

            if orig_idx < len(orig_line):
                chunk = orig_line[orig_idx:]
                line_segments.append((gen_col, 0, line_idx, orig_idx))
                gen_line_parts.append(chunk)
                gen_col += len(chunk)

            if not line_segments:
                line_segments.append((0, 0, line_idx, 0))

            gen_lines.append("".join(gen_line_parts))

            # Encode line segments into VLQ
            seg_strs = []
            last_gen_col = 0
            for gen_c, src_i, orig_l, orig_c in line_segments:
                d_gen = gen_c - last_gen_col
                d_src = src_i - last_src_idx
                d_line = orig_l - last_orig_line
                d_col = orig_c - last_orig_col

                last_gen_col = gen_c
                last_src_idx = src_i
                last_orig_line = orig_l
                last_orig_col = orig_c

                seg_str = "".join([
                    encode_vlq(d_gen),
                    encode_vlq(d_src),
                    encode_vlq(d_line),
                    encode_vlq(d_col)
                ])
                seg_strs.append(seg_str)

            raw_mappings.append(",".join(seg_strs))

        transpiled = "\n".join(gen_lines)
        mappings_str = ";".join(raw_mappings)

        smap = SourceMap(
            file=self.file,
            sources=[self.source_file],
            sourcesContent=[source],
            mappings=mappings_str
        )
        return transpiled, smap


class SourceMapConsumer:
    """Consumes V3 SourceMaps to map runtime Python lines/columns back to Ethiopic source."""

    def __init__(self, smap_data: Any):
        if isinstance(smap_data, str):
            data = json.loads(smap_data)
        elif isinstance(smap_data, SourceMap):
            data = smap_data.to_dict()
        elif isinstance(smap_data, dict):
            data = smap_data
        else:
            raise ValueError(f"Unsupported SourceMap data type: {type(smap_data)}")

        self.version = data.get("version", 3)
        self.file = data.get("file", "")
        self.sources = data.get("sources", [])
        self.sources_content = data.get("sourcesContent", [])
        self.names = data.get("names", [])
        self.mappings_raw = data.get("mappings", "")

        self.decoded_mappings = self._decode_mappings(self.mappings_raw)

    def _decode_mappings(self, raw_mappings: str) -> List[List[Tuple[int, int, int, int]]]:
        """Decode VLQ mapping string into list of lines with segment coordinates."""
        lines = []
        cur_src_idx = 0
        cur_orig_line = 0
        cur_orig_col = 0

        for line_str in raw_mappings.split(";"):
            line_segs = []
            cur_gen_col = 0
            if line_str:
                for seg_str in line_str.split(","):
                    if not seg_str:
                        continue
                    vals = decode_vlq_stream(seg_str)
                    if len(vals) >= 4:
                        cur_gen_col += vals[0]
                        cur_src_idx += vals[1]
                        cur_orig_line += vals[2]
                        cur_orig_col += vals[3]
                        line_segs.append((cur_gen_col, cur_src_idx, cur_orig_line, cur_orig_col))
                    elif len(vals) == 1:
                        cur_gen_col += vals[0]
                        line_segs.append((cur_gen_col, cur_src_idx, cur_orig_line, cur_orig_col))
            lines.append(line_segs)
        return lines

    def lookup(self, gen_line: int, gen_col: int = 0) -> Optional[Dict[str, Any]]:
        """
        Map a 1-based generated Python line number and 0-based column offset
        back to original Ethiopic source file, 1-based line number, and 0-based column.
        """
        line_idx = gen_line - 1
        if line_idx < 0 or line_idx >= len(self.decoded_mappings):
            return None

        segments = self.decoded_mappings[line_idx]
        if not segments:
            return None

        # Binary or linear search for segment with gen_col <= target_col
        best_seg = segments[0]
        for seg in segments:
            if seg[0] <= gen_col:
                best_seg = seg
            else:
                break

        gen_c, src_i, orig_l, orig_c = best_seg
        source_name = self.sources[src_i] if src_i < len(self.sources) else (self.file or "unknown")

        # Offset column accurately
        col_offset = orig_c + max(0, gen_col - gen_c)

        return {
            "source": source_name,
            "line": orig_l + 1,  # 1-based
            "column": col_offset,
            "gen_line": gen_line,
            "gen_column": gen_col
        }

    def resolve_traceback(self, tb_str: str) -> str:
        """
        Rewrite a Python traceback so that stack frames pointing to the generated
        Python file are redirected to the original Ethiopic script file and line.
        """
        pattern = re.compile(r'File "(?P<file>[^"]+)", line (?P<line>\d+)(?:, in (?P<func>\w+))?')

        def replace_frame(match):
            filepath = match.group('file')
            line_num = int(match.group('line'))
            func = match.group('func') or ""

            # Check if file matches or is a relative match
            if self.file and (Path(filepath).name == Path(self.file).name or filepath == self.file or filepath == '<string>'):
                mapped = self.lookup(line_num, 0)
                if mapped:
                    src_file = mapped['source']
                    orig_line = mapped['line']
                    in_func = f", in {func}" if func else ""
                    return f'File "{src_file}", line {orig_line}{in_func} [mapped via GezeLang V3 SourceMap]'
            return match.group(0)

        return pattern.sub(replace_frame, tb_str)
