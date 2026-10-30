"""
tests/test_sourcemap.py — Tests for GezeLang V3 Source Map generator and consumer.
"""

import json
from pathlib import Path
from gezeLang.sourcemap import (
    encode_vlq,
    decode_vlq_stream,
    SourceMap,
    SourceMapGenerator,
    SourceMapConsumer
)


def test_vlq_encoding_decoding_round_trip():
    """Verify that VLQ encoder and decoder are mathematically lossless."""
    test_values = [0, 1, -1, 15, -15, 16, -16, 31, -31, 32, -32, 100, -100, 12345, -12345]
    for val in test_values:
        encoded = encode_vlq(val)
        decoded = decode_vlq_stream(encoded)
        assert len(decoded) == 1
        assert decoded[0] == val


def test_sourcemap_metadata_and_json():
    """Verify standard V3 source map dictionary and JSON output."""
    smap = SourceMap(
        file="program.py",
        sources=["program.amh"],
        sourcesContent=["ስራ ሰላም():\n    አሳይ('ሰላም')"],
        mappings="AAAA,GAAE"
    )
    d = smap.to_dict()
    assert d["version"] == 3
    assert d["file"] == "program.py"
    assert d["sources"] == ["program.amh"]
    assert d["mappings"] == "AAAA,GAAE"

    # JSON export
    raw_json = smap.to_json()
    parsed = json.loads(raw_json)
    assert parsed["version"] == 3

    # Data URL
    url = smap.to_data_url()
    assert url.startswith("data:application/json;charset=utf-8;base64,")

    # Comment
    comment = smap.get_source_mapping_comment(inline=False)
    assert "//# sourceMappingURL=program.py.map" in comment


def test_sourcemap_generation_and_lookup():
    """Verify generating source map from Amharic source and looking up lines."""
    ethiopic_code = """ስራ ደምር(ሀ, ለ):
    መልስ ሀ + ለ

ውጤት = ደምር(10, 20)
አሳይ(ውጤት)
"""
    gen = SourceMapGenerator(file="math_demo.py", source_file="math_demo.amh")
    py_code, smap = gen.generate(ethiopic_code, lang='amharic')

    assert "def ደምር(ሀ, ለ):" in py_code
    assert "return ሀ + ለ" in py_code
    assert len(smap.mappings) > 0

    consumer = SourceMapConsumer(smap)

    # Line 1 in Python: "def ደምር(ሀ, ለ):"
    mapped_l1 = consumer.lookup(gen_line=1, gen_col=0)
    assert mapped_l1 is not None
    assert mapped_l1["source"] == "math_demo.amh"
    assert mapped_l1["line"] == 1
    assert mapped_l1["column"] == 0

    # Line 2 in Python: "    return ሀ + ለ"
    # Column 4 in Python is where "return" begins, corresponding to column 4 in Amharic where "መልስ" began!
    mapped_l2 = consumer.lookup(gen_line=2, gen_col=4)
    assert mapped_l2 is not None
    assert mapped_l2["line"] == 2
    assert mapped_l2["column"] == 4


def test_sourcemap_multidialect_geez():
    """Verify source map generation for Ge'ez dialect."""
    geez_code = """ግበር ሰላም():
    አግብእ "ሰላም"
"""
    gen = SourceMapGenerator(file="geez.py", source_file="geez.geez")
    py_code, smap = gen.generate(geez_code, lang='geez')

    assert "def ሰላም():" in py_code
    assert 'return "ሰላም"' in py_code

    consumer = SourceMapConsumer(smap)
    mapped = consumer.lookup(gen_line=1, gen_col=0)
    assert mapped["line"] == 1
    assert mapped["source"] == "geez.geez"


def test_sourcemap_traceback_rewriter():
    """Verify that Python runtime tracebacks are mapped back to Ethiopic source."""
    ethiopic_code = "x = 10\ny = 0\nz = x / y\n"
    gen = SourceMapGenerator(file="app.py", source_file="app.amh")
    _, smap = gen.generate(ethiopic_code, lang='amharic')
    consumer = SourceMapConsumer(smap)

    sample_tb = '''Traceback (most recent call last):
  File "app.py", line 3, in <module>
    z = x / y
ZeroDivisionError: division by zero'''

    rewritten = consumer.resolve_traceback(sample_tb)
    assert 'File "app.amh", line 3' in rewritten
    assert "[mapped via GezeLang V3 SourceMap]" in rewritten


def test_cli_sourcemap_flag(tmp_path):
    """Verify CLI --emit with --sourcemap writes both .py and .py.map."""
    source_file = tmp_path / "test_prog.amh"
    source_file.write_text("ስራ ፈትሽ():\n    መልስ እውነት\n", encoding='utf-8')

    import subprocess
    import sys
    cmd = [
        sys.executable,
        "-m", "gezeLang.cli",
        str(source_file),
        "--emit",
        "--sourcemap"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0

    py_file = tmp_path / "test_prog.py"
    map_file = tmp_path / "test_prog.py.map"

    assert py_file.exists()
    assert map_file.exists()

    py_content = py_file.read_text(encoding='utf-8')
    assert "//# sourceMappingURL=test_prog.py.map" in py_content

    map_content = json.loads(map_file.read_text(encoding='utf-8'))
    assert map_content["version"] == 3
    assert map_content["file"] == "test_prog.py"
