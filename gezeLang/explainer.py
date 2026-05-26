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
