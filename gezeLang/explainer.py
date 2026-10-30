# explainer.py — Contextual Amharic error explanations
EXPLANATIONS = {
    'E001_missing_colon': {
        'trigger': lambda msg: 'expected' in msg and ':' in msg,
        'title': '❌ ":" ይጎድላል',
        'explanation': 'ከሆነ፣ ስራ፣ ክፍለ፣ ወይም ሉፕ ከጻፉ በኋላ ":" መጨመር አለብዎ።',
        'example': '''
  ❌ ስህተት:
      ስራ ሰላም()
          አሳይ('ሰላም')

  ✅ ትክክለኛ:
      ስራ ሰላም():
          አሳይ('ሰላም')
  '''
    },
    'E002_bad_indent': {
        'trigger': lambda msg: 'indent' in msg.lower(),
        'title': '❌ ምሳሪያ (Indentation) ስህተት',
        'explanation': 'ውስጥ ያለ ኮድ 4 ባዶ ቦታ (spaces) ወይም Tab ሊኖረው ይገባል።',
        'example': '''
  ❌ ስህተት:
      ስራ ሰላም():
      አሳይ('ሰላም')   ← ወደ ፊት ያልተሸጋገረ

  ✅ ትክክለኛ:
      ስራ ሰላም():
          አሳይ('ሰላም')   ← 4 ባዶ ቦታ
  '''
    },
    'E003_undefined_name': {
        'trigger': lambda msg: 'not defined' in msg or 'NameError' in msg,
        'title': '❌ ያልተተረጎመ ስም',
        'explanation': 'ተለዋዋጩ ወይም ተግባሩ ከመጠቀሙ በፊት መተርጎም አለበት።',
        'example': '''
  ❌ ስህተት:
      አሳይ(ስም)   ← ስም ገና አልተተረጎመም

  ✅ ትክክለኛ:
      ስም = 'ቻሉ'
      አሳይ(ስም)
  '''
    },
    'E004_wrong_keyword': {
        'trigger': lambda msg: 'invalid syntax' in msg,
        'title': '❌ ትክክለኛ ያልሆነ ቃል',
        'explanation': 'የተጠቀሙት ቃል የGezeLang ቁልፍ ቃል አይደለም። ትክክለኛ Amharic ቁልፍ ቃል ይጠቀሙ።',
        'example': 'translator.py --help ወይም የቁልፍ ቃሎች ዝርዝር ይመልከቱ።'
    },
}

def explain_error(error_msg: str, line: int, col: int, source_lines: list) -> str:
    """
    Given a Python SyntaxError message, return a rich Amharic explanation.
    """
    for key, entry in EXPLANATIONS.items():
        if entry['trigger'](error_msg):
            context = source_lines[line-1] if line and line <= len(source_lines) else ''
            col_safe = col if col else 1
            return (
                f"\n{'━'*50}\n"
                f"{entry['title']}\n"
                f"{'━'*50}\n"
                f"📍 መስመር {line}, ቦታ {col_safe}\n"
                f"   {context}\n"
                f"   {' '*(col_safe-1)}^\n\n"
                f"💬 {entry['explanation']}\n"
                f"{entry.get('example', '')}\n"
                f"{'━'*50}\n"
            )
    # Fallback
    return (
        f"\nስህተት[E001] መስመር {line}, ቦታ {col}\n"
        f"አገባብ ስህተት — ኮድዎን ያረጋግጡ።\n"
        f"ዝርዝር: {error_msg}\n"
    )

RUNTIME_EXPLANATIONS = {
    'ZeroDivisionError': {
        'title': '❌ በዜሮ ማካፈል አይቻልም (ZeroDivisionError)',
        'explanation': 'ማንኛውንም ቁጥር በዜሮ (0) ማካፈል በሂሳብ አይቻልም።',
    },
    'IndexError': {
        'title': '❌ የዝርዝር ወሰን አልፏል (IndexError)',
        'explanation': 'በዝርዝር (list) ውስጥ ከሚገኙት ብዛት በላይ ያለ ቦታ (index) ለመጠቀም ሞክረዋል።',
    },
    'KeyError': {
        'title': '❌ በመዝገቡ ውስጥ ቁልፍ አልተገኘም (KeyError)',
        'explanation': 'በመዝገብ (dict) ውስጥ የሌለን ቁልፍ ለመፈለግ ሞክረዋል።',
    },
    'TypeError': {
        'title': '❌ የአይነት አለመጣጣም ስህተት (TypeError)',
        'explanation': 'የተጠቀሙት ስሌት ወይም ተግባር ካለው የመረጃ አይነት (data type) ጋር አይጣጣምም።',
    },
    'ValueError': {
        'title': '❌ ትክክለኛ ያልሆነ እሴት (ValueError)',
        'explanation': 'የተሰጠው እሴት ለተፈለገው ተግባር ትክክለኛ አይደለም።',
    },
    'NameError': {
        'title': '❌ ያልተተረጎመ ተለዋዋጭ ስም (NameError)',
        'explanation': 'ተለዋዋጩ ከመጠራቱ በፊት እሴት አልተሰጠውም።',
    },
    'RecursionError': {
        'title': '❌ የተደጋገመ ጥሪ ወሰን አልፏል (RecursionError)',
        'explanation': 'ተግባሩ ራሱን ያለ ማቆሚያ ደጋግሞ በመጥራቱ የማስታወሻ ወሰኑን አልፏል።',
    }
}

def explain_runtime_exception(exc: BaseException, source_path_str: str, source_lines: list) -> str:
    """
    Given a runtime exception from Python execution, inspect traceback,
    map back to original Ethiopic source coordinates, and return formatted diagnostic.
    """
    tb = exc.__traceback__
    target_lineno = None
    
    while tb is not None:
        frame_code = tb.tb_frame.f_code
        if frame_code.co_filename == source_path_str or frame_code.co_filename.endswith(source_path_str):
            target_lineno = tb.tb_lineno
        tb = tb.tb_next
        
    exc_type = type(exc).__name__
    info = RUNTIME_EXPLANATIONS.get(exc_type, {
        'title': f'❌ ስህተት ({exc_type})',
        'explanation': f'ፕሮግራሙ ሲሄድ ችግር ተፈጥሯል: {str(exc)}'
    })
    
    line_info = f"መስመር {target_lineno}" if target_lineno else "ያልታወቀ መስመር"
    code_context = ""
    if target_lineno and 1 <= target_lineno <= len(source_lines):
        code_context = f"\n  {target_lineno} | {source_lines[target_lineno-1]}\n    | ^"
        
    return (
        f"\n{'━'*60}\n"
        f"{info['title']}\n"
        f"{'━'*60}\n"
        f"📍 {line_info} ውስጥ:\n"
        f"{code_context}\n\n"
        f"💬 {info['explanation']}\n"
        f"ዝርዝር መልዕክት: {str(exc)}\n"
        f"{'━'*60}\n"
    )

