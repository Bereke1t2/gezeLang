# stats.py — Language usage statistics for .amh files
import tokenize
import io
from collections import Counter

CATEGORIES = {
    'ፍቺ (Definitions)':    ['ስራ', 'ክፍለ', 'መልስ', 'አጭር'],
    'ቁጥጥር (Control)':     ['ከሆነ', 'ካልሆነ', 'ካልሆነከሆነ', 'እስከሆነ', 'ለእያንዳንዱ', 'ውስጥ', 'አቋርጥ', 'ቀጥል', 'ለጊዜው'],
    'ሎጂክ (Logic)':         ['እና', 'ወይም', 'አይደለም'],
    'ስህተት (Exceptions)':   ['ሞክር', 'ስህተት', 'መጨረሻ'],
    'ሞጁሎች (Imports)':      ['አምጣ', 'ከ', 'እንደ'],
    'ቢልት-ኢን (Builtins)':   ['አሳይ', 'ጠይቅ', 'ርዝመት', 'ክልል', 'ዝርዝር', 'መዝገብ', 'ጽሑፍ', 'ቁጥር', 'ትክክለኛ', 'ክፈት'],
    'ዓይነቶች (Literals)':    ['እውነት', 'ሐሰት', 'ምንም'],
}

def analyze(source: str) -> dict:
    all_amharic = {kw for kws in CATEGORIES.values() for kw in kws}
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except tokenize.TokenError:
        tokens = []

    names = [t.string for t in tokens if t.type == tokenize.NAME]
    keyword_uses = Counter(n for n in names if n in all_amharic)
    amharic_idents = sum(1 for n in names if any('\u1200' <= c <= '\u137F' for c in n) and n not in all_amharic)
    total_idents = len([n for n in names if n not in all_amharic])
    readability = round(amharic_idents / max(total_idents, 1) * 100, 1)

    cat_breakdown = {}
    for cat, kws in CATEGORIES.items():
        count = sum(keyword_uses[k] for k in kws)
        if count:
            cat_breakdown[cat] = count

    return {
        'total_lines': source.count('\n') + 1,
        'total_keywords': sum(keyword_uses.values()),
        'unique_keywords': len(keyword_uses),
        'keyword_uses': keyword_uses,
        'category_breakdown': cat_breakdown,
        'amharic_identifier_ratio': readability,
    }

def print_stats(source: str, filename: str):
    s = analyze(source)
    print(f"\n{'━'*50}")
    print(f"📊 GezeLang ስታቲስቲክስ — {filename}")
    print(f"{'━'*50}")
    print(f"  መስመሮች:          {s['total_lines']}")
    print(f"  ቁልፍ ቃሎች:        {s['total_keywords']} ({s['unique_keywords']} ዓይነት)")
    print(f"  አማርኛ ስሞች:       {s['amharic_identifier_ratio']}%")
    print("\n  📂 ምድብ ዝርዝር:")
    for cat, count in s['category_breakdown'].items():
        bar = '█' * min(count, 20)
        print(f"    {cat:<28} {bar} {count}")
    print("\n  🔝 ብዙ ጊዜ ያገለግሉ ቃሎች:")
    for kw, count in s['keyword_uses'].most_common(5):
        print(f"    {kw:<15} × {count}")
    print(f"{'━'*50}\n")
