import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gezeLang.adapter import AdapterRegistry
from gezeLang.batch import transpile_batch, benchmark_batch
import gezeLang

AdapterRegistry.discover(Path(__file__).parent.parent / 'gezeLang' / 'adapters')

def test_10_plus_ethiopic_dialects_registered():
    """Verify supporting 10+ Ethiopic dialects and regional languages."""
    langs = AdapterRegistry.list_langs()
    assert len(langs) >= 10, f"Expected at least 10 dialects, found {len(langs)}: {langs}"
    # Verify core Ethiopic script dialects are included
    expected_ethiopic = [
        'amharic', 'tigrinya', 'geez', 'gurage', 'silte',
        'harari', 'wolaytta', 'gamo', 'gofa', 'hadiyya',
        'amharic_gojjam', 'amharic_gondar', 'amharic_wollo', 'amharic_shewa'
    ]
    for dialect in expected_ethiopic:
        assert dialect in langs, f"Missing expected Ethiopic dialect: {dialect}"

def test_sub_06s_parse_times_on_1mb_batch():
    """
    Verify achieving sub-0.6s parse/transpile times on 1MB batch script files.
    """
    res = benchmark_batch(size_mb=1.0, lang='amharic')
    print(f"\n[BENCHMARK] 1MB Batch Performance:")
    print(f"  Total Files: {res['total_files']}")
    print(f"  Total Size:  {res['total_kb']:.2f} KB")
    print(f"  Elapsed:     {res['elapsed_seconds']:.4f}s")
    print(f"  Throughput:  {res['throughput_mb_s']:.2f} MB/s")
    
    assert res['total_kb'] >= 1024.0, f"Batch size must be at least 1MB (1024 KB), was {res['total_kb']:.2f} KB"
    assert res['elapsed_seconds'] < 0.6, (
        f"Parse time for 1MB batch exceeded 0.6s target! Took {res['elapsed_seconds']:.4f}s"
    )

def test_batch_transpile_correctness():
    """Verify batch transpilation emits valid Python for various Ethiopic dialects."""
    scripts = [
        "ስራ ሰላም():\n    አሳይ('ሰላም')\n",
        "ከሆነ እውነት:\n    አሳይ('እውነት ነው')\n",
        "ለእያንዳንዱ ተለዋዋጭ ውስጥ ክልል(5):\n    አሳይ(ተለዋዋጭ)\n"
    ]
    outputs = transpile_batch(scripts, lang='amharic')
    assert len(outputs) == 3
    assert 'def ሰላም():' in outputs[0]
    assert 'if True:' in outputs[1]
    assert 'for ተለዋዋጭ in range(5):' in outputs[2]
